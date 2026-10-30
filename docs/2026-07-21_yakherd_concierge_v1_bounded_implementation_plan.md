# Yakherd Concierge V1 - Pre-Intake Bootstrap and Candidate Implementation Architecture

Document date: 2026-07-21
Plan schema: `yakherd-concierge-architecture-plan-v1`
Status: pre-intake candidate for independent Red Team review; no product implementation authority
Architecture owner: Architecture task
Product owner: Jeffrey Martin (`gigajeff`)

## 1. Decision, authority, and exact inputs

The product owner has now made these two decisions:

1. Yakherd `v1.2.0`, rather than a moving "newest release", is the Concierge V1
   target release.
2. Architecture is authorized to convert the static-only directive into this
   bounded plan.

This record does not claim that `v1.2.0` is public yet. On 2026-07-21, the
public GitHub tags page exposed tags only through `v1.1.1`, the GitHub releases
page exposed no `v1.2.0` release, and PyPI reported `1.1.1` as latest. Gate R
below must make and authenticate the public release before any website product
implementation starts.

The exact product-direction input is:

- path: `docs/2026-07-21_yakherd_concierge_v1_build_directive_static_only.md`
- bytes: `17487`
- SHA-256: `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`
- author of record: Jeffrey Martin
- capture limitation: this path is the LF-normalized durable copy selected by
  the owner for Architecture conversion. The earlier attachment had 17,804
  bytes, CRLF line endings, and SHA-256
  `247b10e35f4dea73699807bba0150b4670cd25fe38d077f9b46ef27dd6a24308`.
  No claim is made that the durable copy preserves attachment transport bytes.
  The owner is selecting the reviewed durable copy, identified above, as the
  product-direction bytes for this plan.

The exact first review of that input is:

- path: `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_build_directive_red_team.md`
- bytes: `19030`
- SHA-256: `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`
- verdict: `FAIL`

This pre-intake plan resolves that audit by making the repository, release, byte model,
runtime policy, privacy boundary, fixtures, evidence, and later authorities
explicit. It does not retroactively call the source attachment a completed
installed-project intake. Formal unchanged `product_intake.md` intake occurs
in the separate `yakherd-web` project at Gate P, after `v1.2.0` installs that
contract. The raw prompt there will be the exact 17,487-byte durable directive
above, enclosed in the exact v1.2.0 delimiter envelope. Until Gate P passes,
this document is design evidence only and cannot authorize product code. Gate
P requires a new post-intake implementation plan and a new independent audit;
this pre-intake candidate never becomes executable merely by being copied.

## 2. Product boundary

Build one static browser application that guides a beginner through a fixed
interview, mechanically drafts a master prompt, lets the beginner edit and
approve it, and downloads a deterministic five-file ZIP handoff for Yakherd
`v1.2.0`.

Concierge V1 does not install Yakherd, create or access a GitHub repository,
launch Codex tasks, run product code, call a model, create an account, receive
user input at a server, or deploy anything for the visitor. Those statements
describe runtime product behavior; they do not prohibit separately authorized
maintainers from using Git, tests, or deployment tools to build and publish the
static site.

Not in V1:

- model-backed interrogation or a relay endpoint;
- PHP, Workers, functions, APIs, forms, accounts, sessions, analytics, or
  telemetry;
- the complete governed repository export, local runner, workbench, or private
  GitHub backup;
- DreamHost capability work or the retired v15 preflight;
- a service worker, web manifest, Cache API, background sync, share API, or
  browser notifications;
- any dependency, package install, vendored library, build step, minifier, or
  generated production source.

## 3. Alternatives and selected architecture

Architecture considered three data-loading designs:

1. Runtime `fetch()` of JSON and text. Rejected because it makes the no-request
   boundary timing-dependent and requires `connect-src`.
2. Inline JSON/templates in HTML. Rejected because it needs inline content and
   duplicates authoritative resources in a difficult-to-audit form.
3. Versioned source data files plus one external, committed JavaScript content
   module containing their exact base64 bytes. Selected. A dependency-free
   verifier decodes that module and requires byte equality with every source
   data file. The browser loads only HTML, CSS, JavaScript, and the local image;
   no JavaScript networking API is needed.

Architecture selects plain HTML5, one CSS file, ES2020 JavaScript modules, and
standard-library-only Python and Node verification. There is no compilation or
transformation step. The content module is committed source, not generated at
deploy time.

Hosting is deliberately not selected in this plan. Cloudflare Pages and
Netlify remain candidates. Transport headers, DNS, staging, rollback, and
production are Gate H/D work after a separately reviewed hosting inventory and
owner decision. Application-flow parity under `python -m http.server` is in
scope; TLS, redirects, response headers, caching, compression, MIME overrides,
and host logs are explicitly not locally identical.

## 4. Gates and authority sequence

The gates are strictly serial. A FAIL or missing artifact parks every later
gate. PASS never grants an unnamed action.

### Gate A - plan review (current gate)

An independent Red Team reviews the exact bytes of this plan and the two input
records in Section 1. A PASS may authorize only Gate R preparation. It may not
contact Implementation with product work.

### Gate R - publish and authenticate Yakherd v1.2.0

This is a separate Yakherd engine release task, not website implementation. It
requires a fresh release candidate, all checks in `docs/RELEASE.md`, an exact
artifact inventory, independent final release review, and explicit publication
authority. Per the owner's model policy, the final release gate uses one Sol
Ultra reviewer; Ultra is not used for preparation.

The release evidence must bind all of the following before Gate B:

- tag `v1.2.0` and its full 40-hex commit;
- GitHub release URL;
- PyPI project-version URL;
- wheel and sdist filenames, byte lengths, and lowercase SHA-256 values;
- `README.md`, package `README.md`, package `RELEASE.json`, package
  `MANIFEST.json`, installed `START_HERE.md`, and installed
  `docs/prompts/product_intake.md` paths, lengths, and SHA-256 values;
- the exact `yakherd==1.2.0` installation command and its supported Python
  range;
- evidence that a fresh install from each public artifact passes the release
  smoke test;
- public observations from GitHub and PyPI after publication.

The current intended package contract, which Gate R must either preserve or
explicitly supersede in a newly reviewed candidate, is:

- current engine baseline commit:
  `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`;
- root `README.md`: 12,252 bytes, SHA-256
  `3f520ed064dd57da8bee7260bf02502f12ab8c0198d907b849d66a3365367f02`;
- package `README.md`: 4,778 bytes, SHA-256
  `0bda15f2a8c73198ffb62647b67c880d6b33530225df9110faca09be4951354b`;
- `RELEASE.json`: 473 bytes, SHA-256
  `312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`;
- `MANIFEST.json`: 7,006 bytes, SHA-256
  `ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`;
- bootstrap SHA-256 from `RELEASE.json`:
  `c41f4f5d11e5eb3bfed9eabfdef7444e28612d124a26101df8bfb3628837a8bb`;
- installed `START_HERE.md`: 3,104 bytes, SHA-256
  `6fea5767314320f646c85a4b48de67f6ce564f5c248baa5ec8896023c421d241`;
- installed `product_intake.md`: 2,614 bytes, SHA-256
  `c1582bcc7918eeb547bcae8d4ceec14cfbe36267ed7313131012b0ba95c32604`.

Gate R writes its evidence only to an exact path named in its separately
reviewed release authorization. This plan supplies no tag, GitHub, PyPI,
credential, network, or publication authority.

### Gate B - create the separate governed project root

Target local root: `L:\dev\yakherd-web`.

This gate requires a separate authorization after Gate R. At entry:

- the literal target must not exist;
- `L:\dev` must resolve to the intended parent;
- the target and every ancestor from `L:\dev` downward must not be a symlink,
  junction, mount point, or other reparse point;
- the operator must record the resolved absolute target and parent;
- no GitHub repository, remote, credential, or network write is authorized;
- no existing path may be overwritten.

The gate creates the directory and performs a fresh `yakherd==1.2.0` install
using the exact public artifact and command bound at Gate R, with project name
`yakherd-web`. It first runs the installer's dry run. It then records the
installation receipt, exact installed path inventory, hashes, and verifier
output. No site file is written. The fresh bootstrap Red Team prompt runs from
the new root and must PASS.

