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

- One durable fact has one owner. Summaries link; they do not mirror mutable
  detail.
- Architecture owns plans and gates. Implementation is the sole product
  writer for one authorized slice. Red Team reviews independently and does not
  repair its target. Temporary Branch work has no authority until reviewed and
  merged deliberately. Governor owns findings and risks only.
- Never run two writers in one working tree. Architecture and Red Team may
  write only isolated plan/review records within an explicit boundary.
- Promote durable results to their owner before updating `STATUS.md`.
- Do not infer product correctness from protocol validation.
- Do not ingest or execute a product prompt until Architecture and Red Team
  complete product intake.
- Network access, dependency installation, automation, release, deployment,
  destructive actions, Git publication, and scope escalation require explicit
  authorization.
- Preserve uncertainty. If evidence conflicts, stop and record the conflict.

## Status And Evidence

- `STATUS.md` is compact current state, updated in place, with one dated entry.
- Hard limits are 120 lines and 32,768 UTF-8 bytes; target is at most 80 lines.
- Tests and completion claims require structured run evidence as described in
  `docs/validation_protocol.md`.
- Transcript material is retrieval aid only and has no authority.

## Git Continuity

- Local uncommitted changes are visible only in the shared working tree.
- Remote and other-machine review requires an intentional commit and push.
- Never use blind `git add .`.
- Do not stage, commit, push, rewrite history, change remotes, or delete work
  without explicit human authorization.
- Final reports state branch, HEAD, upstream, dirty state, ahead/behind, and
  remote visibility.

## Completion Gate

Material work is complete only when behavior, applicable checks, structured
evidence, owner promotion, compact status, supersession/staleness records, and
Git visibility reporting agree.

Every task result ends with exactly one:

- `autonomous next action:`
- `human action required:`
- `no next action needed:`
