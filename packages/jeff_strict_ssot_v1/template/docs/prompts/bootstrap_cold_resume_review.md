# Bootstrap Cold-Resume Red Team Prompt

Use a fresh task with no bootstrap implementation chat.

Read all root owner files, `START_HERE.md`, `docs/GITHUB_SETUP.md`,
`docs/task_protocol.md`, validation/governance contracts, the five role prompts,
the Codex launcher, the product-intake prompt, package install manifest, and
validator tests.

Verify that a fresh reader can recover:

- the one-owner rule and authority map;
- current state, blockers, next action, forbidden actions, and archive state;
- accepted/superseded decision mechanics;
- all five task boundaries and single-writer rule;
- explicit creation of all five Codex role agents, their safe initial states,
  coordinator non-authority, and fail-closed handling of a missing role;
- evidence classes and done gate;
- pure-validator prohibitions;
- Governor inactive/delta behavior;
- transcript authority neutrality;
- Git/remote visibility boundary; and
- the human GitHub account/repository checkpoint and installer no-Git boundary;
- raw master-prompt delimiters, hash/byte-length provenance, and independent
  intake review; and
- the block on product implementation before reviewed intake.

Run the protocol/governor validators and tests exactly as listed in
`TESTING.md`, including Python's `-B` flag. Use `python -B` for every other
Python check in this review. Review install-manifest hashes, and fail if the
review creates any `__pycache__`, `.pyc`, or `.pyo` path.
Use one UTC run ID in `YYYYMMDDTHHMMSSZ` form for the whole review. The task may
write exactly these evidence paths, replacing `<RUN_ID>` with that ID:

- `docs/run_records/bootstrap_cold_resume_<RUN_ID>_protocol.json`;
- `docs/run_records/bootstrap_cold_resume_<RUN_ID>_governor.json`;
- `docs/run_records/bootstrap_cold_resume_<RUN_ID>_tests.json`;
- `docs/run_records/bootstrap_cold_resume_<RUN_ID>_manifest.json`; and
- `docs/run_records/bootstrap_cold_resume_<RUN_ID>_evidence_check.json`.

Each file must conform to `docs/templates/run_record.json`, name one bounded
claim, and contain the exact command and bounded output. After writing the
first four records, rerun the protocol validator with each record supplied by
a separate `--evidence` argument, then record that check in the fifth file and
inspect it against the same schema.

Do not edit or repair any other target file. Write one independent review at
`docs/reviews/bootstrap_cold_resume_<RUN_ID>.md`, lead with findings, link the
five run records, and state whether the cold-resume review passes. Product
intake remains a separately promoted next step even after a pass.

End with one required repository marker.
