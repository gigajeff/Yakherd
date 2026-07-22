# Product Master Prompts

Preserve received product intent byte-for-byte with provenance and SHA-256.
Receipt does not make a prompt project law. Architecture extracts requirements,
constraints, unknowns, and acceptance gates into owners; the human confirms
the resulting bounded brief or strict planning scope before implementation.

After bootstrap Red Team PASS, Architecture follows
`../prompts/product_intake.md`. Raw prompt text is stored as
`<RUN_ID>_product_prompt.txt` without a wrapper. Its
`<RUN_ID>_product_prompt.provenance.json` sidecar binds the UTF-8 byte length,
SHA-256, receipt time, source description, and client-capture limitation.

Product intake has no universal Red Team gate. After confirmation, bounded
work may proceed directly to Implementation. Strict work follows the bounded
plan/review cycle in `../task_protocol.md`.

Never put access tokens, passwords, private keys, or other credentials in a
master prompt. GitHub account authorization is handled separately through
`../GITHUB_SETUP.md`.
