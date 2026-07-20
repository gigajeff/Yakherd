#!/usr/bin/env python3
"""Run Yakherd directly from a source checkout."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from yakherd.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
