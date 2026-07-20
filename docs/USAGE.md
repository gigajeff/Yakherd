# Using Yakherd

## Requirements

- Python 3.11 or newer.
- A nonexistent or empty target directory for fresh installation.
- No third-party Python packages.
- An agentic coding environment needs project-file, shell, and Git access.

## Agent Compatibility

- Codex loads the installed `AGENTS.md` when the generated repository is opened
  as the project.
- Claude Code loads the installed `CLAUDE.md` when the generated repository is
  opened as the project in a fresh session. On first use, approve its local
  `@AGENTS.md` import only after verifying that it resolves inside the
  repository, then use `/context` to confirm both instruction files are active.
- Other coding agents must be explicitly told to read and follow `AGENTS.md`
  unless they document native support for it.

`AGENTS.md` remains the single authoritative instruction file. `CLAUDE.md` is
only an adapter and must not duplicate or override its rules. Do not begin work
if the applicable instruction file is absent from the agent's active context.

## Fresh Installation

Always inspect a dry-run first:

```bash
yakherd init \
  --target ~/dev/my-project \
  --project-name my-project \
  --dry-run
```

On Windows PowerShell:

```powershell
yakherd init `
  --target C:\dev\my-project `
  --project-name my-project `
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

The stable low-level package entry point remains available:

```bash
python3 packages/jeff_strict_ssot_v1/bootstrap.py --help
```

On Windows PowerShell:

```powershell
python packages\jeff_strict_ssot_v1\bootstrap.py --help
```
