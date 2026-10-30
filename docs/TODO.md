# Deferred Yakherd Hardening

## Strict-review ledger validator

Add a small, standard-library-only validator for strict-review ledgers. It
should validate declared candidate hashes, `R0/C1/C2` transitions, correction
wave counts, stable finding IDs, recorded scopes, and terminal `PASS` or
`HUMAN_DISPOSITION_REQUIRED` state. It must not infer hazards or root causes,
run product code, access the network, create automation, or block adoption of
the finite review rule documented in `task_protocol.md`.
