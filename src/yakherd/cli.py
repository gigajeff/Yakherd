"""Public, standard-library-only Yakherd 3 command line."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .diagnostics import inspect
from . import migration

INSTALL_RECEIPT = "YAKHERD_INSTALL.json"


def bootstrap_path() -> Path:
    package = Path(__file__).resolve().parent
    bundled = package / "_bundle" / "bootstrap.py"
    return bundled if bundled.is_file() else package.parents[1] / "packages/yakherd_v3/bootstrap.py"


def load_engine():
    path = bootstrap_path()
    spec = importlib.util.spec_from_file_location("yakherd_trusted_bootstrap", path)
    if not spec or not spec.loader:
        raise ValueError("Yakherd installer package is missing")
    module = importlib.util.module_from_spec(spec)
    # Doctor imports only our distributed engine, never code in the target.
    spec.loader.exec_module(module)
    module.load_package_manifest()
    return module


def invoke_bootstrap(bootstrap: Path, forwarded: list[str], *, capture_output: bool = False):
    options = {"check": False, "text": True, "capture_output": capture_output}
    if bootstrap.parent.name != "_bundle":
        return subprocess.run([sys.executable, "-B", str(bootstrap), *forwarded], **options)
    def ignore_generated(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name == "__pycache__" or name.endswith((".pyc", ".pyo"))}
    with tempfile.TemporaryDirectory(prefix="yakherd-") as temporary:
        staged = Path(temporary) / "package"
        shutil.copytree(bootstrap.parent, staged, ignore=ignore_generated)
        return subprocess.run([sys.executable, "-B", str(staged / "bootstrap.py"), *forwarded], **options)


def run_bootstrap(bootstrap: Path, forwarded: list[str]) -> int:
    return invoke_bootstrap(bootstrap, forwarded).returncode


def print_help() -> None:
    print('''Yakherd 3 - stable requirements, measured baseline, one current milestone.

Usage:
  yakherd setup [PATH] [--project-name NAME] [--dry-run]
  yakherd doctor [PATH] [--json]
  yakherd init --target PATH --project-name NAME [--dry-run]
  yakherd migrate plan TARGET --replacements DIR --output PLAN.json
  yakherd migrate preview PLAN.json
  yakherd migrate apply PLAN.json --plan-sha256 SHA256
  yakherd exec [--heavy|--light] [--timeout SECONDS] -- COMMAND [ARG ...]
  yakherd process status
  yakherd process cleanup (--task TASK_ID|--all-owned) [--dry-run] [--verify]
  yakherd process hook
  yakherd package-help

Setup never overwrites existing paths. Migration needs reviewed, hash-pinned
replacement content. Doctor checks structure, not product correctness.
Start Yakherd means resume NOW.md in one implementation task; no team launch.
''')


def doctor(target: Path, *, json_output: bool = False) -> int:
    report = inspect(target, load_engine())
    if json_output:
        print(json.dumps(report, indent=2))
    else:
        print(f"Yakherd doctor: {report['status']} (structural checks only)")
        print(f"Target: {report['target']}")
        for item in report['errors']:
            print(f"ERROR: {item}", file=sys.stderr)
        for item in report['warnings']:
            print(f"NOTE: {item}")
        if report['status'] == 'ready':
            print('Open the project and say: "Start Yakherd". Read the current owners and continue NOW.md.')
    return 0 if report['status'] == 'ready' else 1


def setup(args: list[str]) -> int:
    parser = argparse.ArgumentParser(prog='yakherd setup')
    parser.add_argument('path', nargs='?', type=Path, default=Path.cwd())
    parser.add_argument('--project-name')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--date', help=argparse.SUPPRESS)
    parsed = parser.parse_args(args)
    target = parsed.path.absolute()
    if os.path.lexists(target / INSTALL_RECEIPT):
        print('Yakherd is already set up; validating instead of reinstalling.')
        return doctor(target)
    if os.path.lexists(target / 'JEFF_STRICT_SSOT_INSTALL.json'):
        print('Legacy installation detected. Prepare a reviewed v3 migration; setup will not overwrite it.', file=sys.stderr)
        return 2
    forwarded = ['--target', str(target), '--project-name', parsed.project_name or target.name]
    if parsed.date:
        forwarded += ['--date', parsed.date]
    if parsed.dry_run:
        forwarded.append('--dry-run')
    completed = invoke_bootstrap(bootstrap_path(), forwarded, capture_output=True)
    if completed.returncode:
        print('Yakherd setup stopped. No existing file was overwritten.', file=sys.stderr)
        print((completed.stderr or completed.stdout).strip(), file=sys.stderr)
        return completed.returncode
    result = json.loads(completed.stdout)
    if parsed.dry_run:
        print(json.dumps(result, indent=2))
        return 0
    print(f"Yakherd installed {len(result['files'])} files without overwriting existing files.")
    return doctor(target)


def migrate(args: list[str]) -> int:
    parser = argparse.ArgumentParser(prog='yakherd migrate')
    commands = parser.add_subparsers(dest='action', required=True)
    plan = commands.add_parser('plan')
    plan.add_argument('target', type=Path)
    plan.add_argument('--replacements', type=Path, required=True)
    plan.add_argument('--output', type=Path, required=True)
    preview = commands.add_parser('preview')
    preview.add_argument('plan', type=Path)
    apply = commands.add_parser('apply')
    apply.add_argument('plan', type=Path)
    apply.add_argument('--plan-sha256', required=True)
    parsed = parser.parse_args(args)
    engine = load_engine()
    if parsed.action == 'plan':
        result = migration.prepare(parsed.target, parsed.replacements, parsed.output, engine)
    elif parsed.action == 'preview':
        result = migration.preview(parsed.plan, engine)
    else:
        result = migration.apply(parsed.plan, parsed.plan_sha256, engine)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print('Yakherd 3 is installed. Run: yakherd doctor' if os.path.lexists(Path.cwd()/INSTALL_RECEIPT)
              else 'Run: yakherd setup (new repository) or yakherd migrate (existing repository).')
        print('More commands: yakherd --help')
        return 0
    command = args.pop(0)
    if command in {'--help', '-h', 'help'}:
        print_help()
        return 0
    if command == '--version':
        from . import __version__
        print(__version__)
        return 0
    try:
        if command == 'setup':
            return setup(args)
        if command == 'doctor':
            parser = argparse.ArgumentParser(prog='yakherd doctor')
            parser.add_argument('path', nargs='?', type=Path, default=Path.cwd())
            parser.add_argument('--json', action='store_true')
            parsed = parser.parse_args(args)
            return doctor(parsed.path, json_output=parsed.json)
        if command == 'migrate':
            return migrate(args)
        if command == 'exec':
            from .process_hygiene import run_exec_cli
            return run_exec_cli(args)
        if command == 'process':
            from .process_hygiene import run_process_cli
            return run_process_cli(args)
        if command == 'init':
            return run_bootstrap(bootstrap_path(), args)
        if command == 'package-help':
            return run_bootstrap(bootstrap_path(), ['--help'])
        if command == 'retrofit':
            raise ValueError('The v3 public migration command is yakherd migrate; legacy retrofit plans are not v3 adoption plans.')
        raise ValueError(f'unknown command: {command}')
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        print(f'yakherd_error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
