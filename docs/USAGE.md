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
2. Open the repository as the Codex project and confirm `AGENTS.md` is loaded.
3. In a new main task, send: `Follow START_HERE.md now. Launch the five
   Yakherd role agents and keep this task as their coordinator.`
4. Confirm Codex created all five named agent threads. Red Team runs
   `docs/prompts/bootstrap_cold_resume_review.md`; the other roles begin in
   their defined waiting, parked, or inactive states.
5. If the bootstrap review finds a protocol defect, fix it once and use the
   single permitted recheck. A second failure stops for a human decision.
6. If GitHub hosting is wanted, follow `docs/GITHUB_SETUP.md`. Confirm the
   authenticated account, exact repository, visibility, initial staged paths,
   commit, remote, and first push before allowing mutation.
7. Give the coordinator the actual product master prompt between the documented
   delimiters. Architecture preserves its bytes and provenance under
   `docs/master_prompts/` and extracts the first bounded brief or strict
   planning scope for you to confirm.
8. A confirmed bounded brief goes directly to Implementation. A strict slice
   uses one Architecture plan and at most two Red Team reviews.

## Five Task Roles

In Codex, the explicit launcher creates one agent thread for each role:

- Architecture
- Implementation
- Red Team
- Temporary Branch
- Governor

Chat is not authoritative. Each task reads repository state and writes its
decision, evidence, or finding back to the repository before claiming
completion.

The main task is their coordinator, not a sixth authority. All five role agents
are created at startup, but only Red Team acts immediately. Architecture waits
for the bootstrap gate and master prompt, Implementation and Temporary Branch
park, and Governor stays inactive. If the client cannot create all five, the
launcher must report incomplete startup rather than silently collapsing roles.

Other coding environments may create the same five long-lived sessions
manually from the role prompt files. Automatic role-agent creation is a Codex
adapter, not an installer side effect.

## GitHub Account And Repository

Yakherd never runs Git or accesses GitHub during installation. After bootstrap
PASS, the coordinator can set up the project in the user's own GitHub account
through the generated `docs/GITHUB_SETUP.md` workflow. It uses the existing
authenticated GitHub CLI or connector session, never asks for a pasted token,
suggests private visibility, preserves any existing history/remotes, stages an
explicit reviewed path list, and requests one bounded human approval before
the initial Git mutation and publication.

## Windows Y-PROC-1 Execution

Run finite local commands through the broker after installing Yakherd:

```powershell
yakherd exec --timeout 900 -- cmake --build build
yakherd exec --light --timeout 60 -- git status --short
yakherd process status
yakherd process cleanup --all-owned --dry-run --verify
yakherd process resume --task TASK_ID
```

Heavy is the default. Heavy top-level pipelines queue behind one user-scoped
lock and run below normal priority; the selected build or test command retains
its normal internal parallelism. `--light` is an explicit classification for a
finite low-CPU command that is safe to overlap.

Use `yakherd process cleanup --task TASK_ID --verify` for a selected owned
task. Cleanup checks coherent PID, creation time, executable/image, command
line, task/execution and Job Object identity; it never kills by process name.
PID reuse, legacy records, incomplete telemetry, and contradictory records are
reported as warnings and never terminate the replacement process. Only a live
Job-verified task process whose cleanup failed and has concrete hazard evidence
is a blocker. `yakherd process resume --task TASK_ID` explicitly continues
after a warning once; it cannot override a blocker.

Y-PROC-1.1 does not support persistent leases. Do not bypass the broker for
REPLs, watchers, detached jobs, daemons, or development servers.

`yakherd process hook` is an optional Codex `Stop`/`SubagentStop` handler. It
uses the hook payload's `session_id`, `turn_id`, and `cwd`, cancels only tasks
owned by that Codex session, and warns without touching different-owner work.
It returns `continue: false` only for a scoped verified concrete blocker. Install the
example from the generated `.yakherd/policies/Y-PROC-1.md` only after explicit
human review; the Yakherd installer never creates hook automation.

## Low-Level Package Interface

The stable low-level package entry point remains available:

```bash
python3 packages/jeff_strict_ssot_v1/bootstrap.py --help
```

On Windows PowerShell:

```powershell
python packages\jeff_strict_ssot_v1\bootstrap.py --help
```