The current Implementation task attached to `L:\dev\YAKHERD` is not an
authorized writer for the site. Before Gate I, exactly one Implementation task
must be attached to `L:\dev\yakherd-web`, must demonstrate that the installed
`AGENTS.md` is loaded, and must be the sole product writer. No second
Implementation writer may target that checkout.

Git initialization, branch creation, GitHub repository creation, visibility,
remote creation, push, PR, and publication remain parked for their normal
post-bootstrap owner checkpoint. "Separate repository" at Gate B means a
separate future repository root; it does not smuggle Git authority into this
plan.

### Gate P - unchanged product intake in yakherd-web

After the bootstrap PASS, Architecture receives one handoff whose exact bytes
are:

```text
MASTER PROMPT START
<the exact 17,487 bytes identified in Section 1>
MASTER PROMPT END
```

If the selected prompt ends in LF, the envelope contains that LF plus the one
separate LF immediately preceding `MASTER PROMPT END`; the intake parser
removes only the boundary LF and therefore preserves the prompt's terminal LF.

Architecture follows the installed, hash-bound `product_intake.md` without
modification. In the same bounded intake transaction, it creates the raw
prompt and exact provenance, reads them back, records byte length/hash, makes
the explicit `DECISIONS.md` owner-promotion entry and corresponding `SSOT.md`
owner update while retaining that raw input is not executable authority, and
writes a new, standalone post-intake candidate at
`docs/plans/yakherd_concierge_v1_implementation_plan.md`. That file must bind
the installed raw prompt/provenance/owner-decision identities, actual Gate R
release values, bootstrap evidence, exact Sections 5-17 of this design, all
resolved fixture identities, canonical bytes/hashes for every data file, the
complete user-facing copy inventory required by Section 7A, and its own exact
write/evidence boundaries.
Architecture then sends the raw prompt hash, provenance, exact owner changes,
SSOT diff, extraction path, plan identity, unresolved questions, and complete
diff together to independent Red Team. That one review covers the full
unchanged-intake transaction and the implementation candidate at
`docs/reviews/yakherd_concierge_v1_implementation_plan_red_team.md`. Neither
review path nor plan path may pre-exist. PASS must confirm that the installed
raw prompt is exactly 17,487 bytes with the Section 1 SHA-256 and that every
intake/owner/plan step conforms to the installed contract. There is no earlier
partial "intake PASS." The current pre-intake plan is a design input to that
work, not the executable authorization. Any substitution is a new Architecture
revision and fresh review.

### Gate I - bounded local static implementation

Only a fresh independent PASS of the new post-intake plan, covering Gates A,
R, B, and P, may send its exact Gate I slice to the sole Implementation writer.
Gate I permits only the paths
in Section 5, the behavior in Sections 6-13, the dependency-free local tests in
Section 14, and the exact evidence record in Section 15.

Gate I forbids network use, dependency installation, Git/GitHub mutation,
browser automation, screenshots, OS-matrix work, accessibility scanners,
screen readers, hosting, DNS, credentials, staging, deployment, production,
and publication.

### Later gates - not authorized here

- Gate S: one final independent Sol Ultra security/parser review of exact
  implementation bytes and deterministic archive evidence.
- Gate C: separately authorized Chromium/Firefox/WebKit, two-OS, extraction,
  fresh-install bridge, and qualified manual accessibility evidence.
- Gate G: owner checkpoint for Git initialization, GitHub owner/name/visibility,
  commit, remote, and push.
- Gate H: read-only static-host capability and privacy inventory followed by an
  owner hosting decision and exact response/header/cache/error-file plan.
- Gate D: transactional staging deployment, remote manifest comparison,
  rollback proof, live security/accessibility checks, and Red Team PASS.
- Gate O: explicit production and DNS authority, identical-byte deployment,
  rollback target, final PASS, and publication.

None of these later gates is implied by a Gate I PASS.

## 5. Exact Gate I write set

All paths below are relative to `L:\dev\yakherd-web`. They must be absent at
Gate I entry. Directories may be created only as parents of listed files. The
writer must open each destination exclusively with create-new/no-overwrite
semantics after rechecking containment and reparse-point absence. A collision,
unknown child, symlink, junction, reparse point, case-fold collision, or failed
exclusive create stops the gate without deleting or changing the pre-existing
path.

The Yakherd install already owns `.gitignore`, `README.md`, `AGENTS.md`, the
root authority files, `scripts/ssot/*`, and `tests/ssot/*`. Gate I must verify
those paths against the installation receipt and must not edit them. Product
and project files newly created by Gate I are:

1. `.gitattributes`
2. `LICENSE`
3. `NOTICE.md`
4. `site/index.html`
5. `site/concierge.html`
6. `site/next-steps.html`
7. `site/privacy.html`
8. `site/troubleshooting.html`
9. `site/404.html`
10. `site/assets/styles.css`
11. `site/assets/app.js`
12. `site/assets/concierge.js`
13. `site/assets/state.js`
14. `site/assets/bytes.js`
15. `site/assets/canonical-json.js`
16. `site/assets/crc32.js`
17. `site/assets/zip-store.js`
18. `site/assets/storage.js`
19. `site/assets/scanner.js`
20. `site/assets/content.v1.js`
21. `site/assets/yakherd2.png`
22. `site/data/interview.v1.json`
23. `site/data/prompt_template.v1.txt`
24. `site/data/secret_patterns.v1.json`
25. `site/data/high_stakes_terms.v1.json`
26. `site/data/yakherd_release.v1.json`
27. `site/fallback/master_prompt_template.txt`
28. `docs/CONCIERGE.md`
29. `docs/PRIVACY_BOUNDARY.md`
30. `docs/STATIC_SOURCE_POLICY.md`
31. `docs/BUNDLE_FORMAT.md`
32. `docs/CONTENT_PROVENANCE.md`
33. `scripts/verify_static.py`
34. `tests/test_static_policy.py`
35. `tests/test_content_binding.py`
36. `tests/test_pages.py`
37. `tests/test_bytes.mjs`
38. `tests/test_state.mjs`
39. `tests/test_canonical_json.mjs`
40. `tests/test_crc32.mjs`
41. `tests/test_zip_store.mjs`
42. `tests/test_scanner.mjs`
43. `tests/test_storage.mjs`
44. `tests/test_interview.mjs`
45. `tests/fixtures/bundle_input.v1.json`
46. `tests/fixtures/prompt_ascii_lf.txt`
47. `tests/fixtures/prompt_unicode_lf.txt`
48. `tests/fixtures/prompt_empty.txt`
49. `tests/fixtures/prompt_rejected_lone_surrogate.json`
50. `tests/fixtures/prompt_rejected_delimiter.txt`
51. `tests/fixtures/secret_clean.txt`
52. `tests/fixtures/secret_positive.txt`
53. `tests/fixtures/high_stakes_clean.txt`
54. `tests/fixtures/high_stakes_positive.txt`
55. `tests/golden/MASTER_PROMPT.txt`
56. `tests/golden/MASTER_PROMPT_HANDOFF.txt`
57. `tests/golden/APPROVAL.json`
58. `tests/golden/BUNDLE_MANIFEST.json`
59. `tests/golden/OPEN_IN_CODEX.txt`
60. `tests/golden/yakherd_intake_6e7dd93a7067.zip`
61. `tests/golden/golden_identity.v1.json`
62. `docs/evidence/concierge_v1_local_implementation.json`

No wildcard path is authorized. In particular, no `_headers`, `_redirects`,
hosting configuration, workflow, dependency lockfile, package manifest,
source map, hidden IDE file, screenshot, coverage file, cache, temporary file,
generated test output, archive other than the named golden archive, or public
deployment file may be created in Gate I.

`.gitattributes` has exactly these UTF-8 LF bytes and one terminal LF:

```text
* text=auto eol=lf
*.png binary
*.zip binary
```

