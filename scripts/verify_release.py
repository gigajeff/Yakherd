#!/usr/bin/env python3
"""Verify v3 release bytes, historical V1 bindings and distribution identity."""
from __future__ import annotations
import argparse
import hashlib
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'packages/yakherd_v3'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_package(package):
    errors=[]
    manifest=json.loads((package/'MANIFEST.json').read_text(encoding='utf-8'))
    release=json.loads((package/'RELEASE.json').read_text(encoding='utf-8'))
    for field in ('package_name','package_version'):
        if manifest.get(field)!=release.get(field): errors.append(f'{package.name}: {field} mismatch')
    for name, field in (('bootstrap.py','bootstrap_sha256'),('MANIFEST.json','manifest_sha256')):
        if sha256(package/name)!=release.get(field): errors.append(f'{package.name}: release hash mismatch: {name}')
    actual=sorted(p.relative_to(package/'template').as_posix() for p in (package/'template').rglob('*') if p.is_file())
    hashes=manifest.get('template_sha256',{})
    if actual!=manifest.get('template_files') or set(actual)!=set(hashes): errors.append(f'{package.name}: template inventory mismatch')
    for name in actual:
        if sha256(package/'template'/name)!=hashes.get(name): errors.append(f'{package.name}: template hash mismatch: {name}')
    caches=[str(p.relative_to(package)) for p in package.rglob('*') if p.name=='__pycache__' or p.suffix in {'.pyc','.pyo'}]
    if caches: errors.append(f'{package.name}: generated caches present: {caches}')
    return errors,manifest


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag')
    args=parser.parse_args(argv)
    errors,manifest=verify_package(PACKAGE)
    legacy_errors,_=verify_package(ROOT/'packages/jeff_strict_ssot_v1')
    errors.extend(legacy_errors)
    project=tomllib.loads((ROOT/'pyproject.toml').read_text(encoding='utf-8'))['project']
    if project['name']!='yakherd' or project['version']!=manifest['package_version']:
        errors.append('public package identity/version mismatch')
    init=(ROOT/'src/yakherd/__init__.py').read_text(encoding='utf-8')
    if f'__version__ = "{project["version"]}"' not in init: errors.append('Python adapter version mismatch')
    if args.tag is not None and args.tag!=f'v{project["version"]}': errors.append('release tag mismatch')
    required={'AGENTS.md','SSOT.md','BASELINE.md','NOW.md','README.md','START_HERE.md','CLAUDE.md','.gitignore','.yakherd/profile.json','.yakherd/policies/Y-PROC-1.md'}
    if set(manifest['template_files'])!=required: errors.append('v3 payload does not match the compact harness')
    profile=json.loads((PACKAGE/'template/.yakherd/profile.json').read_text(encoding='utf-8'))
    if profile.get('schema_version')!=3 or profile.get('profile')!='yakherd-ssot': errors.append('wrong profile')
    for path in ('docs/SSOT_PROCESS.md','docs/SSOT_MIGRATION.md','docs/task_protocol.md'):
        if not (ROOT/path).is_file(): errors.append(f'missing canonical documentation: {path}')
    if errors:
        for error in errors: print(f'ERROR: {error}')
        return 1
    print(f'release_verification status=passed version={project["version"]} manifest_files={len(required)} legacy_bindings=passed cache_paths=0')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
