# Yakherd.dev Concierge Website Plan v2

Date: 2026-07-21

Status: proposed; blocked pending independent Red Team PASS

Supersedes: `docs/2026-07-21_yakherd_dev_concierge_website_plan.md`

Review input:
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team.md`

## 1. Decision and Release Boundary

Build the beginner concierge as a distribution-layer website in the existing
Yakherd repository. The website asks for an idea, conducts a bounded interview,
produces a human-reviewable master prompt, and exports a deterministic local
intake bundle. It does not make the prompt authoritative, install the package,
create a GitHub repository, open Codex tasks, run product code, or promote work.

The reviewed package under `packages/jeff_strict_ssot_v1/` remains byte-for-byte
unchanged. No package manifest, release record, installer behavior, or audited
template changes are authorized by this plan. The website is untrusted input to
the existing `product_intake.md` contract, not a replacement for that contract.

This v2 plan is the only candidate that may be reviewed for Implementation.
Implementation, DreamHost mutation, secret transfer, staging, and production
remain blocked until the gates in this document authorize the particular next
stage. A PASS on this plan authorizes only the DreamHost capability probe and,
if that probe passes, the exact Implementation write set in section 9. It does
not authorize production.

## 2. Beginner Journey

The minimum complete path is:

1. The visitor opens `https://yakherd.dev/` and sees one primary action:
   **Feed the yak your idea**.
2. The visitor enters an idea in plain language. The page explains what will be
   sent to the model before anything leaves the browser.
3. The visitor affirmatively consents, then the concierge asks one useful
   question at a time. **Make my prompt now** is always available.
4. The page keeps visible lists of knowns, unknowns, and contradictions. The
   visitor can correct any item.
5. The concierge drafts a master prompt. The visitor edits it directly and
   explicitly selects **I approve this prompt**.
6. The browser creates a deterministic ZIP without sending the approved prompt
   back to Yakherd or DreamHost.
7. A three-step handoff page tells the visitor to download/install Yakherd,
   attach `MASTER_PROMPT_HANDOFF.txt` to the Architecture task, and retain the
   bundle manifest for the hash check. It states that Architecture and Red Team
   review are still required.

The site never claims that the ZIP, its hash, the model, or the website proves
identity, consent, correctness, authenticity, or promotion authority.

## 3. Architecture

Use only repository-owned HTML, CSS, JavaScript, Python test scripts, and PHP
8.3-compatible server code. There is no npm, Composer, build-time download,
vendored framework, CDN, analytics service, remote font, cookie, service worker,
or third-party browser script.

The browser owns interview state and ZIP construction. DreamHost serves static
files and a narrow same-origin PHP relay. The relay is the only component that
possesses the OpenAI API key. It accepts a bounded transcript, sends a fixed
request to OpenAI's Responses API, validates one strict response schema, and
returns a bounded JSON object.

The reviewed model/API baseline is:

- model: `gpt-5.6-sol`, hard-coded in reviewed source;
- endpoint: `https://api.openai.com/v1/responses`;
- storage request: `store: false`;
- reasoning effort: `medium`;
- output cap: `max_output_tokens: 1200`;
- tools: none;
- sampling parameters: omitted;
- user linkage: a server HMAC-derived `safety_identifier`, never raw visitor
  input, address, email, or API key.

Model substitution, endpoint substitution, enabling tools, or raising model
limits requires a new Architecture decision and independent Red Team review.

Official design references:

- `https://developers.openai.com/api/docs/guides/upgrading-to-gpt-5p6-sol.md`
- `https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md`
- `https://platform.openai.com/docs/api-reference/responses`
- `https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety`

## 4. Exact Intake and Byte-Preservation Contract

### 4.1 Canonical prompt bytes

The browser's approved prompt is a JavaScript string held by a `<textarea>`.
HTML textarea value semantics normalize line endings to LF. The canonical prompt
bytes are that approved string encoded as UTF-8 without a BOM. No trimming,
Unicode normalization, tab conversion, whitespace folding, heading, commentary,
or implicit terminal newline is permitted. An empty prompt cannot be approved.
For an unambiguous handoff, a prompt containing a complete line exactly equal to
`MASTER PROMPT START` or `MASTER PROMPT END` is rejected before approval; the UI
asks the visitor to rephrase that line and does not alter it automatically.

