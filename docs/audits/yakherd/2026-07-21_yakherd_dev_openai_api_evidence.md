# Yakherd.dev OpenAI API Design Evidence

- Retrieved: 2026-07-21
- Purpose: pre-Implementation verification for the concierge request contract
- Scope: official OpenAI documentation only; no authenticated API call and no
  secret was used
- Authority: evidence for Architecture and Red Team, not permission to implement,
  create a key, contact the API, deploy, or spend money

## Verified Current Facts

1. The current flagship model identifier is `gpt-5.6-sol`; `gpt-5.6` is its
   alias. The model page reports a 1,050,000-token context window, 128,000 maximum
   output tokens, Responses API support, Structured Outputs support, and current
   list pricing of $5 per million input tokens and $30 per million output tokens.
2. Current model guidance recommends the Responses API, supports `medium`
   reasoning effort, and asks applications serving individual users to send a
   stable privacy-preserving `safety_identifier`.
3. The Responses reference defines `text.format` with `type: json_schema`,
   `name`, `schema`, and `strict`; it defines `max_output_tokens` as including
   visible and reasoning tokens, `truncation: disabled` as fail-on-overflow, and
   response usage fields for input and output tokens. Input message roles include
   `developer`, `user`, and `assistant`, with text carried as `input_text` items.
4. `store: false` is a request setting, not a promise of no provider processing.
   Current data-control documentation says API data is not used for training by
   default unless the customer opts in, but default abuse-monitoring logs may
   contain prompts/responses and may be retained up to 30 days unless a customer
   is approved for Modified Abuse Monitoring or Zero Data Retention. The public
   concierge disclosure must say this plainly.
5. Current project monthly budgets are soft notification thresholds. Official
   project documentation explicitly says requests continue after the threshold;
   therefore Yakherd must not represent the provider budget as a hard cap.
6. API keys belong on the server, outside client code and source control. The
   website design consequently uses a dedicated restricted project key in a
   host-side file outside the web root.

## Official Sources

- GPT-5.6 Sol model:
  `https://developers.openai.com/api/docs/models/gpt-5.6-sol`
- Current model comparison and context/pricing:
  `https://developers.openai.com/api/docs/models/compare`
- Current GPT-5.6 model guidance:
  `https://developers.openai.com/api/docs/guides/latest-model`
- Responses API reference:
  `https://platform.openai.com/docs/api-reference/responses`
- Platform data controls and endpoint retention:
  `https://platform.openai.com/docs/models/default-usage-policies-by-endpoint`
- Project budgets, model usage, and key management:
  `https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform`
- API key safety:
  `https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety`

## Exact Architecture Consequences

- Use `POST https://api.openai.com/v1/responses` with the exact request envelope
  in the v3 website plan.
- Pin `gpt-5.6-sol`, `store: false`, `background: false`, `stream: false`,
  `truncation: disabled`, `reasoning.effort: medium`, `max_output_tokens: 1200`,
  `tools: []`, privacy-preserving `safety_identifier`, and strict
  `text.format.type: json_schema`.
- Treat provider usage fields as settlement evidence only after a completed,
  locally valid response. Reserve the full documented model context headroom
  before each call so hidden framing/schema overhead cannot make the local hard
  token ledger undercount.
- Treat project budgets as alerts only. Enforce the hard request/token boundary
  in the DreamHost relay and recheck current price/context/budget behavior at the
  provider-secret checkpoint.
- Tell visitors about default abuse-monitoring processing/retention and do not
  describe `store: false` as Zero Data Retention.

Any source change, documentation conflict, rejected authenticated schema probe,
model substitution, or unavailable project restriction returns the design to
Architecture and fresh Red Team review.
