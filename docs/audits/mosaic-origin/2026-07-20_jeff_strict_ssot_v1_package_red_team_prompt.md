# Jeff Strict SSOT V1 Package Fresh Red Team Prompt

Date: 2026-07-20
Status: ready for a context-isolated review task

```text
Perform an independent Red Team review of Jeff Strict SSOT V1. Do not use the
implementation chat and do not ask the implementation task to explain choices.

READ

- AGENTS.md
- STATUS.md
- docs/2026-07-20_jeff_strict_ssot_package_and_crochet_splatomatic_plan.md
- docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_implementation.md
- packages/jeff_strict_ssot_v1/README.md
- packages/jeff_strict_ssot_v1/MANIFEST.json
- packages/jeff_strict_ssot_v1/bootstrap.py
- every file under packages/jeff_strict_ssot_v1/template/
- every file under packages/jeff_strict_ssot_v1/tests/
- test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v2/acceptance_record.json
- its seven logs and installed_repository fixture

BOUNDARY

This is read-only review except for one report. Do not repair package files,
modify STATUS/owners, activate automation, access the network, install
dependencies, run product commands, modify CROCHET/SPLATOMATIC, or mutate Git.

You may write only:

docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_review.md

REVIEW

1. Exact match to the authorized package tree and product-neutral scope.
2. Fresh install/dry-run determinism and fail-closed overwrite behavior.
3. Retrofit target, allowlist, reviewed-state, expected-hash, rollback, and
   install-record safety. Look specifically for path traversal, symlink/reparse
   escapes, partial writes, unauthorized files, and TOCTOU weaknesses.
4. Accuracy/completeness of package and installed hash manifests.
5. Bootstrap's standard-library/no-network/no-install/no-product/no-Git/no-
   automation boundary.
6. One-owner model, explicit decision supersession, compact status, archive,
   transcript, Governor, Git continuity, structured evidence, and done gate.
7. Five-task boundaries and single-writer rule.
8. Pure validator's bounded/read-only behavior and whether its checks can be
   bypassed or false-positive on ordinary repository content.
9. Status migration exact-byte preservation and hash-guarded rollback.
10. Positive and negative test adequacy, determinism, and write containment.
11. Empty bootstrap contains no fabricated product fact, transcript record,
    archive, active Governor, schedule, dependency, or technology choice.
12. Cold-resume: from the installed fixture only, recover all hard boundaries,
    current state, next authorization, and forbidden actions.
13. Confirm CROCHET and SPLATOMATIC remain untouched and unapproved.

Run safe bounded checks, including package tests and the generated validators/
tests if useful. Do not treat protocol success as product evidence.

OUTPUT

Lead with P0/P1/P2/P3 findings with exact file/line evidence. Then give verdict
`pass`, `pass_with_fixes`, or `fail`; exact required fixes; whether the package
may become current/usable; residual risks; and confirmation of the review
boundary. End with exactly one AGENTS.md result marker.
```
