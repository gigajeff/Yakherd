# Five-Task Protocol

## Architecture

Owns plans, boundaries, gates, and accepted design changes. It may write only
bounded plan/decision records and does not implement product code.

## Implementation

Sole live writer for one authorized slice. It implements, tests, records
evidence, promotes durable results, and updates compact status.

## Red Team

Independently reviews requirements, behavior, evidence, risk, and the exact
diff. It does not repair the work it reviews. Findings lead the report.

## Temporary Branch

Runs one isolated hypothesis in a branch/worktree. Its output has no authority
until reviewed and deliberately merged. It must not silently modify current
owners or the main working tree.

## Governor

Independent auditor, not builder or second SSOT. It owns only findings, risks,
audit reports, and audit state. It cannot authorize product work. It starts
inactive and follows `docs/governance/GOVERNOR_DELTA_POLICY.md` only after
separate activation approval.

Never run two writers in one working tree. Architecture and Red Team may write
only their isolated output records within an explicit boundary.
