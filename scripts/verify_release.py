#!/usr/bin/env python3
"""Verify the Yakherd V1 release hash chain and repository hygiene."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages" / "jeff_strict_ssot_v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag")
    args = parser.parse_args(argv)
    errors: list[str] = []
    release = json.loads((PACKAGE / "RELEASE.json").read_text(encoding="utf-8"))
    manifest = json.loads((PACKAGE / "MANIFEST.json").read_text(encoding="utf-8"))
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]

    root_protocol = ROOT / "docs" / "task_protocol.md"
    template_protocol = PACKAGE / "template" / "docs" / "task_protocol.md"
    for label, path in (
        ("root task protocol", root_protocol),
        ("installed task protocol", template_protocol),
    ):
        if not path.is_file():
            errors.append(f"{label} missing: {path.relative_to(ROOT)}")

    root_agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    template_agents = (PACKAGE / "template" / "AGENTS.md").read_text(
        encoding="utf-8"
    )
    if "`docs/task_protocol.md` is the canonical SSOT owner" not in root_agents:
        errors.append("root AGENTS.md does not name docs/task_protocol.md as canonical")
    if "`docs/task_protocol.md` owns proportional work modes" not in template_agents:
        errors.append("template AGENTS.md does not name docs/task_protocol.md as owner")

    manifest_in = (ROOT / "MANIFEST.in").read_text(encoding="utf-8").splitlines()
    if "include docs/task_protocol.md" not in manifest_in:
        errors.append("source distribution does not include root docs/task_protocol.md")

    for field in ("package_name", "package_version"):
        if release.get(field) != manifest.get(field):
            errors.append(
                f"release/manifest {field} mismatch: "
                f"{release.get(field)!r} != {manifest.get(field)!r}"
            )

    if project.get("name") != "yakherd":
        errors.append(f"PyPI project name mismatch: {project.get('name')!r}")
    if project.get("version") != release.get("package_version"):
        errors.append(
            "PyPI/release version mismatch: "
            f"{project.get('version')!r} != {release.get('package_version')!r}"
        )
    expected_tag = f"v{project.get('version')}"
    if args.tag is not None and args.tag != expected_tag:
        errors.append(f"release tag mismatch: {args.tag!r} != {expected_tag!r}")

    bindings = {
        "bootstrap.py": release["bootstrap_sha256"],
        "MANIFEST.json": release["manifest_sha256"],
    }
    for relative, expected in bindings.items():
        actual = sha256(PACKAGE / relative)
        if actual != expected:
            errors.append(f"release hash mismatch: {relative}: {actual} != {expected}")

    template_hashes = manifest.get("template_sha256", {})
    if "docs/task_protocol.md" not in manifest.get("template_files", []):
        errors.append("manifest file list omits installed docs/task_protocol.md")
    if "docs/task_protocol.md" not in template_hashes:
        errors.append("manifest hashes omit installed docs/task_protocol.md")
    for relative, expected in template_hashes.items():
        source = PACKAGE / "template" / relative
        if not source.is_file():
            errors.append(f"manifest source missing: {relative}")
            continue
        actual = sha256(source)
        if actual != expected:
            errors.append(
                f"manifest hash mismatch: {relative}: {actual} != {expected}"
            )

    cache_paths = sorted(
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in PACKAGE.rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc"
    )
    if cache_paths:
        errors.append(f"package cache paths present: {cache_paths}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "release_verification status=passed "
        f"manifest_files={len(template_hashes)} cache_paths=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
