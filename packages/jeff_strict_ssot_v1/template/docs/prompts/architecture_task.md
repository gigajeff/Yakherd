# Architecture Task Prompt

Read `AGENTS.md`, `SSOT.md`, `STATUS.md`, `DECISIONS.md`, all named evidence,
and the current product prompt provenance before deciding anything.

During team startup, report readiness and wait for bootstrap Red Team PASS. On
first product intake, follow `docs/prompts/product_intake.md` to preserve the
raw prompt and its provenance before extraction.

Apply the work-mode rules in `docs/task_protocol.md` to the authorized slice,
not hypothetical future scope. For bounded mode, produce only a concise brief
with one work ID, exact goal, write boundary, forbidden scope, and Definition
of Done; do not write an Architecture plan unless the human asks for one. The
human may approve that brief for direct Implementation.

For strict mode, maintain one active plan path using
`docs/templates/architecture_plan.md`. Keep it within the governance budget.
After a failed initial review, make at most one in-place revision addressing
only cited P0/P1 blockers. After a second `FAIL`, stop for the human choices in
the circuit breaker. Do not create version-suffixed candidate files or broaden
requirements to satisfy review.

Do not implement product code, install dependencies, access the network,
create automation, or silently change authority.

Write only the authorized plan/decision paths. Update an owner only when the
task has explicit authority to do so. End with one required repository marker.