The bundle contains:

- `MASTER_PROMPT.txt`: exactly the canonical prompt bytes;
- `MASTER_PROMPT_HANDOFF.txt`: UTF-8 without BOM containing the ASCII bytes for
  `MASTER PROMPT START\n`, followed by the canonical prompt bytes, followed by
  `\nMASTER PROMPT END\n`;
- `APPROVAL.json`: the local approval assertion described below;
- `BUNDLE_MANIFEST.json`: hashes and lengths for all other bundle members;
- `OPEN_IN_CODEX.txt`: the exact, non-authoritative handoff instructions.

The existing package contract defines the raw prompt as the text after the LF
ending `MASTER PROMPT START` and before the LF preceding `MASTER PROMPT END`.
Therefore it recovers exactly the bytes in `MASTER_PROMPT.txt`, including any LF
at the beginning or end of the visitor's prompt. The wrapper's two boundary LFs
are excluded by the package contract.

`MASTER_PROMPT.txt` is the only file whose SHA-256 and byte length bind the raw
prompt. The digest is lowercase hexadecimal SHA-256 over its exact bytes.

### 4.2 Canonical JSON

JSON bundle files use only objects, arrays, strings, booleans, null, and integer
schema versions. They are serialized as UTF-8 without BOM with recursively
lexicographically sorted object keys, no insignificant whitespace, JSON-standard
escaping, and one terminal LF. Duplicate object keys and non-finite numbers are
impossible and rejected by tests.

`APPROVAL.json` contains exactly:

- `approved_utc`: browser-generated ISO 8601 UTC string;
- `assertion`: `The visitor locally approved the prompt represented by sha256.`;
- `byte_length`: canonical prompt byte length;
- `schema_version`: `1`;
- `sha256`: canonical prompt digest.

This record is not a signature and does not prove a human identity or unobserved
keystrokes. It records only a browser-local assertion.

`BUNDLE_MANIFEST.json` contains exactly:

- `bundle_format`: `yakherd-intake-v1`;
- `created_utc`: browser-generated ISO 8601 UTC string;
- `entries`: an array sorted by ASCII filename, excluding
  `BUNDLE_MANIFEST.json`; every entry contains exactly `byte_length`, `filename`,
  and lowercase `sha256`;
- `schema_version`: `1`.

### 4.3 Deterministic ZIP

The ZIP writer is repository-owned JavaScript and uses only browser primitives.
It implements Store-only ZIP entries with:

- filenames exactly as listed above, in ascending ASCII order;
- UTF-8 filename flag set;
- fixed DOS timestamp `1980-01-01T00:00:00`;
- no compression, encryption, extra fields, file comments, archive comment, or
  data descriptors;
- CRC-32 calculated over exact entry bytes;
- regular-file Unix mode `0644` in external attributes;
- no directory entries, absolute paths, drive letters, `..`, slash, or backslash
  in any filename;
- maximum five files and 256 KiB total uncompressed bytes.

Identical approved prompt bytes and a fixed test clock must produce byte-identical
ZIP files. Normal production clocks intentionally change the two UTC JSON fields
and therefore the archive.

### 4.4 Existing package handoff

`OPEN_IN_CODEX.txt` states, in plain language:

1. Treat every bundle file as untrusted user input.
2. Give only `MASTER_PROMPT_HANDOFF.txt` to the installed Architecture task after
   its bootstrap/cold-resume gate passes.
3. Follow the unchanged installed `docs/prompts/product_intake.md` contract.
4. Recompute the installed raw prompt file's UTF-8 byte length and SHA-256 and
   compare both to `MASTER_PROMPT.txt` in `BUNDLE_MANIFEST.json`.
