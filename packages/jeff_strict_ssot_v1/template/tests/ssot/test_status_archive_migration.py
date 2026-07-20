from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts/ssot/migrate_status_archive.py"
SPEC = importlib.util.spec_from_file_location("status_migration", SCRIPT_PATH)
assert SPEC and SPEC.loader
MIGRATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MIGRATION)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class StatusArchiveMigrationTests(unittest.TestCase):
    def run_main_quiet(self, args: list[str]) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return MIGRATION.main(args)

    def fixture(self, base: Path) -> tuple[Path, bytes, bytes, Path]:
        root = base / "repo"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        status = root / "STATUS.md"
        compact = root / "compact_STATUS.md"
        compact_bytes = status.read_bytes()
        compact.write_bytes(compact_bytes)
        original = compact_bytes + b"\n" + (b"historical detail\n" * 130)
        status.write_bytes(original)
        return root, original, compact_bytes, compact

    def prepare_args(self, root: Path, original: bytes, compact: Path, **extra: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "root": root,
            "compact_candidate": compact,
            "record": root / "docs/run_records/status_prepare.json",
            "date": "2026-07-20",
            "expected_current_sha256": digest(original),
            "fault_injector": None,
        }
        values.update(extra)
        return argparse.Namespace(**values)

    def rollback_args(self, root: Path, current: bytes, archive: Path, archived: bytes, **extra: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "root": root,
            "archive": archive,
            "expected_current_sha256": digest(current),
            "expected_archive_sha256": digest(archived),
            "record": root / "docs/run_records/status_rollback.json",
            "fault_injector": None,
        }
        values.update(extra)
        return argparse.Namespace(**values)

    def transaction_journal(self, root: Path) -> dict[str, object]:
        transactions = list(root.glob(f"{MIGRATION.TXN_PREFIX}*"))
        self.assertEqual(1, len(transactions))
        return json.loads((transactions[0] / "journal.json").read_text(encoding="utf-8"))

    def make_junction(self, link: Path, target: Path) -> bool:
        if os.name != "nt":
            try:
                link.symlink_to(target, target_is_directory=True)
                return True
            except OSError:
                return False
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True, check=False)
        return result.returncode == 0

    def remove_link(self, path: Path) -> None:
        if path.is_symlink():
            path.unlink()
        else:
            os.rmdir(path)

    def test_prepare_and_hash_guarded_rollback_preserve_exact_bytes(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root, original, compact_bytes, compact = self.fixture(Path(temp))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, MIGRATION.prepare(self.prepare_args(root, original, compact)))
            archive = root / "docs/status_history/STATUS_2026-07-20_pre_compaction.md"
            self.assertEqual(original, archive.read_bytes())
            self.assertEqual(compact_bytes, (root / "STATUS.md").read_bytes())
            prepare_record = json.loads((root / "docs/run_records/status_prepare.json").read_text(encoding="utf-8"))
            self.assertEqual("committed_verified", prepare_record["transaction_state"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, MIGRATION.rollback(self.rollback_args(root, compact_bytes, archive, original)))
            self.assertEqual(original, (root / "STATUS.md").read_bytes())
            rollback_record = json.loads((root / "docs/run_records/status_rollback.json").read_text(encoding="utf-8"))
            self.assertEqual("committed_verified", rollback_record["transaction_state"])
            self.assertFalse(any(root.glob(f"{MIGRATION.TXN_PREFIX}*")))

    def test_prepare_rejects_noncanonical_date_and_wrong_current_hash(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root, original, _, compact = self.fixture(Path(temp))
            with self.assertRaises((ValueError, TypeError)):
                MIGRATION.prepare(self.prepare_args(root, original, compact, date="2026-7-20"))
            with self.assertRaisesRegex(ValueError, "reviewed expectation"):
                MIGRATION.prepare(self.prepare_args(root, original, compact, expected_current_sha256="0" * 64))

    def test_prepare_rejects_traversal_and_junction_candidate(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            root, original, _, compact = self.fixture(base)
            outside = base / "outside.md"
            outside.write_bytes(compact.read_bytes())
            with self.assertRaisesRegex(ValueError, "escapes repository"):
                MIGRATION.prepare(self.prepare_args(root, original, outside))
            external = base / "external"
            external.mkdir()
            (external / "candidate.md").write_bytes(compact.read_bytes())
            junction = root / "junction"
            if not self.make_junction(junction, external):
                self.skipTest("junction/symlink creation unavailable")
            try:
                with self.assertRaisesRegex(ValueError, "reparse|symlink"):
                    MIGRATION.prepare(self.prepare_args(root, original, junction / "candidate.md"))
            finally:
                self.remove_link(junction)

    def test_prepare_detects_locked_state_change_without_losing_external_write(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root, original, _, compact = self.fixture(Path(temp))
            changed = b"external concurrent edit\n"

            def race(phase: str) -> None:
                if phase == "after_locked_preflight":
                    (root / "STATUS.md").write_bytes(changed)

            with self.assertRaisesRegex(ValueError, "changed immediately"):
                MIGRATION.prepare(self.prepare_args(root, original, compact, fault_injector=race))
            self.assertEqual(changed, (root / "STATUS.md").read_bytes())
            self.assertEqual("rolled_back_after_failure", self.transaction_journal(root)["state"])

    def test_prepare_rolls_back_every_injected_write_phase(self) -> None:
        phases = ["after_locked_preflight", "after_archive", "after_index", "after_status", "after_record", "before_commit"]
        for phase in phases:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root, original, _, compact = self.fixture(Path(temp))

                def fail(current: str, expected: str = phase) -> None:
                    if current == expected:
                        raise RuntimeError(f"injected {expected}")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    MIGRATION.prepare(self.prepare_args(root, original, compact, fault_injector=fail))
                self.assertEqual(original, (root / "STATUS.md").read_bytes())
                self.assertFalse((root / "docs/status_history/STATUS_2026-07-20_pre_compaction.md").exists())
                self.assertFalse((root / "docs/status_history/STATUS_2026-07-20_pre_compaction.index.json").exists())
                self.assertFalse((root / "docs/run_records/status_prepare.json").exists())
                self.assertEqual("rolled_back_after_failure", self.transaction_journal(root)["state"])
                self.assertFalse((root / MIGRATION.LOCK_NAME).exists())

    def test_prepare_detects_nonthrowing_output_tamper_before_commit(self) -> None:
        cases = [
            ("after_archive", "docs/status_history/STATUS_2026-07-20_pre_compaction.md"),
            ("after_index", "docs/status_history/STATUS_2026-07-20_pre_compaction.index.json"),
            ("after_record", "docs/run_records/status_prepare.json"),
        ]
        for phase, relative in cases:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root, original, _, compact = self.fixture(Path(temp))

                def tamper(current: str, expected: str = phase, path: Path = root / relative) -> None:
                    if current == expected:
                        path.write_bytes(b"external tamper\n")

                with self.assertRaises(ValueError):
                    MIGRATION.prepare(self.prepare_args(root, original, compact, fault_injector=tamper))
                self.assertEqual(original, (root / "STATUS.md").read_bytes())
                self.assertEqual("rollback_failed", self.transaction_journal(root)["state"])

    def test_prepare_preserves_external_status_change_after_replacement(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root, original, _, compact = self.fixture(Path(temp))
            external = b"external status after replacement\n"

            def tamper(phase: str) -> None:
                if phase == "after_status":
                    (root / "STATUS.md").write_bytes(external)

            with self.assertRaisesRegex(ValueError, "rollback was incomplete"):
                MIGRATION.prepare(self.prepare_args(root, original, compact, fault_injector=tamper))
            self.assertEqual(external, (root / "STATUS.md").read_bytes())
            self.assertEqual("rollback_failed", self.transaction_journal(root)["state"])

    def test_prepare_rejects_repository_root_junction(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            real_root, original, _, compact = self.fixture(base)
            alias = base / "repo_alias"
            if not self.make_junction(alias, real_root):
                self.skipTest("junction/symlink creation unavailable")
            try:
                alias_compact = alias / compact.relative_to(real_root)
                with self.assertRaisesRegex(ValueError, "reparse|symlink"):
                    MIGRATION.prepare(self.prepare_args(alias, original, alias_compact))
            finally:
                self.remove_link(alias)

    def test_real_cli_rejects_case_alias_and_junction_roots_for_both_actions(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            real_root, original, _, compact = self.fixture(base)
            archive = real_root / "archive_for_alias_test.md"
            archive.write_bytes(b"archive\n")
            aliases: list[Path] = []
            if os.name == "nt":
                aliases.append(real_root.parent / real_root.name.upper())
            junction = base / "root_junction"
            if self.make_junction(junction, real_root):
                aliases.append(junction)
            try:
                for alias in aliases:
                    with self.subTest(alias=str(alias), action="prepare"):
                        self.assertEqual(
                            2,
                            self.run_main_quiet(
                                [
                                    "prepare", "--root", str(alias),
                                    "--compact-candidate", str(alias / compact.relative_to(real_root)),
                                    "--date", "2026-07-20",
                                    "--expected-current-sha256", digest(original),
                                    "--record", str(alias / "docs/run_records/alias_prepare.json"),
                                ]
                            ),
                        )
                    with self.subTest(alias=str(alias), action="rollback"):
                        self.assertEqual(
                            2,
                            self.run_main_quiet(
                                [
                                    "rollback", "--root", str(alias),
                                    "--archive", str(alias / archive.relative_to(real_root)),
                                    "--expected-current-sha256", digest(original),
                                    "--expected-archive-sha256", digest(archive.read_bytes()),
                                    "--record", str(alias / "docs/run_records/alias_rollback.json"),
                                ]
                            ),
                        )
                self.assertEqual(original, (real_root / "STATUS.md").read_bytes())
            finally:
                if junction in aliases:
                    self.remove_link(junction)

    def test_rollback_rejects_wrong_hash_and_traversal(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            root = base / "repo"
            root.mkdir()
            (root / "STATUS.md").write_bytes(b"current")
            archive = root / "archive.md"
            archive.write_bytes(b"archive")
            with self.assertRaisesRegex(ValueError, "current STATUS.md hash"):
                MIGRATION.rollback(self.rollback_args(root, b"wrong", archive, b"archive"))
            outside = base / "outside.md"
            outside.write_bytes(b"archive")
            with self.assertRaisesRegex(ValueError, "escapes repository"):
                MIGRATION.rollback(self.rollback_args(root, b"current", outside, b"archive"))
            self.assertEqual(b"current", (root / "STATUS.md").read_bytes())

    def test_rollback_restores_preoperation_state_at_every_write_phase(self) -> None:
        phases = ["after_locked_preflight", "after_status", "after_record", "before_commit"]
        for phase in phases:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root = Path(temp) / "repo"
                (root / "docs/run_records").mkdir(parents=True)
                current = b"compact current\n"
                archived = b"historical status\n"
                (root / "STATUS.md").write_bytes(current)
                archive = root / "archive.md"
                archive.write_bytes(archived)

                def fail(current_phase: str, expected: str = phase) -> None:
                    if current_phase == expected:
                        raise RuntimeError(f"injected {expected}")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    MIGRATION.rollback(self.rollback_args(root, current, archive, archived, fault_injector=fail))
                self.assertEqual(current, (root / "STATUS.md").read_bytes())
                self.assertFalse((root / "docs/run_records/status_rollback.json").exists())
                self.assertEqual("rolled_back_after_failure", self.transaction_journal(root)["state"])
                self.assertFalse((root / MIGRATION.LOCK_NAME).exists())

    def test_rollback_detects_nonthrowing_record_and_archive_tamper(self) -> None:
        for phase, target_name in [("after_status", "archive"), ("after_record", "record")]:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root = Path(temp) / "repo"
                (root / "docs/run_records").mkdir(parents=True)
                current = b"compact current\n"
                archived = b"historical status\n"
                (root / "STATUS.md").write_bytes(current)
                archive = root / "archive.md"
                archive.write_bytes(archived)
                record = root / "docs/run_records/status_rollback.json"

                def tamper(current_phase: str, expected: str = phase) -> None:
                    if current_phase == expected:
                        (archive if target_name == "archive" else record).write_bytes(b"external tamper\n")

                with self.assertRaises(ValueError):
                    MIGRATION.rollback(self.rollback_args(root, current, archive, archived, fault_injector=tamper))
                self.assertEqual(current, (root / "STATUS.md").read_bytes())
                expected_state = "rollback_failed" if target_name == "record" else "rolled_back_after_failure"
                self.assertEqual(expected_state, self.transaction_journal(root)["state"])


if __name__ == "__main__":
    unittest.main()
