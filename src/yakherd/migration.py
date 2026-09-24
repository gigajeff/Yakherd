"""Reviewed content migrations using the deterministic transactional writer."""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
from datetime import date
from pathlib import Path

from .diagnostics import inspect


MAX_PLAN_BYTES = 16 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024 * 1024
ROOT_FILES = {"AGENTS.md", "SSOT.md", "BASELINE.md", "NOW.md", "README.md", "START_HERE.md",
              "CLAUDE.md", "STATUS.md", "DECISIONS.md", "ARCHITECTURE.md", "TESTING.md",
              "GIT_SYNC.md", "code_review.md", ".gitignore"}
POLICY_FILES = {".yakherd/profile.json", ".yakherd/policies/Y-PROC-1.md"}
REQUIRED = {"AGENTS.md", "SSOT.md", "BASELINE.md", "NOW.md", "README.md", "START_HERE.md"} | POLICY_FILES


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def allowed_path(name: str, engine: object) -> str:
    name = engine.normalize_relative(name)
    if name in ROOT_FILES or name in POLICY_FILES:
        return name
    if name.startswith("docs/") and name.endswith(".md") and not any(
            part.casefold() in {".git", ".github", ".codex", ".agents", "node_modules"}
            for part in name.split("/")):
        return name
    raise ValueError(f"migration path is outside SSOT/documentation scope: {name}")


def regular_bytes(path: Path, engine: object, limit: int) -> bytes:
    engine.validate_existing_chain(path.absolute())
    if not path.is_file() or engine.is_reparse(path):
        raise ValueError(f"expected a regular non-reparse file: {path}")
    if path.stat().st_size > limit:
        raise ValueError(f"file exceeds bounded size: {path}")
    return path.read_bytes()


