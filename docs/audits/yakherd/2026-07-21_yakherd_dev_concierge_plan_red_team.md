# Yakherd.dev Concierge Website Plan Red Team Review

- Date: 2026-07-21
- Review mode: independent pre-implementation plan review
- Target: `docs/2026-07-21_yakherd_dev_concierge_website_plan.md`
- Evidence class: review of repository authority files and the exact local plan
- Verdict: `fail`
- Authority effect: no implementation, DreamHost mutation, secret transfer,
  staging deployment, or production deployment is authorized by this review

## P0 Findings

None.

## P1 Findings

### P1-1: The proposed bundle has no exact, verified path into the audited intake contract

The plan makes a versioned, hash-bound intake bundle its authority boundary and
central deliverable (`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:17-20`,
`:187-200`). It defines `MASTER_PROMPT.txt`, says that it contains the exact
approved prompt "with documented delimiters," and defines a richer provenance
and approval set (`:187-197`). It does not specify whether the delimiters are
inside or outside the bytes hashed as the prompt, the exact delimiter/newline
serialization, or how an installed project verifies and promotes those bytes.

The current audited package has a different and exact contract. It accepts only
text between `MASTER PROMPT START` and `MASTER PROMPT END`, excludes both
delimiter lines and their boundary newlines, writes the resulting bytes to a
run-ID path, and requires a provenance object containing exactly seven named
fields (`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:8-30`).
It then independently verifies the installed file and does not make intake
authoritative until Red Team PASS and owner promotion
(`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:32-35`,
`:46-52`). The website plan deliberately keeps package bytes out of scope
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:53-56`), but supplies no website-side adapter or acceptance
test that bridges these contracts. `OPEN_IN_CODEX.txt` is described only as
plain-language next steps
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:195-197`).

Consequently, the plan does not prove that its core output can enter the current
product-neutral package without byte drift, provenance-schema conflict, or a
beginner manually reconstructing the prompt. Self-consistent hashes inside a
client-generated ZIP do not authenticate the human approval or prove that the
installed project received the same bytes.

Required fix: specify one canonical UTF-8 byte contract, delimiter and newline
rules, canonical JSON rules, ZIP entry rules, and the precise distinction
between self-integrity and authentication. Define a package-compatible,
non-automatic handoff that preserves the website hash while allowing the
installed Architecture role to create its existing exact schema independently.
Add an end-to-end acceptance test against the unchanged current package that
proves the saved prompt bytes and hash survive export, user handoff, intake,
independent verification, and Red Team promotion. No package change is implied
or authorized.

### P1-2: The public model endpoint lacks a bounded abuse, cost, and server-security contract

The selected design is a public PHP JSON endpoint backed by a server-side
OpenAI key and a quality-first model
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:164-176`, `:202-225`).
The plan correctly requires `store: false`, no tools, structured output,
server-side secret handling, and no body logging (`:69-84`, `:174-176`). It does
not define authentication or abuse controls, rate and concurrency limits,
per-session or global spending limits, numeric request/context/output limits,
allowed HTTP methods/content types/origins, CORS/CSRF behavior, timeout and retry
budgets, a fixed outbound host, TLS verification behavior, response-size caps,
or strict rejection of unknown/oversized response fields. The proposed random
browser session identifier is client-controlled and resettable, so it is not a
standalone control against automated key consumption (`:174-176`). Testing
"oversized" requests without normative limits does not close the contract
(`:261-270`).

The production secret's exact location, ownership, permissions, include path,
and rotation/revocation procedure are also absent. The plan says only that it
must not be under the public web root and that a separate transfer gate applies
(`:73-79`), while the implementation write set contains only an example config
(`:248-249`). A public anonymous endpoint can therefore become a cost-denial
surface or key-abuse proxy even when prompt injection cannot trigger tools.

Required fix: define a fail-closed endpoint threat contract with numeric bounds,
server-enforced rate/concurrency/budget controls that cannot be bypassed merely
by resetting browser state, exact HTTP and origin policy, fixed provider egress,
timeouts and bounded retries, strict request and response schemas with length
limits, and generic error mapping. Define a secret installed outside the web
root with exact path class, least-privilege permissions, rotation/revocation,
and a no-secret outage mode. Add adversarial tests for bypass, parallelism,
resource exhaustion, origin spoofing, malformed provider output, HTML/script
payloads, timeout, retry amplification, and budget exhaustion.

### P1-3: Browser-local privacy, consent, and deletion semantics are not defined

The plan says interview state is browser-local by default, forbids server-side
transcript storage, and requires an explanation before the first model call
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:64-84`). It also promises local resume, edit, export, and
deletion (`:86-95`, `:177-179`). It does not name the browser storage mechanism,
stored fields, retention/expiry, origin and shared-device exposure, behavior in
private browsing or when storage is unavailable, migration/version handling, or
what "delete" clears. It requires explanation, but not an affirmative consent
event before sending current interview context to the provider (`:69-72`). It
also does not require disclosure that `store: false` governs API response
storage behavior rather than proving that no provider-side security/abuse
retention or other processing exists.

