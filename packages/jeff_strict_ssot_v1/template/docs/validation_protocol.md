# Validation And Evidence Protocol

## Evidence Classes

- Protocol evidence: repository contract and validator consistency.
- Product evidence: behavior against accepted product requirements.
- Release evidence: deployable artifact and release-gate proof.
- Review evidence: independent assessment of named evidence and diff.

One class does not silently satisfy another.

## Structured Run Record

Each claimed test or completion has a JSON record containing:

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

Git/environment evidence is collected externally and recorded structurally.
