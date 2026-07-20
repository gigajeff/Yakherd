# Using Yakherd

## Requirements

- Python 3.11 or newer.
- A nonexistent or empty target directory for fresh installation.
- No third-party Python packages.

## Fresh Installation

Always inspect a dry-run first:

```powershell
python yakherd.py init `
  --target L:\dev\MY_PROJECT `
  --project-name MY_PROJECT `
  --dry-run
```

The dry-run prints the planned files and hashes without writing the target.
Run the same command without `--dry-run` to install.

## First Repository Workflow

1. Review the generated files and `JEFF_STRICT_SSOT_INSTALL.json` receipt.
2. Run the generated validators and tests.
3. Start a fresh Red Team task with
   `docs/prompts/bootstrap_cold_resume_review.md`.
4. Fix and re-review any protocol defects.
5. Commit the accepted governance shell.
6. Put the actual product master prompt under `docs/master_prompts/`.
7. Let Architecture convert that prompt into the first bounded implementation
   plan.

## Five Task Roles

Use one long-lived task for each role:

- Architecture
- Implementation
- Red Team
- Temporary Branch
- Governor

Chat is not authoritative. Each task reads repository state and writes its
decision, evidence, or finding back to the repository before claiming
completion.

## Low-Level Package Interface

The unchanged audited entry point remains available:

```powershell
python packages\jeff_strict_ssot_v1\bootstrap.py --help
```