`site/assets/yakherd2.png` is an exact byte copy of
`L:\dev\YAKHERD\yakherd2.png`: 3,028,501 bytes, SHA-256
`e45c1c5449fff67c0ea4f2b4ed3af9e4886793939f89a449c9e996e1367a4383`.
The source identity must be checked before reading it into the copy operation;
the destination must be absent and exclusively created; the destination is
then read back and checked. `yakherd.mp4` is never read, copied, hashed, or
touched. The site license is Apache-2.0. `LICENSE` is an exact copy of the
engine Apache-2.0 license: 11,358 bytes, SHA-256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
`NOTICE.md` and `docs/CONTENT_PROVENANCE.md` record
Jeffrey Martin as the supplied image's author/rights owner for this repository
and identify both source and destination hashes. If that assertion cannot be
confirmed by the owner at Gate P, the image is omitted through a new reviewed
plan; it is not substituted.

The exact `NOTICE.md` body is:

```text
# Notice

Yakherd Concierge
Copyright 2026 Jeffrey Martin

Licensed under the Apache License, Version 2.0. See LICENSE.

The yakherd2.png artwork was supplied by Jeffrey Martin for Yakherd and is distributed with this repository under the same Apache-2.0 license.
```

It uses LF and one terminal LF. `docs/CONTENT_PROVENANCE.md` repeats that
statement and the literal source/destination paths, byte length, SHA-256, source
Git blob `79fecd4306c7065c72846eaf0507293c191fff19`, source engine commit bound by
Gate R, copy operator/task ID, and copy/read-back result; it contains no other
asset.

## 6. Exact runtime resource and egress policy

The site has no runtime networking JavaScript. `content.v1.js` is ASCII LF,
has one terminal LF, and exports one frozen object named `CONTENT_V1` with
exactly these keys in this source order: `highStakesTermsBase64`,
`interviewBase64`, `promptTemplateBase64`, `releaseBase64`, and
`secretPatternsBase64`. Each value is one literal canonical RFC 4648 base64
string: padding is present exactly when RFC 4648 requires it, and no whitespace
or alternate alphabet is allowed. The values bind the exact bytes of the five
`site/data/*` source files. `verify_static.py` and
`test_content_binding.py` decode each export with
strict base64 validation and require byte-for-byte equality with the source
file. Application code imports the module and decodes it in memory. It never
calls `fetch`.

Permitted browser-initiated requests are only initial navigation and the
following same-origin static subresources referenced by literal relative paths:

- `assets/styles.css`;
- the listed JavaScript modules reachable from `assets/app.js` or
  `assets/concierge.js` by literal relative import;
- `assets/yakherd2.png` on pages that display it.

The interactive run begins only after all modules and embedded content bytes
are synchronously available and validated. From that ready state through ZIP
download, application code creates no request. Download uses a same-document
Blob URL created from locally computed bytes, immediately removes the anchor,
and revokes the Blob URL in a queued cleanup after the click. The user is told
that the downloaded file leaves browser-managed page memory and is controlled
by the browser and operating system.

The exact meta CSP on every HTML page is:

```text
default-src 'none'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; img-src 'self' blob:; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

`blob:` is restricted to `img-src` only if a locally generated image preview is
actually required. This plan does not require one, so implementation must omit
`blob:` and use `img-src 'self'`; Blob downloads are navigation/download
objects and do not require `img-src`. The resulting required literal is:

```text
default-src 'none'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; img-src 'self'; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

The later host response adds `frame-ancestors 'none'`; the meta policy must not
claim to enforce it. Later response headers also add `X-Content-Type-Options:
nosniff`, `Referrer-Policy: no-referrer`, and the selected HTTPS policy.

No HTML form element is used. All controls are buttons, inputs, textareas,
selects, fieldsets, and ordinary links. Exact external navigation allowlist:

- `https://github.com/gigajeff/Yakherd`
- the Gate R GitHub `v1.2.0` release URL;
- the Gate R PyPI `1.2.0` URL.

External links are static literals, are never constructed from user data, use
`target="_blank"`, and use `rel="noopener noreferrer external"`. The Concierge
run screen contains no external link between the first answer and the download
result; help opens as same-origin page navigation only after an explicit user
action and warns that navigation may lose memory-only state.

Because informational pages must work without JavaScript,
`site/next-steps.html` contains the literal Gate R tag, commit, artifact names,
lengths, hashes, URLs, and commands. `verify_static.py` extracts those fixed
text/anchor values and requires equality with `yakherd_release.v1.json`; it
also requires the home GitHub anchor to equal the allowlist. No runtime code
sets or changes an external `href`.

All JavaScript source must be UTF-8 LF, ASCII except literal UI content imported
from the bound data module, and must use only literal relative imports. Dynamic
`import()`, import maps, inline scripts, inline event handlers, source maps,
`eval`, `Function`, string timers, HTML parser sinks, prototype mutation, and
computed access to browser-global capabilities are forbidden.

The verifier fails on any source occurrence or encoded equivalent of:

- `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`,
  `RTCPeerConnection`, `WebTransport`, `importScripts`, `Worker`,
  `SharedWorker`, `serviceWorker`, `navigator.share`, `window.open`,
  `location.assign`, `location.replace`, `document.write`, `innerHTML`,
  `outerHTML`, or `insertAdjacentHTML`;
- `http:`, `https:`, protocol-relative URLs, `data:`, or remote schemes outside
  the three exact static anchor literals and the identical Gate R GitHub/PyPI
  values in `yakherd_release.v1.json`; the verifier strictly decodes every
  `content.v1.js` base64 export and applies the same rule to those bound bytes;
- HTML `form`, `iframe`, `object`, `embed`, `audio`, `video`, `source`, `track`,
  `portal`, `base`, `meta http-equiv="refresh"`, preload, prefetch, prerender,
  modulepreload, or service-worker registration;
- CSS backslash, `url(`, `image-set`, `src:`, `expression`, or `behavior`.
  The only permitted at-rules are the literal media queries
  `@media (prefers-reduced-motion: reduce)` and
  `@media (forced-colors: active)`; `@import`, `@font-face`, `@supports`,
  `@keyframes`, and every other at-rule fail.

The verifier is a conservative tripwire, not a proof of arbitrary JavaScript
semantics. Gate S separately performs exact-source human review and runtime
request interception. The public copy says the design and CSP prevent the site
code from intentionally transmitting entered text; it does not claim that a
test or browser can mathematically prove all platform behavior.

Safe user-text sinks are exactly textarea/input `.value` and ordinary node
`.textContent`. User text never enters HTML, an attribute, a URL, CSS, a log,
an exception message, a filename, a test artifact, or evidence. Console calls
are forbidden in production source. Error UI uses fixed error codes and fixed
copy only.

The one runtime attribute exception is the ephemeral download anchor: `href`
receives an opaque browser-created Blob URL and `download` receives the fixed
prefix plus prompt-hash prefix from Section 11. Neither attribute contains
prompt text. The Blob itself intentionally contains the locally computed ZIP,
as disclosed to the user.

## 7. Exact interview and prompt assembly

`interview.v1.json` is canonical UTF-8 JSON with LF and one terminal LF. It has
schema `yakherd-interview-v1`, question count 11, and this fixed order:

1. `product_summary`: "What are you hoping to make?"
2. `audience`: "Who is it for?"
3. `core_actions`: "What are the three to seven most important things a user should be able to do?"
4. `data_stored`: "What information will it store, read, or change?"
5. `platforms`: "Where should it run?"
6. `hard_constraints`: "What rules, tools, budget, deadline, or technical limits are non-negotiable?"
7. `non_goals`: "What should this first version deliberately not do?"
8. `success_criteria`: "How will you know the first version works?"
9. `assumptions`: "What assumptions are you making? Leave blank if none."
10. `risks_open_questions`: "What worries you, and what is still undecided?"
11. `high_stakes`: "Could failure affect health, legal rights, money, physical safety, or essential services?"

The top-level object has exactly `questions`, `schema_version`, and `tree_id`;
their values are the question array, integer `1`, and string
`yakherd-interview-v1`. Each of questions 1-10 has exactly `answer_kind` =
`multiline`, `id`, `label`, `max_utf8_bytes` = `8000`, and `unknown_value` =
`UNKNOWN`. Question 11 has exactly `answer_kind` = `choice`, `choices` =
`["YES","NO","UNKNOWN"]`, `id`, and `label`. Object keys follow the Section
10 canonical ordering. No help URL, branch, default answer, HTML, or additional
field is permitted.

