# Yakherd.dev Concierge Website Plan v2 Red Team Recheck

- Date: 2026-07-21
- Review mode: fresh independent pre-implementation recheck
- Target: `docs/2026-07-21_yakherd_dev_concierge_website_plan_v2.md`
- Target SHA-256: `ed116213b9de08dd450776a9c3fb6e4b2b51a73999269d5b120208bcb016d12f`
- Prior plan preserved SHA-256: `7fd244bd2c073f06f39962080b59890341c11712728c6f78e1c34fdd1bcee6f8`
- Prior FAIL audit preserved SHA-256: `20b01088b0fea8ad47ac235a72f49b1197f4a0c78830e5fc9ed522808ecb656d`
- Verdict: `fail`
- Authority effect: Implementation remains parked; no DreamHost capability
  probe or mutation, secret transfer, staging, production, Git mutation,
  package/release change, or publication is authorized

## P0 Findings

None.

## P1 Findings

### P1-1: The advertised hard input-token budget does not reserve the complete request and is not conservatively bounded

V2 defines a global ceiling of 2,000,000 estimated input tokens per UTC day
(`docs/2026-07-21_yakherd_dev_concierge_website_plan_v2.md:262-271`) and calls
`ceil(UTF8_bytes / 2)` a conservative input estimate (`:273-276`). That estimate
is not proven to be an upper bound for every accepted UTF-8 transcript. More
decisively, the upstream request also contains a fixed developer instruction and
strict schema (`:244-246`), neither of which is included in the stated transcript
byte estimate. Request JSON/framing overhead is not reserved either.

The request count and body limits still create an outer resource bound, and the
provider-side project limits add defense in depth (`:221-235`, `:278-281`), but
they do not make the stated 2,000,000-token counter a hard server-side ceiling.
An attacker can consume more actual input tokens than the counter reserves even
without bypassing a session or IP limit. This leaves prior P1-2's cost boundary
open.

Required fix: define a pre-call reservation that upper-bounds the complete
rendered provider request, including developer instruction, response schema,
role/framing overhead, and transcript. Use a proved-safe bound for accepted
UTF-8 rather than an unsupported two-bytes-per-token assumption. Reconcile the
reservation with provider-returned usage without refunding failed/unknown calls,
and prove the global daily counter cannot undercount. Record the exact
provider-side cap behavior from current authorized evidence; an alert alone is
not a hard cap.

### P1-2: Server-side rate/privacy state and access-log retention have no lifecycle or bounded storage contract

V2 correctly makes counters authoritative, lock-protected, and outside the web
root, and avoids persisting raw IP addresses in those counters
(`website_plan_v2.md:254-260`). It nevertheless stores HMAC-derived IP/network
keys plus session and lifetime counters, but specifies no record schema, file
layout, maximum record count, expiry, cleanup transaction, failure behavior
during cleanup, or deletion/retention period. Rotating a daily salt does not
delete prior pseudonymous records. Reset sessions and changing address keys can
therefore accumulate server state indefinitely even under the 500-request daily
call ceiling (`:262-281`).

The browser lifecycle is now detailed (`:313-364`), but the privacy disclosure
requirements do not enumerate these server-side pseudonymous counters or
DreamHost access logs. The capability probe asks only for log locations and
proof that request bodies and secrets are not logged (`:550-566`); it does not
require recording what metadata is logged, how long it is retained, who controls
retention, or what the privacy page must disclose. Thus prior P1-3 is closed for
IndexedDB but remains open for server processing, and the missing counter bound
also weakens prior P1-2's disk/resource-abuse boundary.

Required fix: define the exact server counter and operational-log data
inventory, purpose, retention, maximum cardinality/storage, file permissions,
transactional expiry/compaction, cleanup-failure behavior, and disclosure.
Require the DreamHost probe to establish which access-log fields and retention
controls are actually available. The public privacy page must distinguish
browser state, HMAC-derived server rate state, hosting access logs, provider
processing, and downloaded files. Add bounded tests for long-term key churn,
cleanup races, full storage, corrupted state, retention expiry, and fail-closed
behavior.

### P1-3: Retained releases do not retain the manifest required to authenticate rollback

