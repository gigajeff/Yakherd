# Product Master Prompts

Preserve received product intent byte-for-byte with provenance and SHA-256.
Receipt does not make a prompt project law. Architecture extracts requirements,
constraints, unknowns, and acceptance gates into owners; Red Team reviews that
extraction before implementation.

After bootstrap Red Team PASS, Architecture follows
`../prompts/product_intake.md`. Raw prompt text is stored as
`<RUN_ID>_product_prompt.txt` without a wrapper. Its
`<RUN_ID>_product_prompt.provenance.json` sidecar binds the UTF-8 byte length,
SHA-256, receipt time, source description, and client-capture limitation.

Never put access tokens, passwords, private keys, or other credentials in a
master prompt. GitHub account authorization is handled separately through
`../GITHUB_SETUP.md`.