The missing details matter because model output and idea text are both declared
untrusted (`:59-62`) and browser persistence creates an XSS-accessible copy on
the site's origin. The plan mentions security headers at deployment
(`:291`, `:304-305`) but does not require safe text-only DOM rendering, a
normative CSP, dependency-free rendering, cache controls for API responses, or
a test that deletion removes every versioned key and downloadable in-memory
copy. Best-effort secret detection before a next request (`:80-82`) cannot undo
a secret that was already sent or persisted.

Required fix: define the complete local data inventory and lifecycle, explicit
pre-send consent, exact provider disclosure, storage-unavailable behavior,
retention/expiry, schema migration, shared-device warning, and verifiable
delete-all semantics. Require text-only rendering/escaping, a restrictive CSP,
no sensitive response caching, and XSS/storage-exfiltration tests. Define the
post-send warning and revocation guidance for a credential detected after it
may have left the browser. Privacy language must not equate `store: false` with
zero retention.

### P1-4: The implementation write set is not exact and does not bind asset provenance

Stage 1 grants wildcard write authority over `assets/**`, `js/**`, `css/**`,
`server/api/**`, and `tests/**`, plus an unnamed evidence record anywhere under
`docs/audits/yakherd/`
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:236-257`). That is a directory-level
scope, not the exact write set required by the installed governance model, which
states that Implementation is the sole writer only for one authorized slice and
that Red Team reviews an exact diff
(`packages/jeff_strict_ssot_v1/template/AGENTS.md:28-33`; repository
`docs/ARCHITECTURE.md:28-34`). The plan also permits unspecified existing
"reviewed/tracked" branding assets or new SVG/CSS
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:180-181`)
without naming source files, licenses, hashes, or whether copied bytes become
deployment inputs.

This scope could admit extra runtime code, tests, vendored libraries, assets, or
audit paths without a new Architecture decision. It also prevents a reviewer
from determining the intended file inventory before implementation begins.

Required fix: replace every wildcard and unnamed audit output with a finite path
list. Name every runtime asset and its source, license, expected handling, and
whether it is copied or generated. Explicitly prohibit vendored code, remote
CDNs, runtime package managers, and undeclared PHP/JavaScript dependencies, or
enumerate and hash-review any exception. Any later path addition requires a
revised Architecture plan and review before writing it.

### P1-5: Deployment and rollback are not transactional, and production is pre-authorized before its target exists

The plan promises that failed checks leave production unchanged and that exact
reviewed staging bytes reach production with a recoverable prior release
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:118-126`, `:300-310`). It does not define a source-to-remote
path map, release-directory naming, file modes, ownership, manifest schema,
atomic promotion primitive, behavior for stale/extra remote files, partial
upload recovery, concurrent deploy lock, verified rollback target, or how the
rollback operation avoids an unverified computed remote path. Hashing a set of
files after an in-place upload cannot make the promise that a failed check left
the old site unchanged.

The actual DreamHost plan, account, server, user, web directory, PHP runtime,
DNS, TLS state, staging target, and existing production release are explicitly
unknown until Stage 0
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:109-126`, `:229-234`). Nevertheless the
plan says production publication has already been authorized (`:121-123`) and
ends by claiming no further human action is required for autonomous DreamHost
setup, staging, and production (`:372`). A human cannot knowingly approve the
exact production mutation, remote deletion set, rollback target, and reviewed
manifest before those facts exist. That conflicts with the repository's rule
that consequential deployment and scope escalation require explicit approval
(`packages/jeff_strict_ssot_v1/template/AGENTS.md:38-41`) and with Yakherd's
public non-goal of replacing human approval for consequential decisions
(`README.md:233-243`).