def prepare(target: Path, replacements: Path, output: Path, engine: object) -> dict:
    """Write an unreviewed, self-contained plan; never mutate the target."""
    root, source, output = target.absolute(), replacements.absolute(), output.absolute()
    package = engine.load_package_manifest()
    for path in (root, source):
        engine.validate_existing_chain(path)
        if not path.is_dir():
            raise ValueError(f"not a directory: {path}")
    if source == root or root in source.parents or source in root.parents:
        raise ValueError("replacement directory must be separate from the target tree")
    if output == root or root in output.parents or output == source or source in output.parents:
        raise ValueError("plan output must be outside target and replacement trees")
    records = {}
    for parent, dirs, names in os.walk(source, followlinks=False):
        for name in dirs:
            engine.validate_existing_chain(Path(parent) / name)
        for name in names:
            path = Path(parent) / name
            relative = allowed_path(path.relative_to(source).as_posix(), engine)
            raw = regular_bytes(path, engine, MAX_FILE_BYTES)
            content = raw.decode("utf-8")
            destination = engine.safe_destination(root, relative)
            records[relative] = {"content": content, "sha256": digest(raw),
                                 "expected_existing_sha256": engine.current_state(destination)}
    if not records:
        raise ValueError("replacement directory contains no files")
    for name in sorted(REQUIRED - set(records)):
        path = engine.safe_destination(root, name)
        raw = regular_bytes(path, engine, MAX_FILE_BYTES)
        records[name] = {"content": raw.decode("utf-8"), "sha256": digest(raw),
                         "expected_existing_sha256": digest(raw)}
    receipt_state = engine.current_state(engine.safe_destination(root, engine.INSTALL_MANIFEST_NAME))
    plan = {"schema_version": 3, "reviewed": False, "target": str(root),
            "project_name": root.name, "date": date.today().isoformat(),
            "package_manifest_sha256": engine.sha256_file(engine.PACKAGE_MANIFEST_PATH),
            "allowed_files": sorted([*records, engine.INSTALL_MANIFEST_NAME]),
            "expected_receipt_sha256": receipt_state, "files": dict(sorted(records.items())),
            "review_notes": "Review every replacement and retain product requirements, evidence and real hazards. Set reviewed=true only after that review."}
    raw = (json.dumps(plan, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(raw) > MAX_PLAN_BYTES:
        raise ValueError("migration plan exceeds bounded size")
    engine.validate_existing_chain(output.parent)
    engine.validate_existing_chain(output)
    with output.open("xb") as handle:
        handle.write(raw)
    return {"plan": str(output), "sha256": digest(raw), "reviewed": False,
            "files": plan["allowed_files"], "package_version": package["package_version"]}


def load(plan_path: Path, engine: object, *, require_review: bool, approved_hash: str | None = None) -> tuple:
    raw = regular_bytes(plan_path.absolute(), engine, MAX_PLAN_BYTES)
    plan_hash = digest(raw)
    if approved_hash is not None and (not re.fullmatch(r"[0-9a-f]{64}", approved_hash) or approved_hash != plan_hash):
        raise ValueError("approved plan hash does not match the exact reviewed file")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 3:
        raise ValueError("unsupported migration plan schema")
    if require_review and (data.get("reviewed") is not True or approved_hash is None):
        raise ValueError("apply needs reviewed=true and --plan-sha256 for the exact reviewed plan")
    package = engine.load_package_manifest()
    if data.get("package_manifest_sha256") != engine.sha256_file(engine.PACKAGE_MANIFEST_PATH):
        raise ValueError("migration plan targets different package bytes")
    if not isinstance(data.get("target"), str) or not Path(data["target"]).is_absolute():
        raise ValueError("migration target must be an absolute path")
    target = Path(data["target"])
    engine.validate_existing_chain(target)
    if not target.is_dir():
        raise ValueError("migration target must exist")
    if target in plan_path.absolute().parents:
        raise ValueError("migration plan must be outside its target")
    if not isinstance(data.get("project_name"), str) or not data["project_name"].strip() or any(c in data["project_name"] for c in "\r\n"):
        raise ValueError("project_name must be a nonempty single line")
    if date.fromisoformat(data["date"]).isoformat() != data["date"]:
        raise ValueError("migration date must be canonical YYYY-MM-DD")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("migration plan needs replacement files")
    if not REQUIRED <= set(files):
        raise ValueError("migration plan must pin all current owners and the process policy")
    payload, expected, records = {}, {}, []
    for name, record in files.items():
        allowed_path(name, engine)
        if not isinstance(record, dict) or not isinstance(record.get("content"), str):
            raise ValueError(f"invalid replacement record: {name}")
        content = record["content"].encode("utf-8")
        if len(content) > MAX_FILE_BYTES or digest(content) != record.get("sha256"):
            raise ValueError(f"replacement content hash/size mismatch: {name}")
        state = record.get("expected_existing_sha256")
        if not isinstance(state, str) or (state != "absent" and not re.fullmatch(r"[0-9a-f]{64}", state)):
            raise ValueError(f"invalid expected state: {name}")
        payload[name], expected[name] = content, state
        records.append({"path": name, "rendered_sha256": digest(content), "bytes": len(content),
                        "source": "reviewed migration replacement"})
    expected[engine.INSTALL_MANIFEST_NAME] = data.get("expected_receipt_sha256")
    allowed = data.get("allowed_files")
    if allowed != sorted(expected) or len({p.casefold() for p in allowed}) != len(allowed):
        raise ValueError("allowlist must exactly match replacements and receipt without aliases")
    engine.preflight_retrofit(target, payload, {"allowed_files": allowed, "expected_existing_sha256": expected})
    return data, target, payload, expected, records, package, plan_hash


def preview(plan_path: Path, engine: object) -> dict:
    data, target, payload, _, _, _, plan_hash = load(plan_path, engine, require_review=False)
    diffs = []
    for name, raw in sorted(payload.items()):
        path = engine.safe_destination(target, name)
        old = regular_bytes(path, engine, MAX_FILE_BYTES).decode("utf-8") if path.exists() else ""
        diff = "".join(difflib.unified_diff(old.splitlines(keepends=True), raw.decode("utf-8").splitlines(keepends=True),
                                          fromfile=f"before/{name}", tofile=f"after/{name}"))
        diffs.append({"path": name, "diff": diff})
    return {"status": "preview", "reviewed": data.get("reviewed") is True,
            "target": str(target), "sha256": plan_hash, "changes": diffs}


def apply(plan_path: Path, plan_hash: str, engine: object, *, fault_injector=None) -> dict:
    data, target, payload, expected, records, package, loaded_hash = load(
        plan_path, engine, require_review=True, approved_hash=plan_hash)
    receipt = engine.make_install_manifest(package, target, data["project_name"], data["date"],
                                           "migration", records, plan_path, loaded_hash)
    candidate = inspect(target, engine, overrides={**payload, engine.INSTALL_MANIFEST_NAME: receipt})
    if candidate["errors"]:
        raise ValueError(f"migration candidate is structurally invalid: {candidate['errors']}")
    backup = engine.write_retrofit(target, payload, receipt, data["allowed_files"], expected,
                                  plan_path, loaded_hash, fault_injector, retain_backups=True)
    return {"status": "migrated", "target": str(target), "backup": str(backup),
            "plan_sha256": loaded_hash, "files": data["allowed_files"],
            "next": "Run yakherd doctor and verify retained product requirements and evidence."}