V2 defines a canonical deploy manifest and derives each release directory name
from its hash (`website_plan_v2.md:590-600`). It then gives a finite mapping for
public runtime files and private PHP libraries and expressly excludes unlisted
files (`:601-617`). The manifest itself has no remote destination in that
mapping. The exact repository write set likewise names only the manifest builder
and verifier, not a durable per-release manifest registry (`:472-515`).

Deployment verifies the current manifest before activation (`:618-630`), while
rollback later accepts only a retained manifest hash and requires the selected
directory and contents to reverify (`:632-637`). After the source moves on, the
directory name alone is insufficient to reconstruct the old canonical manifest:
it contains `created_utc`, `source_commit`, source paths, media types, modes, and
entry hashes (`:590-599`). Without an immutable retained copy, rollback cannot
independently prove which entries are required or whether one is missing or
extra. This leaves the verification portion of prior P1-5 open even though the
new upload/symlink-swap design is otherwise transactional.

Required fix: define an exact private, immutable retention location and mapping
for every release manifest, with permissions and self-hash handling that avoid
an undefined recursive digest. Bind it to the release directory, reject
missing/extra metadata, copy it through the reviewed deployment path, and make
both rollback and the production checkpoint verify that retained manifest
without depending on the current source checkout. Exercise the A/B/rollback
drill after removing access to the original A source tree.

### P1-4: The sequence has no explicit authority gate for installing the production provider secret before the staging canary

Section 1 says secret transfer remains blocked until a gate authorizes a
particular next stage and that plan PASS alone authorizes only the capability
probe and bounded Implementation (`website_plan_v2.md:25-30`). The capability
stage expressly forbids transferring an OpenAI key (`:550-553`). The secret
lifecycle then describes how a key would be created and rotated on the host
(`:283-301`), and the sequential promotion gates jump from implementation Red
Team PASS directly to a staging deployment and live model acceptance
(`:643-655`). A live staging canary requires the site-specific key and provider
project controls (`:278-281`), but no intervening human checkpoint authorizes
creation/entry of that secret or identifies the exact provider project and
DreamHost target.

This is fail-closed if read literally, because secret transfer remains blocked;
it is unsafe if Stage 5 is read as implicitly authorizing the transfer. An
authority ambiguity at a credential boundary cannot receive PASS.

Required fix: add a separate explicit human secret-install checkpoint after the
implementation-diff PASS and before any live canary. Show the exact DreamHost
account/domain/config path, site-specific provider project, restricted-key
scope, non-secret limit metadata, installer/operator, and validation action,
without showing the secret. State that it authorizes creation or secure entry of
a new site-specific key only, not copying a local credential. A changed target,
project, scope, path, or permissions invalidates that approval.

## P2 Findings

### P2-1: High-stakes flags have no required beginner-facing consequence

The strict schema now defines medical, legal, financial, and safety-critical
flags and requires the fixture suite to flag seeded cases
(`website_plan_v2.md:366-417`). The beginner journey does not say what the UI
must do when one appears (`:32-54`), and the schema permits `question` or `draft`
with a high-stakes flag because no cross-field rule requires `blocked`, a
warning, narrowed scope, or expert-review constraint (`:368-391`). Flagging a
risk invisibly or without a normative consequence does not complete the
beginner-safety gate.

Required fix: define the exact accessible warning and allowed next actions for
each high-stakes flag. At minimum, prevent the Concierge from presenting domain
advice or implying safety review, preserve the flag and unresolved expert-review
requirement in the draft/handoff, and require explicit visitor acknowledgement
before export. Add UI, schema-transition, screen-reader, and bundle tests.

### P2-2: The exact live Responses request shape and current documentation gate remain incomplete

V2 materially improves the model contract by pinning model, endpoint, storage,
reasoning, output cap, tool absence, sampling omission, schemas, refusal mapping,
fixtures, and pass thresholds (`website_plan_v2.md:69-89`, `:237-252`,
`:366-417`). It still does not specify the complete serialized Responses request
shape, including the exact developer/input item structure and the API field that
enforces the strict JSON schema. The plan cites current external pages, but this
review was forbidden from using the network and therefore could not authenticate
current parameter, model, retention, or restricted-key behavior.

The locally installed OpenAI guidance names live model guidance as canonical for
model IDs, parameters, limits, pricing, and feature availability and requires it
to be fetched before code changes
(`C:/Users/jeff/.codex/skills/.system/openai-docs/references/upgrading-to-gpt-5p6-sol.md:7-15`).
V2 contains no pre-Implementation current-doc evidence gate; the unauthenticated
DreamHost connectivity probe cannot validate an authenticated request body.
This leaves a bounded part of prior P2-3 open.