Required fix: define a finite source-to-destination allowlist with hashes and
modes, validated absolute remote roots, release locking, upload-to-new-release,
complete pre-promotion verification, one atomic or equivalently transactional
promotion mechanism proven to work on the inventoried DreamHost plan, stale-file
handling, and a verified rollback transaction. Add an explicit human checkpoint
after inventory, implementation Red Team PASS, live staging acceptance, and
rollback demonstration. That checkpoint must show the authenticated account,
domain, exact remote roots, deployment manifest hash, production delta,
rollback target, secret status without secret value, and exact promotion
action. Prior general intent is not a substitute for that bounded approval.

## P2 Findings

### P2-1: The DreamHost/PHP feasibility gate omits required runtime capabilities

Option B is selected on the claim that it works on all DreamHost plan classes,
while the actual plan remains unknown
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:135-151`). Stage 0 asks
for the PHP version and high-level hosting state (`:229-234`) but not the
specific capabilities the design needs: outbound HTTPS from PHP to the fixed
provider, cURL or an explicitly chosen standard HTTP mechanism, CA bundle/TLS
validation, JSON support, request/body/time limits, Apache `.htaccess` and
header support, log redaction configuration, filesystem permissions outside the
web root, and the promotion primitive required by P1-5.

Required fix: make those capabilities named Stage 0 proof gates before website
implementation, not assumptions deferred to live staging. Record the evidence
without secrets. If any required capability is absent, return to Architecture;
do not silently adopt the deferred second provider.

### P2-2: Accessibility acceptance does not prove the stated WCAG 2.2 AA target

The requirements appropriately name WCAG 2.2 AA, keyboard use, focus, labels,
contrast, announcements, reduced motion, and non-color cues
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:100-107`). The test and live-acceptance sections cover only
keyboard-only flow, reduced motion, desktop width, and narrow mobile width
(`:261-271`, `:293-298`, `:325-327`). They do not require checks for reflow and
zoom, accessible error association, focus movement and restoration, status/log
announcement behavior with a screen reader, target size, timeout behavior,
contrast measurement, forced colors/high contrast, or the accessibility of the
generated download and privacy/approval controls.

Required fix: add a traceable WCAG 2.2 AA acceptance matrix, automated checks,
and manual keyboard, zoom/reflow, contrast, reduced-motion, and at least one
screen-reader pass for all states, errors, warnings, approval, deletion, and
download. Record browser/assistive-technology versions and evidence.

### P2-3: Model and structured-output evaluation gates are qualitative, not bounded

The plan defaults production to `gpt-5.6-sol`, calls for "intentional balanced
reasoning," and says reasoning will be measured
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:168-176`). It
does not name the exact Responses request fields, reasoning effort, maximum
output, timeout, temperature/sampling policy if supported, schema enforcement
mode, refusal handling, or an eval rubric and pass thresholds for question
quality, stopping, contradiction preservation, sensitivity flags, high-stakes
flags, latency, and cost. The structured response field list has no types,
cardinality, maximum lengths, or cross-field invariants (`:202-225`).

The local OpenAI guidance available to this review confirms that an explicit
GPT-5.6 Sol target requires endpoint-specific reasoning fields and that omitted
reasoning has a behavioral/cost default; current live API parameters and model
availability were not independently fetched because this task forbids network
access. The plan's linked OpenAI and DreamHost claims therefore remain
unverified external assumptions in this review.

Required fix: obtain current official API evidence in an authorized,
network-enabled Architecture step; pin the exact supported request shape and
limits in the plan; define strict schemas and refusal/error handling; and add a
versioned deterministic corpus with quantitative quality, schema-validity,
latency, and cost gates. A model change or fallback must require a new measured
decision rather than an unreviewed environment-variable edit.

### P2-4: Security-header and browser-output requirements are deferred to deployment

The plan requires header verification only during DreamHost staging and
production
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:290-291`, `:302-306`). It does not specify the
expected CSP, `frame-ancestors`, MIME sniffing, referrer, permissions, HSTS,
cross-origin, API cache, or error-page behavior, nor does it bind those headers
to local tests. Prompt-injection text and model output can contain active-markup
payloads even though the model has no tools (`:61-62`, `:223-225`).

Required fix: define the exact header policy and safe DOM/output rules in the
implementation contract, test them locally and on staging, and fail closed on
missing or weakened headers. Include CSP-compatible behavior for all assets and
ensure no inline exception silently expands the script boundary.

