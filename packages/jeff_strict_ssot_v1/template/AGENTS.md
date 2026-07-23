# AGENTS.md

## Repository Rule

Chat directs work. Repository owners remember and prove work. A statement in
chat, a Governor report, or `STATUS.md` is not project truth unless the real
owner and required evidence agree.

## Read First

Before material work, read:

- `SSOT.md`
- `STATUS.md`
- `DECISIONS.md`
- `ARCHITECTURE.md`
- `TESTING.md`
- `GIT_SYNC.md`
- `docs/domain_invariants.md`
- `docs/task_protocol.md`
- `docs/validation_protocol.md`
- `code_review.md`

## Hard Rules

- On Windows, for all local execution obey Yakherd policy `Y-PROC-1` in
  `.yakherd/policies/Y-PROC-1.md`. Do not bypass its execution broker or
  process-lifecycle enforcement.
- One durable fact has one owner. Summaries link; they do not mirror mutable
  detail.
- `docs/task_protocol.md` owns proportional work modes, Red Team scope, and the
  two-review circuit breaker. Architecture owns strict-mode plans and gates.
  Implementation is the sole product writer for one authorized slice. Red
  Team reviews independently and does not repair its target. Temporary Branch
  work has no authority until reviewed and merged deliberately. Governor owns
  findings and risks only.
- Never run two writers in one working tree. Architecture and Red Team may
  write only isolated plan/review records within an explicit boundary.
- Promote durable results to their owner before updating `STATUS.md`.
- Do not infer product correctness from protocol validation.
- Do not treat a product prompt as executable authority. After bootstrap,
  Architecture preserves and extracts it; the human confirms the resulting
  bounded brief or strict planning scope. Product intake has no universal Red
  Team gate.
- Classify only the authorized slice, never imagined future scope. Bounded
  work may proceed from a user-approved brief without an Architecture plan or
  Red Team gate. Strict work follows the plan and review circuit breaker in
  `docs/task_protocol.md`.
- Network access, dependency installation, automation, release, deployment,
  destructive actions, Git publication, and scope escalation require explicit
  authorization.
- Preserve uncertainty. If evidence conflicts, stop and record the conflict.

## Codex Team Startup

- Launch the five Codex role agents only when the user explicitly invokes
  `START_HERE.md` or `docs/prompts/codex_team_launcher.md`.
- That invocation authorizes exactly five direct role agents: Architecture,
  Implementation, Red Team, Temporary Branch, and Governor. It does not
  authorize product work, Git mutation, network access, or nested delegation.
- The invoking task is a coordinator, not a sixth role or authority source.
- Creation of all five roles is a startup invariant. Report incomplete startup
  if any role cannot be created; never simulate a missing role in the
  coordinator.
- A created role may be parked or inactive. Never keep an unauthorized writer
  busy merely to make the team appear active.

## Status And Evidence

- `STATUS.md` is compact current state, updated in place, with one dated entry.
- Hard limits are 120 lines and 32,768 UTF-8 bytes; target is at most 80 lines.
- Evidence is proportional as described in `docs/validation_protocol.md`.
  Strict work and consequential promoted claims require structured records;
  bounded work may use concise command/result reporting.
- Transcript material is retrieval aid only and has no authority.

## Git Continuity

- Local uncommitted changes are visible only in the shared working tree.
- Remote and other-machine review requires an intentional commit and push.
- Never use blind `git add .`.
- Do not stage, commit, push, rewrite history, change remotes, or delete work
  without explicit human authorization.
- Final reports state branch, HEAD, upstream, dirty state, ahead/behind, and
  remote visibility.
- First-time GitHub setup follows `docs/GITHUB_SETUP.md` and its explicit human
  checkpoint. The installer receipt is not publication authorization.

## Completion Gate

Material work is complete only when behavior, applicable checks,
mode-appropriate evidence, owner promotion, compact status,
supersession/staleness records, and Git visibility reporting agree.

Every task result ends with exactly one:

- `autonomous next action:`
- `human action required:`
- `no next action needed:`
