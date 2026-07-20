#!/usr/bin/env python3
"""Friendly launcher for the audited Yakherd SSOT bootstrap package."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BOOTSTRAP = ROOT / "packages" / "jeff_strict_ssot_v1" / "bootstrap.py"


def print_help() -> None:
    print(
        """Yakherd - herds the yaks so your agent stops shaving them.

Usage:
  python yakherd.py init --target PATH --project-name NAME [--dry-run]
  python yakherd.py retrofit --target PATH --project-name NAME \\
      --retrofit-plan PLAN.json [--dry-run]
  python yakherd.py package-help

Commands:
  init          Install into a nonexistent or empty project directory.
  retrofit      Apply a separately reviewed, hash-pinned retrofit plan.
  package-help  Show every low-level package option.
"""
    )


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"-h", "--help", "help"}:
        print_help()
        return 0
    if not BOOTSTRAP.is_file():
        print(f"error: audited bootstrap not found: {BOOTSTRAP}", file=sys.stderr)
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

    completed = subprocess.run(
        [sys.executable, "-B", str(BOOTSTRAP), *forwarded],
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