## P3 Findings

None.

## Positive Boundary Assessment

The plan correctly keeps `packages/jeff_strict_ssot_v1/`, its manifest/release
hash chain, release workflows, tags, PyPI, and GitHub releases outside the
website slice
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:49-62`, `:359-370`). This is consistent with the
repository's separation between distribution and the audited package
(`docs/ARCHITECTURE.md:3-24`) and with the package's product-neutral, no-product-
stack guarantee (`packages/jeff_strict_ssot_v1/README.md:1-25`, `:99-110`;
`MANIFEST.json:106-113`). A website outside the package can make network calls
and product/deployment choices without changing the installer's guarantees,
provided the site never represents itself as part of the reviewed package or
changes package/release bytes.

The plan also correctly states that raw idea text and model output are
untrusted, gives the model no tools, keeps GitHub/Codex/deployment authority out
of user content, defaults to local/private behavior, forbids automatic
publication, requires staging, and keeps unreviewed 1.2.0 release claims out of
scope
(`docs/2026-07-21_yakherd_dev_concierge_website_plan.md:57-62`, `:86-98`, `:174-185`, `:318-345`). Those controls
reduce risk but do not close the P1 findings above.

## Required Fixes Before Recheck

1. Close P1-1 with a canonical byte-level, current-package-compatible handoff
   contract and an unchanged-package end-to-end test.
2. Close P1-2 with a complete public-endpoint, budget, abuse, schema, egress,
   timeout, and secret-lifecycle contract plus adversarial evidence.
3. Close P1-3 with explicit privacy consent, browser storage lifecycle,
   provider disclosure, safe rendering, deletion, and post-exposure behavior.
4. Close P1-4 by replacing wildcard write authority with a finite file and
   asset-provenance list.
5. Close P1-5 with a transactional deployment/rollback design and a bounded
   post-staging human production checkpoint.
6. Address P2-1 through P2-4 with exact feasibility, accessibility, model/eval,
   and browser-security gates.
7. Submit the revised plan for a fresh independent Red Team review. Do not treat
   a documentation edit or ordinary CI result as closing these design findings.

## Validation And Repository State

- `python scripts\verify_release.py`: passed; 47 manifest files verified and
  zero package cache paths found.
- `git diff --check`: passed with exit code 0 and no output. The report itself
  is untracked, so its trailing-whitespace state was checked separately.
- Branch: `main`.
- HEAD: `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`.
- Upstream: `origin/main`.
- Ahead/behind at review start: `0/0`.
- Review-start dirty state: untracked website plan, beginner audit, and
  unrelated `yakherd.mp4`; no staged paths.
- The unrelated untracked `yakherd.mp4` was not read, modified, moved, staged,
  or otherwise touched.

## Residual Risks

Even after the required fixes, residual risks will include best-effort secret
detection misses, user approval on a compromised/shared browser, provider-side
availability and policy change, model nondeterminism, DreamHost control-plane or
runtime compromise, browser ZIP implementation defects, loss of browser-local
state, and a beginner misunderstanding self-hashes as third-party attestation.
These must be disclosed and bounded; they cannot all be eliminated by the site.

The plan's current DreamHost and OpenAI documentation claims were not
independently refreshed because the review authorization explicitly prohibited
network access. They require an authorized current-doc and actual-account proof
before implementation or deployment choices are promoted.

## Verdict And Authority Effect

Verdict: `fail`.

Implementation may **not** receive the plan as written. The P1 findings leave
the central intake output without a proven consumer, expose an insufficiently
bounded public billable endpoint, leave browser privacy and deletion promises
underspecified, grant a non-exact write set, and cannot support the claimed
unchanged-production/rollback guarantees or advance production approval.

This report authorizes no repair, implementation, DreamHost access, network
access, secret transfer, Git mutation, staging, production deployment, package
change, release change, publication, or unrelated-file action. The exact
reviewed plan remains proposed only. Architecture may produce a separately
authorized revised plan; a fresh independent Red Team PASS is required before
Implementation receives any slice.

No product, automation, dependency installation, network, DreamHost, release,
deployment, or Git mutation occurred during this review. No package or release
bytes were changed. The only authorized write was this review record.

human action required: keep Implementation, DreamHost mutation, secret transfer, staging, and production blocked; authorize Architecture only to revise the plan for the P1/P2 requirements above and request a fresh independent Red Team review.
