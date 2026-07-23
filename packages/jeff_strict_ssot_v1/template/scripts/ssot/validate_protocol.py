"""Bounded, deterministic, standard-library, read-only SSOT validator."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


REQUIRED_PATHS = [
    ".gitignore",
    ".yakherd/policies/Y-PROC-1.md",
    "AGENTS.md",
    "ARCHITECTURE.md",
    "CLAUDE.md",
    "DECISIONS.md",
    "GIT_SYNC.md",
    "README.md",
    "SSOT.md",
    "START_HERE.md",
    "STATUS.md",
    "TESTING.md",
    "code_review.md",
    "docs/GITHUB_SETUP.md",
    "docs/domain_invariants.md",
    "docs/governance/AUDIT_STATE.json",
    "docs/governance/GOVERNOR_DELTA_POLICY.json",
    "docs/governance/GOVERNOR_DELTA_POLICY.md",
    "docs/governance/OPEN_FINDINGS.md",
    "docs/governance/README.md",
    "docs/governance/RISK_REGISTER.md",
    "docs/governance/STATUS_MAINTENANCE.md",
    "docs/governance/TRANSCRIPT_REVIEW_POLICY.md",
    "docs/master_prompts/000_PRODUCT_PROMPT_NOT_RECEIVED.md",
    "docs/master_prompts/README.md",
    "docs/plans/README.md",
    "docs/prompts/architecture_task.md",
    "docs/prompts/bootstrap_cold_resume_review.md",
    "docs/prompts/codex_team_launcher.md",
    "docs/prompts/governor_task.md",
    "docs/prompts/implementation_task.md",
    "docs/prompts/product_intake.md",
    "docs/prompts/red_team_task.md",
    "docs/prompts/temp_branch_task.md",
    "docs/reviews/README.md",
    "docs/run_records/README.md",
    "docs/status_history/README.md",
    "docs/task_protocol.md",
    "docs/templates/architecture_plan.md",
    "docs/templates/red_team_review.md",
    "docs/templates/run_record.json",
    "docs/validation_protocol.md",
    "scripts/ssot/migrate_status_archive.py",
    "scripts/ssot/validate_governor_delta_policy.py",
    "scripts/ssot/validate_protocol.py",
    "tests/ssot/test_governor_delta_policy.py",
    "tests/ssot/test_status_archive_migration.py",
    "tests/ssot/test_validate_protocol.py",
]

STATUS_FIELDS = [
    "State",
    "Last updated UTC",
    "Execution surface",
    "Current goal",
    "Current evidence",
    "Test state",
    "Blockers",
    "Next authorized action",
    "Forbidden actions",
    "Git state",
    "Remote visibility",
    "Release/promotion state",
    "Archive",
]

EVIDENCE_FIELDS = {
    "schema_version",
    "evidence_class",
    "timestamp_utc",
    "working_directory",
    "command",
    "exit_code",
    "environment",
    "supported_claim",
    "stdout",
    "stderr",
    "artifacts",
    "authority_effect",
    "limitations",
}

MAX_EVIDENCE_COUNT = 16
MAX_EVIDENCE_BYTES = 1024 * 1024
MAX_EVIDENCE_TOTAL_BYTES = 8 * 1024 * 1024
MAX_STREAM_BYTES = 4 * 1024 * 1024
MAX_ARTIFACT_COUNT = 64
MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
MAX_ARTIFACT_TOTAL_BYTES = 256 * 1024 * 1024
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
OWNER_RE = re.compile(r"\|[^\n]*\|\s*`([^`]+)`\s*\|")
DATED_ENTRY_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2} .+\*\*$", re.MULTILINE)
DECISION_HEADING_RE = re.compile(r"^## (DEC-[A-Za-z0-9_-]+):", re.MULTILINE)
FIELD_RE = re.compile(r"^- ([A-Za-z][A-Za-z /-]+):\s*(.+)$", re.MULTILINE)
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_DECISION_STATES = {"proposed", "accepted", "superseded", "rejected"}


class PathViolation(ValueError):
    pass


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
            raise PathViolation(f"path parent is not a directory: {current}")
        matches = [entry.name for entry in os.scandir(current) if entry.name.casefold() == part.casefold()]
        if not matches:
            raise PathViolation(f"path component is missing: {current / part}")
        if part not in matches:
            raise PathViolation(f"path casing mismatch: requested {part!r}, actual {matches[0]!r}")
        current = current / part
        if is_reparse(current):
            raise PathViolation(f"reparse/symlink component is forbidden: {current}")


def repository_file(root: Path, raw: str | Path, *, max_bytes: int | None = None) -> Path:
    root_absolute = root.absolute()
    value = Path(raw)
    candidate = value.absolute() if value.is_absolute() else (root_absolute / value).absolute()
    try:
        candidate.relative_to(root_absolute)
    except ValueError as exc:
        raise PathViolation(f"path escapes repository: {raw}") from exc
    validate_existing_chain(root_absolute)
    validate_existing_chain(candidate)
    if not candidate.is_file() or is_reparse(candidate):
        raise PathViolation(f"expected regular in-repository file: {raw}")
    try:
        candidate.resolve(strict=True).relative_to(root_absolute.resolve(strict=True))
    except ValueError as exc:
        raise PathViolation(f"resolved path escapes repository: {raw}") from exc
    if max_bytes is not None and candidate.stat().st_size > max_bytes:
        raise PathViolation(f"file exceeds {max_bytes} bytes: {raw}")
    return candidate


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def conflict_marker_lines(text: str) -> list[int]:
    markers: list[int] = []
    fence_character: str | None = None
    fence_length = 0
    marker_re = re.compile(r"^(?:<" + r"{7}|=" + r"{7}|>" + r"{7})(?: .*)?$")
    for number, line in enumerate(text.splitlines(), 1):
        if fence_character is None:
            opening = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line)
            if opening:
                token = opening.group(1)
                fence_character = token[0]
                fence_length = len(token)
                continue
        else:
            closing = re.fullmatch(
                rf"[ \t]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
                line,
            )
            if closing:
                fence_character = None
                fence_length = 0
            continue
        if marker_re.fullmatch(line):
            markers.append(number)
    return markers


def markdown_link_targets(text: str) -> Iterable[str]:
    """Conservative balanced scanner for inline Markdown link destinations."""
    index = 0
    while True:
        start = text.find("](", index)
        if start < 0:
            return
        cursor = start + 2
        depth = 1
        escaped = False
        while cursor < len(text) and depth:
            char = text[cursor]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            cursor += 1
        if depth == 0:
            raw = text[start + 2 : cursor - 1].strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            elif " " in raw:
                raw = raw.split(" ", 1)[0]
            yield raw.replace("\\(", "(").replace("\\)", ")")
        index = max(cursor, start + 2)


def parse_decisions(text: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    errors: list[str] = []
    matches = list(DECISION_HEADING_RE.finditer(text))
    decisions: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        decision_id = match.group(1)
        if decision_id in decisions:
            errors.append(f"duplicate decision ID: {decision_id}")
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        fields: dict[str, str] = {}
        for key, value in FIELD_RE.findall(text[match.end() : end]):
            if key in fields:
                errors.append(f"decision {decision_id} has duplicate field: {key}")
                continue
            fields[key] = value.strip()
        decisions[decision_id] = fields
    if not decisions:
        errors.append("DECISIONS.md has no decision records")
    return decisions, errors


def split_refs(value: str) -> set[str]:
    if value.lower() == "none":
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def strip_code_span(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def validate_stream(root: Path, name: str, value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != {"inline", "path", "sha256"}:
        return [f"{name} must contain exactly inline/path/sha256"]
    inline = value["inline"]
    raw_path = value["path"]
    digest = value["sha256"]
    if (inline is None) == (raw_path is None):
        errors.append(f"{name} must use exactly one of inline or path")
    if inline is not None:
        if not isinstance(inline, str) or len(inline.encode("utf-8")) > 16384:
            errors.append(f"{name}.inline must be a string within 16384 bytes")
        if digest is not None:
            errors.append(f"{name}.sha256 must be null for inline output")
    if raw_path is not None:
        if not isinstance(raw_path, str) or not isinstance(digest, str) or not HASH_RE.fullmatch(digest):
            errors.append(f"{name} path output requires string path and lowercase SHA-256")
        else:
            try:
                path = repository_file(root, raw_path, max_bytes=MAX_STREAM_BYTES)
                if sha256_file(path) != digest:
                    errors.append(f"{name} hash mismatch: {raw_path}")
            except PathViolation as exc:
                errors.append(f"{name} path invalid: {exc}")
    return errors


def validate_evidence(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    try:
        safe_path = repository_file(root, path, max_bytes=MAX_EVIDENCE_BYTES)
        data: dict[str, Any] = json.loads(safe_path.read_text(encoding="utf-8"))
    except (PathViolation, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"evidence unreadable {path}: {exc}"]
    missing = sorted(EVIDENCE_FIELDS - set(data))
    if missing:
        errors.append(f"evidence missing fields {path}: {missing}")
        return errors
    extra = sorted(set(data) - EVIDENCE_FIELDS)
    if extra:
        errors.append(f"evidence has unsupported fields {path}: {extra}")
    if data.get("schema_version") != 1:
        errors.append(f"evidence schema_version must be 1: {path}")
    if data.get("evidence_class") not in {"protocol", "product", "release", "review"}:
        errors.append(f"invalid evidence_class: {path}")
    timestamp = data.get("timestamp_utc")
    timestamp_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z"
    if not isinstance(timestamp, str) or not re.fullmatch(timestamp_pattern, timestamp):
        errors.append(f"timestamp_utc must be an exact UTC date-time ending in Z: {path}")
    else:
        try:
            parsed_timestamp = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if parsed_timestamp.tzinfo != dt.timezone.utc:
                raise ValueError("timestamp is not UTC")
        except ValueError:
            errors.append(f"timestamp_utc is invalid: {path}")
    if not isinstance(data.get("working_directory"), str) or not data["working_directory"]:
        errors.append(f"working_directory must be nonempty: {path}")
    command = data.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(item, str) and item for item in command):
        errors.append(f"command must be a nonempty argv string list: {path}")
    exit_code = data.get("exit_code")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        errors.append(f"exit_code must be an integer: {path}")
    environment = data.get("environment")
    if not isinstance(environment, dict) or not all(isinstance(environment.get(key), str) and environment[key] for key in ("machine", "os", "runtime")):
        errors.append(f"environment requires machine/os/runtime strings: {path}")
    if not isinstance(data.get("supported_claim"), str) or not data["supported_claim"]:
        errors.append(f"supported_claim must be nonempty: {path}")
    errors.extend(validate_stream(root, "stdout", data.get("stdout")))
    errors.extend(validate_stream(root, "stderr", data.get("stderr")))
    if not isinstance(data.get("authority_effect"), str) or not data["authority_effect"]:
        errors.append(f"authority_effect must be nonempty: {path}")
    limitations = data.get("limitations")
    if not isinstance(limitations, list) or not all(isinstance(item, str) for item in limitations):
        errors.append(f"limitations must be a string list: {path}")
    artifacts = data.get("artifacts")
    artifact_total = 0
    if not isinstance(artifacts, list) or len(artifacts) > MAX_ARTIFACT_COUNT:
        errors.append(f"artifacts must be a list of at most {MAX_ARTIFACT_COUNT}: {path}")
    else:
        for artifact in artifacts:
            if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256"}:
                errors.append(f"artifact requires exactly path/sha256: {path}")
                continue
            raw_path, digest = artifact["path"], artifact["sha256"]
            if not isinstance(raw_path, str) or not isinstance(digest, str) or not HASH_RE.fullmatch(digest):
                errors.append(f"artifact path/hash invalid: {path}")
                continue
            try:
                artifact_path = repository_file(root, raw_path, max_bytes=MAX_ARTIFACT_BYTES)
                artifact_total += artifact_path.stat().st_size
                if sha256_file(artifact_path) != digest:
                    errors.append(f"artifact hash mismatch: {raw_path}")
            except PathViolation as exc:
                errors.append(f"artifact path invalid: {exc}")
        if artifact_total > MAX_ARTIFACT_TOTAL_BYTES:
            errors.append(f"artifact total exceeds {MAX_ARTIFACT_TOTAL_BYTES} bytes: {path}")
    return errors


def validate(root: Path, evidence: list[Path], *, evidence_only: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    root = root.absolute()
    try:
        validate_existing_chain(root)
    except PathViolation as exc:
        return [f"invalid repository root: {exc}"], warnings

    if len(evidence) > MAX_EVIDENCE_COUNT:
        errors.append(f"evidence count exceeds {MAX_EVIDENCE_COUNT}: {len(evidence)}")
        evidence = evidence[:MAX_EVIDENCE_COUNT]
    evidence_total = 0
    for path in evidence:
        try:
            safe = repository_file(root, path, max_bytes=MAX_EVIDENCE_BYTES)
            evidence_total += safe.stat().st_size
        except PathViolation as exc:
            errors.append(f"evidence path invalid: {exc}")
            continue
        errors.extend(validate_evidence(safe, root))
    if evidence_total > MAX_EVIDENCE_TOTAL_BYTES:
        errors.append(f"evidence total exceeds {MAX_EVIDENCE_TOTAL_BYTES} bytes")
    if evidence_only:
        return errors, warnings

    paths: dict[str, Path] = {}
    for relative in REQUIRED_PATHS:
        try:
            paths[relative] = repository_file(root, relative)
        except PathViolation as exc:
            errors.append(f"required path invalid: {relative}: {exc}")

    readable: dict[str, str] = {}
    for relative, path in paths.items():
        if path.suffix.lower() not in {".md", ".json", ".py"}:
            continue
        try:
            readable[relative] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"unreadable UTF-8 protocol file {relative}: {exc}")

    for relative, text in readable.items():
        markers = conflict_marker_lines(text)
        if markers:
            errors.append(f"unresolved conflict marker lines in {relative}: {markers}")
        if re.search(r"[ \t]+$", text, re.MULTILINE):
            errors.append(f"trailing whitespace: {relative}")

    claude_adapter = readable.get("CLAUDE.md")
    if claude_adapter is not None and claude_adapter.strip() != "@AGENTS.md":
        errors.append("CLAUDE.md must contain only the @AGENTS.md import")

    agents = readable.get("AGENTS.md", "")
    if ".yakherd/policies/Y-PROC-1.md" not in agents:
        errors.append("AGENTS.md must point to the Y-PROC-1 policy owner")

    process_policy = readable.get(".yakherd/policies/Y-PROC-1.md", "")
    process_policy_requirements = {
        "every finite local command must run through `yakherd exec`",
        "BELOW_NORMAL_PRIORITY_CLASS",
        "executable-name matching",
        "Approved persistent-process leases are not part of Y-PROC-1.1",
        "explicit human authorization",
        "mosaic_colmap",
        "SPLATOMATIC",
        "CROCHET",
        "yakherd.process-task.v1.1",
        "PID_REUSED_UNRELATED",
        "OWNERSHIP_RECORD_INCONSISTENT",
        "yakherd process resume --task TASK_ID",
    }
    for requirement in sorted(process_policy_requirements):
        if requirement not in process_policy:
            errors.append(f"Y-PROC-1 policy missing safety boundary: {requirement}")

    launcher = readable.get("docs/prompts/codex_team_launcher.md", "")
    launcher_requirements = {
        "exactly five direct role agents",
        "`architecture`",
        "`implementation`",
        "`red_team`",
        "`temporary_branch`",
        "`governor`",
        "startup as incomplete",
        "docs/prompts/bootstrap_cold_resume_review.md",
        "docs/prompts/product_intake.md",
    }
    for requirement in sorted(launcher_requirements):
        if requirement not in launcher:
            errors.append(f"Codex team launcher missing invariant: {requirement}")

    github_setup = readable.get("docs/GITHUB_SETUP.md", "")
    github_requirements = {
        "Required Human Checkpoint",
        "gh auth status --active --hostname github.com",
        "Never use `git add .`",
        "--source=. --remote=origin --push",
        "Stop without mutation",
    }
    for requirement in sorted(github_requirements):
        if requirement not in github_setup:
            errors.append(f"GitHub setup missing safety boundary: {requirement}")

    product_intake = readable.get("docs/prompts/product_intake.md", "")
    intake_requirements = {
        "MASTER PROMPT START",
        "MASTER PROMPT END",
        "byte_length",
        "capture_limitations",
        "sha256",
        "human confirmation",
        "no automatic Architecture plan or Red Team review",
    }
    for requirement in sorted(intake_requirements):
        if requirement not in product_intake:
            errors.append(f"product intake missing provenance boundary: {requirement}")

    task_protocol = readable.get("docs/task_protocol.md", "")
    review_control_requirements = {
        "`bounded` or `strict`",
        "Classify only the authorized slice, not hypothetical future features.",
        "Bounded mode needs no Architecture plan and no Red Team gate.",
        "A missing enhancement outside accepted scope is not a finding.",
        "Only P0 and P1 block",
        "one initial review and at most one recheck",
        "After a second consecutive `FAIL`",
        "Do not create `_v2`, `_v3`",
        "cannot itself create a new requirement or a fresh-review obligation",
    }
    for requirement in sorted(review_control_requirements):
        if requirement not in task_protocol:
            errors.append(f"task protocol missing review control: {requirement}")

    implementation_prompt = readable.get(
        "docs/prompts/implementation_task.md", ""
    )
    if "user-approved bounded brief" not in implementation_prompt:
        errors.append("Implementation prompt missing direct bounded authorization")

    red_team_prompt = readable.get("docs/prompts/red_team_task.md", "")
    red_team_requirements = {
        "Bounded work has no Red Team gate.",
        "outside accepted scope is not a finding",
        "Only P0/P1 block",
        "After a second `FAIL`",
        "cannot require a third review",
    }
    for requirement in sorted(red_team_requirements):
        if requirement not in red_team_prompt:
            errors.append(f"Red Team prompt missing scope control: {requirement}")

    bootstrap_review = readable.get(
        "docs/prompts/bootstrap_cold_resume_review.md", ""
    )
    bootstrap_review_requirements = {
        "human confirmation of the extracted bounded brief or strict planning scope",
        "Bounded mode has no product-intake Red Team gate.",
        "direct Implementation authorization for a confirmed bounded brief",
        "two-review circuit breaker",
    }
    for requirement in sorted(bootstrap_review_requirements):
        if requirement not in bootstrap_review:
            errors.append(
                f"bootstrap review missing proportional workflow: {requirement}"
            )

    review_template = readable.get("docs/templates/red_team_review.md", "")
    if "pass_with_fixes" in review_template.lower():
        errors.append("Red Team review template permits pass_with_fixes")
    for requirement in ("- Review cycle: 1 | 2", "- Verdict: PASS | FAIL"):
        if requirement not in review_template:
            errors.append(f"Red Team review template missing circuit breaker: {requirement}")

    status_path = paths.get("STATUS.md")
    if status_path:
        status_bytes = status_path.read_bytes()
        try:
            status = status_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"STATUS.md is not UTF-8: {exc}")
            status = ""
        lines = status.splitlines()
        if len(lines) > 120:
            errors.append(f"STATUS.md exceeds 120 lines: {len(lines)}")
        if len(status_bytes) > 32768:
            errors.append(f"STATUS.md exceeds 32768 UTF-8 bytes: {len(status_bytes)}")
        entries = DATED_ENTRY_RE.findall(status)
        if len(entries) != 1:
            errors.append(f"STATUS.md must have exactly one dated current entry: {len(entries)}")
        for field in STATUS_FIELDS:
            if not re.search(rf"^- {re.escape(field)}:", status, re.MULTILINE):
                errors.append(f"STATUS.md missing field: {field}")
        timestamp_match = re.search(
            r"^- Last updated UTC: `([^`]+)`", status, re.MULTILINE
        )
        if timestamp_match:
            try:
                updated = dt.datetime.fromisoformat(
                    timestamp_match.group(1).replace("Z", "+00:00")
                )
                if updated.tzinfo != dt.timezone.utc:
                    raise ValueError("timestamp is not UTC")
            except ValueError:
                errors.append("STATUS.md Last updated UTC is invalid")

    ssot = readable.get("SSOT.md", "")
    owner_paths = OWNER_RE.findall(ssot)
    if not owner_paths:
        errors.append("SSOT.md contains no mechanically readable owner paths")
    for owner in owner_paths:
        try:
            repository_file(root, owner)
        except PathViolation as exc:
            errors.append(f"SSOT.md owner path invalid: {owner}: {exc}")

    decisions, decision_errors = parse_decisions(readable.get("DECISIONS.md", ""))
    errors.extend(decision_errors)
    required_decision_fields = {"Date", "Status", "Current owner", "Supersedes", "Superseded by", "Retained boundary", "Decision", "Evidence"}
    for decision_id, fields in decisions.items():
        missing = sorted(required_decision_fields - set(fields))
        if missing:
            errors.append(f"decision {decision_id} missing fields: {missing}")
            continue
        if fields["Status"] not in ALLOWED_DECISION_STATES:
            errors.append(f"decision {decision_id} has invalid status: {fields['Status']}")
        try:
            repository_file(root, strip_code_span(fields["Current owner"]))
        except PathViolation as exc:
            errors.append(f"decision {decision_id} current owner invalid: {exc}")
        for ref in split_refs(fields["Supersedes"]) | split_refs(fields["Superseded by"]):
            if ref not in decisions:
                errors.append(f"decision {decision_id} references missing decision: {ref}")
    for decision_id, fields in decisions.items():
        if required_decision_fields - set(fields):
            continue
        predecessors = split_refs(fields["Supersedes"])
        successors = split_refs(fields["Superseded by"])
        if fields["Status"] == "superseded" and not successors:
            errors.append(f"superseded decision {decision_id} must name a successor")
        if successors and fields["Status"] != "superseded":
            errors.append(f"decision {decision_id} with successor must be superseded")
        if predecessors and fields["Status"] not in {"accepted", "superseded"}:
            errors.append(f"linked superseding decision {decision_id} must be accepted or superseded")
        for predecessor in predecessors:
            if decision_id not in split_refs(decisions.get(predecessor, {}).get("Superseded by", "none")):
                errors.append(f"decision supersession is not reciprocal: {predecessor} -> {decision_id}")
        for successor in successors:
            if decisions.get(successor, {}).get("Status") not in {"accepted", "superseded"}:
                errors.append(f"decision successor {successor} must be accepted or superseded")
            if decision_id not in split_refs(decisions.get(successor, {}).get("Supersedes", "none")):
                errors.append(f"decision supersession is not reciprocal: {decision_id} -> {successor}")

    for relative in [item for item in REQUIRED_PATHS if item.endswith(".md")]:
        text = readable.get(relative, "")
        base = (root / relative).parent
        for raw_target in markdown_link_targets(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("#"):
                continue
            try:
                repository_file(root, base / target)
            except PathViolation as exc:
                errors.append(f"broken/unsafe relative link in {relative}: {raw_target}: {exc}")

    governor_path = paths.get("docs/governance/GOVERNOR_DELTA_POLICY.json")
    if governor_path:
        try:
            governor = json.loads(governor_path.read_text(encoding="utf-8"))
            modes = governor["modes"]
            expected = {
                "quiet": (2, 512, False),
                "delta": (120, 16384, True),
                "rebaseline": (240, 32768, True),
            }
            for mode, values in expected.items():
                actual = modes.get(mode, {})
                if (actual.get("max_lines"), actual.get("max_utf8_bytes"), actual.get("writes_allowed")) != values:
                    errors.append(f"Governor limits mismatch: {mode}")
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid Governor policy: {exc}")
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence", action="append", type=Path, default=[])
    parser.add_argument("--evidence-only", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args(argv)
    errors, warnings = validate(args.root, args.evidence, evidence_only=args.evidence_only)
    if not args.summary:
        for error in errors:
            print(f"error: {error}")
        for warning in warnings:
            print(f"warning: {warning}")
    failed = bool(errors or (args.strict and warnings))
    print(
        "protocol_validation "
        f"status={'failed' if failed else 'passed'} "
        f"errors={len(errors)} warnings={len(warnings)} evidence={len(args.evidence)}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
