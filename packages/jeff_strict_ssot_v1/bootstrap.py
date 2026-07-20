"""Deterministic installer for the Jeff Strict SSOT V1 package."""

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
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, Callable


PACKAGE_ROOT = Path(__file__).resolve().parent
PACKAGE_MANIFEST_PATH = PACKAGE_ROOT / "MANIFEST.json"
INSTALL_MANIFEST_NAME = "JEFF_STRICT_SSOT_INSTALL.json"
RETROFIT_LOCK_NAME = ".jeff_strict_ssot_retrofit.lock"
RETROFIT_TXN_PREFIX = ".jeff_strict_ssot_retrofit_txn_"
FRESH_LOCK_NAME = ".jeff_strict_ssot_fresh.lock"
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class BootstrapError(RuntimeError):
    """A fail-closed bootstrap error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


def is_reparse(path: Path) -> bool:
    info = path.lstat()
    attributes = getattr(info, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & REPARSE_ATTRIBUTE)


def validate_existing_chain(path: Path) -> None:
    """Reject case aliases and reparse points for every existing component."""
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        if not current.is_dir():
            if lexists(current):
                raise BootstrapError(f"path parent is not a directory: {current}")
            return
        matches = [entry.name for entry in os.scandir(current) if entry.name.casefold() == part.casefold()]
        if not matches:
            return
        if part not in matches:
            raise BootstrapError(f"path casing mismatch: requested {part!r}, actual {matches[0]!r}")
        current = current / part
        if is_reparse(current):
            raise BootstrapError(f"reparse/symlink path component is forbidden: {current}")


def safe_destination(target: Path, relative: str) -> Path:
    normalized = normalize_relative(relative)
    target_absolute = target.absolute()
    destination = target_absolute / Path(normalized)
    try:
        destination.relative_to(target_absolute)
    except ValueError as exc:
        raise BootstrapError(f"destination escapes target: {relative}") from exc
    validate_existing_chain(target_absolute)
    validate_existing_chain(destination.parent)
    if lexists(destination):
        validate_existing_chain(destination)
        if is_reparse(destination):
            raise BootstrapError(f"destination is a reparse/symlink: {relative}")
    existing_parent = destination.parent
    while not lexists(existing_parent):
        if existing_parent == target_absolute:
            break
        existing_parent = existing_parent.parent
    resolved_target = target_absolute.resolve(strict=True)
    resolved_parent = existing_parent.resolve(strict=True)
    try:
        resolved_parent.relative_to(resolved_target)
    except ValueError as exc:
        raise BootstrapError(f"destination parent escapes target: {relative}") from exc
    return destination


def current_state(path: Path) -> str:
    if not lexists(path):
        return "absent"
    if is_reparse(path) or not path.is_file():
        raise BootstrapError(f"expected regular non-reparse file: {path}")
    return sha256_file(path)


def create_missing_parents(target: Path, parent: Path, created: list[Path]) -> None:
    target_absolute = target.absolute()
    missing: list[Path] = []
    cursor = parent
    while not lexists(cursor):
        if cursor == target_absolute:
            break
        missing.append(cursor)
        cursor = cursor.parent
    validate_existing_chain(cursor)
    for directory in reversed(missing):
        directory.mkdir()
        validate_existing_chain(directory)
        created.append(directory)


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    content = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
        temporary = None
        if path.read_bytes() != content:
            raise BootstrapError(f"atomic JSON post-write mismatch: {path}")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def normalize_relative(raw: str) -> str:
    value = PurePosixPath(raw.replace("\\", "/"))
    if value.is_absolute() or not value.parts or ".." in value.parts:
        raise BootstrapError(f"unsafe relative path: {raw!r}")
    return value.as_posix()


def load_package_manifest() -> dict[str, Any]:
    data = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise BootstrapError("unsupported package manifest schema")
    listed = [normalize_relative(item) for item in data.get("template_files", [])]
    if listed != sorted(set(listed)):
        raise BootstrapError("template_files must be sorted and unique")
    template_root = PACKAGE_ROOT / str(data.get("template_root", "template"))
    actual = sorted(
        path.relative_to(template_root).as_posix()
        for path in template_root.rglob("*")
        if path.is_file()
    )
    if listed != actual:
        missing = sorted(set(listed) - set(actual))
        extra = sorted(set(actual) - set(listed))
        raise BootstrapError(
            f"package manifest/template mismatch; missing={missing}, extra={extra}"
        )
    data["template_files"] = listed
    expected_hashes = data.get("template_sha256")
    if not isinstance(expected_hashes, dict) or set(expected_hashes) != set(listed):
        raise BootstrapError("package manifest needs an exact template_sha256 map")
    for relative in listed:
        actual_hash = sha256_file(template_root / relative)
        if expected_hashes.get(relative) != actual_hash:
            raise BootstrapError(f"package template hash mismatch: {relative}")
    return data


def render_template(source: bytes, project_name: str, install_date: str) -> bytes:
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BootstrapError("all V1 templates must be UTF-8 text") from exc
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{BOOTSTRAP_DATE}}": install_date,
    }
    for needle, replacement in replacements.items():
        text = text.replace(needle, replacement)
    if re.search(r"\{\{[A-Z][A-Z0-9_]*\}\}", text):
        raise BootstrapError("unresolved template placeholder")
    return text.encode("utf-8")


def build_payload(
    manifest: dict[str, Any], project_name: str, install_date: str
) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    template_root = PACKAGE_ROOT / str(manifest["template_root"])
    payload: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    for relative in manifest["template_files"]:
        source_path = template_root / relative
        source = source_path.read_bytes()
        rendered = render_template(source, project_name, install_date)
        payload[relative] = rendered
        records.append(
            {
                "path": relative,
                "source_template_sha256": sha256_bytes(source),
                "rendered_sha256": sha256_bytes(rendered),
                "bytes": len(rendered),
            }
        )
    return payload, records


def load_retrofit_plan(path: Path, target: Path) -> dict[str, Any]:
    plan_path = path.absolute()
    validate_existing_chain(plan_path)
    if not plan_path.is_file() or is_reparse(plan_path):
        raise BootstrapError("retrofit plan must be a regular non-reparse file")
    source = plan_path.read_bytes()
    data = json.loads(source.decode("utf-8"))
    if data.get("schema_version") != 1 or data.get("reviewed") is not True:
        raise BootstrapError("retrofit plan must use schema 1 and reviewed=true")
    allowed = [normalize_relative(item) for item in data.get("allowed_files", [])]
    if not allowed or allowed != sorted(set(allowed)):
        raise BootstrapError("retrofit allowed_files must be nonempty, sorted, unique")
    expected = data.get("expected_existing_sha256")
    if not isinstance(expected, dict) or set(expected) != set(allowed):
        raise BootstrapError("retrofit plan needs an expected state for every allowed file")
    recorded_target = str(Path(str(data.get("target", ""))).absolute())
    requested_target = str(target.absolute())
    if recorded_target != requested_target:
        raise BootstrapError("retrofit plan target does not match --target")
    data["_source_sha256"] = sha256_bytes(source)
    return data


def preflight_fresh(target: Path, relative_paths: list[str]) -> None:
    validate_existing_chain(target.absolute())
    if target.exists() and not target.is_dir():
        raise BootstrapError("fresh target exists and is not a directory")
    if target.exists() and any(target.iterdir()):
        raise BootstrapError("fresh target must be nonexistent or empty")
    for relative in relative_paths + [INSTALL_MANIFEST_NAME]:
        destination = safe_destination(target, relative) if target.exists() else target / relative
        if lexists(destination):
            raise BootstrapError(f"refusing to overwrite: {relative}")


def preflight_retrofit(
    target: Path,
    payload: dict[str, bytes],
    plan: dict[str, Any],
) -> tuple[list[str], dict[str, str]]:
    validate_existing_chain(target.absolute())
    if not target.is_dir():
        raise BootstrapError("retrofit target must be an existing directory")
    if lexists(target / RETROFIT_LOCK_NAME):
        raise BootstrapError("retrofit lock already exists")
    stale = sorted(path.name for path in target.iterdir() if path.name.startswith(RETROFIT_TXN_PREFIX))
    if stale:
        raise BootstrapError(f"unresolved retrofit transaction journal(s): {stale}")
    allowed = list(plan["allowed_files"])
    permitted_payload = set(payload) | {INSTALL_MANIFEST_NAME}
    if not set(allowed) <= permitted_payload:
        raise BootstrapError("retrofit plan names files outside the package payload")
    if INSTALL_MANIFEST_NAME not in allowed:
        raise BootstrapError("retrofit allowlist must include the install manifest")
    for relative in allowed:
        destination = safe_destination(target, relative)
        expected = str(plan["expected_existing_sha256"][relative])
        actual = current_state(destination)
        if expected != actual:
            raise BootstrapError(f"retrofit expected-state mismatch: {relative}")
    return allowed, {relative: str(plan["expected_existing_sha256"][relative]) for relative in allowed}


def make_install_manifest(
    package: dict[str, Any],
    target: Path,
    project_name: str,
    install_date: str,
    mode: str,
    records: list[dict[str, Any]],
    retrofit_plan: Path | None,
    retrofit_plan_sha256: str | None = None,
) -> bytes:
    if retrofit_plan is not None and retrofit_plan_sha256 is None:
        retrofit_plan_sha256 = sha256_file(retrofit_plan)
    record = {
        "schema_version": 1,
        "package_name": package["package_name"],
        "package_version": package["package_version"],
        "mode": mode,
        "project_name": project_name,
        "install_date": install_date,
        "rendered_timestamp_utc": f"{install_date}T00:00:00Z",
        "target": str(target.resolve()),
        "package_manifest_sha256": sha256_file(PACKAGE_MANIFEST_PATH),
        "retrofit_plan": str(retrofit_plan.absolute()) if retrofit_plan else None,
        "retrofit_plan_sha256": retrofit_plan_sha256,
        "files": records,
        "limitations": [
            "no product prompt ingested",
            "no network access",
            "no dependency installation",
            "no Git mutation",
            "no automation creation",
        ],
    }
    return (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_fresh(
    target: Path,
    payload: dict[str, bytes],
    install_manifest: bytes,
    fault_injector: Callable[[str], None] | None = None,
) -> None:
    target_created = not target.exists()
    created_files: list[Path] = []
    created_dirs: list[Path] = []
    inject = fault_injector if fault_injector is not None else lambda phase: None
    lock_fd: int | None = None
    try:
        target.mkdir(parents=True, exist_ok=True)
        validate_existing_chain(target)
        lock_path = target / FRESH_LOCK_NAME
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        created_files.append(lock_path)
        try:
            os.write(lock_fd, b"Jeff Strict SSOT fresh install lock\n")
            os.fsync(lock_fd)
        finally:
            os.close(lock_fd)
            lock_fd = None
        for relative, content in sorted(payload.items()):
            destination = safe_destination(target, relative)
            create_missing_parents(target, destination.parent, created_dirs)
            destination = safe_destination(target, relative)
            with destination.open("xb") as handle:
                created_files.append(destination)
                inject(f"after_create:{relative}")
                handle.write(content)
                inject(f"after_write:{relative}")
                handle.flush()
                inject(f"after_flush:{relative}")
                os.fsync(handle.fileno())
                inject(f"after_fsync:{relative}")
            if sha256_file(destination) != sha256_bytes(content):
                raise BootstrapError(f"post-write hash mismatch: {relative}")
            inject(f"after_verify:{relative}")
        manifest_path = target / INSTALL_MANIFEST_NAME
        with manifest_path.open("xb") as handle:
            created_files.append(manifest_path)
            inject(f"after_create:{INSTALL_MANIFEST_NAME}")
            handle.write(install_manifest)
            inject(f"after_write:{INSTALL_MANIFEST_NAME}")
            handle.flush()
            inject(f"after_flush:{INSTALL_MANIFEST_NAME}")
            os.fsync(handle.fileno())
            inject(f"after_fsync:{INSTALL_MANIFEST_NAME}")
        if sha256_file(manifest_path) != sha256_bytes(install_manifest):
            raise BootstrapError("install manifest post-write hash mismatch")
        inject(f"after_verify:{INSTALL_MANIFEST_NAME}")
        lock_path.unlink()
        created_files.remove(lock_path)
    except Exception:
        if lock_fd is not None:
            os.close(lock_fd)
        for path in reversed(created_files):
            path.unlink(missing_ok=True)
        for path in sorted(set(created_dirs), key=lambda item: len(item.parts), reverse=True):
            try:
                path.rmdir()
            except OSError:
                pass
        if target_created:
            try:
                target.rmdir()
            except OSError:
                pass
        raise


def write_retrofit(
    target: Path,
    payload: dict[str, bytes],
    install_manifest: bytes,
    allowed: list[str],
    expected_states: dict[str, str],
    retrofit_plan: Path | None = None,
    retrofit_plan_sha256: str | None = None,
    fault_injector: Callable[[str], None] | None = None,
) -> None:
    content_by_path = dict(payload)
    content_by_path[INSTALL_MANIFEST_NAME] = install_manifest
    lock_path = target / RETROFIT_LOCK_NAME
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    transaction_dir: Path | None = None
    try:
        os.write(lock_fd, b"Jeff Strict SSOT retrofit transaction lock\n")
        os.fsync(lock_fd)
        os.close(lock_fd)
        lock_fd = -1
        transaction_id = uuid.uuid4().hex
        transaction_dir = Path(tempfile.mkdtemp(prefix=RETROFIT_TXN_PREFIX, dir=target))
        backup_dir = transaction_dir / "backups"
        backup_dir.mkdir()
        journal_path = transaction_dir / "journal.json"
        journal: dict[str, Any] = {
            "schema_version": 1,
            "transaction_id": transaction_id,
            "state": "preflight_under_lock",
            "target": str(target.absolute()),
            "allowed_files": allowed,
            "expected_states": expected_states,
            "backups": {},
            "created_directories": [],
            "temporary_files": [],
            "replacements": [],
            "rollback": [],
        }
        write_json_atomic(journal_path, journal)
    except Exception:
        if lock_fd >= 0:
            os.close(lock_fd)
        if transaction_dir is not None:
            shutil.rmtree(transaction_dir, ignore_errors=True)
        lock_path.unlink(missing_ok=True)
        raise
    backups: dict[str, Path | None] = {}
    created_dirs: list[Path] = []
    temporary_files: list[Path] = []
    replaced: list[str] = []
    written_states = {relative: sha256_bytes(content_by_path[relative]) for relative in allowed}

    def inject(phase: str) -> None:
        if fault_injector is not None:
            fault_injector(phase)

    try:
        validate_existing_chain(target)
        if retrofit_plan is not None:
            validate_existing_chain(retrofit_plan)
            if not retrofit_plan.is_file() or is_reparse(retrofit_plan):
                raise BootstrapError("retrofit plan changed type before commit")
            if sha256_file(retrofit_plan) != retrofit_plan_sha256:
                raise BootstrapError("retrofit plan changed before commit")
        for relative in allowed:
            destination = safe_destination(target, relative)
            if current_state(destination) != expected_states[relative]:
                raise BootstrapError(f"retrofit state changed before commit: {relative}")
        inject("after_locked_preflight")

        for index, relative in enumerate(allowed):
            destination = safe_destination(target, relative)
            state = current_state(destination)
            if state != expected_states[relative]:
                raise BootstrapError(f"retrofit state changed before replacement: {relative}")
            if state == "absent":
                backups[relative] = None
                journal["backups"][relative] = None
            else:
                backup = backup_dir / f"{index:04d}.bin"
                shutil.copyfile(destination, backup)
                if sha256_file(backup) != state:
                    raise BootstrapError(f"backup hash mismatch: {relative}")
                backups[relative] = backup
                journal["backups"][relative] = {
                    "path": backup.relative_to(transaction_dir).as_posix(),
                    "sha256": state,
                }
            write_json_atomic(journal_path, journal)
        journal["state"] = "backups_verified"
        write_json_atomic(journal_path, journal)
        inject("after_backups")

        for relative in allowed:
            destination = safe_destination(target, relative)
            create_missing_parents(target, destination.parent, created_dirs)
            journal["created_directories"] = [path.relative_to(target).as_posix() for path in created_dirs]
            if current_state(destination) != expected_states[relative]:
                raise BootstrapError(f"retrofit state changed at replacement: {relative}")
            with tempfile.NamedTemporaryFile(
                dir=destination.parent, prefix=f".{destination.name}.", delete=False
            ) as handle:
                handle.write(content_by_path[relative])
                handle.flush()
                os.fsync(handle.fileno())
                temp_path = Path(handle.name)
            temporary_files.append(temp_path)
            journal["temporary_files"] = [str(path) for path in temporary_files]
            write_json_atomic(journal_path, journal)
            if sha256_file(temp_path) != sha256_bytes(content_by_path[relative]):
                raise BootstrapError(f"temporary hash mismatch: {relative}")
            inject(f"before_replace:{relative}")
            destination = safe_destination(target, relative)
            if current_state(destination) != expected_states[relative]:
                raise BootstrapError(f"retrofit state changed immediately before replace: {relative}")
            os.replace(temp_path, destination)
            temporary_files.remove(temp_path)
            replaced.append(relative)
            journal["temporary_files"] = [str(path) for path in temporary_files]
            journal["replacements"].append(relative)
            write_json_atomic(journal_path, journal)
            if sha256_file(destination) != sha256_bytes(content_by_path[relative]):
                raise BootstrapError(f"post-write hash mismatch: {relative}")
            inject(f"after_replace:{relative}")
        inject("before_commit")
        for relative in allowed:
            destination = safe_destination(target, relative)
            if current_state(destination) != written_states[relative]:
                raise BootstrapError(f"retrofit output changed before commit: {relative}")
        journal["state"] = "committed_verified"
        write_json_atomic(journal_path, journal)
        shutil.rmtree(transaction_dir)
    except Exception as original_error:
        rollback_errors: list[str] = []
        for path in list(temporary_files):
            try:
                path.unlink(missing_ok=True)
                journal["rollback"].append({"temporary_removed": str(path)})
            except OSError as exc:
                rollback_errors.append(f"temporary cleanup {path}: {exc}")
        for relative in reversed(replaced):
            destination = safe_destination(target, relative)
            backup = backups[relative]
            try:
                if current_state(destination) != written_states[relative]:
                    rollback_errors.append(f"refused to overwrite externally changed destination {relative}")
                    continue
                if backup is None:
                    destination.unlink()
                    journal["rollback"].append({"removed_created_file": relative})
                else:
                    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}.rollback.", delete=False) as handle:
                        handle.write(backup.read_bytes())
                        handle.flush()
                        os.fsync(handle.fileno())
                        restore_temp = Path(handle.name)
                    os.replace(restore_temp, destination)
                    if sha256_file(destination) != expected_states[relative]:
                        raise BootstrapError(f"rollback hash mismatch: {relative}")
                    journal["rollback"].append({"restored": relative})
            except Exception as exc:
                rollback_errors.append(f"rollback {relative}: {exc}")
        for directory in sorted(created_dirs, key=lambda item: len(item.parts), reverse=True):
            try:
                directory.rmdir()
                journal["rollback"].append({"directory_removed": str(directory)})
            except OSError as exc:
                rollback_errors.append(f"directory cleanup {directory}: {exc}")
        journal["state"] = "rollback_failed" if rollback_errors else "rolled_back_after_failure"
        journal["original_error"] = str(original_error)
        journal["rollback_errors"] = rollback_errors
        write_json_atomic(journal_path, journal)
        if rollback_errors:
            raise BootstrapError(f"retrofit failed and rollback was incomplete; inspect {journal_path}: {rollback_errors}") from original_error
        raise
    finally:
        lock_path.unlink(missing_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--date", dest="install_date", default=date.today().isoformat())
    parser.add_argument("--mode", choices=("fresh", "retrofit"), default="fresh")
    parser.add_argument("--retrofit-plan", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        project_name = args.project_name.strip()
        if not project_name or "\n" in project_name or "\r" in project_name:
            raise BootstrapError("project name must be a nonempty single line")
        try:
            parsed_date = date.fromisoformat(args.install_date)
        except ValueError as exc:
            raise BootstrapError("--date must be YYYY-MM-DD") from exc
        if parsed_date.isoformat() != args.install_date:
            raise BootstrapError("--date must be canonical YYYY-MM-DD")

        target = args.target.absolute()
        package = load_package_manifest()
        payload, records = build_payload(package, project_name, args.install_date)
        retrofit_plan = args.retrofit_plan.absolute() if args.retrofit_plan else None
        retrofit_plan_sha256: str | None = None

        if args.mode == "fresh":
            if retrofit_plan is not None:
                raise BootstrapError("--retrofit-plan is invalid in fresh mode")
            preflight_fresh(target, list(payload))
            selected = sorted(payload)
        else:
            if retrofit_plan is None:
                raise BootstrapError("retrofit mode requires --retrofit-plan")
            plan = load_retrofit_plan(retrofit_plan, target)
            retrofit_plan_sha256 = str(plan.pop("_source_sha256"))
            selected, expected_states = preflight_retrofit(target, payload, plan)
            records = [item for item in records if item["path"] in selected]

        install_manifest = make_install_manifest(
            package,
            target,
            project_name,
            args.install_date,
            args.mode,
            records,
            retrofit_plan,
            retrofit_plan_sha256,
        )
        preview = {
            "status": "dry_run" if args.dry_run else "installed",
            "mode": args.mode,
            "target": str(target),
            "project_name": project_name,
            "files": selected + ([INSTALL_MANIFEST_NAME] if args.mode == "fresh" else []),
        }
        if args.dry_run:
            print(json.dumps(preview, indent=2, sort_keys=True))
            return 0

        if args.mode == "fresh":
            write_fresh(target, payload, install_manifest)
        else:
            write_retrofit(
                target,
                payload,
                install_manifest,
                selected,
                expected_states,
                retrofit_plan,
                retrofit_plan_sha256,
            )
        print(json.dumps(preview, indent=2, sort_keys=True))
        return 0
    except (BootstrapError, OSError, json.JSONDecodeError) as exc:
        print(f"bootstrap_error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(run())
