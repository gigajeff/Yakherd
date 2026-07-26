"""Command-line adapter for the reviewed Yakherd installer."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


INSTALL_RECEIPT = "JEFF_STRICT_SSOT_INSTALL.json"
REPARSE_ATTRIBUTE = 0x400
MAX_RECEIPT_BYTES = 8 * 1024 * 1024
CRITICAL_INSTALLED_FILES = (
    "scripts/ssot/validate_protocol.py",
    "scripts/ssot/validate_governor_delta_policy.py",
)


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

Quick start:
  cd YOUR_PROJECT
  yakherd setup

Usage:
  yakherd setup [PATH] [--project-name NAME] [--dry-run]
  yakherd doctor [PATH]
  yakherd init --target PATH --project-name NAME [--dry-run]
  yakherd retrofit --target PATH --project-name NAME \\
      --retrofit-plan PLAN.json [--dry-run]
  yakherd exec [--heavy|--light] [--timeout SECONDS] -- COMMAND [ARG ...]
  yakherd process status
  yakherd process cleanup (--task TASK_ID|--all-owned) [--dry-run] [--verify]
  yakherd process hook
  yakherd package-help

Commands:
  setup         Safely set up and verify a project. This is the normal command.
  doctor        Read-only validation of an existing Yakherd project.
  init          Low-level no-overwrite installation command.
  retrofit      Apply a separately reviewed, hash-pinned retrofit plan.
  exec          Run a finite local command through Windows policy Y-PROC-1.
  process       Inspect, reconcile, or clean verified Y-PROC-1 process state.
  package-help  Show every low-level package option.
"""
    )


def print_quick_start(target: Path | None = None) -> None:
    """Print one non-mutating, state-aware next step."""
    selected = (Path.cwd() if target is None else target).absolute()
    receipt = selected / INSTALL_RECEIPT
    print("Yakherd is installed.")
    if os.path.lexists(receipt):
        print(f"This folder has a Yakherd installation receipt: {selected}")
        print("Verify it: yakherd doctor")
        print('Then, in Codex, say: "Start Yakherd"')
    else:
        print(f"Set up this folder: {selected}")
        print("Run: yakherd setup")
    print("More commands: yakherd --help")


