# Yakherd Task Protocol

## Canonical ownership

This file is the canonical SSOT owner for work-mode classification,
independent-review scope and severity, the review-cycle budget, and role
handoffs while developing Yakherd itself.

`AGENTS.md` remains the repository-wide instruction owner and points here for
those fields. The separate
`packages/jeff_strict_ssot_v1/template/docs/task_protocol.md` is retained as
the historical installed owner for V1 repositories. V3 products follow their
local SSOT owners generated from `packages/yakherd_v3/template/` and the
specification in `docs/SSOT_PROCESS.md`. This development review ledger is not
installed into v3 product repositories.

## Work modes

### Bounded work

Reversible local repository work is bounded when the user-approved request has
an exact goal, write boundary, forbidden scope, and Definition of Done. It may
proceed directly to one Implementation writer with relevant regression checks.
It does not require an Architecture plan or Red Team gate merely because a
stricter future task is imaginable.

### Strict work

Use strict mode when the exact authorized slice includes release or deployment,
credentials or secrets, destructive or difficult-to-reverse changes, personal
or regulated data, spending, safety-critical behavior, installer changes,
governance-core changes, or an explicit user request for strict review.

Classify only the authorized slice. Do not import hypothetical future release,
deployment, website, credential, or product scope into a bounded task.

## Roles and writer boundary

- Architecture owns the smallest accepted plan for strict work.
- Implementation is the sole writer for the authorized implementation slice.
- Red Team independently reviews strict work against the accepted contract and
  exact diff; it does not implement repairs or add requirements.
- Temporary Branch work remains isolated and non-authoritative until reviewed
  and deliberately merged.
- Governor reports bounded deltas and cannot authorize product or release work.
- Never run two implementation writers against the same checkout.

## Independent-review circuit breaker

Strict work uses a persisted, hash-bound ledger. Review stays within R0-frozen
accepted requirements and the approved boundary. Only P0/P1 block; P2/P3 are
advisory.

`R0 -> PASS | C1 | HUMAN_DISPOSITION_REQUIRED.`
`C1 -> PASS | C2 | HUMAN_DISPOSITION_REQUIRED.`
`C2 -> PASS | HUMAN_DISPOSITION_REQUIRED.`
Each `C` stage permits one repair-and-recheck wave; a crash resumes that stage.

Only a concrete, safely evidenced violation of an R0-frozen accepted
requirement or non-waivable safety invariant blocks. Findings sharing a root
cause or substantially the same repair keep one ID; renaming, changing
reviewer/work ID, or forking cannot reset budgets.

Repairs must be minimal, reversible, local, inside the approved write set, and
cannot weaken acceptance or expand authority. Rechecks cover open findings and
direct repair regressions. A newly discovered blocker prevents `PASS`, creates
no budget, and may use only a remaining `C` wave.

One unchanged-candidate evidence rerun per ledger is allowed only within
existing execution/effects authority; it adds neither authority nor budget.
Before acting, record the candidate hash, stage, findings, scopes, and
transition. Keep one active plan and review path per work ID; revise in place.

After `C2`, an unresolved blocker requires human disposition: accept a real
residual risk, authorize an eligible canonical-equivalence correction, narrow
or materially change the scope, or cancel. A review cannot create a requirement
or reset a review budget.

### Canonical-equivalence correction

A canonical-equivalence correction is not residual-risk acceptance. It is a
human disposition for a cycle-2 `FAIL` whose only remaining P1 finding is that
the accepted contract rejects one representation of already accepted, frozen
input or output even though an exact mechanical transform can prove the same
meaning. It is eligible only when all of these facts are true:

- there is no P0, no other P1, and no concrete residual hazard to waive;
- the transform is total, deterministic, and bijective over an exact frozen
  inventory, with pre-transform and post-transform counts, order, identities,
  and SHA-256 values recorded;
- the accepted goal, data set, write boundary, commands, dependencies,
  thresholds, safety controls, external effects, and Definition of Done do not
  change; and
- all original containment and rejection controls remain effective.

For repository-relative paths, removing exactly one leading `./` may qualify
only after proving that every result remains a unique relative path beneath the
same fixed root. Absolute, drive-qualified, UNC, empty, `.`, `..`, additional
dot-prefixed, percent-decoded, reparse/symlink, and root-escaping paths remain
rejected. No other case, Unicode, separator, or textual rewriting is implied.

The human authorization must name the work ID, exact `C2` review and finding, the
exact transform, the frozen inventory identity, and the required proof checks.
Architecture may record that authorization as an in-place disposition addendum
and Implementation may execute only that correction. The `FAIL` remains part
of history; the disposition does not turn it into `PASS`, reset the work ID,
authorize review cycle 3, waive another finding, or permit autonomous repair.
Completion requires the recorded equivalence proof and every unchanged
acceptance check to pass.

## Completion and release boundary

Bounded work is complete when its Definition of Done and relevant regression
checks pass. Strict work is complete only after its required accepted review
gate. Changes under either installer package additionally require the
package tests, clean acceptance, regenerated release bindings, release
verification, and independent review required by `AGENTS.md` and
`docs/RELEASE.md` before publication.
