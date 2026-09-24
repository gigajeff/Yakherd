"""Record finite v3 dry-run, install, doctor, migration and rollback acceptance."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package-root', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    parser.add_argument('--date', required=True)
    args = parser.parse_args()
    package, output = args.package_root.resolve(), args.output_root.resolve()
    root = package.parents[1]
    if output.exists() and any(output.iterdir()):
        parser.error('output root must be absent or empty')
    output.mkdir(parents=True, exist_ok=True)
    records = []
    errors = []

    def execute(label, command, expected=0):
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        number = len(records) + 1
        stdout, stderr = output / f'{number:02d}_stdout.txt', output / f'{number:02d}_stderr.txt'
        stdout.write_text(result.stdout, encoding='utf-8')
        stderr.write_text(result.stderr, encoding='utf-8')
        record = {'label': label, 'command': command, 'exit_code': result.returncode,
                  'expected_exit_code': expected,
                  'stdout': {'path': stdout.name, 'sha256': digest(stdout)},
                  'stderr': {'path': stderr.name, 'sha256': digest(stderr)}}
        records.append(record)
        if result.returncode != expected:
            errors.append(f'{label}: exit {result.returncode}, expected {expected}')
        return result

    python = [sys.executable, '-B']
    dry_target, target = output / 'dry-target', output / 'installed'
    common = ['--project-name', 'Acceptance Fixture', '--date', args.date]
    dry = [*python, str(package / 'bootstrap.py'), '--target', str(dry_target), *common, '--dry-run']
    first = execute('dry-run', dry)
    second = execute('repeat deterministic dry-run', dry)
    if (first.stdout, first.stderr) != (second.stdout, second.stderr) or dry_target.exists():
        errors.append('dry-run changed output or wrote target')
    install = [*python, str(package / 'bootstrap.py'), '--target', str(target), *common]
    execute('fresh install', install)
    execute('read-only doctor', [*python, str(root / 'yakherd.py'), 'doctor', str(target), '--json'])
    before = {p.relative_to(target).as_posix(): digest(p) for p in target.rglob('*') if p.is_file()}
    execute('no-overwrite refusal', install, expected=2)
    after = {p.relative_to(target).as_posix(): digest(p) for p in target.rglob('*') if p.is_file()}
    if before != after:
        errors.append('refused installation changed target bytes')
    manifest = json.loads((package / 'MANIFEST.json').read_text(encoding='utf-8'))
    if set(after) != set(manifest['template_files']) | {'YAKHERD_INSTALL.json'}:
        errors.append('unexpected installed file tree')
    receipt = json.loads((target / 'YAKHERD_INSTALL.json').read_text(encoding='utf-8'))
    for item in receipt['files']:
        if digest(target / item['path']) != item['rendered_sha256']:
            errors.append(f"installed hash mismatch: {item['path']}")
    execute('migration drift, containment, review, backup and rollback regressions',
            [*python, '-m', 'unittest', 'discover', '-s', str(root / 'tests'), '-p', 'test_v3_migration.py', '-v'])
    execute('release bindings', [*python, str(root / 'scripts/verify_release.py')])
    report = {'schema_version': 3, 'status': 'failed' if errors else 'passed',
              'package_version': manifest['package_version'], 'commands': records,
              'installed_files': after, 'errors': errors,
              'limitations': ['structural/package evidence only', 'not product validation',
                              'independent candidate review still required']}
    path = output / 'acceptance_aggregate.json'
    path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'aggregate': str(path), 'errors': errors}))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
