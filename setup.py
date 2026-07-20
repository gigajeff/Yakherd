#!/usr/bin/env python3
"""Build the PyPI distribution with the reviewed installer package bundled."""

from __future__ import annotations

import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


ROOT = Path(__file__).resolve().parent
AUDITED_PACKAGE = ROOT / "packages" / "jeff_strict_ssot_v1"


def ignore_generated(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name == "__pycache__" or name.endswith((".pyc", ".pyo"))
    }


class BuildWithAuditedPackage(build_py):
    """Copy reviewed source bytes into the platform-independent wheel."""

    def run(self) -> None:
        super().run()
        destination = Path(self.build_lib) / "yakherd" / "_bundle"
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(AUDITED_PACKAGE, destination, ignore=ignore_generated)


setup(cmdclass={"build_py": BuildWithAuditedPackage})