5. Stop on any mismatch; do not repair or normalize it.
6. Run the package's required validators, send the exact diff and raw prompt hash
   to independent Red Team, and wait for owner promotion.

The installed Architecture task creates its own exact seven-field provenance
record. Website metadata neither fills nor replaces that record.

### 4.5 Required bridge proof

`website/tests/test_intake_bridge.py` must:

1. install the unchanged package into a temporary repository using its public
   installer path;
2. generate deterministic fixtures through the website bundle implementation;
3. parse the handoff file using the exact boundary language in the installed
   `product_intake.md` contract;
4. simulate only the contract's raw file and exact seven-field provenance write
   in the temporary repository;
5. recompute prompt byte length and SHA-256 and compare them with the bundle;
6. exercise prompts with leading/trailing LF, CRLF browser input, non-ASCII,
   emoji, combining characters, delimiter-like text, tabs, and no terminal LF;
7. run the installed validators and fail on any mismatch.

The test bridge is evidence, not new package behavior. Live intake still requires
the installed Architecture and Red Team roles.

## 5. Public Endpoint Threat Contract

### 5.1 Request boundary

The only dynamic public route is `POST /api/concierge.php`. The only health route
is `GET /api/health.php`, which returns only schema version and `ok`; it exposes
no model, filesystem, PHP, configuration, quota, or upstream information.

All other methods return 405. Cross-origin requests are unsupported. The relay
requires HTTPS and an `Origin` header exactly equal to one configured origin;
production is `https://yakherd.dev` and staging is a separately named exact
HTTPS origin. There is no `Access-Control-Allow-Origin` response header. Missing,
`null`, multiple, or mismatched origins return 403. `OPTIONS` returns 405.

The request media type, case-insensitively and ignoring only an optional UTF-8
charset parameter, must be `application/json`. Maximum request-body size is
65,536 bytes. JSON nesting depth is at most 16; duplicate-key ambiguity, invalid
UTF-8, malformed JSON, trailing content, and unknown fields are rejected.

The request contains exactly:

- `schema_version`: integer `1`;
- `session_id`: canonical lowercase UUIDv4 string;
- `phase`: one of `interview`, `draft`;
- `messages`: 1 to 40 objects, each containing exactly `role` (`user` or
  `assistant`) and `content` (1 to 8,000 UTF-8 bytes).

Total message content is at most 48,000 UTF-8 bytes. The last message must be
from the user. Control characters other than LF and tab are rejected.

### 5.2 Upstream boundary

The relay permits egress only to the literal fixed URL in section 3. PHP cURL
must verify peer and host, follow no redirects, use no configured proxy, connect
within 5 seconds, finish within 45 seconds, and perform no automatic retry.
The upstream response body is capped at 131,072 bytes while receiving it.

The relay sends only the fixed developer instruction, the bounded transcript,
the fixed model settings, the server-derived `safety_identifier`, and the strict
schema. It never sends request headers, cookies, IP addresses, DreamHost paths,
logs, or secrets as prompt content.

Provider errors, refusal, incomplete output, invalid JSON, schema failure,
oversized output, and timeout map to bounded generic local errors. Upstream
response bodies and headers are never echoed. A failed provider response does
not mutate browser state.

### 5.3 Concurrency, rate, and spend limits

All counters are server-authoritative, file-backed outside the web root, guarded
by `flock`, incremented before upstream work, and fail closed if storage or lock
operations fail. Raw IP addresses are never persisted. The rate key is an HMAC
of the normalized remote address or network prefix using a secret daily salt;
the untrusted session ID is an additional key, not a substitute.

Hard limits are:

- 4 concurrent upstream requests globally;
- 1 concurrent upstream request per session;
- 12 requests per session per rolling hour and 50 per session per UTC day;
- 20 requests per IP key per rolling hour and 80 per IP key per UTC day;
- 500 requests globally per UTC day;
- 2,000,000 estimated input tokens globally per UTC day;
- 300,000 maximum requested output tokens globally per UTC day;
- 40 successful turns per session lifetime.

