# AGENTS.md

## Repository Purpose

Yakherd is a product-neutral SSOT governance harness for agentic software
projects. Correctness, fail-closed behavior, auditability, and deterministic
installation matter more than patch volume.

## Read First

Before changing package behavior, read:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/RELEASE.md`
- `packages/jeff_strict_ssot_v1/README.md`
- `packages/jeff_strict_ssot_v1/MANIFEST.json`
- `packages/jeff_strict_ssot_v1/RELEASE.json`

## Hard Rules

- Keep the installer product-neutral and standard-library-only.
- Do not add network, dependency-install, product-execution, automation, or
  target-repository Git behavior to the installer.
- Fresh install must remain no-overwrite and fail closed.
- Retrofit must remain reviewed, allowlisted, hash-pinned, transactional, and
  recoverable.
- Any change under `packages/jeff_strict_ssot_v1/` invalidates the current
  reviewed source snapshot. Regenerate manifest/release hashes, acceptance
  evidence, and independent Red Team review before release.
- Never commit `__pycache__`, `.pyc`, generated acceptance output, secrets, or
  machine-local state.
- Use `python -B` for package verification where practical.
- Do not claim that repository CI replaces independent review.

## Required Validation

For package changes:

```powershell
python -B -m unittest discover -s packages\jeff_strict_ssot_v1\tests -v
python packages\jeff_strict_ssot_v1\tests\run_acceptance.py `
  --package-root packages\jeff_strict_ssot_v1 `
  --output-root .tmp\acceptance `
  --date 2026-07-20
python scripts\verify_release.py
git diff --check
```

For documentation-only changes, run `python scripts\verify_release.py` and
`git diff --check` at minimum.

## Git Boundary

- Review staged paths before commit.
- Never use blind `git add .`.
- Do not rewrite history, delete releases, alter remotes, or publish without
  explicit human approval.
- Report branch, HEAD, upstream, clean/dirty state, and ahead/behind after
  meaningful Git work.