Required fix: before Implementation, record authorized current official API
evidence for the exact model and request fields and place the complete canonical
request template/schema invocation in the plan. Treat any discrepancy as an
Architecture return, not an implementation choice. Bind the resulting request
template and developer instruction hashes to tests and implementation review.

### P2-3: Staging topology and the required clean source commit are not sequenced as explicit reviewed transitions

The capability probe records a staging root (`website_plan_v2.md:550-566`), but
the transactional layout defines only the production site's `public` symlink
and release tree (`:574-588`). It does not define the access-controlled staging
vhost's exact web-root/symlink mapping, how it targets the new release before
production activation, or how staging access-control bytes/config remain outside
the production manifest.

The deploy manifest requires `source_commit`, scripts refuse dirty/unreviewed
source, and the production checkpoint names the reviewed source commit
(`:590-600`, `:639-641`, `:657-668`). The sequential gates contain no explicit
reviewed staged-path/commit authorization between implementation PASS and
staging (`:643-655`). Repository rules forbid implicit Git mutation
(`AGENTS.md:53-60`). The omission currently blocks staging safely, but the plan
must not leave a future operator to infer Git authority.

Required fix: define the exact staging symlink/root and access-control mapping,
then add a separate intentional Git checkpoint that shows the exact reviewed
paths and diff, commit message, branch, and resulting commit identity before any
commit. Staging may consume only that reviewed clean commit and matching
manifest; plan PASS and implementation PASS do not themselves authorize Git
mutation.

### P2-4: Canonical JSON and ZIP byte rules leave serializer/header choices open

V2 now specifies key ordering, whitespace, a terminal LF, entry ordering,
timestamps, CRC, modes, and path restrictions (`website_plan_v2.md:123-169`).
However, "JSON-standard escaping" permits more than one valid representation of
the same string, and several ZIP header fields that affect archive bytes are not
fixed, including version-made-by/version-needed values and unspecified reserved
attributes. A byte-identical regression test for one implementation is useful,
but it does not make the written format independently reproducible.

Required fix: name the exact JSON string-escaping algorithm and every ZIP local
and central-directory field, or narrow the promise to deterministic output from
the reviewed implementation and provide an independent parser/fixture verifier.
Include golden archive hashes for boundary/Unicode cases and verify extracted
entries independently from the writer.

## P3 Findings

None.

## Prior-Finding Closure Matrix

| Prior finding | Recheck result | Evidence |
| --- | --- | --- |
| P1-1 intake bridge | Closed except the lower-severity serializer precision in P2-4 | Canonical prompt and handoff bytes, package-independent provenance, and unchanged-package bridge proof are defined at `website_plan_v2.md:91-205`. |
| P1-2 endpoint abuse/cost/security | Partially closed; P1-1 and P1-2 remain | HTTP, schema, egress, concurrency, rate, error, and secret controls are explicit at `:207-311`; full token accounting and bounded counter lifecycle are not. |
| P1-3 browser privacy/deletion | Browser portion closed; server portion remains in P1-2 | Consent, memory default, IndexedDB lifecycle, deletion, safe rendering, post-exposure warning, and no-store caching are defined at `:313-364`. |
| P1-4 exact write set/assets | Closed | Finite paths and exact tracked asset provenance are defined at `:472-534`; the recorded asset length/hash match `yakherd2.png`. |
| P1-5 transactional deploy/rollback/checkpoint | Partially closed; P1-3 and P1-4 remain | Atomic new-release promotion and fresh production checkpoint are defined at `:574-673`; retained manifest evidence and the pre-canary secret gate are incomplete. |
| P2-1 DreamHost capability proof | Closed at plan level | The pre-Implementation probe and fail-closed capability list are defined at `:536-572`; actual proof remains a future gate. |
| P2-2 accessibility proof | Closed at plan level | Traceable automated/manual WCAG evidence and a recorded assistive-technology pass are required at `:419-445`. |
| P2-3 model/schema evaluation | Partially closed; P2-2 remains | Model fields, schema, refusal behavior, corpus, and gates are defined at `:69-89` and `:366-417`; current request-shape evidence remains gated. |
| P2-4 headers/output safety | Closed | Exact headers, cache rules, CSP, text-only DOM sinks, and local/staging assertions are defined at `:313-364` and `:447-470`. |

