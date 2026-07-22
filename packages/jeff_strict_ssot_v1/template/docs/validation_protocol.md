# Validation And Evidence Protocol

## Evidence Classes

- Protocol evidence: repository contract and validator consistency.
- Product evidence: behavior against accepted product requirements.
- Release evidence: deployable artifact and release-gate proof.
- Review evidence: independent assessment of named evidence and diff.

One class does not silently satisfy another.

## Proportional Evidence

Bounded work may report the exact commands/checks run and their results
concisely in the task result and applicable owner. It does not need a JSON run
record unless the user requests one or the work promotes a durable
consequential product claim.

Strict work, release/deployment work, and consequential promoted claims use the
structured run record below. Evidence requirements cannot be enlarged merely
because a reviewer can imagine a future use outside the authorized slice.

## Structured Run Record

Each claim for which structured evidence is required has a JSON record
containing:

- schema version and evidence class;
- UTC timestamp and working directory;
- exact command and exit code;
- environment identity;
- supported claim;
- bounded stdout/stderr or exact raw-output paths;
- artifact paths and hashes;
- authority effect and limitations.

Use `docs/templates/run_record.json`. Chat and prose summaries cannot replace
the record.

## Pure Validator Boundary

`scripts/ssot/validate_protocol.py` is standard-library-only, bounded,
deterministic, and read-only. It does not import product modules, launch
subprocesses, access the network, invoke Git, install dependencies, inspect
bulky artifact trees, infer domain correctness, or write files.

Deterministic means its result depends only on repository bytes and explicit
arguments. It validates recorded timestamps structurally but never reads the
ambient wall clock. Time-based status policy belongs in separately authorized
governance or review work with an explicit reference time.

Git/environment evidence is collected externally and recorded structurally.