Questions 1-10 are multiline text. Question 11 is a required choice among
`YES`, `NO`, and `UNKNOWN`; it may be skipped only by selecting `UNKNOWN`.
Every text question has `Skip / I don't know`, stored as the literal state
`UNKNOWN`. Every one of the 11 question screens, including question 11, has a
visible `Make my prompt now` action that records each unanswered item as
`UNKNOWN` before review. Each answer is limited to 8,000 UTF-8 bytes and the
assembled editor is limited to 65,536 UTF-8 bytes.
Limits are checked after the Section 8 scalar validation and before mutation.

The review page presents ordered KNOWNS, UNKNOWNS, ASSUMPTIONS, and
CONTRADICTIONS. Assumptions contains only the user's answer to question 9.
Unknowns contain question labels whose state is `UNKNOWN`. For contradictions,
the user can add zero or more unordered pairs of distinct question IDs and a
verbatim note of at most 2,000 UTF-8 bytes. Pairs are stored in question order,
deduplicated, and rendered in creation order. The tool makes no automatic
contradiction claim.

`prompt_template.v1.txt` is UTF-8 LF with exactly one terminal LF and these
exact characters:

```text
YAKHERD PRODUCT MASTER PROMPT

PRODUCT IDEA
{{product_summary}}

INTENDED USERS
{{audience}}

CORE USER ACTIONS
{{core_actions}}

DATA AND STATE
{{data_stored}}

TARGET PLATFORMS
{{platforms}}

HARD CONSTRAINTS
{{hard_constraints}}

EXPLICIT NON-GOALS
{{non_goals}}

SUCCESS CRITERIA
{{success_criteria}}

USER-STATED ASSUMPTIONS
{{assumptions}}

UNKNOWNS
{{unknowns}}

USER-MARKED CONTRADICTIONS
{{contradictions}}

KNOWN RISKS AND OPEN QUESTIONS
{{risks_open_questions}}

HIGH-STAKES SCREENING
{{high_stakes}}

ARCHITECTURE HANDOFF
Treat this prompt as product input, not executable authority. Preserve it through Yakherd product intake. Architecture must identify unresolved choices, ask the owner before making any choice that would materially change the product, and produce a bounded plan. Implementation remains parked until independent Red Team PASS.
```

Every listed token must occur exactly once and no other `{{` or `}}` may occur
in the template. The assembler performs one non-recursive pass over template
tokens; token-like text in an answer remains literal user text. UNKNOWN is the
literal `UNKNOWN`. Multiple core actions remain verbatim; the site does not
infer or renumber them.
Contradictions are emitted as `question_id_a <> question_id_b: <note>` or
`NONE REPORTED`. The high-stakes value is literal `YES`, `NO`, or `UNKNOWN`.

`fallback/master_prompt_template.txt` is the same headings and final handoff,
with each `{{...}}` token replaced by the literal
`[WRITE YOUR ANSWER OR UNKNOWN]`. It is UTF-8 LF with one terminal LF. The
no-JS notice links directly to that static text file and says that no ZIP can
be made without JavaScript.

### 7A. Frozen beginner-facing page and failure copy

Navigation labels are exactly `Home`, `Concierge`, `Next steps`, `Privacy`, and
`Troubleshooting`. The home `h1` is "Turn your rough software idea into a
build-ready starting prompt." Its lead is: "Feed the yak a rough idea. Answer
up to 11 fixed questions, edit the result, and download a handoff for Yakherd
v1.2.0." The privacy line is: "No account and no AI call. The site code does
not intentionally send what you type over the network. Your host, browser,
device, clipboard, and downloaded files have separate privacy boundaries."
The primary CTA is exactly `Feed the yak your idea`; secondary links are
`How it works` and `View Yakherd on GitHub`. The mascot caption is "Idea in.
Prompt bundle out." It does not animate approval, code execution, or shipping.

The Concierge page and download result show this directive-required disclaimer
verbatim:

```text
This tool creates a starting prompt and a handoff file. It does not install Yakherd, run any code, or approve anything. Your Yakherd project's Architecture and Red Team roles still review everything.
```

Before any input control is enabled, Concierge requires
`window.isSecureContext === true`, `globalThis.crypto` to exist, and
`typeof globalThis.crypto.subtle?.digest === "function"`. Failure enters a
terminal no-input state; the app does not read stored session text or render an
editor. Exact failure copy: "This browser context cannot make the SHA-256
checks required for a safe bundle. Open yakherd.dev over HTTPS or use localhost
with a current browser. You can still use the plain master-prompt template."
The only actions are same-origin `Troubleshooting` and
`Open the plain template`. `file:` is unsupported even if a particular browser
exposes WebCrypto there. Any digest rejection later revokes approval and stops
copy/download with fixed error code `HASH_UNAVAILABLE`; no fallback hash is
implemented.

The Next steps page begins: "Your ZIP is a handoff, not an installer. Keep it
private if your idea is private." It shows the complete Gate R artifact names,
lengths, hashes, GitHub release URL, and PyPI version URL, then these literal
command templates:

```text
Windows PowerShell
py --version
git --version
py -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
Get-FileHash -Algorithm SHA256 ".\<WHEEL_FILENAME>"
py -m pip install --no-index --no-deps ".\<WHEEL_FILENAME>"
yakherd init --target "C:\dev\my-project" --project-name "my-project" --dry-run
yakherd init --target "C:\dev\my-project" --project-name "my-project"

macOS shell
python3 --version
git --version
python3 -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
shasum -a 256 "./<WHEEL_FILENAME>"
python3 -m pip install --no-index --no-deps "./<WHEEL_FILENAME>"
yakherd init --target "$HOME/dev/my-project" --project-name "my-project" --dry-run
yakherd init --target "$HOME/dev/my-project" --project-name "my-project"

Linux shell
python3 --version
git --version
python3 -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
sha256sum "./<WHEEL_FILENAME>"
python3 -m pip install --no-index --no-deps "./<WHEEL_FILENAME>"
yakherd init --target "$HOME/dev/my-project" --project-name "my-project" --dry-run
yakherd init --target "$HOME/dev/my-project" --project-name "my-project"
```

At Gate R, `<WHEEL_FILENAME>` is replaced by the one literal reviewed wheel
filename; no angle-bracket placeholder ships. Adjacent copy says: "Compare the
printed SHA-256 with the wheel SHA-256 shown above. Stop if any character
differs. Then replace the example project path and name with your own.
Use a folder that does not exist or is empty. Read the dry-run result before
running the final command. Do not point fresh install at an existing project."
It then gives the exact seven numbered `OPEN_IN_CODEX.txt` steps from Section
9. It never says the site ran a command or created a repository.

The Privacy page uses the exact six boundary bullets in Section 13 and this
heading: "The site code does not intentionally send your idea. Copy, save,
download, browser, and device behavior have separate boundaries." It avoids
the absolute words "anonymous", "never retained", and
"nothing leaves the browser". The optional-save panel uses the exact storage
success/failure language in Section 13.

The Troubleshooting page contains these fixed problem headings and actions:

- `JavaScript is off`: use the plain template; ZIP creation is unavailable.
- `Secure hashing is unavailable`: use HTTPS or localhost in a current browser;
  do not proceed from `file:` or an insecure remote origin.
- `The download was blocked`: keep the approved page open, allow this one
  download in browser controls, and retry; the site cannot inspect the browser's
  download folder.
- `Copy did not work`: select the visible text and use the operating system's
  copy command; clipboard history or sync is outside the site's control.
- `Saved data could not be verified or deleted`: manage storage for this site
  in browser settings; the page cannot claim the data is gone.
- `Yakherd did not create all five roles`: return to the installed
  `START_HERE.md`, report the missing role, and do not pretend startup passed.
- `The pinned release is unavailable`: stop; do not install another release or
  use a branch in its place.

The 404 page says: "That page is not in this static release." and provides only
same-origin Home and Concierge links. The post-intake plan must include an
exact copy inventory for every other label, error, help paragraph, button,
link, command, `aria-label`, and live-region announcement before Gate I. No
user-facing prose is left to Implementation discretion.