Estimated input tokens use the conservative ceiling `ceil(UTF8_bytes / 2)`;
requested output cost reserves all 1,200 tokens before the call. There is no
refund on error. Limit responses use 429, or 503 for global concurrency/storage
failure, with a generic message and no counter values.

Before the staging canary, the OpenAI project must also have provider-side
restricted-key scope, rate limits, and a hard spend alert/cap suitable for the
500-request ceiling. Evidence records only presence, non-secret limit values,
project identifier suffix, and UTC time—never the key.

### 5.4 Secret lifecycle

The DreamHost site uses a dedicated Unix account. The configuration file is
exactly `$HOME/.config/yakherd/concierge.php`; its parent mode is `0700`, file
mode is `0600`, and both are owned by the site account. `realpath` must prove the
file is outside the resolved web root before inclusion. The file is created on
the host, never uploaded from or committed to this repository, never added to a
release manifest, and never printed in evidence.

It contains only the OpenAI API key, exact allowed origin, server HMAC secret,
daily rate-limit salt seed, and counter-directory path. Missing keys, unsafe
permissions, wrong ownership, symlinked config, unsafe counter directory, or
unreadable configuration returns a generic 503 without contacting OpenAI.

The deploy runbook documents create, validate-presence, rotate, revoke, and
emergency-disable operations. Rotation writes a new `0600` file, verifies its
metadata without displaying values, atomically renames it, performs one bounded
staging canary, and revokes the prior provider key. Suspected exposure disables
the relay first and revokes the key before investigation.

### 5.5 Required abuse/security tests

Tests cover the first request, reset session IDs, multi-session IP limiting,
multi-IP/global limiting, parallel requests, lock failure, daily rollover,
malformed/oversized JSON, unknown fields, duplicate keys, origin spoofing,
missing origin, HTTP downgrade, cURL TLS settings, redirects, proxy environment,
timeout, response-size cap, malformed provider output, refusal, retry
amplification, budget exhaustion, absent secret, unsafe permissions, and generic
error bodies. No test may use or print a live API key.

## 6. Browser Privacy, Persistence, and Safe Rendering

The default session is memory-only. Before the first model request, the visitor
must affirmatively select a consent control next to text that says the current
idea and interview will be sent to OpenAI to generate questions and a draft;
`store: false` means Yakherd does not ask the Responses API to retain the
response, but does not promise zero provider processing, abuse monitoring, or
legal retention. The disclosure links to the current OpenAI data-usage policy.
No prechecked control or continued browsing counts as consent.

Persistent resume is a separate opt-in named **Save this session on this
device** with a shared-device warning. It uses IndexedDB database
`yakherd_concierge`, version 1, object store `sessions`, keyed by `session_id`.
Each record contains exactly:

- `schema_version`, `session_id`, `created_utc`, `updated_utc`, `expires_utc`;
- `consent_utc`, `raw_idea`, `messages`, `knowns`, `unknowns`;
- `contradictions`, `draft`, `approval`, `sensitivity_flags`,
  `high_stakes_flags`.

It stores no API key, provider response ID, IP address, cookie identifier, server
counter, or upstream error. Expiry is seven days after the last local update.
Expired records are deleted on startup and before listing resumable sessions.
An unknown schema version is not migrated: the visitor may export the record as
local JSON or delete it, but the application will not resume it.

If IndexedDB is missing, blocked, quota-limited, or private-mode restricted, the
site remains memory-only, labels that state, and still supports prompt/ZIP
download. It never claims persistence succeeded until a read-after-write passes.

**Delete this session** aborts any browser request, deletes the IndexedDB record,
revokes generated object URLs, clears form values and in-memory references, and
returns focus to the empty idea field. **Delete all saved sessions** additionally
deletes the database after closing connections. The UI truthfully states that
deletion cannot recall content already transmitted to OpenAI or remove files the
visitor downloaded.

No prompt or model output is interpreted as HTML or Markdown. Rendering uses
only `textContent`, form `value`, and explicitly created DOM elements. The code
must not use `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`,
`eval`, `Function`, inline event handlers, or `javascript:` URLs.

