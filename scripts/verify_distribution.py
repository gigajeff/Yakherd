#!/usr/bin/env python3
"""Verify built wheel/sdist contents against the reviewed package bytes."""

from __future__ import annotations

import argparse
import tarfile
import tomllib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages" / "jeff_strict_ssot_v1"


def reviewed_files() -> dict[str, bytes]:
    return {
        path.relative_to(PACKAGE).as_posix(): path.read_bytes()
        for path in PACKAGE.rglob("*")
        if path.is_file()
        and path.name != "__pycache__"
        and path.suffix not in {".pyc", ".pyo"}
    }


def one(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {pattern}, found {matches}")
    return matches[0]


def verify_wheel(path: Path, expected: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    prefix = "yakherd/_bundle/"
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            errors.append("wheel contains duplicate paths")
        actual = {
            name[len(prefix) :]: archive.read(name)
            for name in names
            if name.startswith(prefix) and not name.endswith("/")
        }
    compare("wheel", actual, expected, errors)
    return errors


def verify_sdist(path: Path, expected: dict[str, bytes], version: str) -> list[str]:
    errors: list[str] = []
    prefix = f"yakherd-{version}/packages/jeff_strict_ssot_v1/"
    with tarfile.open(path, "r:gz") as archive:
        members = [member for member in archive.getmembers() if member.isfile()]
        names = [member.name for member in members]
        if len(names) != len(set(names)):
            errors.append("sdist contains duplicate paths")
        actual: dict[str, bytes] = {}
        for member in members:
            if not member.name.startswith(prefix):
                continue
            handle = archive.extractfile(member)
            if handle is None:
                errors.append(f"sdist member unreadable: {member.name}")
                continue
            actual[member.name[len(prefix) :]] = handle.read()
    compare("sdist", actual, expected, errors)
    return errors


def compare(
    label: str,
    actual: dict[str, bytes],
    expected: dict[str, bytes],
    errors: list[str],
) -> None:
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatched = sorted(
        relative
        for relative in set(expected) & set(actual)
        if expected[relative] != actual[relative]
    )
    forbidden = sorted(
        relative
        for relative in actual
        if "__pycache__" in Path(relative).parts
        or Path(relative).suffix in {".pyc", ".pyo"}
    )
    if missing:
        errors.append(f"{label} reviewed files missing: {missing}")
    if extra:
        errors.append(f"{label} reviewed files extra: {extra}")
    if mismatched:
        errors.append(f"{label} reviewed files mismatched: {mismatched}")
    if forbidden:
        errors.append(f"{label} contains generated cache paths: {forbidden}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    version = str(project["version"])
    wheel = one(args.directory, f"yakherd-{version}-*.whl")
    sdist = one(args.directory, f"yakherd-{version}.tar.gz")
    expected = reviewed_files()
    errors = verify_wheel(wheel, expected)
    errors.extend(verify_sdist(sdist, expected, version))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "distribution_verification status=passed "
        f"reviewed_files={len(expected)} wheel={wheel.name} sdist={sdist.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
