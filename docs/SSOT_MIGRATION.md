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

Use [the v3 templates](../packages/yakherd_v3/template/) as structure, not as permission to
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

## Transactional CLI

Prepare project-specific replacement files in a separate directory, using
the same relative paths they will have in the target. Keep this directory and
the plan outside the target. Copy forward the accepted product content and
retire conflicting entry points explicitly. Supply the v3 profile, startup
instructions and policy when absent. Keep the existing process policy if it
is still applicable. Do not include an installation receipt in the replacements.

```text
yakherd migrate plan TARGET --replacements PREPARED --output PLAN.json
yakherd migrate preview PLAN.json
```

Plan creation writes only the selected output file, using exclusive creation.
It snapshots exact current hashes and embeds replacement content plus output
hashes. Existing core owners omitted from PREPARED are carried forward and
hash-pinned; this never means their old rules have been semantically migrated.
Preview prints the exact before/after diffs without modifying the target.

Inspect the complete plan, including retained requirements and evidence. Set
`reviewed` to `true` only after review. Compute the SHA-256 of that final plan
(for example, `Get-FileHash PLAN.json -Algorithm SHA256` in PowerShell; use its
lowercase hash), then apply those exact reviewed bytes:

```text
yakherd migrate apply PLAN.json --plan-sha256 REVIEWED_SHA256
yakherd doctor TARGET
```

Apply rejects content/hash mismatches, unsafe paths, missing owners, remaining
recognized legacy startup directives, stale target bytes and unresolved
migration journals. It uses a lock, verified backups, atomic file replacement,
post-write verification and rollback on failure. It does not run target code,
Git, network requests or dependency installation. Root owner files, the profile,
process policy and Markdown documentation are eligible; product code and Git
configuration are outside the migration writer's scope.

Successful migration reports `.yakherd-backup-ID/` containing the exact
originals and a completed journal. Preserve that directory until recovery is
no longer needed; it can contain private project content and should not be
committed. A failed migration keeps `.yakherd-migrate-txn-ID/journal.json`,
even after automatic rollback. Another migration remains blocked until the
interrupted transaction is inspected. Never delete a live lock or journal to
force progress.

For recovery, stop competing writers, inspect `expected_states`,
`written_states`, `backups`, `replacements` and `rollback_errors` in the journal,
and verify every backup hash. Restore only files whose current bytes match
the recorded transaction output; preserve conflicting external edits for a
human decision. An original state of `absent` means a newly created path,
not a missing backup. Recovery is a deliberate local maintenance operation;
the current CLI does not automatically undo a successful migration. Once a
failed transaction is fully reconciled, preserve its journal outside the active
transaction prefix before preparing a new exact-state plan.

The plan and backups may contain sensitive original content. Keep them local
unless separately reviewed for publication. A reviewed plan does not grant
new publication, spending, data-transfer or product authority.