## 8. Editor, Unicode, approval, and copy contract

The browser textarea value is the approval domain. Browsers expose a Unicode
string, not user-authored bytes. The UI states that textarea line breaks are LF
before approval. The site rejects any carriage return code point and any
unpaired UTF-16 surrogate. It performs no Unicode normalization. It encodes the
accepted scalar string with `TextEncoder` UTF-8, without BOM. Those exact bytes
are the approved prompt bytes. Empty prompt and prompt over 65,536 UTF-8 bytes
are rejected.

The site also rejects a prompt containing either exact delimiter as a complete
LF-delimited line:

- `MASTER PROMPT START`
- `MASTER PROMPT END`

This closes the v1.2.0 intake collision. Substrings that are not complete lines
are allowed.

Approval is one reducer transition. It requires the native checkbox to be
currently checked and the exact fixed statement visible:

```text
I wrote or reviewed this prompt and I approve this exact text.
```

The transition validates the string, captures the string, UTF-8 bytes, byte
length, SHA-256, a complete bundle-input fingerprint, and the checkbox state;
then makes the textarea read-only. The approval record is valid only while all
captured values still compare equal. The Download button re-encodes and
re-hashes immediately before bundle construction and fails closed on mismatch.

Approval first performs the Section 12 secret scan. A clean result continues.
A positive result enters `AWAITING_SECRET_ACK`, remains unapproved, leaves the
editor unlocked, shows the exact spans, and offers Edit (default) or the fixed
acknowledgment. Checking that acknowledgment records it only for the current
prompt SHA-256; the user must press Approve again. Approval then reads the
injected/current clock exactly once, after text, secret, and high-stakes
validation and before committing the transition. It converts that
value to the Section 10 `generated_at`; an invalid clock or conversion failure
leaves the state unapproved. Time passing after approval does not alter the
captured timestamp. The snapshot retains the exact editor JavaScript string,
an immutable copy of its UTF-8 bytes, and this canonical fingerprint object:

```text
approval_statement
checkbox_checked
editor_bytes
editor_sha256
generated_at
high_stakes_acknowledged
high_stakes_flagged
initial_draft_sha256
prompt_edited_by_user
release_pin_sha256
secret_acknowledged
secret_flagged
secret_scan_sha256
tool_version
yakherd_target_release
```

`checkbox_checked` is literal true. `editor_bytes` is the integer UTF-8 byte
count from 1 through 65,536. `initial_draft_sha256` is SHA-256 over the initial
draft encoded under the same Section 8 scalar/no-normalization/UTF-8 rules.
`secret_flagged` is the scan boolean;
`secret_acknowledged` is true exactly when flagged and the fixed acknowledgment
was checked for the same prompt hash, otherwise false. `secret_scan_sha256`
binds a Section 10 canonical JSON object with exactly `matches`,
`prompt_sha256`, and `schema_version` = 1. `matches` is an array in merged-range
order; each row has exactly `detector_ids`, `end_utf16`, and `start_utf16`.
Offsets are nonnegative integers, end is greater than start, and detector IDs
are unique in the Section 12 detector order. A clean result has `matches: []`.
Matched text and display labels are not retained in this object. The canonical
bytes have one terminal LF. All hashes are 64 lowercase hex.
`release_pin_sha256` binds the exact canonical
`yakherd_release.v1.json` bytes. At download, the reducer reconstructs this
object from current state while retaining only the captured `generated_at`,
serializes it under Section 10, reruns both scans, and requires exact byte
equality with the captured fingerprint plus exact editor-string/UTF-8-byte
equality. There is no object-identity shortcut.

Every transition that can alter editor text, answers, contradictions,
high-stakes state, acknowledgment, release pin, restored
state, or tool version revokes approval first, clears the checkbox, clears the
snapshot, and disables download. The only route back to editing is an explicit
`Edit prompt` action that revokes approval before removing read-only state.
Checkbox deselection also revokes approval. Program code cannot assign the
editor value outside the reducer/render module. Tests invoke the shipped event
handlers and reducer, not replicas.

Once approval commits, the approval, secret, and high-stakes checkboxes are
disabled. `Edit prompt` is the only route that re-enables them, and it revokes
the snapshot before doing so.

Copy actions are native user actions with this exact disclosure adjacent:
"Copying places this text on your device clipboard. Yakherd Concierge cannot
erase clipboard history or synced clipboard copies." A failed Clipboard API
write is reported without claiming success; the visible textarea remains
selectable for manual copy. Copy never creates approval. Download requires a
valid approval snapshot.

## 9. Exact v1.2.0 handoff and bundle file bytes

`site/data/yakherd_release.v1.json` is incomplete and Gate I must not begin
until Gate R has supplied every exact public value listed in Section 4. It is a
canonical object with keys:

```text
engine_commit
github_release_url
manifest_bytes
manifest_sha256
package_readme_bytes
package_readme_sha256
product_intake_bytes
product_intake_sha256
pypi_version_url
release_json_bytes
release_json_sha256
root_readme_bytes
root_readme_sha256
sdist_bytes
sdist_filename
sdist_sha256
sdist_url
start_here_bytes
start_here_sha256
tag
version
wheel_bytes
wheel_filename
wheel_sha256
wheel_url
```

The fixed `tag` is `v1.2.0` and fixed `version` is `1.2.0`. No blank,
placeholder, `latest`, redirect-only, branch, abbreviated hash, or unverified
value is permitted. The data module must byte-bind this file like the other
data resources.

The approved prompt bytes are `P`. `MASTER_PROMPT.txt` is exactly `P`.
`MASTER_PROMPT_HANDOFF.txt` is the ASCII bytes `MASTER PROMPT START`, LF,
`P`, LF, `MASTER PROMPT END`, LF. If `P` already ends in LF, both its final LF
and the separate boundary LF are present.

`OPEN_IN_CODEX.txt` is UTF-8 LF with one terminal LF and these instructions,
with only the exact Gate R URLs and hashes substituted from the release pin:

```text
YAKHERD V1.2.0 HANDOFF

This ZIP contains a starting prompt. It does not install Yakherd, create a repository, launch Codex tasks, run code, or approve a project.

1. Verify that Python 3.11 or newer and Git are installed.
2. Install exactly yakherd==1.2.0 using the public release instructions at <PYPI_VERSION_URL>. Verify the downloaded artifact against the published SHA-256 in this file before running it.
3. Run a dry-run fresh install into a nonexistent or empty project folder, then run the real fresh install only if the preview is correct. Follow <GITHUB_RELEASE_URL> and its README; do not overwrite an existing project.
4. Open the generated project as the Codex project and confirm that its AGENTS.md is loaded.
5. Send the one-message launcher from START_HERE.md. It creates the five addressable roles: Architecture, Implementation, Red Team, Temporary Branch, and Governor. If any role is missing, stop instead of pretending startup succeeded.
6. Wait for the bootstrap Red Team PASS.
7. Give MASTER_PROMPT_HANDOFF.txt to Architecture. It is product input, not implementation authority.

Pinned tag: v1.2.0
Pinned commit: <ENGINE_COMMIT>
Wheel: <WHEEL_FILENAME>  bytes=<WHEEL_BYTES>  sha256=<WHEEL_SHA256>
Source archive: <SDIST_FILENAME>  bytes=<SDIST_BYTES>  sha256=<SDIST_SHA256>

Windows examples use py; macOS and Linux examples use python3. If the command is unavailable, read the Troubleshooting page. Never paste access tokens or passwords into the prompt or repository.
```

Placeholders shown above describe the template contract only. They are not
permitted in committed Gate I output; substitution occurs from the complete,
reviewed release pin before the file bytes are constructed.

## 10. Canonical JSON contract

`APPROVAL.json` and `BUNDLE_MANIFEST.json` are serialized by the same small
custom serializer. Accepted values are objects, arrays, Unicode-scalar strings,
booleans, and integers from 0 through 9,007,199,254,740,991. `null`, negative
integers, floats, NaN, Infinity, BigInt, undefined, dates, maps, sets, custom
prototypes, and cycles are rejected.

