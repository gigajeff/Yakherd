"""Command-line adapter for the reviewed Yakherd installer."""

from __future__ import annotations

import subprocess
import shutil
import sys
import tempfile
from pathlib import Path


def bootstrap_path() -> Path:
    """Locate bundled release bytes, falling back to the source checkout."""
    package = Path(__file__).resolve().parent
    bundled = package / "_bundle" / "bootstrap.py"
    if bundled.is_file():
        return bundled

    source = package.parents[1] / "packages" / "jeff_strict_ssot_v1" / "bootstrap.py"
    if source.is_file():
        return source
    return bundled


def print_help() -> None:
    print(
        """Yakherd - herds the yaks so your agent stops shaving them.

Usage:
  yakherd init --target PATH --project-name NAME [--dry-run]
  yakherd retrofit --target PATH --project-name NAME \\
      --retrofit-plan PLAN.json [--dry-run]
  yakherd package-help

Commands:
  init          Install into a nonexistent or empty project directory.
  retrofit      Apply a separately reviewed, hash-pinned retrofit plan.
  package-help  Show every low-level package option.
"""
    )


def run_bootstrap(bootstrap: Path, forwarded: list[str]) -> int:
    """Run source bytes directly or stage a cache-free installed bundle."""
    if bootstrap.parent.name != "_bundle":
        completed = subprocess.run(
            [sys.executable, "-B", str(bootstrap), *forwarded],
            check=False,
        )
        return completed.returncode

    def ignore_generated(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name == "__pycache__" or name.endswith((".pyc", ".pyo"))
        }

    with tempfile.TemporaryDirectory(prefix="yakherd-") as temporary:
        staged = Path(temporary) / "reviewed-package"
        shutil.copytree(bootstrap.parent, staged, ignore=ignore_generated)
        completed = subprocess.run(
            [sys.executable, "-B", str(staged / "bootstrap.py"), *forwarded],
            check=False,
        )
        return completed.returncode


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help", "help"}:
        print_help()
        return 0

    bootstrap = bootstrap_path()
    if not bootstrap.is_file():
        print(f"error: reviewed bootstrap not found: {bootstrap}", file=sys.stderr)
        return 2

    command = args.pop(0)
    if command == "init":
        forwarded = ["--mode", "fresh", *args]
    elif command == "retrofit":
        forwarded = ["--mode", "retrofit", *args]
    elif command == "package-help":
        forwarded = ["--help"]
    else:
        print(f"error: unknown command: {command}", file=sys.stderr)
        print_help()
        return 2

    return run_bootstrap(bootstrap, forwarded)
