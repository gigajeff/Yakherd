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
    def test_process_broker_uses_only_standard_library_imports(self) -> None:
        path = ROOT / "src" / "yakherd" / "process_hygiene.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
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
