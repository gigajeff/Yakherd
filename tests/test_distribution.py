"""Checks for the public Python distribution adapter."""

from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yakherd.cli import run_bootstrap  # noqa: E402


class DistributionTests(unittest.TestCase):
    def run_source_cli(
        self,
        arguments: list[str],
        *,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "yakherd.py"), *arguments],
            cwd=ROOT if cwd is None else cwd,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_public_runtime_uses_only_standard_library_imports(self) -> None:
        for relative in ("cli.py", "process_hygiene.py"):
            with self.subTest(relative=relative):
                path = ROOT / "src" / "yakherd" / relative
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                imported = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported.update(
                            alias.name.split(".", 1)[0] for alias in node.names
                        )
                    elif (
                        isinstance(node, ast.ImportFrom)
                        and node.module
                        and node.level == 0
                    ):
                        imported.add(node.module.split(".", 1)[0])
                self.assertTrue(
                    imported <= sys.stdlib_module_names,
                    f"non-stdlib imports: {sorted(imported - sys.stdlib_module_names)}",
                )

    def test_public_version_matches_reviewed_release(self) -> None:
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        release = json.loads(
            (
                ROOT / "packages" / "jeff_strict_ssot_v1" / "RELEASE.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(project["project"]["name"], "yakherd")
        self.assertEqual(
            project["project"]["version"], release["package_version"]
        )

    def test_source_cli_performs_a_dry_run(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            target = Path(temporary) / "new-project"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "yakherd.py"),
                    "init",
                    "--target",
                    str(target),
                    "--project-name",
                    "Distribution Smoke Test",
                    "--date",
                    "2026-07-20",
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("dry_run", completed.stdout)
            self.assertFalse(target.exists())

    def test_no_argument_cli_prints_non_mutating_quick_start(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            target = Path(temporary)
            completed = self.run_source_cli([], cwd=target)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("Run: yakherd setup", completed.stdout)
            self.assertIn("More commands: yakherd --help", completed.stdout)
            self.assertEqual([], list(target.iterdir()))

    def test_setup_derives_name_installs_validates_and_is_idempotent(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            target = Path(temporary) / "FriendlyProject"
            first = self.run_source_cli(
                ["setup", str(target), "--date", "2026-07-20"]
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("without overwriting existing files", first.stdout)
            self.assertIn("Yakherd doctor: ready", first.stdout)
            self.assertIn('say: "Start Yakherd"', first.stdout)
            self.assertIn(
                "# FriendlyProject",
                (target / "README.md").read_text(encoding="utf-8"),
            )
            before = {
                path.relative_to(target).as_posix(): path.read_bytes()
                for path in target.rglob("*")
                if path.is_file()
            }

            second = self.run_source_cli(["setup", str(target)])

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("validating instead of reinstalling", second.stdout)
            after = {
                path.relative_to(target).as_posix(): path.read_bytes()
                for path in target.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)

    def test_setup_preserves_unrelated_files_and_stops_on_collision(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            root = Path(temporary)
            additive = root / "additive"
            additive.mkdir()
            product = additive / "product.txt"
            product.write_bytes(b"product bytes\n")

            completed = self.run_source_cli(
                ["setup", str(additive), "--date", "2026-07-20"]
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(b"product bytes\n", product.read_bytes())
            self.assertTrue((additive / "JEFF_STRICT_SSOT_INSTALL.json").is_file())

            collision = root / "collision"
            collision.mkdir()
            readme = collision / "README.md"
            readme.write_bytes(b"keep me\n")
            blocked = self.run_source_cli(
                ["setup", str(collision), "--date", "2026-07-20"]
            )

            self.assertEqual(blocked.returncode, 2)
            self.assertIn("No existing file was overwritten", blocked.stderr)
            self.assertIn("README.md", blocked.stderr)
            self.assertEqual([readme], list(collision.iterdir()))
            self.assertEqual(b"keep me\n", readme.read_bytes())

    def test_doctor_is_read_only_and_rejects_changed_installed_validator(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            root = Path(temporary)
            target = root / "project"
            installed = self.run_source_cli(
                ["setup", str(target), "--date", "2026-07-20"]
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            sentinel = root / "executed.txt"
            validator = target / "scripts" / "ssot" / "validate_protocol.py"
            validator.write_text(
                f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('bad')\n",
                encoding="utf-8",
                newline="\n",
            )

            checked = self.run_source_cli(["doctor", str(target)])

            self.assertEqual(checked.returncode, 1)
            self.assertIn("installed validator has changed", checked.stderr)
            self.assertFalse(sentinel.exists())

    def test_doctor_reports_uninitialized_directory(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            target = Path(temporary)
            completed = self.run_source_cli(["doctor", str(target)])
            self.assertEqual(completed.returncode, 2)
            self.assertIn("no Yakherd installation receipt", completed.stderr)
            self.assertIn("yakherd setup", completed.stderr)

    def test_source_cli_reports_empty_process_state(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            environment = dict(os.environ)
            environment["YAKHERD_PROCESS_STATE"] = str(Path(temporary) / "state")
            completed = subprocess.run(
                [sys.executable, "-B", str(ROOT / "yakherd.py"), "process", "status"],
                cwd=ROOT,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual(report["policy"], "Y-PROC-1.1")
            self.assertEqual(report["active_finite_tasks"], [])

    def test_installed_bundle_ignores_pip_bytecode(self) -> None:
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            root = Path(temporary)
            bundle = root / "_bundle"
            shutil.copytree(
                ROOT / "packages" / "jeff_strict_ssot_v1",
                bundle,
            )
            cache = bundle / "template" / "tests" / "ssot" / "__pycache__"
            cache.mkdir()
            (cache / "pip-generated.pyc").write_bytes(b"not reviewed source")
            target = root / "new-project"

            returncode = run_bootstrap(
                bundle / "bootstrap.py",
                [
                    "--mode",
                    "fresh",
                    "--target",
                    str(target),
                    "--project-name",
                    "Bytecode Staging Test",
                    "--date",
                    "2026-07-20",
                    "--dry-run",
                ],
            )

            self.assertEqual(returncode, 0)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
