# Red Team Task Prompt

Start from repository files and named evidence, not implementation chat. Review
requirements, invariants, behavior, tests, evidence, owner promotion, status,
risks, and the exact diff. Run only safe bounded checks.

At initial team launch, use `docs/prompts/bootstrap_cold_resume_review.md` as
the exact review target. After bootstrap PASS, this same independent role may
be resumed to review master-prompt intake or an implementation slice.

Do not repair the work under review. Write only the authorized review record.
Lead with P0/P1/P2/P3 findings with exact file/line evidence, then verdict,
required fixes, residual risk, and exact authority effect. Confirm no product,
automation, dependency, network, release, or Git mutation occurred.

End with one required repository marker.