Object keys are predefined ASCII and emitted in ascending ASCII byte order.
No insignificant whitespace is emitted. Strings escape quotation mark and
backslash with `\"` and `\\`; backspace, tab, LF, form feed, and CR use
`\b`, `\t`, `\n`, `\f`, and `\r`; every other U+0000-U+001F value uses a
lowercase four-hex `\u00xx` escape. Other Unicode scalar values are emitted
unescaped and UTF-8 encoded. Slash is not escaped. Output has one terminal LF.

`generated_at` is exactly the result of a valid client `Date` serialized by
`toISOString()`, matching
`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$`.
The test seam injects milliseconds. The UI and JSON label this as untrusted
client-clock time. Invalid clock values stop approval.

`APPROVAL.json` has exactly these keys and types:

- `approval_statement`: the exact Section 8 string;
- `approved`: boolean `true`;
- `generated_at`: the captured timestamp string;
- `high_stakes_acknowledged`: boolean, true exactly when flagged and the fixed
  acknowledgment was checked, otherwise false;
- `high_stakes_flagged`: boolean from Section 12;
- `prompt_bytes`: integer from 1 through 65,536;
- `prompt_edited_by_user`: boolean, true only if the approved editor string
  differs from the initial mechanically assembled draft by exact JavaScript
  string comparison;
- `prompt_sha256`: 64 lowercase hex characters over `MASTER_PROMPT.txt`;
- `schema_version`: integer `1`;
- `timestamp_source`: string `client`;
- `tool`: string `yakherd-concierge`;
- `tool_version`: string `1.0.0`;
- `yakherd_target_release`: string `v1.2.0`.

No other field is permitted. The serializer sorts them; the order above is
descriptive, not a second serialization order.

`BUNDLE_MANIFEST.json` has exactly `bundle_schema_version`, `files`, and
`yakherd_target_release`. Schema version is `1`. `files` lists the other four
files, not the manifest itself, in this fixed order:

1. `MASTER_PROMPT.txt`
2. `MASTER_PROMPT_HANDOFF.txt`
3. `APPROVAL.json`
4. `OPEN_IN_CODEX.txt`

`bundle_schema_version` is integer 1 and `yakherd_target_release` is string
`v1.2.0`. Each entry has exactly `bytes` (integer 0 through 262,144), `path`
(one of the four literal ASCII names), and `sha256` (64 lowercase hex). The
manifest serializer still sorts each object's keys; array order remains fixed.

## 11. Exact ZIP32 Store-only contract

The archive contains exactly the five directive filenames in fixed order, with
`BUNDLE_MANIFEST.json` fourth and `OPEN_IN_CODEX.txt` fifth. Names are literal
ASCII but the UTF-8 flag is set. Each entry is Store-only and its bytes are the
bytes defined above.

All integers are little-endian. Local header values:

- signature `0x04034b50`;
- version needed `20`;
- general-purpose flags `0x0800` only;
- compression method `0`;
- DOS time `0x0000` and DOS date `0x0021` (1980-01-01 00:00:00);
- IEEE CRC-32, compressed size, and uncompressed size in the header;
- filename byte length and filename bytes;
- extra-field length `0`; no data descriptor.

Central header values:

- signature `0x02014b50`;
- version made by `0x0314` (Unix, ZIP 2.0);
- version needed, flags, method, time, date, CRC, sizes, name length, and name
  bytes identical to the local values;
- extra length `0`, comment length `0`, disk start `0`, internal attributes
  `0`, external attributes `0x81a40000` (regular file mode 0644), and the exact
  local-header offset.

EOCD values:

- signature `0x06054b50`;
- disk number and central-directory disk `0`;
- entry counts `5` and `5`;
- exact central-directory size and offset;
- comment length `0` and no comment.

CRC-32 uses reflected polynomial `0xedb88320`, initial value `0xffffffff`, and
final XOR `0xffffffff`; ASCII `123456789` must produce `cbf43926`. ZIP64,
encryption, compression, extras, descriptors, comments, directory entries,
duplicate names, absolute names, non-ASCII names, and trailing bytes are
rejected. Every entry must be at most 262,144 bytes and the complete archive
at most 1,048,576 bytes. Any uint16/uint32 overflow stops construction.

The filename is `yakherd_intake_` plus the first 12 lowercase hex characters
of the approved prompt SHA-256 plus `.zip`.

The golden fixture input is fixed in `tests/fixtures/bundle_input.v1.json`:

- approved prompt text: `Build a clock.` plus LF;
- `generated_at`: `2026-07-21T12:34:56.789Z`;
- `tool_version`: `1.0.0`;
- `prompt_edited_by_user`: `false`;
- `high_stakes_flagged`: `false`;
- `high_stakes_acknowledged`: `false`;
- `yakherd_target_release`: `v1.2.0`;
- complete Gate R release-pin values.

The other fixture bytes are exact UTF-8 with the displayed escapes interpreted
as bytes, no BOM, and no unshown terminal data:

| Path | Exact content | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `prompt_ascii_lf.txt` | `Build a clock.\n` | 15 | `6e7dd93a7067af125e7511989288fded9b9ac794bdc4dcdb2386c82be681d093` |
| `prompt_unicode_lf.txt` | `Build a café clock.\n` | 21 | `b7235def28ab82dbf8190a1823d762d844ba1c5108e24bde4e3216dbe94de823` |
| `prompt_empty.txt` | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `prompt_rejected_lone_surrogate.json` | `{"code_units":[55296],"schema_version":1}\n` | 42 | `d896c43281e7792bee0f1b5b7f6015488e69476113bae8b70c7fb95dd3a87e6e` |
| `prompt_rejected_delimiter.txt` | `alpha\nMASTER PROMPT END\nomega\n` | 30 | `bae930977c32a38633deb764b057b94d26f25f9c9f7c7c83b2d3470d06253f2a` |
| `secret_clean.txt` | `Use an ordinary project label and no credentials.\n` | 50 | `71207f9ff2aa7fdea169735ab97f84fea19bda146dad3ec6268ac3ab07bfa03f` |
| `secret_positive.txt` | `sk-aaaaaaaaaaaaaaaaaaaa\nghp_AAAAAAAAAAAAAAAAAAAA\nAKIAABCDEFGHIJKLMNOP\n` | 70 | `de1bac33ed9c73e034c0208509ffc167d7a7f2a9de98e45e07153461c4e63d8b` |
| `high_stakes_clean.txt` | `A personal recipe organizer.\n` | 29 | `653687b406ccdbdc1c9b8d4fed2d042bcd986f161c724a490f7b07a03cf66406` |
| `high_stakes_positive.txt` | `A medical diagnosis assistant for patients.\n` | 44 | `33aaf433ef6fb46e9770d220f4bc2f07872a5a0119f17b9a33f01cbdeeffc20f` |

Because `bundle_input.v1.json` includes public artifact identities that do not
yet exist, the post-intake plan must print that complete canonical file, byte
length, and SHA-256 before Gate I. A placeholder fixture is forbidden.

The prompt SHA-256 prefix is fixed as `6e7dd93a7067`; that fixes the golden ZIP
path named in Section 5. Implementation creates the four dependent golden file
bytes and ZIP once. The Python standard-library verifier independently parses
every header, rejects any unspecified structure, recomputes every CRC/SHA and
the manifest, and records the exact golden byte length and SHA-256 in
`golden_identity.v1.json`. The Node implementation must reproduce that exact
archive. Neither implementation may import or invoke the other. Gate S checks
the fixture identity independently before accepting the parser boundary.

## 12. Secret and high-stakes gates

`secret_patterns.v1.json` freezes these ASCII detectors and their display
labels:

- `private_key`, label `Private-key header`:
  `-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----`;
- `openai_like`, label `API-key-shaped text`: `sk-[A-Za-z0-9_-]{20,}`;
- `github_token`, label `GitHub-token-shaped text`:
  `gh[pousr]_[A-Za-z0-9]{20,}`;
- `aws_access_key`, label `AWS-access-key-shaped text`:
  `AKIA[0-9A-Z]{16}`;
