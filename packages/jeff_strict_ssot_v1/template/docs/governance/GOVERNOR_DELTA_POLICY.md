# Governor Delta Policy

Status: installed but inactive pending separate human activation.

The Governor is an auditor, not a builder, scheduler, authorization source, or
second SSOT.

## Modes

- `quiet`: no material delta; at most 2 lines / 512 UTF-8 bytes; no governance
  write.
- `delta`: new/resolved/reopened/severity-changed/materially changed findings
  only; at most 120 lines / 16,384 UTF-8 bytes.
- `rebaseline`: broken continuity or explicit human authorization only; at
  most 240 lines / 32,768 UTF-8 bytes.

Unchanged findings are IDs and owner links only. A scheduled wakeup, if later
approved, is not permission to emit a material report.

## Activation And Utility

Activation requires separate human approval and a useful manual baseline.
Cadence changes require separate approval. A dated utility review must measure
new verified findings, resolutions, false/unsupported findings, repeated prose,
and maintenance time before continuation or expansion.

Machine-readable limits are in `GOVERNOR_DELTA_POLICY.json`.
