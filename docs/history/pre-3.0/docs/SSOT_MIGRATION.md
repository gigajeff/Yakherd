# Adopting the current SSOT process in an existing repository

Use this guide with explicit authorization to replace the repository's old
operating model. Adding `NOW.md` while retaining an active five-role launcher
does not perform the migration. The current model is specified in
[SSOT_PROCESS.md](SSOT_PROCESS.md).

## Preserve before changing authority

Inspect the actual checkout, existing changes, task/process state, evidence
and product requirements. Coordinate a single writer; do not resume stopped
work or kill unrelated processes. Identify the exact affected files and
preserve their original bytes in Git or a task-local archive when not already
recoverable. Keep raw research packets and source hashes unchanged.

Separate durable product requirements, measured technical facts and genuine
hazards from obsolete workflow rules. Preserve the former in active owners
before demoting historical documents. Never resolve a real data-loss,
privacy/security or scientific-validity finding by relabeling it legacy.

## Adapt the owners in place

| Existing material | Destination or treatment |
| --- | --- |
| Mission and accepted product requirements | `SSOT.md`, or a single linked product-spec owner |
| Reproduced technical results, constraints, uncertainty | `BASELINE.md` with evidence links |
| Current objective, scope, DoD, blockers and next action | One `NOW.md` |
| Agent rules and long read-first lists | Concise `AGENTS.md` pointing to the current owners |
| `STATUS.md` and duplicate active plans | Preserve history; retire as current owners and link to `NOW.md`/`BASELINE.md` |
| `DECISIONS.md`, architecture, domain and testing records | Extract still-current facts to their named owner; retain useful detail as linked technical evidence |
| Five-role launchers and role prompts | Explicitly supersede their mandatory startup/gating rules; redirect active entry points to the current owners |
| Review ledgers, Governor and authorization registers | Preserve as history; remove mandatory execution dependencies |
| Process containment, data/security and Git controls | Retain the actual applicable controls and authority |
| Old validators | Retain useful checks; distinguish obsolete protocol checks from product/security checks |

Use [the starter files](ssot-starter/) as structure, not as permission to
overwrite product content with placeholders. Preserve any valid existing
owner and point to it; do not create parallel mutable specifications.

Update every active entry point that can resurrect the old process, including
`START_HERE.md`, `docs/task_protocol.md`, role launchers, intake/completion
instructions, `code_review.md` and editor adapters when present. A historical
banner must clearly remove the old text's authority; retain originals in the
archive and use short redirects where that is clearer. Merely adding a note
to `NOW.md` while `AGENTS.md` still requires the old gates is insufficient.

Preserve a one-line `CLAUDE.md` import if present; never create a second policy
copy. Do not edit an installation receipt to pretend that migrated bytes are
still the original installed payload. A legacy `yakherd doctor` failure about
retired owners or review ledgers is compatibility evidence, not an instruction
to restore those rules. Investigate genuine broken links, missing evidence,
integrity/security failures and product regressions on their own merits.

## Verify and resume

Check local links, current owner uniqueness, retained technical requirements,
absence of unresolved template placeholders, and all active startup paths.
A fresh reader must reconstruct the goal, baseline, current milestone,
unresolved inputs and next action without the preceding chat. Use independent
review when requested or warranted, not as a new universal migration ceremony.

Run relevant product regression checks if behavior changed. Report preserved
evidence, changed operating owners, any real unresolved risk and the next
executable action. Continue only within the authorized task; a request to
prepare a handoff does not authorize resuming a stopped task or publishing.

This is a local instruction migration. It does not change the installer,
install dependencies, create automation, modify other repositories, or grant
new publication/spending/data-transfer authority. If the legacy retrofit
command is deliberately used, its exact-state, reviewed allowlist and recovery
requirements still apply.
