from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts/ssot/validate_protocol.py"
SPEC = importlib.util.spec_from_file_location("strict_ssot_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ProtocolValidatorTests(unittest.TestCase):
    def clone(self, destination: Path) -> Path:
        root = destination / "repo"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return root

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

    def evidence(self, root: Path, **changes: object) -> Path:
        stdout = root / "stdout.txt"
        stderr = root / "stderr.txt"
        artifact = root / "artifact.txt"
        stdout.write_text("ok\n", encoding="utf-8")
        stderr.write_text("", encoding="utf-8")
        artifact.write_text("artifact\n", encoding="utf-8")
        data: dict[str, object] = {
            "schema_version": 1,
            "evidence_class": "protocol",
            "timestamp_utc": "2026-07-20T12:00:00Z",
            "working_directory": str(root),
            "command": ["python", "check.py"],
            "exit_code": 0,
            "environment": {"machine": "fixture", "os": "test", "runtime": "python"},
            "supported_claim": "bounded fixture claim",
            "stdout": {"inline": None, "path": "stdout.txt", "sha256": digest(stdout)},
            "stderr": {"inline": None, "path": "stderr.txt", "sha256": digest(stderr)},
            "artifacts": [{"path": "artifact.txt", "sha256": digest(artifact)}],
            "authority_effect": "none",
            "limitations": ["fixture only"],
        }
        data.update(changes)
        path = root / "evidence.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_bootstrap_repository_passes(self) -> None:
        errors, warnings = VALIDATOR.validate(ROOT, [])
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_pure_validator_has_no_ambient_clock_dependency(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        ambient_clock = re.compile(
            r"\b(?:dt\.)?(?:datetime|date)\.(?:now|today)\s*\("
        )
        self.assertIsNone(ambient_clock.search(source))

        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            status = root / "STATUS.md"
            original = status.read_text(encoding="utf-8")
            text = re.sub(
                r"(?<=- Last updated UTC: `)\d{4}-\d{2}-\d{2}T00:00:00Z(?=`)",
                "2000-01-01T00:00:00Z",
                original,
                count=1,
            )
            self.assertNotEqual(original, text)
            status.write_text(text, encoding="utf-8", newline="\n")
            errors, warnings = VALIDATOR.validate(root, [])
            self.assertEqual([], errors)
            self.assertEqual([], warnings)

            status.write_text(
                text.replace("2000-01-01T00:00:00Z", "2000-01-01T00:00:00"),
                encoding="utf-8",
                newline="\n",
            )
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(
                any("Last updated UTC is invalid" in item for item in errors),
                errors,
            )

    def test_cold_resume_prompt_authorizes_structured_run_records(self) -> None:
        prompt = (
            ROOT / "docs" / "prompts" / "bootstrap_cold_resume_review.md"
        ).read_text(encoding="utf-8")
        for suffix in (
            "protocol",
            "governor",
            "tests",
            "manifest",
            "evidence_check",
        ):
            self.assertIn(
                f"docs/run_records/bootstrap_cold_resume_<RUN_ID>_{suffix}.json",
                prompt,
            )
        self.assertIn("docs/templates/run_record.json", prompt)
        self.assertIn("--evidence", prompt)
        self.assertIn("__pycache__", prompt)
        self.assertIn("START_HERE.md", prompt)
        self.assertIn("docs/GITHUB_SETUP.md", prompt)
        self.assertIn("Codex launcher", prompt)
        self.assertIn("product-intake prompt", prompt)
        self.assertIn("all five Codex role agents", prompt)

        testing = (ROOT / "TESTING.md").read_text(encoding="utf-8")
        commands = [line for line in testing.splitlines() if line.startswith("python ")]
        self.assertEqual(3, len(commands))
        self.assertTrue(all(line.startswith("python -B ") for line in commands))

    def test_codex_launcher_github_and_prompt_intake_boundaries_are_required(self) -> None:
        errors, _ = VALIDATOR.validate(ROOT, [])
        self.assertEqual([], errors)

        mutations = [
            (
                "docs/prompts/codex_team_launcher.md",
                "exactly five direct role agents",
                "Codex team launcher missing invariant",
            ),
            (
                "docs/GITHUB_SETUP.md",
                "Required Human Checkpoint",
                "GitHub setup missing safety boundary",
            ),
            (
                "docs/prompts/product_intake.md",
                "capture_limitations",
                "product intake missing provenance boundary",
            ),
        ]
        for relative, required, expected in mutations:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory(
                dir=ROOT.parent
            ) as temp:
                root = self.clone(Path(temp))
                path = root / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace(required, "removed", 1),
                    encoding="utf-8",
                    newline="\n",
                )
                errors, _ = VALIDATOR.validate(root, [])
                self.assertTrue(any(expected in item for item in errors), errors)

    def test_y_proc_1_policy_and_compact_agents_pointer_are_required(self) -> None:
        errors, _ = VALIDATOR.validate(ROOT, [])
        self.assertEqual([], errors)

        mutations = [
            (
                "AGENTS.md",
                ".yakherd/policies/Y-PROC-1.md",
                "AGENTS.md must point to the Y-PROC-1 policy owner",
            ),
            (
                ".yakherd/policies/Y-PROC-1.md",
                "executable-name matching",
                "Y-PROC-1 policy missing safety boundary",
            ),
            (
                ".yakherd/policies/Y-PROC-1.md",
                "explicit human authorization",
                "Y-PROC-1 policy missing safety boundary",
            ),
        ]
        for relative, required, expected in mutations:
            with self.subTest(relative=relative, required=required), tempfile.TemporaryDirectory(
                dir=ROOT.parent
            ) as temp:
                root = self.clone(Path(temp))
                path = root / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace(required, "removed", 1),
                    encoding="utf-8",
                    newline="\n",
                )
                errors, _ = VALIDATOR.validate(root, [])
                self.assertTrue(any(expected in item for item in errors), errors)

    def test_proportional_modes_and_review_circuit_breaker_are_required(self) -> None:
        mutations = [
            (
                "docs/task_protocol.md",
                "Classify only the authorized slice, not hypothetical future features.",
                "task protocol missing review control",
            ),
            (
                "docs/task_protocol.md",
                "Bounded mode needs no Architecture plan and no Red Team gate.",
                "task protocol missing review control",
            ),
            (
                "docs/task_protocol.md",
                "A missing enhancement outside accepted scope is not a finding.",
                "task protocol missing review control",
            ),
            (
                "docs/task_protocol.md",
                "After a second consecutive `FAIL`",
                "task protocol missing review control",
            ),
            (
                "docs/task_protocol.md",
                "Do not create `_v2`, `_v3`",
                "task protocol missing review control",
            ),
            (
                "docs/prompts/implementation_task.md",
                "user-approved bounded brief",
                "Implementation prompt missing direct bounded authorization",
            ),
            (
                "docs/prompts/red_team_task.md",
                "outside accepted scope is not a finding",
                "Red Team prompt missing scope control",
            ),
        ]
        for relative, required, expected in mutations:
            with self.subTest(relative=relative, required=required), tempfile.TemporaryDirectory(
                dir=ROOT.parent
            ) as temp:
                root = self.clone(Path(temp))
                path = root / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace(required, "removed", 1),
                    encoding="utf-8",
                    newline="\n",
                )
                errors, _ = VALIDATOR.validate(root, [])
                self.assertTrue(any(expected in item for item in errors), errors)

    def test_product_intake_is_human_confirmed_not_universally_red_teamed(self) -> None:
        intake = (ROOT / "docs/prompts/product_intake.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("independent Red Team PASS", intake)
        self.assertIn("human confirmation", intake)
        self.assertIn("no automatic Architecture plan or Red Team review", intake)

    def test_review_template_has_binary_verdict_and_two_cycle_limit(self) -> None:
        template = (ROOT / "docs/templates/red_team_review.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("pass_with_fixes", template.lower())
        self.assertIn("- Review cycle: 1 | 2", template)
        self.assertIn("- Verdict: PASS | FAIL", template)
        self.assertIn("cannot require cycle 3", template)

    def test_bootstrap_review_does_not_restore_universal_intake_gate(self) -> None:
        prompt = (
            ROOT / "docs/prompts/bootstrap_cold_resume_review.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("independent\n  intake review", prompt)
        self.assertNotIn("before reviewed intake", prompt)
        self.assertIn("Bounded mode has no product-intake Red Team gate.", prompt)
        self.assertIn("direct Implementation authorization", prompt)
        self.assertIn("two-review circuit breaker", prompt)

    def test_status_caps_are_hard_failures(self) -> None:
        for suffix, expected in [("\n" + "\n".join("extra" for _ in range(130)), "exceeds 120 lines"), ("x" * 33000, "exceeds 32768")]:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root = self.clone(Path(temp))
                status = root / "STATUS.md"
                status.write_text(status.read_text(encoding="utf-8") + suffix, encoding="utf-8")
                errors, _ = VALIDATOR.validate(root, [])
                self.assertTrue(any(expected in item for item in errors), errors)

    def test_required_path_casing_and_reparse_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            status = root / "STATUS.md"
            interim = root / "STATUS.tmp"
            status.rename(interim)
            interim.rename(root / "status.md")
            errors, _ = VALIDATOR.validate(root, [])
            expected = "casing mismatch" if os.name == "nt" else "required path invalid"
            self.assertTrue(any(expected in item for item in errors), errors)
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            root = self.clone(base)
            external = base / "external_governance"
            shutil.copytree(root / "docs/governance", external)
            shutil.rmtree(root / "docs/governance")
            if not self.make_junction(root / "docs/governance", external):
                self.skipTest("junction/symlink creation unavailable")
            try:
                errors, _ = VALIDATOR.validate(root, [])
                self.assertTrue(any("reparse/symlink" in item for item in errors), errors)
            finally:
                self.remove_link(root / "docs/governance")

    def test_claude_adapter_is_required_and_exact(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            (root / "CLAUDE.md").unlink()
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("required path invalid: CLAUDE.md" in item for item in errors), errors)
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            (root / "CLAUDE.md").write_text("# Duplicated rules\n", encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("must contain only the @AGENTS.md import" in item for item in errors), errors)

    def test_owner_path_must_resolve(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            ssot = root / "SSOT.md"
            ssot.write_text(ssot.read_text(encoding="utf-8").replace("`ARCHITECTURE.md`", "`MISSING_OWNER.md`", 1), encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("owner path" in item and "invalid" in item for item in errors), errors)

    def test_decision_ids_states_owners_and_reciprocity_are_enforced(self) -> None:
        cases = {
            "duplicate": ("\n## DEC-0001: Duplicate\n\n- Date: 2026-07-20\n", "duplicate decision ID"),
            "state": (None, "invalid status"),
            "owner": (None, "current owner invalid"),
            "reciprocal": (None, "not reciprocal"),
        }
        for case, (_, expected) in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root = self.clone(Path(temp))
                decisions = root / "DECISIONS.md"
                text = decisions.read_text(encoding="utf-8")
                if case == "duplicate":
                    text += cases[case][0] or ""
                elif case == "state":
                    text = text.replace("- Status: accepted", "- Status: maybe", 1)
                elif case == "owner":
                    text = text.replace("- Current owner: `DECISIONS.md`", "- Current owner: MISSING.md", 1)
                else:
                    text += (
                        "\n## DEC-0002: Successor\n\n"
                        "- Date: 2026-07-20\n- Status: accepted\n- Current owner: DECISIONS.md\n"
                        "- Supersedes: DEC-0001\n- Superseded by: none\n"
                        "- Retained boundary: fixture\n- Decision: fixture\n- Evidence: none\n"
                    )
                decisions.write_text(text, encoding="utf-8")
                errors, _ = VALIDATOR.validate(root, [])
                self.assertTrue(any(expected in item for item in errors), errors)

    def test_superseded_decision_requires_an_accepted_reciprocal_successor(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            decisions = root / "DECISIONS.md"
            text = decisions.read_text(encoding="utf-8").replace("- Status: accepted", "- Status: superseded", 1)
            decisions.write_text(text, encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("must name a successor" in item for item in errors), errors)
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            decisions = root / "DECISIONS.md"
            text = decisions.read_text(encoding="utf-8")
            text = text.replace("- Status: accepted", "- Status: superseded", 1)
            text = text.replace("- Superseded by: none", "- Superseded by: DEC-0002", 1)
            text += (
                "\n## DEC-0002: Proposed Successor\n\n"
                "- Date: 2026-07-20\n- Status: proposed\n- Current owner: `DECISIONS.md`\n"
                "- Supersedes: DEC-0001\n- Superseded by: none\n"
                "- Retained boundary: fixture\n- Decision: fixture\n- Evidence: none\n"
            )
            decisions.write_text(text, encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("must be accepted" in item for item in errors), errors)

    def test_decision_duplicate_fields_fail_and_three_generation_chain_passes(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            decisions = root / "DECISIONS.md"
            text = decisions.read_text(encoding="utf-8").replace(
                "- Status: accepted", "- Status: accepted\n- Status: proposed", 1
            )
            decisions.write_text(text, encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("duplicate field: Status" in item for item in errors), errors)
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            decisions = root / "DECISIONS.md"
            text = decisions.read_text(encoding="utf-8")
            text = text.replace("- Status: accepted", "- Status: superseded", 1)
            text = text.replace("- Superseded by: none", "- Superseded by: DEC-0002", 1)
            text += (
                "\n## DEC-0002: Middle Generation\n\n"
                "- Date: 2026-07-20\n- Status: superseded\n- Current owner: `DECISIONS.md`\n"
                "- Supersedes: DEC-0001\n- Superseded by: DEC-0003\n"
                "- Retained boundary: fixture\n- Decision: fixture\n- Evidence: none\n"
                "\n## DEC-0003: Current Generation\n\n"
                "- Date: 2026-07-20\n- Status: accepted\n- Current owner: `DECISIONS.md`\n"
                "- Supersedes: DEC-0002\n- Superseded by: none\n"
                "- Retained boundary: fixture\n- Decision: fixture\n- Evidence: none\n"
            )
            decisions.write_text(text, encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertEqual([], [item for item in errors if "decision" in item.lower()], errors)

    def test_conflict_markers_ignore_fences_but_reject_real_marker_lines(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            readme = root / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n```text\n=======\n```\n", encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertFalse(any("conflict marker" in item for item in errors), errors)
            readme.write_text(readme.read_text(encoding="utf-8") + "\n=======\n", encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertTrue(any("conflict marker" in item for item in errors), errors)

    def test_long_fence_is_not_closed_by_a_shorter_literal_fence(self) -> None:
        text = "````text\n```\n=======\n````\n"
        self.assertEqual([], VALIDATOR.conflict_marker_lines(text))

    def test_parenthesized_relative_link_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = self.clone(Path(temp))
            note = root / "docs/note_(v1).md"
            note.write_text("# Note\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n[Note](docs/note_(v1).md)\n", encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [])
            self.assertFalse(any("note_(v1)" in item for item in errors), errors)

    def test_valid_evidence_passes_and_schema_failures_are_detected(self) -> None:
        mutations = [
            ({}, None),
            ({"timestamp_utc": "not-a-timeZ"}, "exact UTC date-time"),
            ({"timestamp_utc": "2026-07-20Z"}, "exact UTC date-time"),
            ({"timestamp_utc": "2026-07-20T12:00:00"}, "exact UTC date-time"),
            ({"timestamp_utc": "2026-07-20T12:00:00+00:00"}, "exact UTC date-time"),
            ({"exit_code": None}, "exit_code must be an integer"),
            ({"exit_code": True}, "exit_code"),
            ({"environment": {}}, "environment requires"),
            ({"unexpected": "field"}, "unsupported fields"),
        ]
        for changes, expected in mutations:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
                root = Path(temp)
                evidence = self.evidence(root, **changes)
                errors, _ = VALIDATOR.validate(root, [evidence], evidence_only=True)
                if expected is None:
                    self.assertEqual([], errors)
                else:
                    self.assertTrue(any(expected in item for item in errors), errors)

    def test_evidence_stream_and_artifact_containment_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            root = base / "root"
            root.mkdir()
            evidence = self.evidence(root)
            data = json.loads(evidence.read_text(encoding="utf-8"))
            data["stdout"]["sha256"] = "0" * 64
            evidence.write_text(json.dumps(data), encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [evidence], evidence_only=True)
            self.assertTrue(any("stdout hash mismatch" in item for item in errors), errors)
            evidence = self.evidence(root)
            data = json.loads(evidence.read_text(encoding="utf-8"))
            data["artifacts"][0]["sha256"] = "0" * 64
            evidence.write_text(json.dumps(data), encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [evidence], evidence_only=True)
            self.assertTrue(any("artifact hash mismatch" in item for item in errors), errors)
            outside = base / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            evidence = self.evidence(root)
            data = json.loads(evidence.read_text(encoding="utf-8"))
            data["stdout"] = {"inline": None, "path": str(outside), "sha256": digest(outside)}
            evidence.write_text(json.dumps(data), encoding="utf-8")
            errors, _ = VALIDATOR.validate(root, [evidence], evidence_only=True)
            self.assertTrue(any("stdout path invalid" in item for item in errors), errors)

    def test_evidence_count_and_size_limits_are_bounded(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            root = Path(temp)
            evidence = self.evidence(root)
            errors, _ = VALIDATOR.validate(root, [evidence] * (VALIDATOR.MAX_EVIDENCE_COUNT + 1), evidence_only=True)
            self.assertTrue(any("evidence count exceeds" in item for item in errors), errors)
            evidence.write_bytes(b"{" + (b"x" * VALIDATOR.MAX_EVIDENCE_BYTES) + b"}")
            errors, _ = VALIDATOR.validate(root, [evidence], evidence_only=True)
            self.assertTrue(any("exceeds" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
