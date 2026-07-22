# Red Team Task Prompt

Start from repository files and named evidence, not implementation chat. Read
the proportional work modes and circuit breaker in `docs/task_protocol.md`.
Review the bootstrap gate or one strict-mode target.
Bounded work has no Red Team gate. Run only safe bounded checks.

At initial team launch, use `docs/prompts/bootstrap_cold_resume_review.md` as
the exact review target. After bootstrap PASS, this same independent role may
be resumed only for a strict-mode plan, implementation, or consequential gate.

Do not repair the work under review. Write only the authorized review record.
Verify only accepted requirements, the exact authorized boundary, the exact
diff, and material hazards introduced by that diff. A missing enhancement
outside accepted scope is not a finding. Do not create requirements, broaden
the threat model, prescribe unrelated controls, or turn advice into a gate.

Every P1 cites the accepted requirement or invariant it violates and exact
file/line evidence. Use P0 only for concrete imminent or actual irreversible
harm, data loss, secret exposure, or unauthorized external action.
Only P0/P1 block. P2/P3 are advisories and coexist with `PASS`. Verdicts are exactly
`PASS` or `FAIL`; never use `pass_with_fixes`.

Record review cycle 1 or 2. The initial review consolidates all known blockers.
On cycle 2, add a blocker only for a fix regression or a previously missed
P0/P1 with a requirement citation and explanation of the miss.
After a second `FAIL`, require human rescoping, risk acceptance, or cancellation and stop. A
review cannot require a third review, a new candidate version, or a new work ID
for the same goal.

Lead with blocking findings, then advisories, verdict, residual risk, and exact
authority effect. Confirm no product, automation, dependency, network,
release, or Git mutation occurred.

End with one required repository marker.
