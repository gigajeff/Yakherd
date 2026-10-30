# Yakherd.dev Concierge Website Plan v3 Red Team Review

- Date: 2026-07-21
- Review mode: fresh independent pre-implementation review
- Target: `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`
- Target SHA-256: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`
- OpenAI evidence SHA-256: `ec3a2737972cda8b184675712b7bf403a92c250a2576584f4fb43ddd759da768`
- Verdict: `pass`
- Authority effect: plan-level PASS only; Architecture may run the bounded,
  non-secret DreamHost capability probe in section 10, and Implementation remains
  parked until that probe passes

## P0 Findings

None.

## P1 Findings

None.

## P2 Findings

None.

## P3 Findings

None.

## V2 P1/P2 Closure Review

### Prior P1-1: complete-request token admission and settlement

Closed.

V3 removes the transcript byte/token estimate and reserves 1,048,800 input
tokens plus all 1,200 requested output tokens before every upstream call. The
input reservation is the recorded 1,050,000-token context window less the full
output request and explicitly includes developer instruction, schema, roles,
framing, transcript, and provider tokenization overhead
(`docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md:368-396`). Admission
counts settled, retained unknown/failure, in-flight, and new reservations against
the hard daily ledgers (`:379-396`).

Only a complete, locally schema-valid response with present, bounded usage may
settle reservations. Missing, malformed, refused, incomplete, timed-out, or
otherwise unknown calls retain the full reservation; an unexpectedly larger
usage value disables the relay (`:387-402`). The fixed 250-request limit and
300,000 requested-output-token limit also agree exactly at 1,200 tokens per call
(`:368-377`).

The separately recorded current official evidence confirms the context/output
facts, response usage fields, inclusion of reasoning in output accounting, and
that provider project budgets are soft alerts rather than hard caps
(`docs/audits/yakherd/2026-07-21_yakherd_dev_openai_api_evidence.md:10-35`,
`:54-70`). V3 now describes the PHP admission ledger, not the provider budget,
as the hard boundary (`website_plan_v3.md:462-470`).

### Prior P1-2: bounded server counter, application-log, and host-log lifecycle

Closed at plan level.

V3 defines the state root, exact file inventory, canonical event schema, modes,
ownership, eight-date/2,000-event/4-MiB data limits, 6-MiB root limit, lock,
atomic compaction, lease recovery, cron, fail-closed corruption/full-storage
behavior, and adversarial tests (`website_plan_v3.md:404-437`). It separately
defines application-log fields and exclusions, eight-date retention, 8-MiB cap,
and fail-closed rotation/deletion (`:439-449`).

DreamHost access-log fields, controller, permissions, retention controls, and a
maximum enforceable or contractually verified 30-day retention are mandatory
capability-probe evidence; an unavailable bound blocks production
(`:451-460`, `:783-806`). The public disclosure must distinguish browser state,
HMAC rate state, application logs, host logs, OpenAI processing, and downloaded
files (`:455-460`, `:503-557`). Actual DreamHost behavior remains a future probe,
not a plan assumption.

### Prior P1-3: retained self-verifying release manifests and source-independent rollback

Closed.

V3 maps the generated canonical manifest to
`private/release-manifest.json`, mode `0444`, as the sole permitted remote
metadata file outside its own entry array (`website_plan_v3.md:833-860`). It
defines the non-recursive self-hash calculation, directory-name binding,
canonical reserialization, exact-entry verification, missing/extra rejection,
and immutable release modes (`:865-880`).

Rollback reads only the retained remote manifest, verifies its self-hash and
every release byte without the current checkout, and the required drill removes
or denies access to the original A source and local manifest before rolling back
to A (`:889-898`). The production checkpoint must independently verify its
rollback hash from the retained manifest (`:889-896`, `:967-985`).

### Prior P1-4: exact pre-canary provider-secret checkpoint

Closed.

The promotion sequence deploys static/mock staging before any live provider key,
then requires a separate secret checkpoint and a fresh yes at action time before
creating or entering one new site-specific key (`website_plan_v3.md:910-965`).
The checkpoint identifies the OpenAI project suffix, dedicated-project status,
model allowlist, supported restricted-key scope, rate/pricing/soft-budget facts,
DreamHost account/site user/host/config path, owner and modes, origin, server hard
limits, operator, disable/revoke paths, and exact canary (`:939-957`).

It expressly excludes copying an existing credential, displaying the value,
expanding model/endpoint authority, production activation, Git publication, and
reuse; changed facts invalidate approval (`:959-965`). No key is authorized by
this plan PASS or the capability probe.

### Prior P2-1: high-stakes beginner behavior

Closed.

The fixed developer instruction forbids domain advice and requires flags and an
unresolved expert-review requirement (`website_plan_v3.md:107-118`). Every
non-`none` flag triggers a fixed, model-independent accessible warning; allowed
actions are bounded; domain advice, hidden flags, and professional-review claims
are forbidden; every draft preserves a `Safety and expert review` section; and
export requires a bound acknowledgement that is cleared by relevant changes
(`:596-613`).

The approval schema binds acknowledgement time and sorted flags (`:216-229`),
and the fixture, screen-reader, warning, refusal, preservation, and export-block
gates are explicit (`:615-644`).

### Prior P2-2: exact current Responses request and schema evidence

Closed at plan level.

The supplied evidence file matches its required SHA-256 and records current
official sources, retrieval date, model/API/storage/retention/budget facts, and
the architecture consequences without an authenticated call or secret
(`docs/audits/yakherd/2026-07-21_yakherd_dev_openai_api_evidence.md:1-8`,
`:10-74`).

V3 binds that evidence and gives the exact developer instruction, complete
top-level request envelope, developer/user/assistant `input_text` items,
`background`, `stream`, `store`, `truncation`, reasoning, tools, safety ID,
output cap, and strict `text.format` JSON Schema placement
(`website_plan_v3.md:91-169`). It also gives the exact response schema object and
local validation rules (`:559-594`). Tests bind the no-placeholder request,
developer instruction, schema, and serialized request hashes (`:164-169`). Any
current-doc or authenticated staging disagreement returns to Architecture
(`:102-105`).

### Prior P2-3: staging topology and Git sequencing

Closed.

The capability probe must prove separate production and staging symlink swaps,
the exact access-controlled staging vhost, and protection before all content,
API, and error responses (`website_plan_v3.md:778-806`). V3 defines
`staging-public`, its exact vhost web directory, vhost-level Basic Auth outside
release bytes, isolation from production, and atomic `staging-public.next`
promotion (`:808-831`).

After implementation-diff PASS, a fresh Git checkpoint presents the reviewed
paths/diff, branch/HEAD, proposed branch, exact commit message, staged paths, and
exclusions. Only an exact human yes authorizes branch creation, deliberate
staging, index review, and commit; no push or PR is authorized. Staging consumes
only the resulting reviewed source commit and matching manifest
(`:910-937`). This satisfies root `AGENTS.md:53-60`; plan PASS and capability
PASS do not themselves authorize Git mutation.

### Prior P2-4: independently reproducible JSON and ZIP byte rules

Closed.

V3 fixes UTF-16 surrogate handling, key sorting, every JSON string escape,
direct UTF-8 scalar handling, BOM/whitespace/terminal-LF rules, and duplicate/
number rejection (`website_plan_v3.md:203-214`). It enumerates every local ZIP
header, central header, EOCD, flag, method, timestamp, CRC/size, offset,
attribute, filename, path, count, and forbidden feature (`:240-262`).

Two whole-archive golden hashes and an independent Python parser must validate
all headers, CRCs, entry hashes, JSON rules, and extracted prompt without calling
the JavaScript writer (`:264-272`). The package bridge still proves exact
unchanged-package intake across newline, Unicode, tab, and delimiter boundaries
(`:274-308`).

## Package, Write-Scope, Privacy, Accessibility, And Deployment Boundary

The website remains in the distribution layer and is explicitly untrusted input
to the unchanged package intake contract (`website_plan_v3.md:12-30`). That is
consistent with the current package rule that receiving a prompt does not
authorize implementation and that intake becomes authoritative only after
independent review and owner promotion
(`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:3-4`,
`:46-52`).

The Implementation write set is finite, contains no wildcard, and excludes the
audited package, releases, root evidence, and `yakherd.mp4`
(`website_plan_v3.md:699-762`). The tracked branding asset's stated byte length
and SHA-256 match the repository file. No dependency manager, remote asset,
vendored framework, CDN, analytics, cookie, or third-party browser script is
authorized (`:56-67`, `:751-762`).

Browser consent, optional IndexedDB persistence, expiry, failure labeling,
deletion, text-only rendering, secret warning, provider-retention disclosure,
and no-store response caching remain explicit (`:503-557`). WCAG 2.2 AA evidence,
manual assistive-technology coverage, exact security headers, and safe DOM rules
remain mandatory gates (`:646-697`).

Deployment remains new-release-only, locked, path-contained, hash-verified,
read-only after construction, atomic, and rollback-tested (`:808-909`). The
fresh production checkpoint still requires exact account, paths, source commit,
manifest, delta, acceptance evidence, current/rollback releases, and activation
action, plus a new yes at action time (`:967-985`).

## Validation And Preservation Evidence

- `python scripts\verify_release.py`: passed; 47 manifest files verified and
  zero package cache paths found.
- `git diff --check`: passed with exit code 0 and no output. This review is
  untracked, so its trailing-whitespace state was checked separately.
- Branch: `main`.
- HEAD: `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`.
- Upstream: `origin/main`.
- Ahead/behind at review start: `0/0`.
- No staged paths; no tracked package diff.
- V1 plan SHA-256:
  `7fd244bd2c073f06f39962080b59890341c11712728c6f78e1c34fdd1bcee6f8`.
- V2 plan SHA-256:
  `ed116213b9de08dd450776a9c3fb6e4b2b51a73999269d5b120208bcb016d12f`.
- First FAIL audit SHA-256:
  `20b01088b0fea8ad47ac235a72f49b1197f4a0c78830e5fc9ed522808ecb656d`.
- V2 FAIL recheck SHA-256:
  `4d44c22d6b2416352012e202e23fcfdbe2efb2ada11d9eaca2bff2ba6a8eaa09`.
- OpenAI evidence SHA-256:
  `ec3a2737972cda8b184675712b7bf403a92c250a2576584f4fb43ddd759da768`.
- V3 plan SHA-256:
  `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`.
- Unrelated `yakherd.mp4` was not read, modified, moved, staged, or touched.

## Required Fixes

None before the next bounded stage. Future capability, implementation, Git,
secret, staging, and production evidence are gates, not claims already passed.

## Residual Risks And Mandatory Future Gates

This PASS does not prove DreamHost supports the required PHP, filesystem, cron,
vhost, log-retention, access-control, or atomic-symlink behavior. Section 10 must
prove each item without a provider secret; failure or ambiguity returns to
Architecture and keeps Implementation parked.

Even after later gates, residual risk includes best-effort secret-detection
misses, compromised/shared browsers, inaccurate local clocks, provider or price
change, model nondeterminism, address-rate-limit unfairness behind proxies,
DreamHost/account compromise, assistive-technology variation, local-state loss,
and user misunderstanding of self-hashes. The plan discloses or gates these; the
site must not claim to eliminate them.

The recorded OpenAI evidence used no authenticated API call. The first
authenticated schema/canary result remains behind the implementation review,
Git checkpoint, staging deployment, and separate site-secret checkpoint. Any
API/doc/schema/model/price/project-control conflict returns to Architecture and
fresh review.

## Verdict And Exact Next-Stage Authority

Verdict: `pass` for the exact v3 plan bytes identified above.

This PASS authorizes Architecture to perform only section 10's DreamHost
capability stage: configure the dedicated site user/hosting and access-controlled
staging hostname needed for the probe, upload and execute only the temporary
non-secret bounded probe, record redacted capability evidence, and delete the
probe. It does not authorize deploying the Concierge or installing/transferring
an OpenAI key.

Implementation remains parked until every section 10 capability passes. If and
only if they all pass, this plan plus that evidence authorizes Implementation to
write only the exact section 9 paths and run local non-secret tests. Any failed
or ambiguous capability, new path, dependency, package/release change, or plan
deviation returns to Architecture and requires fresh review before writing.

This PASS does not authorize Git branch creation, staging, commit, push, PR,
network publication, provider-secret creation/transfer, live API calls, staging
live canary, production activation, release/tag/PyPI changes, package changes,
or unrelated-file action. Those remain behind the exact later checkpoints and
fresh implementation-diff PASS in sections 12 and 13.

No product, automation, dependency installation, network, DreamHost, secret,
deployment, release, or Git mutation occurred during this review. No package or
release bytes changed. The only authorized write was this review record.

autonomous next action: Architecture may run only the section 10 non-secret DreamHost capability probe; Implementation remains parked until every capability gate passes and the probe evidence is recorded.