## Positive Boundary Assessment

V2 preserves the product-neutral audited package boundary. It explicitly keeps
the package byte-for-byte unchanged and treats the website as untrusted input to
the existing intake contract (`website_plan_v2.md:12-30`). Its finite write set
excludes package/release bytes and unrelated `yakherd.mp4` (`:472-534`). This is
consistent with root `AGENTS.md:20-34` and the unchanged package intake rule that
prompt receipt does not authorize implementation and becomes authoritative only
after independent review and owner promotion
(`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:3-4`,
`:46-52`).

V2 also makes substantial fail-closed progress: it separates self-integrity from
identity/authenticity, forbids automatic authority, eliminates undeclared
dependencies, gives the model no tools, validates bounded same-origin JSON,
keeps secrets outside the web root, defaults to memory-only state, defines safe
text rendering, requires accessibility evidence, uses new immutable release
directories and an atomic symlink swap, and requires a fresh exact production
checkpoint. Those improvements do not cure the remaining P1 findings.

## Required Fixes Before Another Recheck

1. Correct the complete-request token reservation and prove the spend counter
   cannot undercount.
2. Define and test the bounded lifecycle and disclosure of all server counters
   and hosting/operational logs.
3. Retain and independently verify each immutable release manifest so rollback
   does not depend on the current checkout.
4. Add an explicit human site-secret installation checkpoint before any live
   staging canary.
5. Define high-stakes beginner behavior, authenticate the exact current Responses
   request shape before Implementation, and close the staging/Git and canonical
   serialization details in P2-1 through P2-4.
6. Preserve v1 and its FAIL audit, revise v2 through Architecture only, and
   request another fresh independent review.

## Validation And Repository State

- `python scripts\verify_release.py`: passed; 47 manifest files verified and
  zero package cache paths found.
- `git diff --check`: passed with exit code 0 and no output. This recheck is
  untracked, so its trailing-whitespace state was checked separately.
- Branch: `main`.
- HEAD: `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`.
- Upstream: `origin/main`.
- Ahead/behind at review start: `0/0`.
- Review-start dirty state: untracked v1 plan, v2 plan, beginner audit, prior
  Red Team audit, and unrelated `yakherd.mp4`; no staged paths.
- `yakherd2.png` matches v2's stated 3,028,501-byte length and SHA-256
  `e45c1c5449fff67c0ea4f2b4ed3af9e4886793939f89a449c9e996e1367a4383`.
- The unrelated `yakherd.mp4` was not read, modified, moved, staged, or touched.

## Residual Risk

After the findings are fixed, residual risk will still include best-effort
secret-detection misses, compromised/shared browsers, inaccurate client clocks,
provider policy/availability/model drift, model nondeterminism, DreamHost
control-plane or account compromise, rate-limit unfairness behind proxies,
assistive-technology differences, loss of local browser state, and a beginner
misunderstanding a self-hash as third-party attestation. The site must disclose
and bound these risks rather than claim to eliminate them.

The current OpenAI and DreamHost claims were not independently refreshed or
tested because this review explicitly prohibited network and DreamHost access.
Actual current-doc, account, runtime, provider, staging, and rollback evidence
remain future gates and cannot be inferred from this documentation review.

## Verdict And Authorization Boundary

Verdict: `fail`.

Implementation must remain parked. A PASS is not available while the public
cost counter can undercount, server-side privacy/resource state has no lifecycle,
rollback lacks retained manifest evidence, and the provider-secret authority
transition is ambiguous. The P2 findings also require an Architecture revision
before another review.

This report authorizes no repair, Implementation slice, DreamHost capability
probe or mutation, secret transfer, network access, staging, production, Git
mutation, package/release change, deployment, commit, push, publication, or
unrelated-file action. V1 and its FAIL audit remain preserved. Architecture may
produce a separately authorized revised candidate; only a fresh independent PASS
on that exact candidate may unpark the next bounded stage.

No product, automation, dependency installation, network, DreamHost, release,
deployment, or Git mutation occurred. No package or release bytes changed. The
only authorized write was this recheck record.

human action required: keep Implementation and every DreamHost, secret, staging, production, Git, and publication action blocked; authorize Architecture only to revise the exact P1/P2 requirements above and request another fresh independent Red Team review.