- `jwt_like`, label `JWT-shaped text`:
  `eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}`;
- `password_adjacent`, label `Password- or secret-labeled value`,
  ASCII-case-insensitive:
  `(api[_ -]?key|token|password|passwd|secret)[ \t]*[:=][ \t]*[^ \t\r\n]{8,}`;
- `entropy_token`, label `High-entropy token-shaped text`:
  `[A-Za-z0-9_-]{32,}` only when the matched ASCII string contains an
  uppercase letter, lowercase letter, and digit, has at least 16 distinct
  characters, and no one character occupies more than 25 percent of the
  match. This is deliberately described as a token-shape heuristic, not an
  entropy measurement guarantee.

The file is canonical JSON with exactly `detectors` and `schema_version` = 1.
The detector array is in the order above. Regex detector objects have exactly
`flags`, `id`, `kind`, `label`, and `pattern`; `kind` is `regex`, and `flags`
is either the empty string or `i` only as stated above. The entropy detector
has exactly `alphabet`, `id`, `kind` = `entropy_ascii`, `label`,
`max_dominant_percent` = 25, `min_bytes` = 32, `min_unique` = 16, and
`required_classes` = `["upper","lower","digit"]`. The percentage check is
the exact integer inequality `dominant_count * 100 <= length * 25`. Runtime
constructs only the named fixed regular expressions and adds the global scan
flag itself.

Matching runs on the exact editor JavaScript string. Because all patterns are
ASCII, match offsets are UTF-16 code-unit half-open ranges that begin and end
on ASCII code units. Sort by start, then longer match, then detector order;
merge overlaps into one flagged range while retaining all labels. The warning
shows the exact range through `.textContent`, never HTML, and offers Edit
(default) or a separate `Download anyway` checkbox with exact text: "I
understand this may include a secret and still want to download it." Any edit
clears this acknowledgment. The check occurs before approval as specified in
Section 8; after checking, the user presses Approve again, and download later
requires the same prompt hash and scan result. Detectors are best-effort and
never described as proof that text is secret-free.

`high_stakes_terms.v1.json` contains exactly these ASCII lowercase terms:

```text
diagnosis
medical
medicine
patient
prescription
legal advice
lawsuit
contract rights
investment
financial advice
trading
credit decision
life safety
emergency
industrial control
essential service
```

The file is canonical JSON with exactly `schema_version` = 1 and `terms` = the
array above in that order. Blank, duplicate, uppercase, or additional terms
fail content validation.

Matching uses ASCII lowercase and substring search on answers and the editor;
it performs no locale or Unicode normalization. `high_stakes_flagged` is true
if question 11 is `YES` or a term matches. A short warning is visible for every
user, even when false: "Software can cause harm. If health, legal rights,
money, physical safety, or essential services are involved, use qualified
human experts." When flagged, the site also says: "Yakherd and its agents are
not suitable for regulated or safety-critical products without qualified human
experts. This bundle does not change that." Download is blocked until a
separate checkbox says: "I understand this prompt needs qualified human review
before anyone relies on the resulting software." Editing or changing answers
clears it.

## 13. Honest storage and privacy state machine

Default state is memory-only. Controls use `autocomplete="off"` and
`spellcheck="false"`, but copy states that browsers, extensions, operating
systems, input methods, crash recovery, form restoration, backups, and synced
devices are outside the site's control. The site says: "This page does not
intentionally save your text unless you turn on Save in this browser. Your
browser or device may still restore or retain data. Use Clear this session,
close the tab, and manage downloaded or clipboard copies yourself."

Optional persistence uses `localStorage` only, at the exact origin-scoped key
`yakherd.concierge.v1.session`. IndexedDB, cookies, sessionStorage, Cache API,
URL state, history state, and server state are forbidden. The stored canonical
JSON has exactly these top-level keys and types:

- `answers`: an 11-row array in question order; each row has exactly `id`,
  `state`, and `value`. ID is the fixed question ID, state is `ANSWERED` or
  `UNKNOWN`, and value is a validated scalar string up to 8,000 UTF-8 bytes for
  `ANSWERED` or the empty string for `UNKNOWN`. Zero-length text becomes
  `UNKNOWN`; nonempty whitespace is retained verbatim.
- `contradictions`: an array of rows with exactly `id_a`, `id_b`, and `note`,
  under the ordering, uniqueness, and 2,000-byte rules in Section 7.
- `current_step`: integer 0-13, where 0-10 are questions, 11 is review, 12 is
  editor, and 13 is approval; the download result is never persisted.
- `editor_text`: validated scalar string, empty before drafting and otherwise
  at most 65,536 UTF-8 bytes.
- `expires_at_ms`: nonnegative safe integer.
- `initial_draft`: validated scalar string, empty before drafting and otherwise
  at most 65,536 UTF-8 bytes.
- `saved_at_ms`: nonnegative safe integer.
- `schema_version`: integer 1.

No additional or missing key, row, ID, or type is accepted. The object uses the
Section 10 canonical serializer and is at most 262,144 UTF-8 bytes. It never
stores a valid approval snapshot or either download-anyway acknowledgment;
restoration always requires fresh approval and acknowledgments.

Expiry is `saved_at_ms + 604800000`, based on the untrusted client clock.
Expiry is checked on initial read and every state transition. Invalid JSON,
wrong schema, impossible type/range, expired value, or clock rollback before
`saved_at_ms` causes a best-effort `removeItem` and no restoration. Save claims
success only when `setItem`, immediate `getItem`, and exact string comparison
all succeed. Delete claims success only when immediate `getItem` returns
`null`. Quota, security, read, write, or deletion failure uses fixed truthful
copy: data may remain in browser storage; the site cannot verify deletion.

Turning Save on performs one immediate synchronous save. While enabled, every
successful reducer transition that changes a stored field constructs a new
object, captures `saved_at_ms` from `Date.now()`, derives `expires_at_ms` with
checked safe-integer addition, serializes, bounds, writes, reads, and compares
before the UI says `Saved in this browser for up to seven days`. There is no
timer, debounce, unload handler, or background write. A failed operation turns
autosave off without retry and says: `Save could not be verified. Your current
work is still on this page, and a browser copy may remain.` Turning Save
off or choosing Delete attempts verified removal and says either `Browser copy
deleted and verified` or `Deletion could not be verified; use browser site-data
settings.`

The `storage` event for this exact key from another tab invalidates approval,
stops autosave, and requires an explicit Reload or Keep this tab decision; no
automatic merge occurs. Reload reparses under the same rules. Keep this tab
performs no write until the user explicitly re-enables save.

`Clear this session` revokes approval, clears in-memory state and controls,
attempts and verifies removal of the one key, and reports verified/uncertain
separately. It cannot delete clipboard contents, downloaded files, host logs,
browser history, extensions, backups, or platform restoration state.

The privacy page and adjacent disclosure say, in substance and without broader
claims:

- site application code does not intentionally send typed answers or prompts
  over the network;
- the static host necessarily receives ordinary page/asset requests and may
  retain IP address, user-agent, time, and request metadata under its own
  policy; the site has no client analytics;
- optional save is origin-local browser storage and can fail or be retained by
  the platform;
- copying and downloading are intentional transfers to OS-managed locations;
- handing the file to Codex/Yakherd is a later user action governed by those
  tools, not by this site;
- no account and no site-issued login are used; the word "anonymous" is not
  used as an absolute claim;
- secret and high-stakes checks are local best-effort warnings, not guarantees.

## 14. Gate I verification and acceptance

Permitted prerequisites are an already installed Python 3.11+ and Node 20+
runtime. No package manager or browser is invoked. Exact commands from the
new project root:

```powershell
python -B scripts\verify_static.py
python -B -m unittest discover -s tests -p "test_*.py" -v
node --test tests\test_bytes.mjs tests\test_state.mjs tests\test_canonical_json.mjs tests\test_crc32.mjs tests\test_zip_store.mjs tests\test_scanner.mjs tests\test_storage.mjs tests\test_interview.mjs
git diff --check
```

If Git has not yet been initialized under the separate owner checkpoint, the
last command is recorded `NOT_APPLICABLE_NOT_A_GIT_REPOSITORY`, not silently
substituted. Gate I does not initialize Git.

