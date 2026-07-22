# Governance

This directory owns governance findings, risks, audit state, and bounded
policies. It does not own product truth, architecture decisions, authorization,
or current project status.

- `OPEN_FINDINGS.md`: current audit findings only.
- `RISK_REGISTER.md`: current governance risks only.
- `AUDIT_STATE.json`: machine-readable Governor state.
- `STATUS_MAINTENANCE.md`: compact-status contract.
- `GOVERNOR_DELTA_POLICY.*`: reporting limits.
- `TRANSCRIPT_REVIEW_POLICY.md`: conditional transcript metadata rules.

Work modes, Red Team scope, and the review circuit breaker are product-work
boundaries owned by `../task_protocol.md`, not by the Governor.

The Governor begins inactive. No schedule or automation is created by this
bootstrap.
