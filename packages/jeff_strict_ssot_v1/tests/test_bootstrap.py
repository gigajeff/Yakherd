from __future__ import annotations

import ast
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_PATH = PACKAGE_ROOT / "bootstrap.py"
SPEC = importlib.util.spec_from_file_location("jeff_strict_bootstrap", BOOTSTRAP_PATH)
assert SPEC and SPEC.loader
BOOTSTRAP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BOOTSTRAP)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BootstrapTests(unittest.TestCase):
    def run_quiet(self, args: list[str]) -> int:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return BOOTSTRAP.run(args)

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

    def retrofit_inputs(self, target: Path) -> tuple[dict[str, bytes], bytes, list[str], dict[str, str]]:
        package = BOOTSTRAP.load_package_manifest()
        payload, records = BOOTSTRAP.build_payload(package, "Retrofit", "2026-07-20")
        allowed = sorted([BOOTSTRAP.INSTALL_MANIFEST_NAME, "README.md"])
        selected_records = [item for item in records if item["path"] in allowed]
        manifest = BOOTSTRAP.make_install_manifest(package, target, "Retrofit", "2026-07-20", "retrofit", selected_records, None)
        expected = {
            BOOTSTRAP.INSTALL_MANIFEST_NAME: "absent",
            "README.md": sha256(target / "README.md"),
        }
        return payload, manifest, allowed, expected

    def test_manifest_matches_template_tree(self) -> None:
        manifest = BOOTSTRAP.load_package_manifest()
        self.assertGreater(len(manifest["template_files"]), 30)
        release = json.loads((PACKAGE_ROOT / "RELEASE.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["package_name"], release["package_name"])
        self.assertEqual(manifest["package_version"], release["package_version"])

    def test_runtime_scripts_use_only_standard_library_imports(self) -> None:
        paths = [
            BOOTSTRAP_PATH,
            PACKAGE_ROOT / "template/scripts/ssot/validate_protocol.py",
            PACKAGE_ROOT / "template/scripts/ssot/validate_governor_delta_policy.py",
            PACKAGE_ROOT / "template/scripts/ssot/migrate_status_archive.py",
        ]
        for path in paths:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            self.assertTrue(imported <= sys.stdlib_module_names, f"non-stdlib imports in {path}: {sorted(imported - sys.stdlib_module_names)}")

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "dry"
            code = self.run_quiet(["--target", str(target), "--project-name", "Dry", "--date", "2026-07-20", "--dry-run"])
            self.assertEqual(0, code)
            self.assertFalse(target.exists())

    def test_fresh_install_hashes_and_generated_validation(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "project"
            code = self.run_quiet(["--target", str(target), "--project-name", "Example Project", "--date", "2026-07-20"])
            self.assertEqual(0, code)
            self.assertIn("Example Project", (target / "README.md").read_text(encoding="utf-8"))
            self.assertEqual("@AGENTS.md\n", (target / "CLAUDE.md").read_text(encoding="utf-8"))
            record = json.loads((target / BOOTSTRAP.INSTALL_MANIFEST_NAME).read_text(encoding="utf-8"))
            self.assertEqual(
                BOOTSTRAP.load_package_manifest()["package_version"],
                record["package_version"],
            )
            for item in record["files"]:
                self.assertEqual(item["rendered_sha256"], sha256(target / item["path"]))
            protocol = subprocess.run(
                [sys.executable, str(target / "scripts/ssot/validate_protocol.py"), "--root", str(target), "--strict", "--summary"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, protocol.returncode, protocol.stdout + protocol.stderr)
            tests = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", str(target / "tests/ssot"), "-v"],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, tests.returncode, tests.stdout + tests.stderr)

    def test_second_fresh_install_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "project"
            args = ["--target", str(target), "--project-name", "Example", "--date", "2026-07-20"]
            self.assertEqual(0, self.run_quiet(args))
            original = sha256(target / "STATUS.md")
            self.assertNotEqual(0, self.run_quiet(args))
            self.assertEqual(original, sha256(target / "STATUS.md"))

    def test_rendered_files_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            first = Path(temp) / "first"
            second = Path(temp) / "second"
            common = ["--project-name", "Deterministic", "--date", "2026-07-20"]
            self.assertEqual(0, self.run_quiet(["--target", str(first), *common]))
            self.assertEqual(0, self.run_quiet(["--target", str(second), *common]))
            manifest = BOOTSTRAP.load_package_manifest()
            for relative in manifest["template_files"]:
                self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes(), relative)
            first_manifest = json.loads((first / BOOTSTRAP.INSTALL_MANIFEST_NAME).read_text(encoding="utf-8"))
            second_manifest = json.loads((second / BOOTSTRAP.INSTALL_MANIFEST_NAME).read_text(encoding="utf-8"))
            first_manifest["target"] = "<target>"
            second_manifest["target"] = "<target>"
            self.assertEqual(first_manifest, second_manifest)

    def test_repeated_dry_run_output_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "dry"
            args = ["--target", str(target), "--project-name", "Dry", "--date", "2026-07-20", "--dry-run"]
            outputs = []
            for _ in range(2):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    code = BOOTSTRAP.run(args)
                outputs.append((code, stdout.getvalue(), stderr.getvalue()))
            self.assertEqual(outputs[0], outputs[1])
            self.assertFalse(target.exists())

    def test_retrofit_requires_reviewed_exact_hash_plan(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "project"
            target.mkdir()
            status = target / "STATUS.md"
            status.write_text("old", encoding="utf-8")
            plan = Path(temp) / "plan.json"
            plan.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "reviewed": False,
                        "target": str(target.resolve()),
                        "allowed_files": ["STATUS.md"],
                        "expected_existing_sha256": {"STATUS.md": sha256(status)},
                    }
                ),
                encoding="utf-8",
            )
            code = self.run_quiet(["--mode", "retrofit", "--retrofit-plan", str(plan), "--target", str(target), "--project-name", "Retrofit", "--date", "2026-07-20"])
            self.assertNotEqual(0, code)
            self.assertEqual("old", status.read_text(encoding="utf-8"))

    def test_reviewed_retrofit_changes_only_allowlisted_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "project"
            target.mkdir()
            readme = target / "README.md"
            untouched = target / "product.txt"
            readme.write_text("old readme", encoding="utf-8")
            untouched.write_text("product state", encoding="utf-8")
            plan = Path(temp) / "plan.json"
            allowed = [BOOTSTRAP.INSTALL_MANIFEST_NAME, "README.md"]
            plan.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "reviewed": True,
                        "target": str(target.resolve()),
                        "allowed_files": allowed,
                        "expected_existing_sha256": {
                            BOOTSTRAP.INSTALL_MANIFEST_NAME: "absent",
                            "README.md": sha256(readme),
                        },
                    }
                ),
                encoding="utf-8",
            )
            code = self.run_quiet(["--mode", "retrofit", "--retrofit-plan", str(plan), "--target", str(target), "--project-name", "Retrofit", "--date", "2026-07-20"])
            self.assertEqual(0, code)
            self.assertIn("Retrofit", readme.read_text(encoding="utf-8"))
            self.assertEqual("product state", untouched.read_text(encoding="utf-8"))
            self.assertTrue((target / BOOTSTRAP.INSTALL_MANIFEST_NAME).is_file())

    def test_retrofit_rejects_target_alias_case_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "MixedCaseProject"
            target.mkdir()
            alias = target.parent / "mixedcaseproject"
            if os.name == "nt":
                with self.assertRaisesRegex(BOOTSTRAP.BootstrapError, "casing mismatch"):
                    BOOTSTRAP.validate_existing_chain(alias)
            else:
                self.assertFalse(alias.exists())

    def test_real_cli_rejects_fresh_and_retrofit_target_case_aliases(self) -> None:
        if os.name != "nt":
            self.skipTest("Windows case-alias behavior only")
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            base = Path(temp)
            target = base / "MixedCaseProject"
            target.mkdir()
            alias = base / "mixedcaseproject"
            self.assertEqual(
                2,
                self.run_quiet(["--target", str(alias), "--project-name", "Unsafe", "--date", "2026-07-20", "--dry-run"]),
            )
            readme = target / "README.md"
            readme.write_text("old", encoding="utf-8")
            plan = base / "plan.json"
            plan.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "reviewed": True,
                        "target": str(alias.absolute()),
                        "allowed_files": [BOOTSTRAP.INSTALL_MANIFEST_NAME, "README.md"],
                        "expected_existing_sha256": {
                            BOOTSTRAP.INSTALL_MANIFEST_NAME: "absent",
                            "README.md": sha256(readme),
                        },
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                2,
                self.run_quiet(["--mode", "retrofit", "--retrofit-plan", str(plan), "--target", str(alias), "--project-name", "Unsafe", "--date", "2026-07-20", "--dry-run"]),
            )
            self.assertEqual("old", readme.read_text(encoding="utf-8"))

    def test_retrofit_rejects_junction_parent_escape(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            base = Path(temp)
            target = base / "project"
            target.mkdir()
            external = base / "external"
            external.mkdir()
            junction = target / "docs"
            if not self.make_junction(junction, external):
                self.skipTest("junction/symlink creation unavailable")
            try:
                with self.assertRaisesRegex(BOOTSTRAP.BootstrapError, "reparse|symlink"):
                    BOOTSTRAP.safe_destination(target, "docs/task_protocol.md")
            finally:
                self.remove_link(junction)

    def test_retrofit_detects_race_and_preserves_external_change(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "project"
            target.mkdir()
            readme = target / "README.md"
            readme.write_text("old readme", encoding="utf-8")
            payload, manifest, allowed, expected = self.retrofit_inputs(target)
            external = "concurrent external edit"

            def race(phase: str) -> None:
                if phase == "before_replace:README.md":
                    readme.write_text(external, encoding="utf-8")

            with self.assertRaisesRegex(BOOTSTRAP.BootstrapError, "state changed immediately"):
                BOOTSTRAP.write_retrofit(target, payload, manifest, allowed, expected, fault_injector=race)
            self.assertEqual(external, readme.read_text(encoding="utf-8"))
            self.assertFalse((target / BOOTSTRAP.INSTALL_MANIFEST_NAME).exists())
            journals = list(target.glob(f"{BOOTSTRAP.RETROFIT_TXN_PREFIX}*/journal.json"))
            self.assertEqual(1, len(journals))
            self.assertEqual("rolled_back_after_failure", json.loads(journals[0].read_text(encoding="utf-8"))["state"])
            self.assertFalse((target / BOOTSTRAP.RETROFIT_LOCK_NAME).exists())

    def test_retrofit_rolls_back_injected_replacement_failures(self) -> None:
        for phase in [f"after_replace:{BOOTSTRAP.INSTALL_MANIFEST_NAME}", "after_replace:README.md"]:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
                target = Path(temp) / "project"
                target.mkdir()
                readme = target / "README.md"
                readme.write_text("old readme", encoding="utf-8")
                payload, manifest, allowed, expected = self.retrofit_inputs(target)

                def fail(current: str, expected_phase: str = phase) -> None:
                    if current == expected_phase:
                        raise RuntimeError(f"injected {expected_phase}")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    BOOTSTRAP.write_retrofit(target, payload, manifest, allowed, expected, fault_injector=fail)
                self.assertEqual("old readme", readme.read_text(encoding="utf-8"))
                self.assertFalse((target / BOOTSTRAP.INSTALL_MANIFEST_NAME).exists())
                self.assertFalse((target / BOOTSTRAP.RETROFIT_LOCK_NAME).exists())
                self.assertFalse(list(target.glob(".README.md.*")))
                journals = list(target.glob(f"{BOOTSTRAP.RETROFIT_TXN_PREFIX}*/journal.json"))
                self.assertEqual(1, len(journals))
                journal = json.loads(journals[0].read_text(encoding="utf-8"))
                self.assertEqual("rolled_back_after_failure", journal["state"])
                self.assertTrue(journal["rollback"])

    def test_retrofit_rejects_nonthrowing_commit_tamper_and_preserves_external_bytes(self) -> None:
        for fail_later in (False, True):
            with self.subTest(fail_later=fail_later), tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
                target = Path(temp) / "project"
                target.mkdir()
                readme = target / "README.md"
                readme.write_text("old readme", encoding="utf-8")
                payload, manifest, allowed, expected = self.retrofit_inputs(target)
                install = target / BOOTSTRAP.INSTALL_MANIFEST_NAME
                external = b"external-after-verified-write"

                def tamper(phase: str) -> None:
                    if phase == f"after_replace:{BOOTSTRAP.INSTALL_MANIFEST_NAME}":
                        install.write_bytes(external)
                    if fail_later and phase == "before_replace:README.md":
                        raise RuntimeError("later failure")

                with self.assertRaisesRegex(BOOTSTRAP.BootstrapError, "rollback was incomplete"):
                    BOOTSTRAP.write_retrofit(target, payload, manifest, allowed, expected, fault_injector=tamper)
                self.assertEqual(external, install.read_bytes())
                self.assertEqual("old readme", readme.read_text(encoding="utf-8"))
                journals = list(target.glob(f"{BOOTSTRAP.RETROFIT_TXN_PREFIX}*/journal.json"))
                self.assertEqual(1, len(journals))
                journal = json.loads(journals[0].read_text(encoding="utf-8"))
                self.assertEqual("rollback_failed", journal["state"])
                self.assertTrue(any("externally changed destination" in item for item in journal["rollback_errors"]))

    def test_template_tamper_is_rejected_by_source_hash_baseline(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            copied = Path(temp) / "package"
            shutil.copytree(PACKAGE_ROOT, copied, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            with (copied / "template/README.md").open("a", encoding="utf-8") as handle:
                handle.write("\ntampered\n")
            result = subprocess.run(
                [sys.executable, "-B", str(copied / "bootstrap.py"), "--target", str(Path(temp) / "target"), "--project-name", "Tamper", "--date", "2026-07-20", "--dry-run"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("template hash mismatch", result.stderr)

    def test_source_template_bytecode_is_rejected_not_ignored(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            copied = Path(temp) / "package"
            shutil.copytree(PACKAGE_ROOT, copied, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            cache = copied / "template/__pycache__"
            cache.mkdir()
            (cache / "unexpected.pyc").write_bytes(b"not authorized source")
            result = subprocess.run(
                [sys.executable, "-B", str(copied / "bootstrap.py"), "--target", str(Path(temp) / "target"), "--project-name", "Cache", "--date", "2026-07-20", "--dry-run"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("manifest/template mismatch", result.stderr)

    def test_fresh_install_cleans_every_created_file_after_write_phase_failure(self) -> None:
        phases = [
            "after_create:A.txt",
            "after_write:A.txt",
            "after_flush:A.txt",
            "after_fsync:A.txt",
            "after_verify:A.txt",
            f"after_create:{BOOTSTRAP.INSTALL_MANIFEST_NAME}",
            f"after_write:{BOOTSTRAP.INSTALL_MANIFEST_NAME}",
            f"after_flush:{BOOTSTRAP.INSTALL_MANIFEST_NAME}",
            f"after_fsync:{BOOTSTRAP.INSTALL_MANIFEST_NAME}",
            f"after_verify:{BOOTSTRAP.INSTALL_MANIFEST_NAME}",
        ]
        for phase in phases:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
                target = Path(temp) / "project"

                def fail(current: str, expected: str = phase) -> None:
                    if current == expected:
                        raise RuntimeError(f"injected {expected}")

                with self.assertRaisesRegex(RuntimeError, "injected"):
                    BOOTSTRAP.write_fresh(target, {"A.txt": b"payload"}, b"{}\n", fault_injector=fail)
                self.assertFalse(target.exists(), list(target.rglob("*")) if target.exists() else [])

    def test_fresh_install_cleans_file_after_post_write_hash_failure(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            target = Path(temp) / "project"
            original = BOOTSTRAP.sha256_file
            try:
                BOOTSTRAP.sha256_file = lambda path: "0" * 64
                with self.assertRaisesRegex(BOOTSTRAP.BootstrapError, "post-write hash mismatch"):
                    BOOTSTRAP.write_fresh(target, {"A.txt": b"payload"}, b"{}\n")
            finally:
                BOOTSTRAP.sha256_file = original
            self.assertFalse(target.exists(), list(target.rglob("*")) if target.exists() else [])

    def test_cli_rejects_fresh_target_through_junction(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            base = Path(temp)
            external = base / "external"
            external.mkdir()
            junction = base / "junction"
            if not self.make_junction(junction, external):
                self.skipTest("junction/symlink creation unavailable")
            try:
                code = self.run_quiet(["--target", str(junction / "project"), "--project-name", "Unsafe", "--date", "2026-07-20"])
                self.assertEqual(2, code)
                self.assertFalse((external / "project").exists())
            finally:
                self.remove_link(junction)

    def test_real_cli_rejects_fresh_and_retrofit_junction_targets(self) -> None:
        with tempfile.TemporaryDirectory(dir=PACKAGE_ROOT.parent) as temp:
            base = Path(temp)
            real_target = base / "real_target"
            real_target.mkdir()
            junction = base / "junction_target"
            if not self.make_junction(junction, real_target):
                self.skipTest("junction/symlink creation unavailable")
            try:
                self.assertEqual(
                    2,
                    self.run_quiet(["--target", str(junction), "--project-name", "Unsafe", "--date", "2026-07-20", "--dry-run"]),
                )
                readme = real_target / "README.md"
                readme.write_text("old", encoding="utf-8")
                plan = base / "plan.json"
                plan.write_text(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "reviewed": True,
                            "target": str(junction.absolute()),
                            "allowed_files": [BOOTSTRAP.INSTALL_MANIFEST_NAME, "README.md"],
                            "expected_existing_sha256": {
                                BOOTSTRAP.INSTALL_MANIFEST_NAME: "absent",
                                "README.md": sha256(readme),
                            },
                        }
                    ),
                    encoding="utf-8",
                )
                self.assertEqual(
                    2,
                    self.run_quiet(["--mode", "retrofit", "--retrofit-plan", str(plan), "--target", str(junction), "--project-name", "Unsafe", "--date", "2026-07-20", "--dry-run"]),
                )
                self.assertEqual("old", readme.read_text(encoding="utf-8"))
            finally:
                self.remove_link(junction)


if __name__ == "__main__":
    unittest.main()