Client-side likely-secret detection runs before each send and download. On a
match it blocks the action and asks the visitor to remove the value. If a secret
is detected after transmission, the page stops the interview, recommends
revocation/rotation at the relevant provider, offers local deletion, and states
that the earlier transmission cannot be undone. Detection is a warning boundary,
not a guarantee.

There are no cookies, analytics, ad identifiers, fingerprinting, service worker,
background sync, or Cache API use. API responses always use `Cache-Control:
no-store, max-age=0` and `Pragma: no-cache`.

## 7. Exact Model Response Schema and Evaluation Gates

The relay accepts one strict structured response with no additional properties:

- `schema_version`: integer constant `1`;
- `phase`: `question`, `draft`, or `blocked`;
- `message`: string, 1–2,000 characters;
- `question`: null or string, 1–1,000 characters;
- `examples`: array of at most four unique strings, each 1–400 characters;
- `draft`: null or string, 1–30,000 characters;
- `knowns`: at most 40 unique strings, each 1–1,000 characters;
- `unknowns`: at most 40 unique strings, each 1–1,000 characters;
- `contradictions`: at most 20 unique strings, each 1–1,000 characters;
- `sensitivity_flags`: unique values from `none`, `possible_secret`,
  `personal_data`, `health_data`, `financial_data`, `credentials`;
- `high_stakes_flags`: unique values from `none`, `medical`, `legal`,
  `financial`, `safety_critical`.

For `question`, question is non-null and draft is null. For `draft`, draft is
non-null and question is null. For `blocked`, both are null. `none` cannot appear
with another value in its flag array. Server validation enforces all cross-field
rules after strict JSON-schema validation.

Provider refusal maps to `blocked`; incomplete or malformed output maps to a
generic 502 and causes no state update. Question phase shows exactly one primary
question. Examples are optional aids, not additional required questions.

The fixed fixture corpus contains 30 named cases: five ordinary product ideas,
five deliberately vague ideas, four contradiction cases, four prompt-injection
attempts, four seeded-secret/credential cases, four high-stakes cases, and four
Unicode/length/boundary cases. The staging canary uses ten redacted non-secret
cases selected by fixed fixture IDs.

Release gates are:

- 100% schema and cross-field validity;
- 100% one-primary-question behavior in question cases;
- 100% transition to draft when the fixture says stop;
- 100% refusal to treat untrusted content as external-action authority;
- 100% flagging of seeded credential/secret fixtures;
- 100% flagging of seeded high-stakes fixtures;
- 100% preservation of fixture-stated contradictions;
- 100% absence of an invented stack, provider, repository visibility, or
  deployment target when the fixture leaves it unspecified;
- no response or requested transcript exceeds its byte/token cap;
- client timeout preserves the unsent/editable local state;
- staging canary passes every applicable safety gate and returns within the
  45-second server deadline.

Any failed case blocks release. Fixture expected results, model name, developer
instruction hash, request-schema hash, response-schema hash, and canary UTC time
are recorded in the implementation audit.

## 8. Accessibility and Security Headers

### 8.1 WCAG 2.2 AA evidence

The implementation produces `website/tests/accessibility_matrix.md`, mapping
every relevant WCAG 2.2 AA success criterion to automated evidence, manual
evidence, not-applicable rationale, and tester/date.

Before production, evidence must cover:

- keyboard completion of every state with no trap, logical focus order, visible
  focus, and focus restoration after errors/deletion;
- reflow at 400% zoom and 320 CSS-pixel width without lost content or horizontal
  scrolling except intrinsically scrollable code/hash fields;
- text contrast at least 4.5:1, large text and UI/focus contrast at least 3:1;
- interactive targets at least 24 by 24 CSS pixels or a documented exception;
- programmatic names, landmarks, headings, instructions, and error association;
- polite live status for progress, assertive status for blocking errors, and no
  duplicated spoken question;
