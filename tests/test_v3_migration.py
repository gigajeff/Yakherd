"""Adversarial migration/doctor checks against real temporary repositories."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from yakherd.cli import load_engine
from yakherd import migration
from yakherd.diagnostics import inspect


class MigrationTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".tmp").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "project"
        self.target.mkdir()
        self.replacements = self.root / "prepared"
        self.replacements.mkdir()
        self.plan = self.root / "plan.json"
        self.engine = load_engine()
        payload, _ = self.engine.build_payload(self.engine.load_package_manifest(), "Test Product", "2026-09-24")
        for name, value in payload.items():
            path = self.replacements / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
        (self.target / "README.md").write_bytes(b"# Original product\nKeep these original bytes.\n")
        (self.target / "product.py").write_bytes(b"product source untouched\n")

    def prepare(self):
        return migration.prepare(self.target, self.replacements, self.plan, self.engine)

    def review(self, edit=None):
        data = json.loads(self.plan.read_text(encoding="utf-8"))
        data["reviewed"] = True
        if edit:
            edit(data)
        self.plan.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return migration.digest(self.plan.read_bytes())

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes() for p in self.target.rglob("*") if p.is_file()}

    def test_plan_and_preview_do_not_write_target(self):
        before = self.snapshot()
        result = self.prepare()
        preview = migration.preview(self.plan, self.engine)
        self.assertFalse(result["reviewed"])
        self.assertEqual(before, self.snapshot())
        self.assertIn("Original product", next(x["diff"] for x in preview["changes"] if x["path"] == "README.md"))

    def test_requires_review_and_exact_plan_hash(self):
        self.prepare()
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "reviewed=true"):
            migration.apply(self.plan, migration.digest(self.plan.read_bytes()), self.engine)
        sha = self.review()
        with self.assertRaisesRegex(ValueError, "plan hash"):
            migration.apply(self.plan, "0" * 64, self.engine)
        self.assertEqual(before, self.snapshot())
        self.assertNotEqual(sha, "0" * 64)

    def test_applies_exact_content_retains_originals_and_read_only_doctor(self):
        original = (self.target / "README.md").read_bytes()
        self.prepare()
        result = migration.apply(self.plan, self.review(), self.engine)
        self.assertEqual((self.replacements / "README.md").read_bytes(), (self.target / "README.md").read_bytes())
        self.assertEqual(b"product source untouched\n", (self.target / "product.py").read_bytes())
        backup = Path(result["backup"])
        journal = json.loads((backup / "journal.json").read_text(encoding="utf-8"))
        self.assertEqual("committed_verified", journal["state"])
        self.assertEqual(original, (backup / journal["backups"]["README.md"]["path"]).read_bytes())
        before = self.snapshot()
        report = inspect(self.target, self.engine)
        self.assertEqual("ready", report["status"], report)
        self.assertEqual(before, self.snapshot())

    def test_target_drift_rejected_without_clobbering(self):
        self.prepare()
        sha = self.review()
        (self.target / "README.md").write_text("new human work", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(self.engine.BootstrapError, "expected-state mismatch"):
            migration.apply(self.plan, sha, self.engine)
        self.assertEqual(before, self.snapshot())

    def test_embedded_content_tamper_and_package_drift_rejected(self):
        self.prepare()
        sha = self.review(lambda p: p["files"]["README.md"].update(content="tampered"))
        with self.assertRaisesRegex(ValueError, "content hash"):
            migration.apply(self.plan, sha, self.engine)
        sha = self.review(lambda p: p.update(package_manifest_sha256="0" * 64))
        with self.assertRaisesRegex(ValueError, "different package"):
            migration.apply(self.plan, sha, self.engine)

    def test_plan_cannot_write_product_code_git_config_or_escape(self):
        for name in ("../outside.md", "/outside.md", "C:/outside.md", "docs/../outside.md",
                     ".git/config", "product.py", "docs/.git/config.md", "CON.md", "docs/a:stream.md"):
            with self.subTest(name=name), self.assertRaises((ValueError, self.engine.BootstrapError)):
                migration.allowed_path(name, self.engine)

    def test_alias_allowlist_and_missing_owner_rejected(self):
        self.prepare()
        sha = self.review(lambda p: p["allowed_files"].append("readme.md"))
        with self.assertRaisesRegex(ValueError, "allowlist"):
            migration.apply(self.plan, sha, self.engine)
        sha = self.review(lambda p: p["files"].pop("NOW.md"))
        with self.assertRaisesRegex(ValueError, "pin all"):
            migration.apply(self.plan, sha, self.engine)

    def test_invalid_candidate_fails_before_target_changes(self):
        (self.replacements / "NOW.md").write_text("# Not a milestone\n", encoding="utf-8")
        self.prepare()
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "structurally invalid"):
            migration.apply(self.plan, self.review(), self.engine)
        self.assertEqual(before, self.snapshot())

    def test_existing_legacy_launcher_must_be_retired_explicitly(self):
        launcher = self.target / "docs/prompts/codex_team_launcher.md"
        launcher.parent.mkdir(parents=True)
        launcher.write_text("Create exactly five direct role agents\n", encoding="utf-8")
        self.prepare()
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "active legacy startup"):
            migration.apply(self.plan, self.review(), self.engine)
        self.assertEqual(before, self.snapshot())

    def test_interrupted_write_restores_originals_and_leaves_recovery_journal(self):
        self.prepare()
        sha = self.review()
        before = self.snapshot()
        def fault(phase):
            if phase == "after_replace:README.md":
                raise RuntimeError("injected interruption")
        with self.assertRaisesRegex(RuntimeError, "injected interruption"):
            migration.apply(self.plan, sha, self.engine, fault_injector=fault)
        after = self.snapshot()
        for name, content in before.items():
            self.assertEqual(content, after[name])
        self.assertFalse((self.target / self.engine.INSTALL_MANIFEST_NAME).exists())
        journals = list(self.target.glob(self.engine.RETROFIT_TXN_PREFIX + "*/journal.json"))
        self.assertEqual(1, len(journals))
        self.assertEqual("rolled_back_after_failure", json.loads(journals[0].read_text())["state"])
        with self.assertRaisesRegex(self.engine.BootstrapError, "unresolved"):
            migration.apply(self.plan, sha, self.engine)

    def test_plan_change_after_preflight_is_detected_under_lock(self):
        self.prepare()
        sha = self.review()
        original = self.engine.write_retrofit
        def change_plan(*args, **kwargs):
            self.plan.write_bytes(self.plan.read_bytes() + b" ")
            return original(*args, **kwargs)
        self.engine.write_retrofit = change_plan
        with self.assertRaisesRegex(self.engine.BootstrapError, "plan changed"):
            migration.apply(self.plan, sha, self.engine)
        self.assertEqual(b"# Original product\nKeep these original bytes.\n", (self.target / "README.md").read_bytes())

    def test_preview_has_no_target_execution(self):
        marker = self.root / "executed"
        (self.target / "README.md").write_text(f"[data](https://example.com/)\n{marker}", encoding="utf-8")
        trap = self.target / "scripts/ssot/validate_protocol.py"
        trap.parent.mkdir(parents=True)
        trap.write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()", encoding="utf-8")
        self.prepare()
        migration.preview(self.plan, self.engine)
        migration.apply(self.plan, self.review(), self.engine)
        self.assertEqual("ready", inspect(self.target, self.engine)["status"])
        self.assertFalse(marker.exists())

    @unittest.skipIf(os.name == "nt", "Windows junction containment covered in package transaction tests")
    def test_symlinked_source_is_rejected(self):
        outside = self.root / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        path = self.replacements / "README.md"
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaisesRegex(self.engine.BootstrapError, "symlink"):
            self.prepare()


if __name__ == "__main__":
    unittest.main()
