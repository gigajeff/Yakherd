#!/usr/bin/env python3
"""Verify the Yakherd V1 release hash chain and repository hygiene."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages" / "jeff_strict_ssot_v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    release = json.loads((PACKAGE / "RELEASE.json").read_text(encoding="utf-8"))
    manifest = json.loads((PACKAGE / "MANIFEST.json").read_text(encoding="utf-8"))

    for field in ("package_name", "package_version"):
        if release.get(field) != manifest.get(field):
            errors.append(
                f"release/manifest {field} mismatch: "
                f"{release.get(field)!r} != {manifest.get(field)!r}"
            )

    bindings = {
        "bootstrap.py": release["bootstrap_sha256"],
        "MANIFEST.json": release["manifest_sha256"],
    }
    for relative, expected in bindings.items():
        actual = sha256(PACKAGE / relative)
        if actual != expected:
            errors.append(f"release hash mismatch: {relative}: {actual} != {expected}")

    template_hashes = manifest.get("template_sha256", {})
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