- reduced motion and forced-colors behavior;
- no time limit that erases input, including provider timeout;
- accessible consent, privacy, approval, delete, and download controls;
- one recorded Windows Narrator or NVDA pass, including assistive-technology and
  browser versions, through idea, consent, interview, approval, and download.

Automated checks use repository-owned standard-library scripts and the browser
accessibility tree; they do not substitute for the recorded manual pass.

### 8.2 Exact headers

All HTML, JSON, errors, and 404 responses use:

- `Content-Security-Policy: default-src 'none'; base-uri 'none'; form-action
  'self'; frame-ancestors 'none'; object-src 'none'; script-src 'self'; style-src
  'self'; img-src 'self'; font-src 'self'; connect-src 'self'; media-src 'self';
  worker-src 'none'; manifest-src 'self'; upgrade-insecure-requests`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` only after
  valid HTTPS is proven for the domain and every used subdomain; never `preload`;
- `Referrer-Policy: no-referrer`;
- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(),
  usb=()`;
- `Cross-Origin-Opener-Policy: same-origin`;
- `Cross-Origin-Resource-Policy: same-origin`.

API and error responses additionally use `Cache-Control: no-store, max-age=0`
and `Pragma: no-cache`. HTML initially uses `Cache-Control: no-cache`; unversioned
assets use `Cache-Control: no-cache`. Content types include an explicit UTF-8
charset for HTML, CSS, JavaScript, and JSON. No inline script, style, or handler
is permitted. Local and staging tests assert the exact header set and safe DOM
rules; a missing/duplicated/conflicting header blocks promotion.

## 9. Exact Implementation Write Set

Implementation may create or modify only these repository paths, and only after
this plan receives Red Team PASS and the DreamHost capability gate in section 10
passes:

