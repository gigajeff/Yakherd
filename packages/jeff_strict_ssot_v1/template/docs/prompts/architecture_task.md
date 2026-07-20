# Architecture Task Prompt

Read `AGENTS.md`, `SSOT.md`, `STATUS.md`, `DECISIONS.md`, all named evidence,
and the current product prompt provenance before deciding anything.

Produce one bounded architecture plan using
`docs/templates/architecture_plan.md`. Define invariants, alternatives,
tradeoffs, implementation stages, evidence, acceptance gates, stop gates, and
forbidden scope. Do not implement product code, install dependencies, access
the network, create automation, or silently change authority.

Write only the authorized plan/decision paths. Update an owner only when the
task has explicit authority to do so. End with one required repository marker.
