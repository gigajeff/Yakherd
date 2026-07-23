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
- `docs/task_protocol.md`
- `packages/jeff_strict_ssot_v1/README.md`
- `packages/jeff_strict_ssot_v1/MANIFEST.json`
- `packages/jeff_strict_ssot_v1/RELEASE.json`

## Hard Rules

- LOCAL PROCESS HYGIENE (`Y-PROC-1`): use one finite top-level local execution
  pipeline at a time and preserve normal internal parallelism. Run heavy work
  below normal priority; never start unapproved REPLs, watchers, detached or
  persistent processes; and verify zero task-owned descendants without killing
  pre-existing or unrelated processes. Process ownership requires a matching
  PID, creation time, executable path, internally consistent command-line
  identity, and a reliable task marker such as Job Object membership; never
  infer it from PID or parent PID alone. An incomplete or inconsistent record
  is `ownership_record_inconsistent_unverified`: a warning, not a work embargo,
  unless fresh verified evidence shows a concrete interference or safety risk.
  Explicit human authorization may override a non-hazardous warning.
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

## Proportional Review Rule

`docs/task_protocol.md` is the canonical SSOT owner for work-mode
classification, review scope and severity, the review-cycle budget, and role
handoffs in this repository. The rules below are a repository-instruction
summary; resolve any conflict in those fields in favor of the canonical owner.

- Reversible local repository work with a user-approved goal, write boundary,
  forbidden scope, and Definition of Done is bounded work. It does not require
  an Architecture plan or Red Team gate merely because stricter future work is
  imaginable.
- Release/deployment, credentials, destructive changes, personal or regulated
  data, spending, safety-critical behavior, installer changes, and governance-
  core changes are strict work.
- Red Team verifies accepted requirements and hazards introduced by the exact
  diff. It cannot add product requirements or make an out-of-scope enhancement
  a finding. Only P0/P1 findings block; P2/P3 are advisory.
- A strict target gets one initial review and one recheck. After two
  consecutive failures, stop for human rescoping, risk acceptance, or
  cancellation. Do not create V3/V4 candidates or a new work ID for the same
  goal to evade the limit.
- Keep one active plan and review path per work ID; revise in place. A review
  cannot itself create a fresh-review requirement.

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
