"""Smoke-install the exact wheel and sdist into separate clean environments."""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.absolute()
    if output.exists() and any(output.iterdir()):
        parser.error('output must be absent or empty')
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for kind, pattern in [('wheel', 'yakherd-3.0.0-*.whl'), ('sdist', 'yakherd-3.0.0.tar.gz')]:
        matches = list(args.directory.absolute().glob(pattern))
        if len(matches) != 1:
            parser.error(f'expected exactly one {pattern}')
        env = output / f'{kind}-env'
        subprocess.run([sys.executable, '-m', 'venv', str(env)], check=True)
        scripts = env / ('Scripts' if os.name == 'nt' else 'bin')
        python = scripts / ('python.exe' if os.name == 'nt' else 'python')
        command = scripts / ('yakherd.exe' if os.name == 'nt' else 'yakherd')
        install = [str(python), '-m', 'pip', 'install', '--no-deps']
        if kind == 'wheel':
            install.append('--no-index')
        # Source builds may fetch the exact pinned build-system requirement.
        subprocess.run([*install, str(matches[0])], check=True)
        version = subprocess.run([str(command), '--version'], check=True, text=True, capture_output=True)
        if version.stdout.strip() != '3.0.0':
            raise RuntimeError(f'{kind}: unexpected installed version')
        project = output / f'{kind}-project'
        subprocess.run([str(command), 'setup', str(project), '--date', '2026-09-24'], check=True)
        checked = subprocess.run([str(command), 'doctor', str(project), '--json'], check=True, text=True, capture_output=True)
        report = json.loads(checked.stdout)
        if report['status'] != 'ready':
            raise RuntimeError(f'{kind}: structural smoke check failed')
        records.append({'kind': kind, 'artifact': matches[0].name, 'version': version.stdout.strip(), 'doctor': report['status']})
    (output / 'smoke.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'passed', 'checks': records}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
