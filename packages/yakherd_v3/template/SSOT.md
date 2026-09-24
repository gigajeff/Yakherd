# {{PROJECT_NAME}} single source of truth

## Mission and accepted requirements

Product requirements have not yet been supplied. Preserve the user's actual request here, or link one product specification when it is substantial.

## Stable technical invariants

No product-specific invariants have been accepted yet. Do not invent them.

## Current owners and authority

Subject to platform instructions, current human direction controls authority.
Read `AGENTS.md`, this file, `BASELINE.md`, `NOW.md`, then relevant executable
source/config/tests and linked evidence. An observed result can disprove a
summary: correct the affected owner rather than concealing the conflict.

- `AGENTS.md`: agent entry point and read order.
- `SSOT.md`: stable mission, requirements, invariants and operating rules.
- `BASELINE.md`: proven current facts, evidence, limitations and unknowns.
- `NOW.md`: sole active milestone, Definition of Done and next action.
- `README.md`: product setup, use and resume entry point.

Add a linked product specification or technical program only when useful;
assign each requirement to exactly one owner. History lives in Git and
preserved source/run artifacts. Historical prompts, plans, review verdicts,
status entries and numeric caps have no current authority unless deliberately
retained here or in the current objective/config. The adopted local owners
govern this project; upstream process changes do not apply automatically.

## Operating rules

One implementation task is the default. Work directly through authorized
reversible local implementation, tests and experiments. A clear human request
does not need another approval after being recorded in `NOW.md`. Research or
planning is a valid deliverable when requested; otherwise deliver working
artifacts and measured results. Do not create a roster of waiting agents,
bootstrap review gate, Governor, or authorization/review ledgers.

Use Architecture for a concrete design/experiment choice and independent
review for an actual diff, experiment, model or consequential claim. Follow
the environment's delegation rules. When helpers are authorized, give them
bounded useful tasks; keep one integration writer and one compute pipeline.
Reviewers do not repair their review target.

Only concrete accepted-requirement violations or correctness, scientific
validity, data-loss, security/privacy or unapproved-cost hazards block. A
finding identifies the artifact, evidence and smallest fix. Suggestions cannot
add requirements. Repair defects and recheck the affected behavior; reviews
do not require reviews of reviews. There is no universal review-count stop.
After two material fixes fail on the same issue, use a different technical
approach or discriminating diagnostic. Never weaken acceptance to declare
success. Missing required independent evidence blocks the dependent claim,
not unrelated safe work. Honor explicit task-specific budgets.

Ask for a real product/scope/risk decision or missing authority for a
destructive or hard-to-recover action, publication/deployment, remote Git
mutation, spending, credential access or private-data transfer. Reuse specific
existing authorization. Do not invent scope/compute caps. Platform permissions
still apply; a denial is not a new scientific rule. Preserve safety and
data-integrity constraints even when correcting stale documentation.

## Evidence and memory

Run relevant regression checks for changed behavior. Before meaningful
compute, record the question, controlled change, exact input/config identity,
expected output and decision rule. Use an experiment large enough to test the
claim and cheap enough to discriminate the live hypotheses.

Keep reproducible evidence, source provenance, decision rationale and useful
failed experiments with the fact's actual owner or linked artifacts. Distinguish
measured facts, hypotheses and unknowns. Synthetic tests do not establish field
performance; citations and process checks do not prove product correctness.
Consequential scientific claims need appropriate independent validation.

Replace superseded facts in `BASELINE.md` and rewrite `NOW.md` in place. Do not
append a status diary or make old transcripts required reading. On resume,
inspect the actual checkout, current changes, artifacts and interrupted work;
verify the mission, current state, blocker and next executable action from
repository files alone.

## Process hygiene and Git

Use one finite top-level local compute pipeline at a time, normal internal
parallelism and below-normal priority for heavy work. No unapproved persistent
processes, watchers or detached workers. Verify no task-owned descendants
remain; never kill unrelated work. Process ownership needs coherent PID,
creation time, executable path, command identity and a reliable task marker.
Incomplete records are warnings unless fresh evidence shows a concrete hazard.
Retain an existing applicable process broker/policy; these instructions alone
do not provide OS containment.

Preserve unrelated and uncommitted work. Inspect exact staged paths/diffs;
never use blind `git add .`. Keep secrets, raw datasets, generated runs, caches
and machine-local state out of commits unless specifically selected and
appropriate. Do not rewrite history, change remotes, publish or push without
authority. After meaningful Git work report branch, HEAD, upstream, dirty
state and ahead/behind.

## Milestone transitions

Finish only when `NOW.md`'s Definition of Done has artifact/evidence support.
Then update `BASELINE.md`, replace `NOW.md` with the next authorized objective,
and revise or retire the linked technical program. Do not carry obsolete
scope limits or permissions forward automatically. Archive completed role
tasks when applicable and authorized; new tasks resume from these files.
If no next scope is authorized, report completion rather than inventing work.

Process provenance: Yakherd 3.0 SSOT process, {{BOOTSTRAP_DATE}}. No external checkout is
required to interpret this repository's operating rules.
