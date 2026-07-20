from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts/ssot/validate_governor_delta_policy.py"
SPEC = importlib.util.spec_from_file_location("governor_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class GovernorPolicyTests(unittest.TestCase):
    def test_bootstrap_policy_passes(self) -> None:
        self.assertEqual([], VALIDATOR.validate(ROOT))

    def test_quiet_write_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = Path(temp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            path = root / "docs/governance/GOVERNOR_DELTA_POLICY.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["modes"]["quiet"]["writes_allowed"] = True
            path.write_text(json.dumps(data), encoding="utf-8")
            errors = VALIDATOR.validate(root)
            self.assertTrue(any("quiet.writes_allowed" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