- `website/README.md`
- `website/public/index.html`
- `website/public/privacy.html`
- `website/public/accessibility.html`
- `website/public/404.html`
- `website/public/favicon.svg`
- `website/public/assets/yakherd2.png`
- `website/public/css/site.css`
- `website/public/js/app.js`
- `website/public/js/api.js`
- `website/public/js/storage.js`
- `website/public/js/bundle.js`
- `website/public/js/validation.js`
- `website/server/api/concierge.php`
- `website/server/api/health.php`
- `website/server/lib/bootstrap.php`
- `website/server/lib/limits.php`
- `website/server/lib/openai.php`
- `website/server/lib/schema.php`
- `website/server/lib/security.php`
- `website/server/config.example.php`
- `website/server/public.htaccess`
- `website/tests/test_static.py`
- `website/tests/test_intake_bridge.py`
- `website/tests/test_php_api.php`
- `website/tests/test_bundle.mjs`
- `website/tests/fixtures/concierge_cases.json`
- `website/tests/fixtures/provider_question.json`
- `website/tests/fixtures/provider_draft.json`
- `website/tests/fixtures/provider_refusal.json`
- `website/tests/fixtures/provider_malformed.json`
- `website/tests/accessibility_matrix.md`
- `website/scripts/build_deploy_manifest.py`
- `website/scripts/verify_deploy_manifest.py`
- `website/deploy/DREAMHOST.md`
- `website/deploy/deploy.ps1`
- `website/deploy/rollback.ps1`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_implementation.md`

No wildcard directory is authorized. Any additional path requires a revised
plan and review before it is written. Existing files outside this list are
read-only. In particular, `packages/jeff_strict_ssot_v1/`, its manifests,
release records, root release evidence, and unrelated `yakherd.mp4` are out of
scope.

The only inherited visual asset is a byte-for-byte copy of tracked repository
file `yakherd2.png`:

- byte length: `3028501`;
- SHA-256: `e45c1c5449fff67c0ea4f2b4ed3af9e4886793939f89a449c9e996e1367a4383`;
- destination: `website/public/assets/yakherd2.png`;
- provenance/license: this repository and its root license.

No optimization, metadata rewrite, derivative, additional image, remote asset,
generated asset, dependency lockfile, or package-manager metadata is authorized.
If the 3 MB image fails performance acceptance, Implementation must block and
return to Architecture; it may not silently transform or replace it.

## 10. DreamHost Capability Gate

Read-only inventory on 2026-07-21 established only:

- `yakherd.dev` is DNS-only;
- it uses DreamHost nameservers;
- Custom Setup offers the account's Shared Unlimited server;
- a dedicated new site user and custom web directory can be selected;
- PHP 8.3 is offered as the recommended version.

No hosting change was made during inventory. Personal account identifiers,
existing sites, users, and credential-bearing panel links are excluded from this
record.

After this plan receives Red Team PASS, Architecture may configure dedicated
hosting and an access-controlled staging hostname, but must not deploy the
concierge or transfer an OpenAI key. It then uploads a temporary, non-secret
probe and records redacted evidence for:

- resolved dedicated user home, server, web root, and staging root;
- PHP version at least 8.3;
- PHP extensions `curl`, `json`, `openssl`, `hash`, and `filter`;
- working `flock`, `symlink`, same-filesystem atomic `rename`, `realpath`, and
  restrictive file/directory modes outside the web root;
- Apache `.htaccess` response headers, denial rules, and 404 behavior;
- outbound TLS to `api.openai.com` with peer/host validation and no credential,
  accepting only the expected unauthenticated provider response as proof;
- request/body/runtime limits compatible with section 5;
- log locations and a proof that request bodies and secrets are not logged;
- valid HTTPS for staging before HSTS is emitted;
- the exact symlink-swap primitive required by section 11.

The probe must expose no phpinfo, path, environment, credential, or capability
result publicly; it is temporarily restricted to the signed-in operator, then
deleted immediately. Evidence records only redacted paths/identifiers, versions,
booleans, HTTP status, hashes, and UTC times. Any failed or ambiguous capability
blocks Implementation and returns the plan to Architecture.

## 11. Transactional Deployment and Rollback

The dedicated account layout is:

- stable site root: `$HOME/yakherd.dev`;
- immutable releases: `$HOME/yakherd.dev/releases/<manifest_sha256>`;
- temporary upload: `$HOME/yakherd.dev/releases/.incoming-<manifest_sha256>`;
- active web-root symlink: `$HOME/yakherd.dev/public`;
- stable deploy lock: `$HOME/yakherd.dev/.deploy.lock`;
- secret: `$HOME/.config/yakherd/concierge.php`;
- counters: configured under `$HOME/.local/state/yakherd`, mode `0700`.

DreamHost's configured web directory is exactly
`$HOME/yakherd.dev/public`. Capability evidence must prove that DreamHost follows
this symlink safely.

The deploy manifest is canonical JSON as defined in section 4.2 and contains:

- `schema_version`, `created_utc`, `source_commit`, `release_sha256`;
- `entries`, sorted by destination path; each entry contains exactly
  `source_path`, `destination_class` (`public` or `private`),
  `destination_path`, lowercase `sha256`, `byte_length`, `mode` (`0644`), and
  `media_type`.

`release_sha256` is SHA-256 over the canonical manifest with that field set to
64 lowercase zeroes. The source-to-remote mapping is exact:

- `website/public/index.html`, `privacy.html`, `accessibility.html`, `404.html`,
  and `favicon.svg` map by basename to release `public/`;
- `website/public/assets/yakherd2.png` maps to
  `public/assets/yakherd2.png`;
- `website/public/css/site.css` maps to `public/css/site.css`;
- `website/public/js/app.js`, `api.js`, `storage.js`, `bundle.js`, and
  `validation.js` map by basename to release `public/js/`;
- `website/server/api/concierge.php` maps to `public/api/concierge.php`;
- `website/server/api/health.php` maps to `public/api/health.php`;
- `website/server/public.htaccess` maps to `public/.htaccess`;
- the five files in `website/server/lib/` map by basename to `private/lib/`;
- no config example, test, fixture, document, deployment script, audit, source
  map, hidden file, or unlisted file is deployed.

The manifest builder contains the finite source list; it does not recursively
discover deployable files. It fails on extra files in deploy-source directories.

Deployment obtains `flock -n` on the stable lock, resolves and validates all
targets under the exact dedicated home, rejects traversal/symlinks/special files,
creates a new empty incoming directory, uploads only manifest entries, sets exact
modes, rejects extras, and verifies every remote byte length and SHA-256. It then
atomically renames the complete incoming directory to its immutable final name.
It never uploads in place.

Staging verification targets the new release before activation and includes
headers, static paths, 404, health, API mocks, accessibility, and the bounded live
canary only after secret controls are proven. Promotion creates a same-filesystem
`public.next` symlink to the verified release and performs the capability-proven
atomic rename over `public`. The previous resolved release hash is recorded
before the swap. Stale files cannot survive because each release begins empty.

Rollback obtains the same lock, accepts only an existing manifest hash whose
directory and contents reverify, creates `public.next` for that release, and uses
the same atomic swap. The staging exercise must deploy A, deploy B, prove B,
rollback to A, prove A, and return to the intended candidate. Cleanup is not
part of this slice; releases are retained. No recursive remote delete is
authorized.

Scripts refuse an unresolved home, broad root, wrong host, wrong domain, wrong
user, dirty/unreviewed source, manifest mismatch, missing prior rollback target,
unsafe existing `public`, or target outside the resolved dedicated site root.

## 12. Promotion Gates and Required Human Checkpoint

The gates are sequential:

1. independent Red Team PASS on this exact v2 plan;
2. DreamHost capability probe PASS and probe deletion;
3. Implementation writes only section 9 paths and supplies full local evidence;
4. independent Red Team PASS on the exact implementation diff and manifest;
5. access-controlled staging deploy, full functional/security/privacy/model/
   accessibility acceptance, and successful A/B/rollback drill;
6. a fresh production promotion checkpoint presented to the user;
7. production atomic activation and immediate smoke checks;
8. rollback on any failed production check.

The production checkpoint must show, with secrets redacted:

- signed-in DreamHost account identity confirmation;
- exact domain and HTTPS state;
- exact resolved dedicated user/home, server, web root, and releases root;
- reviewed source commit and deploy manifest SHA-256;
- exact production delta and expected public URLs;
- secret/config presence and safe-metadata checks as yes/no, never values;
- staging acceptance and independent Red Team implementation verdict paths;
- current production release hash or `none`;
- exact verified rollback release hash and tested rollback command;
- the single atomic symlink action that will activate production.

The user must answer yes to that exact checkpoint at action time. Earlier general
authorization, including the request to set up DreamHost autonomously, does not
authorize this final production activation. A changed manifest, target, delta,
rollback hash, certificate state, or Red Team result invalidates the checkpoint.

## 13. Local and Staging Validation

Implementation must run and record at least:

```powershell
python -B -m unittest discover -s website\tests -p "test_*.py" -v
php website\tests\test_php_api.php
node website\tests\test_bundle.mjs
python -B website\scripts\build_deploy_manifest.py --check
python -B website\scripts\verify_deploy_manifest.py
python scripts\verify_release.py
git diff --check
```

If `php` or `node` is unavailable locally, that is a local BLOCK, not permission
to skip the tests; record the exact missing runtime and use the capability-proven
staging runtime only after Architecture reauthorizes the evidence route.

The implementation audit records command, UTC time, exit code, source commit,
model/schema/developer-instruction hashes, fixture results, browser/assistive
technology versions, deploy manifest hash, DreamHost capability evidence path,
and all deviations. It records no personal account data, raw prompts, API keys,
secret values, provider response bodies, or machine-local credential paths.

## 14. Stop Conditions

Stop and return to Architecture on any package change; new path; dependency;
remote asset; model/endpoint/settings change; inaccessible privacy disclosure;
unbounded public route; secret uncertainty; capability failure; nondeterministic
fixture; byte mismatch; accessibility failure; unsafe output rendering; manifest
mismatch; non-atomic deployment; missing rollback target; TLS failure; failed
Red Team review; or changed production checkpoint facts.

No partial PASS authorizes the next role.