`verify_static.py` fails unless:

- Section 5 paths 1-61 are present during verification, path 62 (the final
  evidence record) is absent until evidence finalization, and no unexpected
  path exists beneath `site`, `tests/fixtures`, or `tests/golden`;
- all pre-existing Yakherd-installed files, including `scripts/ssot/*` and
  `tests/ssot/*`, still match the installation receipt, while the only new
  child directly under `scripts` is `verify_static.py` and the only new
  product test paths are the exact Section 5 entries;
- every text file is valid UTF-8, follows its required LF/terminal-LF rule, and
  has no BOM or trailing whitespace; HTML/CSS/JS satisfy the Section 6 policy;
- every internal link and subresource resolves to an allowlisted regular file
  inside `site` with no symlink/reparse escape;
- content-module bytes equal all five source data files;
- release pin is complete, canonical, `v1.2.0`, and matches Gate R evidence;
- image and license identities match Section 5;
- no secret fixture value occurs in product, evidence, error text, or generated
  retained output;
- ZIP golden archive satisfies every Section 11 byte rule and its identity
  record;
- total unminified JavaScript is at most 153,600 bytes;
- informational pages contain meaningful main text and navigation without
  JavaScript, and Concierge has the no-JS notice/fallback;
- all pages have one `h1`, named landmarks, labels, logical heading order,
  skip link, language, viewport, meta CSP, no autoplay/motion dependency, and
  no disallowed element/attribute;
- CSS includes visible focus, 320px reflow rules, reduced-motion, forced-colors,
  and declared colors meeting the fixed tested contrast pairs at 4.5:1 or 3:1
  for large text.

Unit tests cover empty/ASCII/Unicode/LF values, surrogate and CR rejection,
every approval-invalidating transition, checkbox deselection, direct shipped
handlers, storage corruption/quota/delete/multi-tab events, delimiter
collision, canonical JSON lexical bytes, CRC fixture, ZIP header/limit
failures, deterministic golden equality, clean and positive secret fixtures,
all high-stakes terms, UNKNOWN handling, contradiction ordering, editor size,
and content binding. Temporary test files use an OS-created unique temp
directory and are removed by the test owner in `finally`; cleanup failure fails
the test and records only the temp basename, never an absolute machine path.

No Gate I test claims cross-browser, screen-reader, host-header, TLS, real fresh
public install, extraction on other operating systems, or deployed behavior.
Those are later gates.

## 15. Exact Gate I evidence and failure behavior

The sole durable Gate I evidence path is
`docs/evidence/concierge_v1_local_implementation.json`. It is canonical JSON,
schema `yakherd-concierge-local-evidence-v1`, and contains:

- reviewed plan path, bytes, and SHA-256;
- authorizing Red Team audit path, bytes, SHA-256, and PASS;
- Gate R evidence identity and complete release pin;
- bootstrap and product-intake evidence identities and PASS audits;
- absolute project root and its non-reparse observation;
- implementation task ID, model, effort, and statement that it was sole writer;
- exact authorized path list;
- before state for all 62 paths (`ABSENT`) and after bytes/SHA-256/type for
  product paths 1-61 only; the evidence object cannot contain its own byte
  length or hash;
- source image and destination identity;
- runtime versions;
- each exact command, exit code, and bounded stdout/stderr SHA-256;
- each acceptance check as `PASS`, `FAIL`, or `NOT_APPLICABLE`, with
  `NOT_APPLICABLE` allowed only for the explicitly named Git check;
- final unexpected-path list, which must be empty for PASS;
- overall status derived as PASS only if every required check is PASS.

The evidence contains no user test prompt other than hashes of the public
non-secret fixtures, no source body, no machine username, no secret, no
absolute temp path, no browser content, no screenshot, and no credential.
Command output is retained only in memory long enough to compute exit status,
bounded last 16 KiB, and SHA-256; the evidence stores a fixed summary and hash,
not raw output. Any command output containing an absolute user-profile path or
fixture secret makes evidence finalization fail.

Implementation never cleans an unknown or pre-existing path. On failure it
stops, records which exclusively created listed paths exist, and asks
Architecture for a recovery plan. It does not retry, delete, overwrite, commit,
reset, move, or publish. Only a separately reviewed recovery plan may remove
created files. A complete PASS evidence file is itself the last authorized
create; if its exclusive create or read-back validation fails, Gate I is FAIL
and Implementation reports in chat without inventing a substitute path.
After successful read-back and schema validation, Implementation reports the
evidence file's byte length and SHA-256 in its handoff message; Red Team
independently reproduces them. Those values are deliberately not embedded in
the file itself.

## 16. Later acceptance requirements retained from the directive

The following remain required for product completion but are intentionally not
part of Gate I:

- identical bundle bytes for the fixed fixture in current Chromium, Firefox,
  and WebKit on at least two operating systems;
- request interception proving only the exact initial same-origin assets load
  and zero requests occur from interactive-ready through download;
- ZIP extraction with default tools on Windows, macOS, and Linux, followed by
  exact hashes;
- a fresh public-artifact `v1.2.0` install and unchanged `product_intake.md`
  bridge preserving prompt length/hash, including terminal LF;
- keyboard-only, 320px reflow, zoom, forced-colors, reduced-motion, and
  qualified screen-reader walkthrough, plus a named automated scanner whose
  installation/capability is separately authorized;
- no-JS and secure-context/insecure-context behavior;
- exact-source security/parser Red Team PASS;
- GitHub, staging, hosting headers, custom error, MIME, caching, compression,
  redirects, public allowlist, rollback, and production evidence;
- staging and production serving the same committed site bytes.

The final Definition of Done is all of the above plus an owner-approved public
release. A plan PASS, local implementation PASS, or staging PASS is not product
completion.

## 17. Stop conditions and forbidden improvisation

Stop without workaround if:

- `v1.2.0` is not public and exactly authenticated;
- its public intake or START_HERE bytes differ from the release pin;
- the target root or a destination is present, ambiguous, or reparse-backed;
- the new task cannot prove installed `AGENTS.md` is active;
- a second writer is active on the same checkout;
- the exact source directive cannot pass unchanged product intake;
- a prompt contains a delimiter line or an unsupported Unicode value;
- deterministic golden ZIP bytes diverge;
- the site would need a network API, third-party resource, dependency, build
  step, backend, inline script, unsafe sink, or unlisted file;
- local novice testing tempts the team to describe fixed logic as AI;
- a test capability is absent;
- an exact public, GitHub, hosting, DNS, credential, staging, deployment,
  rollback, or production fact is unknown.

Do not substitute another release, host, repository, asset, task, framework,
test tool, path, or privacy promise. Return to Architecture for a new exact
candidate and fresh independent review.

## 18. Model routing and handoff

- Mechanical inventories and hashing: Luna medium when available.
- Routine implementation/research: Terra medium/high.
- Architecture or difficult debugging: Sol high/xhigh.
- Final independent security, parser, deployment, or release gate: one Sol
  Ultra agent only. Do not use Ultra for drafting or routine work, and do not
  start a second Ultra agent without owner permission.
- Never run two implementation writers against the same checkout.

Every delegated message states task role, model, effort, routing reason, exact
input hashes, permitted write set, forbidden actions, evidence path, stop
conditions, and whether token usage is task-bounded or continuation-based.

For the current review, Red Team must return PASS or FAIL against this exact
plan and exclusively create only
`docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team.md`.
That path must be absent at entry. On PASS,
Red Team may tell the existing Implementation task only that product work
remains parked pending Gates R/B/P and a correctly attached separate-repo
Implementation task. It must not send Gate I as executable work until those
gates have exact independent PASS evidence.

## 19. Current authority effect

This candidate authorizes only documentation validation and fresh independent
Red Team review. It does not authorize release mutation, Git/tag/GitHub/PyPI,
network or browser action, creation of `L:\dev\yakherd-web`, product intake,
Implementation, dependency use, image copying, evidence-skeleton creation,
credentials, hosting inventory, DNS, staging, deployment, production, or
publication. All prior v15/DreamHost records remain preserved future work and
stay parked.
