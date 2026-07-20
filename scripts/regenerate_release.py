#!/usr/bin/env python3
"""Regenerate the audited package manifest and release hash bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages" / "jeff_strict_ssot_v1"
TEMPLATE = PACKAGE / "template"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    manifest_path = PACKAGE / "MANIFEST.json"
    release_path = PACKAGE / "RELEASE.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    release = json.loads(release_path.read_text(encoding="utf-8"))

    files = sorted(
        path.relative_to(TEMPLATE).as_posix()
        for path in TEMPLATE.rglob("*")
        if path.is_file()
        and path.name != "__pycache__"
        and path.suffix not in {".pyc", ".pyo"}
    )
    manifest["template_files"] = files
    manifest["template_sha256"] = {
        relative: sha256(TEMPLATE / relative) for relative in files
    }
    write_json(manifest_path, manifest)

    release["bootstrap_sha256"] = sha256(PACKAGE / "bootstrap.py")
    release["manifest_sha256"] = sha256(manifest_path)
    write_json(release_path, release)
    print(f"regenerated package release bindings files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
