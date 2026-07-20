"""Recoverable exact-byte STATUS.md archive preparation and rollback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable


ENTRY_RE = re.compile(rb"(?m)^\*\*(\d{4}-\d{2}-\d{2}) .+\*\*$")
LOCK_NAME = ".jeff_strict_status_migration.lock"
TXN_PREFIX = ".jeff_strict_status_txn_"
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


def is_reparse(path: Path) -> bool:
    info = path.lstat()
    return path.is_symlink() or bool(getattr(info, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def validate_existing_chain(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        if not current.is_dir():
            if lexists(current):
                raise ValueError(f"path parent is not a directory: {current}")
            return
        matches = [entry.name for entry in os.scandir(current) if entry.name.casefold() == part.casefold()]
        if not matches:
            return
        if part not in matches:
            raise ValueError(f"path casing mismatch: requested {part!r}, actual {matches[0]!r}")
        current = current / part
        if is_reparse(current):
            raise ValueError(f"reparse/symlink component is forbidden: {current}")


def ensure_under(root: Path, path: Path, *, must_exist: bool | None = None) -> Path:
    root_absolute = root.absolute()
    candidate = path if path.is_absolute() else root_absolute / path
    candidate = candidate.absolute()
    try:
        candidate.relative_to(root_absolute)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {path}") from exc
    validate_existing_chain(root_absolute)
    validate_existing_chain(candidate.parent)
    if lexists(candidate):
        validate_existing_chain(candidate)
        if is_reparse(candidate):
            raise ValueError(f"reparse/symlink destination is forbidden: {candidate}")
    if must_exist is True and not candidate.is_file():
        raise ValueError(f"required file is missing: {candidate}")
    if must_exist is False and lexists(candidate):
        raise ValueError(f"refusing to overwrite: {candidate}")
    existing_parent = candidate.parent
    while not lexists(existing_parent):
        existing_parent = existing_parent.parent
    try:
        existing_parent.resolve(strict=True).relative_to(root_absolute.resolve(strict=True))
    except ValueError as exc:
        raise ValueError(f"path parent escapes repository: {candidate}") from exc
    return candidate


def atomic_write(path: Path, data: bytes) -> None:
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_new(path: Path, data: bytes) -> None:
    temporary: Path | None = None
    linked = False
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.link(temporary, path)
        linked = True
        if path.read_bytes() != data:
            raise ValueError(f"new-file post-write verification failed: {path}")
    except Exception:
        if linked and temporary is not None:
            try:
                if path.exists() and os.path.samefile(path, temporary):
                    path.unlink()
            except OSError:
                pass
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_json_new(path: Path, value: dict[str, Any]) -> bytes:
    content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    write_new(path, content)
    return content


def write_json(path: Path, value: dict[str, Any]) -> bytes:
    content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    atomic_write(path, content)
    if path.read_bytes() != content:
        raise ValueError(f"post-write verification failed: {path}")
    return content


def verify_exact_file(path: Path, expected: bytes, label: str) -> None:
    if not path.is_file() or path.read_bytes() != expected:
        raise ValueError(f"{label} changed during status transaction: {path}")


def strict_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("--date must be canonical YYYY-MM-DD")
    return value


def injector(args: argparse.Namespace) -> Callable[[str], None]:
    callback = getattr(args, "fault_injector", None)
    return callback if callback is not None else lambda phase: None


def open_transaction(root: Path, action: str) -> tuple[Path, Path, int, dict[str, Any]]:
    validate_existing_chain(root)
    stale = sorted(path.name for path in root.iterdir() if path.name.startswith(TXN_PREFIX))
    if stale:
        raise ValueError(f"unresolved status transaction journal(s): {stale}")
    lock = root / LOCK_NAME
    lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    transaction: Path | None = None
    try:
        os.write(lock_fd, f"Jeff Strict SSOT status {action} lock\n".encode())
        os.fsync(lock_fd)
        transaction = Path(tempfile.mkdtemp(prefix=TXN_PREFIX, dir=root))
        journal = {
            "schema_version": 1,
            "transaction_id": uuid.uuid4().hex,
            "action": action,
            "state": "started",
            "root": str(root),
            "writes": [],
            "rollback": [],
        }
        write_json(transaction / "journal.json", journal)
        return lock, transaction, lock_fd, journal
    except Exception:
        os.close(lock_fd)
        lock.unlink(missing_ok=True)
        if transaction is not None:
            shutil.rmtree(transaction, ignore_errors=True)
        raise


def finish_transaction(lock: Path, transaction: Path, lock_fd: int, success: bool) -> None:
    os.close(lock_fd)
    lock.unlink(missing_ok=True)
    if success:
        shutil.rmtree(transaction)


def prepare(args: argparse.Namespace) -> int:
    root = args.root.absolute()
    validate_existing_chain(root)
    if not root.is_dir():
        raise ValueError("repository root must be an existing directory")
    migration_date = strict_date(args.date)
    status = ensure_under(root, Path("STATUS.md"), must_exist=True)
    candidate = ensure_under(root, args.compact_candidate, must_exist=True)
    record_path = ensure_under(root, args.record, must_exist=False)
    archive = ensure_under(root, Path("docs/status_history") / f"STATUS_{migration_date}_pre_compaction.md", must_exist=False)
    index = ensure_under(root, archive.with_suffix(".index.json"), must_exist=False)
    expected_current = args.expected_current_sha256.lower()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_current):
        raise ValueError("--expected-current-sha256 must be 64 lowercase hex characters")
    current = status.read_bytes()
    compact = candidate.read_bytes()
    compact_hash = sha256(compact)
    if sha256(current) != expected_current:
        raise ValueError("current STATUS.md hash does not match reviewed expectation")
    if len(current.splitlines()) <= 120 and len(current) <= 32768:
        raise ValueError("current STATUS.md does not exceed a hard cap")
    if len(compact.splitlines()) > 120 or len(compact) > 32768:
        raise ValueError("compact candidate exceeds a hard cap")
    if len(ENTRY_RE.findall(compact)) != 1:
        raise ValueError("compact candidate must contain exactly one dated entry")

    lock, transaction, lock_fd, journal = open_transaction(root, "prepare")
    journal_path = transaction / "journal.json"
    (transaction / "original_STATUS.md").write_bytes(current)
    inject = injector(args)
    success = False
    archive_content: bytes | None = None
    index_content: bytes | None = None
    record_content: bytes | None = None
    status_replaced = False
    try:
        if sha256(status.read_bytes()) != expected_current:
            raise ValueError("STATUS.md changed after transaction lock")
        inject("after_locked_preflight")
        entry_offsets = [match.start() for match in ENTRY_RE.finditer(current)]
        index_data = {
            "schema_version": 1,
            "archive": archive.relative_to(root).as_posix(),
            "sha256": sha256(current),
            "bytes": len(current),
            "lines": len(current.splitlines()),
            "dated_entry_byte_offsets": entry_offsets,
            "immutable": True,
        }
        record = {
            "schema_version": 1,
            "action": "prepare",
            "transaction_state": "committed_verified",
            "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "archive_sha256": sha256(current),
            "previous_status_sha256": expected_current,
            "compact_status_sha256": compact_hash,
            "archive": archive.relative_to(root).as_posix(),
        }
        archive = ensure_under(root, archive, must_exist=False)
        write_new(archive, current)
        archive_content = current
        journal["writes"].append(str(archive.relative_to(root)))
        write_json(journal_path, journal)
        inject("after_archive")
        index = ensure_under(root, index, must_exist=False)
        index_content = write_json_new(index, index_data)
        journal["writes"].append(str(index.relative_to(root)))
        write_json(journal_path, journal)
        inject("after_index")
        status = ensure_under(root, Path("STATUS.md"), must_exist=True)
        candidate = ensure_under(root, candidate, must_exist=True)
        if sha256(status.read_bytes()) != expected_current or sha256(candidate.read_bytes()) != compact_hash:
            raise ValueError("STATUS.md or compact candidate changed immediately before replacement")
        verify_exact_file(archive, archive_content, "archive")
        verify_exact_file(index, index_content, "archive index")
        atomic_write(status, compact)
        status_replaced = True
        inject("after_status")
        verify_exact_file(status, compact, "compact STATUS.md")
        verify_exact_file(archive, archive_content, "archive")
        verify_exact_file(index, index_content, "archive index")
        journal["writes"].append("STATUS.md")
        record_path = ensure_under(root, record_path, must_exist=False)
        record_content = write_json_new(record_path, record)
        journal["writes"].append(str(record_path.relative_to(root)))
        inject("after_record")
        verify_exact_file(status, compact, "compact STATUS.md")
        verify_exact_file(archive, archive_content, "archive")
        verify_exact_file(index, index_content, "archive index")
        verify_exact_file(record_path, record_content, "migration record")
        inject("before_commit")
        verify_exact_file(status, compact, "compact STATUS.md")
        verify_exact_file(archive, archive_content, "archive")
        verify_exact_file(index, index_content, "archive index")
        verify_exact_file(record_path, record_content, "migration record")
        journal["state"] = "committed_verified"
        write_json(journal_path, journal)
        success = True
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0
    except Exception as original_error:
        rollback_errors: list[str] = []
        if status_replaced:
            try:
                if status.is_file() and status.read_bytes() == compact:
                    atomic_write(status, current)
                    if sha256(status.read_bytes()) != expected_current:
                        raise ValueError("STATUS.md rollback hash mismatch")
                    journal["rollback"].append("STATUS.md restored")
                else:
                    rollback_errors.append("refused to overwrite externally changed STATUS.md")
            except Exception as exc:
                rollback_errors.append(f"STATUS.md rollback: {exc}")
        for path, content in ((record_path, record_content), (index, index_content), (archive, archive_content)):
            if content is None:
                continue
            try:
                if path.is_file() and path.read_bytes() == content:
                    path.unlink()
                    journal["rollback"].append(f"removed {path.relative_to(root)}")
                elif path.exists():
                    rollback_errors.append(f"refused cleanup of changed path {path}")
            except OSError as exc:
                rollback_errors.append(f"cleanup {path}: {exc}")
        journal["state"] = "rollback_failed" if rollback_errors else "rolled_back_after_failure"
        journal["original_error"] = str(original_error)
        journal["rollback_errors"] = rollback_errors
        write_json(journal_path, journal)
        if rollback_errors:
            raise ValueError(f"prepare failed and rollback was incomplete; inspect {journal_path}: {rollback_errors}") from original_error
        raise
    finally:
        finish_transaction(lock, transaction, lock_fd, success)


def rollback(args: argparse.Namespace) -> int:
    root = args.root.absolute()
    validate_existing_chain(root)
    if not root.is_dir():
        raise ValueError("repository root must be an existing directory")
    status = ensure_under(root, Path("STATUS.md"), must_exist=True)
    archive = ensure_under(root, args.archive, must_exist=True)
    record_path = ensure_under(root, args.record, must_exist=False)
    expected_current = args.expected_current_sha256.lower()
    expected_archive = args.expected_archive_sha256.lower()
    for label, value in (("current", expected_current), ("archive", expected_archive)):
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError(f"expected {label} hash must be 64 lowercase hex characters")
    current = status.read_bytes()
    archived = archive.read_bytes()
    if sha256(current) != expected_current:
        raise ValueError("current STATUS.md hash does not match reviewed expectation")
    if sha256(archived) != expected_archive:
        raise ValueError("archive hash does not match reviewed expectation")

    lock, transaction, lock_fd, journal = open_transaction(root, "rollback")
    journal_path = transaction / "journal.json"
    (transaction / "pre_rollback_STATUS.md").write_bytes(current)
    inject = injector(args)
    success = False
    record_content: bytes | None = None
    status_replaced = False
    try:
        if sha256(status.read_bytes()) != expected_current or sha256(archive.read_bytes()) != expected_archive:
            raise ValueError("status or archive changed after transaction lock")
        inject("after_locked_preflight")
        record = {
            "schema_version": 1,
            "action": "rollback",
            "transaction_state": "committed_verified",
            "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "replaced_status_sha256": expected_current,
            "restored_archive_sha256": expected_archive,
            "archive": archive.relative_to(root).as_posix(),
        }
        status = ensure_under(root, Path("STATUS.md"), must_exist=True)
        archive = ensure_under(root, archive, must_exist=True)
        if sha256(status.read_bytes()) != expected_current or sha256(archive.read_bytes()) != expected_archive:
            raise ValueError("status or archive changed immediately before rollback")
        atomic_write(status, archived)
        status_replaced = True
        inject("after_status")
        verify_exact_file(status, archived, "restored STATUS.md")
        verify_exact_file(archive, archived, "source archive")
        journal["writes"].append("STATUS.md")
        record_path = ensure_under(root, record_path, must_exist=False)
        record_content = write_json_new(record_path, record)
        journal["writes"].append(str(record_path.relative_to(root)))
        inject("after_record")
        verify_exact_file(status, archived, "restored STATUS.md")
        verify_exact_file(archive, archived, "source archive")
        verify_exact_file(record_path, record_content, "rollback record")
        inject("before_commit")
        verify_exact_file(status, archived, "restored STATUS.md")
        verify_exact_file(archive, archived, "source archive")
        verify_exact_file(record_path, record_content, "rollback record")
        journal["state"] = "committed_verified"
        write_json(journal_path, journal)
        success = True
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0
    except Exception as original_error:
        rollback_errors: list[str] = []
        if status_replaced:
            try:
                if status.is_file() and status.read_bytes() == archived:
                    atomic_write(status, current)
                    if sha256(status.read_bytes()) != expected_current:
                        raise ValueError("pre-rollback STATUS.md restore hash mismatch")
                    journal["rollback"].append("pre-rollback STATUS.md restored")
                else:
                    rollback_errors.append("refused to overwrite externally changed STATUS.md")
            except Exception as exc:
                rollback_errors.append(f"STATUS.md restore: {exc}")
        if record_content is not None:
            try:
                if record_path.is_file() and record_path.read_bytes() == record_content:
                    record_path.unlink()
                    journal["rollback"].append(f"removed {record_path.relative_to(root)}")
                elif record_path.exists():
                    rollback_errors.append(f"refused cleanup of changed record {record_path}")
            except OSError as exc:
                rollback_errors.append(f"record cleanup: {exc}")
        journal["state"] = "rollback_failed" if rollback_errors else "rolled_back_after_failure"
        journal["original_error"] = str(original_error)
        journal["rollback_errors"] = rollback_errors
        write_json(journal_path, journal)
        if rollback_errors:
            raise ValueError(f"rollback failed and recovery was incomplete; inspect {journal_path}: {rollback_errors}") from original_error
        raise
    finally:
        finish_transaction(lock, transaction, lock_fd, success)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("--root", type=Path, required=True)
    prepare_parser.add_argument("--compact-candidate", type=Path, required=True)
    prepare_parser.add_argument("--date", required=True)
    prepare_parser.add_argument("--expected-current-sha256", required=True)
    prepare_parser.add_argument("--record", type=Path, required=True)
    prepare_parser.set_defaults(func=prepare)
    rollback_parser = sub.add_parser("rollback")
    rollback_parser.add_argument("--root", type=Path, required=True)
    rollback_parser.add_argument("--archive", type=Path, required=True)
    rollback_parser.add_argument("--expected-current-sha256", required=True)
    rollback_parser.add_argument("--expected-archive-sha256", required=True)
    rollback_parser.add_argument("--record", type=Path, required=True)
    rollback_parser.set_defaults(func=rollback)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"status_migration_error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
