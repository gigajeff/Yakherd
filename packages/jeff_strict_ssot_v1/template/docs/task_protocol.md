# Five-Task Protocol

The five roles may be created together, but they do not become five concurrent
writers. In Codex, `docs/prompts/codex_team_launcher.md` creates five direct
role agents under one non-authoritative coordinator. Other environments may use
five long-lived role sessions.

| Role | Bootstrap state | Activation gate |
| --- | --- | --- |
| Architecture | waiting | bootstrap PASS plus product intake or a strict planning task |
| Implementation | parked | user-approved bounded brief or reviewed strict plan |
| Red Team | active for bootstrap review | bootstrap or strict review target and bounded write set |
| Temporary Branch | parked | approved named hypothesis and isolated branch/worktree |
| Governor | inactive | useful baseline plus separate human activation |

## Proportional Work Modes And Review Circuit Breaker

Every implementation slice has one stable work ID and exactly one mode:
`bounded` or `strict`.
Classify only the authorized slice, not hypothetical future features.

`bounded` is the default for reversible repository work when the user has
approved an exact goal, write boundary, forbidden scope, and Definition of
Done, and none of the strict triggers below is present. Ambiguity calls for one
concise human question; it does not authorize expanding the task.

`strict` is required for a slice that actually includes production release or
deployment, credentials or secrets, authentication or authorization,
destructive or difficult-to-reverse changes, personal or regulated data,
database or schema migration, external spending, safety/medical/legal/financial
behavior, installer or governance-core changes, or an explicit user request
for strict review.

Bounded mode needs no Architecture plan and no Red Team gate. Implementation
may proceed directly from the user-approved bounded brief. Verification is
limited to the Definition of Done and relevant regression checks. Structured
evidence is optional unless the user requests it or the slice promotes a
durable consequential claim.

Strict mode uses one active Architecture plan, structured evidence, and an
independent Red Team gate. The plan defaults to at most 240 lines and 32,768
UTF-8 bytes; a review defaults to at most 120 lines and 16,384 UTF-8 bytes.
Only the human may approve a larger governance budget.

Red Team verifies accepted requirements, the exact authorized boundary, the
exact diff, and material hazards introduced by that diff.
A missing enhancement outside accepted scope is not a finding.
Red Team cannot create
product requirements, broaden the threat model, prescribe unrelated controls,
or turn an advisory into an acceptance criterion. Every P1 finding cites the
accepted requirement or invariant it violates and exact evidence. P0 is
reserved for concrete imminent or actual irreversible harm, data loss, secret
exposure, or unauthorized external action. P1 means the accepted Definition of
Done is materially false. P2 and P3 are advisory. Only P0 and P1 block; a
review with only advisories is `PASS`. Verdicts are exactly `PASS` or `FAIL`.

For one work ID, Red Team gets one initial review and at most one recheck. The
initial review must consolidate all known blockers. The recheck verifies the
fixes and may add a blocker only for a regression introduced by those fixes or
a previously missed P0/P1; the latter must cite an accepted requirement and
explain why it was missed initially. Architecture may make one bounded
revision addressing only blocking findings.

After a second consecutive `FAIL`, all autonomous Architecture/Red Team
iteration stops. Ask the human to accept the risk, narrow or change the
requirements, or cancel the work. Do not create a third review, mint a new
work ID for the same goal, or continue by calling the same candidate V3. A
human decision that materially resets scope starts a new work ID and review
budget.

One work ID has one active plan path and one active review path. Revise those
files in place; Git history or explicitly authorized archival records preserve
history. Do not create `_v2`, `_v3`, or parallel candidate files merely to
continue a review cycle. A review report records findings.
It cannot itself create a new requirement or a fresh-review obligation.

## Architecture

Owns strict-mode plans, boundaries, gates, and accepted design changes. It may
also turn product intake into a concise bounded brief. It does not implement
product code. During startup it waits for bootstrap PASS. Product intake then
follows `docs/prompts/product_intake.md`.

## Implementation

Sole live writer for one authorized slice. Authorization is either a
user-approved bounded brief or a reviewed strict plan. It implements, tests,
records mode-appropriate evidence, promotes durable results, and updates
compact status. If neither authorization exists, it reports `parked` and
makes no edits.

## Red Team

Independently reviews the bootstrap gate and strict-mode targets. It does not
repair the work it reviews, add requirements, or gate bounded work. Findings
lead the report and obey the scope, severity, and two-review limits above.

## Temporary Branch

Runs one isolated hypothesis in a branch/worktree. Its output has no authority
until reviewed and deliberately merged. It must not silently modify current
owners or the main working tree.
It remains parked until a named hypothesis and isolation boundary are approved.

## Governor

Independent auditor, not builder or second SSOT. It owns only findings, risks,
audit reports, and audit state. It cannot authorize product work. It starts
inactive and follows `docs/governance/GOVERNOR_DELTA_POLICY.md` only after
separate activation approval.
Creation of its agent thread is not activation approval.
Governor output cannot reset a review budget, add product requirements, or
create a fresh-review obligation.

Never run two writers in one working tree. Architecture and Red Team may write
only their isolated output records within an explicit boundary.
