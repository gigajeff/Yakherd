# Five-Task Protocol

The five roles may be created together, but they do not become five concurrent
writers. In Codex, `docs/prompts/codex_team_launcher.md` creates five direct
role agents under one non-authoritative coordinator. Other environments may use
five long-lived role sessions.

| Role | Bootstrap state | Activation gate |
| --- | --- | --- |
| Architecture | waiting | bootstrap Red Team PASS plus received master prompt |
| Implementation | parked | reviewed Architecture authorization for one slice |
| Red Team | active for bootstrap review | exact review target and bounded write set |
| Temporary Branch | parked | approved named hypothesis and isolated branch/worktree |
| Governor | inactive | useful baseline plus separate human activation |

## Architecture

Owns plans, boundaries, gates, and accepted design changes. It may write only
bounded plan/decision records and does not implement product code.
During startup it waits for bootstrap PASS. Product intake then follows
`docs/prompts/product_intake.md`.

## Implementation

Sole live writer for one authorized slice. It implements, tests, records
evidence, promotes durable results, and updates compact status.
If no reviewed slice exists, it reports `parked` and makes no edits.

## Red Team

Independently reviews requirements, behavior, evidence, risk, and the exact
diff. It does not repair the work it reviews. Findings lead the report.
It runs the bootstrap cold-resume review during team launch, then remains the
independent reviewer for product intake and later implementation slices.

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

Never run two writers in one working tree. Architecture and Red Team may write
only their isolated output records within an explicit boundary.