def invoke_bootstrap(
    bootstrap: Path,
    forwarded: list[str],
    *,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run source bytes directly or stage a cache-free installed bundle."""
    options = {
        "check": False,
        "text": True,
        "capture_output": capture_output,
    }
    if bootstrap.parent.name != "_bundle":
        return subprocess.run(
            [sys.executable, "-B", str(bootstrap), *forwarded],
            **options,
        )

    def ignore_generated(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name == "__pycache__" or name.endswith((".pyc", ".pyo"))
        }

    with tempfile.TemporaryDirectory(prefix="yakherd-") as temporary:
        staged = Path(temporary) / "reviewed-package"
        shutil.copytree(bootstrap.parent, staged, ignore=ignore_generated)
        return subprocess.run(
            [sys.executable, "-B", str(staged / "bootstrap.py"), *forwarded],
            **options,
        )


def run_bootstrap(bootstrap: Path, forwarded: list[str]) -> int:
    """Compatibility adapter for the low-level public commands."""
    return invoke_bootstrap(bootstrap, forwarded).returncode


def is_reparse(path: Path) -> bool:
    info = path.lstat()
    attributes = getattr(info, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & REPARSE_ATTRIBUTE)


def load_receipt(target: Path) -> dict[str, object]:
    receipt = target / INSTALL_RECEIPT
    if not os.path.lexists(receipt):
        raise ValueError("no Yakherd installation receipt was found")
    if not receipt.is_file() or is_reparse(receipt):
        raise ValueError("the Yakherd installation receipt is not a regular file")
    if receipt.stat().st_size > MAX_RECEIPT_BYTES:
        raise ValueError("the Yakherd installation receipt is too large")
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"the Yakherd installation receipt is unreadable: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("the Yakherd installation receipt has an unsupported schema")
    if data.get("package_name") != "jeff_strict_ssot":
        raise ValueError("the Yakherd installation receipt has the wrong package name")
    if not isinstance(data.get("package_version"), str):
        raise ValueError("the Yakherd installation receipt has no package version")
    if not isinstance(data.get("files"), list):
        raise ValueError("the Yakherd installation receipt has no file inventory")
    return data


def verify_critical_installed_files(
    target: Path,
    receipt: dict[str, object],
) -> str | None:
    """Authenticate target-side executable validators without executing them."""
    raw_records = receipt["files"]
    assert isinstance(raw_records, list)
    records: dict[str, dict[str, object]] = {}
    for item in raw_records:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            return "the installation receipt contains an invalid file record"
        relative = item["path"]
        if relative in records:
            return f"the installation receipt repeats {relative}"
        records[relative] = item

    for relative in CRITICAL_INSTALLED_FILES:
        record = records.get(relative)
        if record is None:
            return f"the installation receipt omits {relative}"
        expected = record.get("rendered_sha256")
        if not isinstance(expected, str) or len(expected) != 64:
            return f"the installation receipt has an invalid hash for {relative}"
        path = target / Path(relative)
        if not path.is_file() or is_reparse(path):
            return f"the installed validator is missing or unsafe: {relative}"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            return f"the installed validator has changed: {relative}"
    return None


def doctor(target: Path) -> int:
    """Validate target bytes with bundled, reviewed validators."""
    selected = target.absolute()
    if not selected.is_dir():
        print(
            f"Yakherd doctor: not ready ({selected} is not a directory)",
            file=sys.stderr,
        )
        return 2
    try:
        receipt = load_receipt(selected)
    except ValueError as exc:
        print(f"Yakherd doctor: not ready ({exc})", file=sys.stderr)
        print(f'Run: yakherd setup "{selected}"', file=sys.stderr)
        return 2

    bootstrap = bootstrap_path()
    reviewed_template = bootstrap.parent / "template"
    checks = (
        (
            "protocol",
            reviewed_template / "scripts" / "ssot" / "validate_protocol.py",
            ["--root", str(selected), "--strict", "--summary"],
        ),
        (
            "governor policy",
            reviewed_template
            / "scripts"
            / "ssot"
            / "validate_governor_delta_policy.py",
            ["--root", str(selected), "--strict"],
        ),
    )
    for label, script, arguments in checks:
        if not script.is_file():
            print(
                f"Yakherd doctor: not ready (reviewed {label} validator is missing)",
                file=sys.stderr,
            )
            return 2
        completed = subprocess.run(
            [sys.executable, "-B", str(script), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            print(
                f"Yakherd doctor: not ready ({label} validation failed)",
                file=sys.stderr,
            )
            if completed.stdout.strip():
                print(completed.stdout.strip(), file=sys.stderr)
            if completed.stderr.strip():
                print(completed.stderr.strip(), file=sys.stderr)
            return 1
        print(f"[ok] {label}")
        if label == "protocol":
            critical_error = verify_critical_installed_files(selected, receipt)
            if critical_error is not None:
                print(
                    f"Yakherd doctor: not ready ({critical_error})",
                    file=sys.stderr,
                )
                return 1
            print("[ok] installed validator identities")

    version = receipt["package_version"]
    files = len(receipt["files"])
    print(f"Yakherd doctor: ready ({version}, {files} managed payload files)")
    print(f"Target: {selected}")
    print('Next, open this folder in Codex and say: "Start Yakherd"')
    return 0


def run_doctor_command(args: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="yakherd doctor")
    parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    parsed = parser.parse_args(args)
    return doctor(parsed.path)


def run_setup_command(args: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="yakherd setup")
    parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--project-name")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--date", help=argparse.SUPPRESS)
    parsed = parser.parse_args(args)
    target = parsed.path.absolute()

    if os.path.lexists(target / INSTALL_RECEIPT):
        if parsed.dry_run:
            print("Yakherd is already set up; validating without changes.")
        else:
            print("Yakherd is already set up; validating instead of reinstalling.")
        return doctor(target)

    if target.exists() and not target.is_dir():
        print(
            f"Yakherd setup stopped: target is not a directory: {target}",
            file=sys.stderr,
        )
        return 2
    project_name = parsed.project_name or target.name
    if not project_name:
        print(
            "Yakherd setup stopped: cannot derive a project name; use --project-name.",
            file=sys.stderr,
        )
        return 2

    bootstrap = bootstrap_path()
    if not bootstrap.is_file():
        print(
            f"Yakherd setup stopped: reviewed bootstrap not found: {bootstrap}",
            file=sys.stderr,
        )
        return 2
    forwarded = [
        "--mode",
        "fresh",
        "--target",
        str(target),
        "--project-name",
        project_name,
    ]
    if parsed.date:
        forwarded.extend(["--date", parsed.date])
    if parsed.dry_run:
        forwarded.append("--dry-run")
    completed = invoke_bootstrap(bootstrap, forwarded, capture_output=True)
    if completed.returncode != 0:
        print("Yakherd setup stopped. No existing file was overwritten.", file=sys.stderr)
        details = (completed.stderr or completed.stdout).strip()
        if details:
            print(details, file=sys.stderr)
        return completed.returncode
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        print("Yakherd setup stopped: installer returned invalid output.", file=sys.stderr)
        return 2
    file_count = len(result.get("files", []))
    if parsed.dry_run:
        print("Yakherd setup preview")
        print(f"Target: {target}")
        print(f"Project: {project_name}")
        print(f"Files to add: {file_count}")
        print("Nothing changed. Run the same command without --dry-run to install.")
        return 0

    print(f"Yakherd installed {file_count} files without overwriting existing files.")
    return doctor(target)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print_quick_start()
        return 0
    if args[0] in {"-h", "--help", "help"}:
        print_help()
        return 0

    command = args.pop(0)
    if command == "setup":
        return run_setup_command(args)
    if command == "doctor":
        return run_doctor_command(args)
    if command == "exec":
        from .process_hygiene import run_exec_cli

        return run_exec_cli(args)
    if command == "process":
        from .process_hygiene import run_process_cli

        return run_process_cli(args)

    bootstrap = bootstrap_path()
    if not bootstrap.is_file():
        print(f"error: reviewed bootstrap not found: {bootstrap}", file=sys.stderr)
        return 2

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
