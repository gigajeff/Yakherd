# Product Master-Prompt Intake

This prompt is for the Architecture role after the bootstrap cold-resume review
passes. Receiving a product prompt does not authorize implementation.

## Preserve The Input

Treat only the text between `MASTER PROMPT START` and `MASTER PROMPT END` as the
product prompt. If delimiters are absent, ask the user to resend the prompt with
them. The raw prompt begins immediately after the newline ending the start
delimiter and ends immediately before the newline preceding the end delimiter;
exclude both delimiter lines and those two boundary newlines. Do not interpret
or write partial input.

Create a UTC run ID in `YYYYMMDDTHHMMSSZ` form and preserve:

- the prompt text, with no heading, wrapper, whitespace normalization, or
  commentary, at `docs/master_prompts/<RUN_ID>_product_prompt.txt`; and
- provenance at `docs/master_prompts/<RUN_ID>_product_prompt.provenance.json`.

The provenance record must contain exactly:

- `schema_version`: `1`;
- `received_utc`: the full UTC timestamp;
- `source`: a short description of the user-controlled chat input;
- `encoding`: `UTF-8`;
- `byte_length`: the byte length of the installed prompt file;
- `sha256`: lowercase SHA-256 of the installed prompt file; and
- `capture_limitations`: note that the hash binds the text delivered by the
  client to this agent, not keystrokes or bytes that the client did not expose.

Read the prompt back and verify the recorded byte length and SHA-256 before
extracting anything. Update the product-prompt entry in `SSOT.md` only through
an explicit decision that names the prior placeholder, the new raw prompt, and
the retained boundary that raw input is not executable authority.

## Extract Without Inventing

Using `docs/templates/architecture_plan.md`, extract requirements, users,
constraints, non-goals, unknowns, risks, acceptance gates, stop gates, and
proposed implementation stages. Preserve ambiguity and ask the user about any
choice that would materially change the product. Do not choose a language,
framework, dependency, service, data model, deployment target, or GitHub
visibility unless the prompt or a separate accepted decision supplies it.

Write only the authorized prompt/provenance, plan, decision, and affected owner
paths. Do not implement product code, install dependencies, use the network,
create automation, mutate Git, or activate Governor.

Send the raw prompt hash, extraction paths, owner changes, unresolved questions,
and exact diff to the Red Team role. Product intake becomes authoritative only
after independent Red Team PASS and required owner promotion.
