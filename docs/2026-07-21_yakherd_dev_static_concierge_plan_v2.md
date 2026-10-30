# Architecture Plan: Yakherd.dev Static Concierge First Release v2

- Date: 2026-07-21
- Status: proposed
- Owner: `docs/2026-07-21_yakherd_dev_static_concierge_plan_v2.md`
- Supersedes: `docs/2026-07-21_yakherd_dev_static_concierge_plan.md`
  as the active static-concierge candidate only
- Superseded by: none
- Authority effect: none until this exact plan receives independent Red Team
  PASS

## Goal

Ship a charming, useful, browser-first Yakherd concierge for an absolute
beginner without first solving hosted model inference, server secrets, dynamic
rate limiting, provider logging, PHP capability, automated GitHub setup, or the
complete Yakherd operating system.

The first release helps a visitor turn a rough software idea into an editable
candidate master prompt by answering a small fixed set of questions. All idea
processing occurs in the loaded browser page. The visitor can review the
candidate, then use site-provided Copy or Download controls to obtain an exact
handoff envelope that the unchanged Yakherd product-intake contract can accept.

This release is a useful front door, not a claim of end-to-end autonomous
building. It does not interrogate with a frontier model, install Yakherd, create
accounts or repositories, launch Codex tasks, approve a prompt on the visitor's
behalf, or deploy software.

## Evidence Read

- `AGENTS.md`
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/RELEASE.md`
- `docs/Yakherd Audit for Absolute Beginners.md`
- `docs/2026-07-21_yakherd_dev_concierge_website_plan.md`
- `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`
- `docs/2026-07-21_yakherd_dev_concierge_website_plan_v13.md`
- `docs/2026-07-21_yakherd_dev_concierge_website_plan_v14.md`
- `docs/2026-07-21_yakherd_dev_concierge_website_plan_v15.md`
- `docs/2026-07-21_yakherd_dev_static_concierge_plan.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_static_concierge_plan_red_team.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v13.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability_red_team.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v14.md`
- `packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md`
- `packages/jeff_strict_ssot_v1/template/docs/prompts/architecture_task.md`
- `packages/jeff_strict_ssot_v1/template/docs/task_protocol.md`

The unchanged product-intake contract is 2,614 bytes with SHA-256
`c1582bcc7918eeb547bcae8d4ceec14cfbe36267ed7313131012b0ba95c32604`.
Any mismatch at implementation or review time makes this plan stale and stops
the slice; it does not authorize a package change.

The v13 plan PASS, exhausted v13 capability FAIL, v14 plan FAIL, unreviewed v15
draft, first static-plan FAIL, and every earlier plan and audit remain immutable
historical evidence. Nothing in this plan changes their bytes or retroactively
changes a verdict. The v15 preflight/retry path is parked indefinitely and
receives no skeleton, browser action, DreamHost action, retry, or further Red
Team cycle under this release scope.

## Invariants And Boundaries

### Product and authority boundary

- The page produces a **candidate master prompt** and a transport envelope. The
  visitor's review checkbox is an acknowledgement for the site's controls, not
  a signature, security boundary, or Yakherd authority transition.
- The candidate acquires no Yakherd authority until the visitor supplies the
  envelope to the Architecture task and the unchanged preservation,
  provenance, extraction, owner-promotion, and independent-review gates pass.
- The page never claims that a prompt has been signed, installed, accepted, or
  reviewed by Yakherd, or that architecture, implementation, a repository,
  backup, or deployment has been created.
- User-entered text is inert data. It is never evaluated as HTML, Markdown,
  JavaScript, a URL, or an instruction to the website.
- The audited installer and package remain product-neutral, standard-library-
  only, no-network, no-Git, no-automation, and otherwise unchanged.
- No file under `packages/jeff_strict_ssot_v1/` is in the Implementation write
  set. Package manifests, release hashes, tests, and distribution metadata are
  out of scope.

### Static-only trust boundary

- Production-capable source consists only of repository-owned HTML, CSS,
  JavaScript, and SVG.
- There is no PHP, server application, model call, API endpoint, secret,
  database, authentication, analytics, advertising, telemetry, third-party
  font, remote image, package manager, service worker, or build dependency.
- The only automatic requests made by site code are the initial same-origin
  GETs for the exact HTML, CSS, JavaScript module, imported JavaScript module,
  and SVG paths in the reviewed public allowlist. They contain no visitor data,
  query, or generated fragment.
- Site JavaScript uses no cookies, `localStorage`, `sessionStorage`, IndexedDB,
  Cache API, browser history, URL query, or URL fragment for visitor input.
- No input is placed in a URL. No HTML form element or form submission exists.
  All action buttons have `type="button"`, and CSP sets `form-action 'none'`
  and `connect-src 'none'`.
- Clipboard access is a user-initiated transfer to the operating-system/browser
  clipboard and may be retained or synchronized outside site control. If the
  site-provided copy action is unavailable or denied, the candidate remains
  selectable; the visitor may review it again and use Download Handoff.
- Native keyboard, context-menu, accessibility-tool, extension, or browser copy
  from the editable textarea cannot be prevented and is not gated by the review
  checkbox. The page says that a native copy contains only the candidate and
  may lack the required Yakherd envelope.
- Site-provided download uses a browser-created UTF-8 text Blob and a temporary
  object URL. Its creation, click, cleanup, and failure rules are exact below.
- The site does not intentionally persist or transmit visitor text. It cannot
  guarantee erasure by browser form restoration, BFCache, crash/session
  recovery, autofill, extensions, input methods, clipboard history/sync,
  screenshots, operating-system memory, or downloaded files. The privacy page
  discloses those boundaries before making any deletion claim.
- Normal host access logs may record page requests and network metadata, but
  site code sends no idea, answer, candidate, or envelope to the host.

### Beginner and safety boundary

- The first screen uses plain language and contains one primary call to action:
  `Tell the yak your idea`.
- It says before the first field: do not paste passwords, private keys, API
  keys, access tokens, medical records, or other information the visitor is not
  comfortable keeping on the current device.
- Only the rough idea is required. Every follow-up permits an empty answer and
  explains that Yakherd will mark it as unresolved rather than inventing one.
- `Make my prompt now` is available throughout the questions after a nonempty
  idea exists.
- The candidate is an editable plain-text `<textarea>`. The visitor must select
  `I reviewed this draft and want the site to prepare my Yakherd handoff` before
  the site's Copy Handoff or Download Handoff buttons are enabled.
- The checkbox gates only those two site controls. It does not prevent native
  copying and is not described as access control.
- `Clear everything` clears all visible controls, the output, validation
  messages, and in-memory approval snapshot in the current document. It does
  not claim to wipe browser, clipboard, download, extension, or OS retention.
- External links are visibly labeled as leaving Yakherd.dev, never initiate an
  account or mutation, and are limited in this slice to:
  `https://github.com/gigajeff/Yakherd` and
  `https://pypi.org/project/yakherd/`.
- A fixed warning is shown for every generated result: medical, legal,
  financial, security-critical, and safety-critical projects require qualified
  human review; this candidate is only a planning aid. No content
  classification, diagnosis, or safety conclusion occurs.

### Accessibility and presentation boundary

- Target WCAG 2.2 AA for the implemented experience, with semantic landmarks,
  explicit labels and instructions, useful heading order, keyboard-only
  operation, visible focus, associated errors, a polite result status region,
  sufficient contrast, and no color-only meaning.
- The layout remains usable at 320 CSS pixels and 400% zoom without loss of
  content or two-dimensional page scrolling.
- Every pointer target is at least 24 by 24 CSS pixels unless an allowed WCAG
  exception is documented in evidence.
- Animation is decorative, never communicates the only copy of state, and is
  disabled under `prefers-reduced-motion: reduce`.
- The visual motif is a friendly original SVG yak. An idea card moves toward
  the yak and a prompt card appears behind it when the visitor generates a
  result. Text describes the state independently; the mascot is decorative and
  hidden from the accessibility tree.
- Copy may be playful (`Feed the yak`, `Fresh prompt`) but must not shame the
  visitor, sexualize the theme, obscure the result, or substitute humor for a
  privacy/authority disclosure.
- No existing multi-megabyte PNG is copied into the website release. The full
  public tree is at most 250,000 bytes before transfer encoding, and no
  individual public file exceeds 100,000 bytes.

## Options And Tradeoffs

### Option A: informational landing page

This has the smallest attack surface but leaves the most important beginner
gap untouched: a visitor still has no help turning an idea into a useful
prompt.

### Option B: deterministic client-only prompt builder

This supplies immediate value while retaining a static hosting and privacy
boundary. It cannot adaptively interrogate, judge contradictions, or improve
the prompt with a model. Selected for the first release.

### Option C: hosted model concierge

This could ask adaptive questions, but it reintroduces the exact provider,
secret, abuse, cost, logging, consent, PHP capability, and rollback system that
consumed v3-v15. Deferred until real use of the static release proves that the
extra value justifies a separately funded and separately reviewed product.

### Option D: automated Codex or GitHub handoff

This would reduce later friction but adds account identity, authorization,
visibility, repository mutation, deep-link, and client-version boundaries.
Deferred. The first release provides honest copy/download instructions only.

## Decision

### Visitor journey

1. The visitor reads a one-sentence promise and the local-processing/no-secrets
   notice.
2. The visitor enters a rough idea of 1-8,000 JavaScript UTF-16 code units.
3. The page presents eight optional prompts, organized into short, skippable
   groups: `audience`, `outcome`, `must_haves`, `boundaries`, `platform`,
   `data_safety`, `success`, and `unresolved`.
4. Each optional value permits 0-3,000 UTF-16 code units. The page rejects
   over-limit or ill-formed values and never silently truncates or repairs them.
5. The visitor selects `Make my prompt now`. A brief optional yak animation
   runs, and the deterministic candidate appears in an editable textarea.
6. The visitor edits the candidate. Any edit to an input or candidate clears
   the review checkbox, erases the approval snapshot, and disables the two site
   handoff controls synchronously in that input event.
7. After reviewing the current valid candidate, the visitor selects the review
   checkbox. The site stores the exact current candidate string in memory as
   `approvedCandidate` and derives `approvedEnvelope` from that snapshot.
8. The site-provided Copy Handoff and Download Handoff controls operate only on
   that exact snapshot after rechecking equality and validity. The next-step
   panel tells the visitor to send the complete envelope to Yakherd Architecture.

### Input and well-formed-string contract

`public/assets/prompt-builder.js` exports pure functions for input validation,
candidate validation, candidate construction, envelope construction, and
export-spec construction. It has no DOM, clock, random, locale, storage, or
network dependency.

An `isWellFormedString` loop rejects:

- a high surrogate in `0xD800-0xDBFF` not immediately followed by a low
  surrogate in `0xDC00-0xDFFF`; and
- a low surrogate not immediately preceded by a high surrogate.

No replacement is permitted. The check applies independently to every input
before building and to the edited candidate before review, copy, and download.
Lone-high and lone-low inputs fail with a visible error and no export snapshot.

For form inputs, normalization is exactly:

1. reject an ill-formed JavaScript string;
2. convert CRLF and remaining CR to LF;
3. apply JavaScript `String.prototype.trim()` to the whole value;
4. reject the idea if empty or over 8,000 UTF-16 code units;
5. reject any optional field over 3,000 UTF-16 code units; and
6. replace an empty optional field in the candidate with the exact sentence
   `Not decided yet - ask me before choosing.`

Each field and the builder reject a normalized value containing a complete line
exactly equal to `MASTER PROMPT START` or `MASTER PROMPT END`. A line is text
between LF boundaries, including the first or last line. No case folding or
whitespace folding applies to this collision check.

### Deterministic candidate contract

The initial candidate has the following exact headings and order, separated by
one blank line:

```text
Project idea
<idea>

Who this is for
<audience>

What should happen
<outcome>

Must-have behavior
<must_haves>

Boundaries and things to avoid
<boundaries>

Platform and context
<platform>

Data, privacy, and safety
<data_safety>

What success looks like
<success>

Open questions
<unresolved>

Instructions to the Yakherd Architecture task
Preserve this prompt verbatim before extracting requirements.
Treat unresolved or contradictory points as questions for me, not permission to guess.
Do not silently choose technologies, providers, accounts, repository visibility, budgets, licenses, legal conclusions, or deployment targets.
Produce a bounded plan and require independent Red Team review before Implementation begins.
```

The pure builder returns LF line endings and no terminal LF. Identical
normalized input produces identical initial JavaScript strings and UTF-8 bytes.
Well-formed Unicode is preserved. No answer is parsed as a heading, instruction,
URL, HTML, or Markdown by the page.

The candidate textarea starts with that exact string. Visitor edits are
allowed. Candidate validation rejects an empty string, any CR code unit, any
ill-formed surrogate sequence, and either complete delimiter line. It otherwise
preserves every code unit, including leading/trailing LF and other whitespace.

### Exact Yakherd handoff envelope

For one valid exact candidate string `C`, the pure envelope function returns:

```text
MASTER PROMPT START\n + C + \nMASTER PROMPT END\n
```

The notation above describes concatenation; the exported bytes contain no plus
signs or spaces added around `C`. The exact construction is
`"MASTER PROMPT START\n" + C + "\nMASTER PROMPT END\n"`.

Because delimiter-line collisions are rejected and the one LF immediately
before the end delimiter is the boundary LF, the unchanged product-intake
grammar extracts exactly `C`, including any leading or trailing LF already
inside `C`. The envelope has LF line endings and one terminal LF.

When the checkbox is selected, the handler validates the current textarea,
sets `approvedCandidate` to its exact current value, constructs
`approvedEnvelope`, checks that product-intake extraction returns a string
strictly equal to `approvedCandidate`, then enables the two site controls. Any
failure leaves no snapshot, checkbox, or enabled site control.

Before either site-provided export, the handler synchronously requires all of:

- checkbox checked;
- non-null `approvedCandidate` and `approvedEnvelope`;
- current textarea value strictly equal to `approvedCandidate`;
- current candidate validation PASS; and
- re-derived envelope strictly equal to `approvedEnvelope`.

Failure atomically invalidates approval and performs no clipboard/download
operation. Candidate edit, any source-answer edit after generation,
regeneration, clear-all, builder error, candidate error, clipboard error, or
download-construction error clears the snapshot, unchecks the box, and disables
both site controls. A successful site Copy does not invalidate the snapshot. A
successful Download does not invalidate it. Native manual copy remains outside
this state machine and is disclosed as unwrapped.

Site Copy writes exactly `approvedEnvelope` to the Clipboard API. Site Download
uses an export spec with exactly:

- filename: `yakherd-master-prompt.txt`;
- MIME type: `text/plain;charset=utf-8`; and
- text: `approvedEnvelope`.

The download function uses a pre-existing hidden anchor; it does not create an
element. After successful object-URL creation it sets only that anchor's `href`
to the returned `blob:` URL and `download` to the exact filename, invokes one
click, then in `finally` removes `href` and calls `URL.revokeObjectURL` exactly
once. If Blob or URL creation fails, no click occurs. If assignment or click
throws after URL creation, `finally` still removes `href`, revokes exactly once,
invalidates approval, and reports a non-secret error. Tests inject fakes to
prove success and every failure branch without creating a real file.

### Site-controlled lifecycle safeguards

Every input/textarea sets `autocomplete="off"`; no visitor value appears in
markup. On module initialization and on every `pageshow` event, the app runs the
same clear-all function before accepting interaction. This is a bounded attempt
to clear the current document after normal load, BFCache return, or browser
restoration that emits `pageshow`; it is not proof of browser or OS erasure.

The privacy notice says that Back, refresh, crash/session recovery, autofill,
extensions, input methods, clipboard history/sync, screenshots, and downloaded
files can retain text outside site control. Visitors are told to use Clear
Everything, clear clipboard history if relevant, delete downloaded copies when
done, and use a trusted device/browser for sensitive ideas. The site makes no
claim about inaccessible memory after clearing.

### Exact static source and egress policy

Every HTML page contains an early meta CSP with at least:

```text
default-src 'self'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; frame-src 'none'; img-src 'self'; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

There are no inline scripts, inline styles, inline event handlers, `eval`,
`Function`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`,
HTML-producing template insertion, or third-party resources. Dynamic user text
is assigned only through form-control `.value` or node `.textContent`.

The dependency-free Python source-policy verifier uses `html.parser`,
`xml.etree.ElementTree`, and direct UTF-8 source inspection. It applies the
following closed policy; Implementation may not expand it:

1. HTML elements are limited to `html`, `head`, `meta`, `title`, `link`,
   `script`, `body`, `header`, `main`, `footer`, `nav`, `section`, `div`, `h1`,
   `h2`, `h3`, `p`, `ol`, `ul`, `li`, `a`, `button`, `label`, `textarea`,
   `input`, `fieldset`, `legend`, `span`, `strong`, `em`, `small`, `details`,
   `summary`, `noscript`, `pre`, and `img`.
   The complete global attribute allowlist is `id`, `class`, `hidden`, `lang`,
   `dir`, `role`, `aria-hidden`, `aria-live`, `aria-atomic`,
   `aria-describedby`, `aria-invalid`, `aria-controls`, `aria-labelledby`,
   `aria-current`, `aria-expanded`, and `aria-required`. Element-specific
   additions are: `charset`, `name`, `content`, and `http-equiv` on `meta`;
   `rel` and `href` on `link`; `type` and `src` on `script`; `href`, `target`,
   `rel`, and `download` on `a`; `type` and `disabled` on `button`; `for` on
   `label`; `rows`, `maxlength`, `autocomplete`, and `spellcheck` on
   `textarea`; `type` and `autocomplete` on `input`; `open` on `details`; and
   `src`, `alt`, `width`, `height`, `decoding`, and `loading` on `img`. Every
   other attribute, including every unlisted `aria-*` or `data-*`, is rejected.
2. No `form`, `base`, `iframe`, `frame`, `object`, `embed`, `applet`, `audio`,
   `video`, `source`, `track`, `canvas`, or meta refresh exists.
3. Executable script markup is exactly one external
   `<script type="module" src="assets/app.js">` on `index.html`; other pages
   contain no script. Every `link` is exactly
   `<link rel="stylesheet" href="assets/styles.css">`; every `img` source is
   exactly `assets/yak.svg`. Local anchor hrefs are limited to `index.html`,
   `privacy.html`, and `accessibility.html`. There is no `srcset`, `ping`,
   `action`, `formaction`, `background`,
   `poster`, `data`, `codebase`, `archive`, `profile`, or event attribute.
4. The only off-site anchor hrefs are the two frozen URLs above. Each has
   `target="_blank"` and `rel="external noopener noreferrer"`. No JavaScript
   changes or activates those anchors.
5. The only JavaScript module specifier is exactly
   `./prompt-builder.js`, in one static import in `app.js`. There is no dynamic
   import, import map, worker, or generated code.
6. Public JavaScript contains no Unicode identifier escape, hexadecimal
   identifier escape, bracketed string property access, source-map directive,
   or minified line over 160 characters. It contains none of these exact
   identifiers/property names: `fetch`, `XMLHttpRequest`, `WebSocket`,
   `EventSource`, `sendBeacon`, `WebTransport`, `RTCPeerConnection`,
   `RTCDataChannel`, `Worker`, `SharedWorker`, `ServiceWorker`, `importScripts`,
   `BroadcastChannel`, `location`, `history`, `pushState`, `replaceState`,
   `window.open`, `globalThis`, `self`, `opener`, `frames`, `parent`, `top`,
   `postMessage`, `MessageChannel`, `MessagePort`, `execCommand`, `Image`,
   `Audio`, `createElement`, `setAttribute`, `innerHTML`, `outerHTML`,
   `insertAdjacentHTML`, `document.write`, `DOMParser`,
   `createContextualFragment`, `eval`, `Function`, `setTimeout`, `setInterval`,
   `atob`, `btoa`, `cookie`, `localStorage`, `sessionStorage`, `indexedDB`,
   `caches`, `CSSStyleSheet`, `adoptedStyleSheets`, `insertRule`, or
   `registerProtocolHandler`.
7. The only egress-capable operations permitted in JavaScript are the literal
   static module import, one user-initiated
   `navigator.clipboard.writeText(approvedEnvelope)` call, and the reviewed
   hidden-anchor `blob:` download operations above. The verifier requires
   exactly those source occurrences and rejects any additional `navigator`,
   `.href`, `.src`, `.style`, `.click()`, `.download`, `Blob`,
   `createObjectURL`, `revokeObjectURL`, or `removeAttribute` occurrence.
8. CSS contains no `@import`, `url(`, `expression`, `behavior`,
   `-moz-binding`, external scheme, or source-map directive.
9. `yak.svg` is well-formed XML and permits only `svg`, `g`, `path`, `circle`,
   `ellipse`, `rect`, `line`, `polyline`, `polygon`, and `title`. Attributes are
   limited to `xmlns`, `viewBox`, `role`, `aria-hidden`, `focusable`, `fill`,
   `stroke`, `stroke-width`, `stroke-linecap`, `stroke-linejoin`, `opacity`,
   `transform`, `d`, `cx`, `cy`, `r`, `rx`, `ry`, `x`, `y`, `width`, `height`,
   `x1`, `y1`, `x2`, `y2`, and `points`. No `script`, `style`, `a`, `use`,
   `image`, `foreignObject`, event attribute, `href`, `xlink`, entity,
   stylesheet, external reference, animation element, or `url(` is permitted.

The verifier rejects malformed UTF-8, duplicate IDs, unknown elements,
attributes, URLs, imports, operations, and policy exceptions. Runtime browser
evidence records `performance.getEntriesByType("resource")` before and after
every valid, invalid, edit, approve, copy-success, copy-denial,
download-success-with-fakes, download-failure, regeneration, and clear flow.
The sorted URL/path set must remain exactly the reviewed initial same-origin
asset allowlist with no query. DevTools/browser observation must show no
additional request. Static source checks and runtime observation are both
required; neither alone proves the invariant.

Server-enforced response headers, TLS, caching, `frame-ancestors`,
`X-Content-Type-Options`, `Referrer-Policy`, and deployed 404 behavior are not
claimed by local HTML. They belong to the later reviewed hosting sequence.

## Staged Implementation

### Stage 0: independent plan review

Red Team reviews this exact file and may write only:

`docs/audits/yakherd/2026-07-21_yakherd_dev_static_concierge_plan_red_team_v2.md`

A FAIL permits Architecture to create only a new plan candidate and request a
fresh exact review. It grants no Implementation or deployment authority. A PASS
authorizes Architecture to send only Stage 1 to the existing Implementation
task.

### Stage 1: local static implementation

The sole Implementation writer may create exactly these directory entries:

- `website/`
- `website/static-concierge/`
- `website/static-concierge/public/`
- `website/static-concierge/public/assets/`
- `website/static-concierge/tests/`
- `.tmp/` as an existing-or-created ordinary parent directory only
- `.tmp/static-concierge-acceptance/` only for the disposable download below

Directory authorization permits only the exact files listed next. It does not
authorize an extra file, symlink, junction, device, socket, stream, or nested
directory.

The sole Implementation writer may create exactly these durable files:

- `website/static-concierge/README.md`
- `website/static-concierge/public/index.html`
- `website/static-concierge/public/privacy.html`
- `website/static-concierge/public/accessibility.html`
- `website/static-concierge/public/404.html`
- `website/static-concierge/public/assets/styles.css`
- `website/static-concierge/public/assets/app.js`
- `website/static-concierge/public/assets/prompt-builder.js`
- `website/static-concierge/public/assets/yak.svg`
- `website/static-concierge/tests/test_static.py`
- `website/static-concierge/tests/test_prompt_builder.mjs`
- `website/static-concierge/tests/accessibility_checklist.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_static_concierge_implementation.md`

The only disposable filesystem artifact is:

`.tmp/static-concierge-acceptance/yakherd-master-prompt.txt`

It contains only the fixed synthetic test candidate and exact envelope. Before
the real-download observation, Implementation resolves and confirms `.tmp` and
the acceptance directory are ordinary directories inside the repository, are
not reparse points, and contain no child other than the permitted artifact.
It confirms the literal artifact path is absent. The browser/tool is configured
to write that exact filename without
auto-renaming. After byte/hash comparison it deletes only that literal file and
then the empty literal acceptance directory, without recursion, and verifies
both are absent. If exact destination control is unavailable, the observation
stops without clicking Download. If creation, comparison, or cleanup fails,
Stage 1 fails; evidence records presence, type, length, and SHA-256 when
observable, and the exact artifact remains the only permitted retained
failure. No cleanup authority expands beyond that file and empty directory.

No screenshot file is required or authorized. Visual inspection may use
transient tool output that does not create a repository/workspace file; the
durable evidence is a textual checklist using fixed synthetic content.

Implementation must not modify any existing plan, audit, root asset,
package/release byte, root documentation, Git state, or DreamHost state. It
must not install a dependency or access an external network. Localhost browser
validation is allowed.

Implementation may use only Python's standard library, the already available
Node runtime and its built-in test runner, and browser primitives. If a usable
Node runtime is absent, it stops and records the missing prerequisite; it does
not install Node or add a package manager file.

### Exact all-new candidate boundary

At Stage 1 completion, every durable path above is initially untracked. No
staging is allowed. The implementation evidence contains path, regular-file
type, byte length, and lowercase SHA-256 for the first twelve durable files; it
cannot self-hash. Architecture freezes the record after Implementation stops,
computes its byte length and SHA-256 without editing it, and sends Red Team an
exact thirteen-row candidate table.

Before handoff, these must all hold:

- `git diff --cached --name-only` is empty;
- `git diff --name-only` is empty;
- `git status --porcelain=v1 --untracked-files=all -- website/static-concierge`
  contains exactly the twelve authorized site/test files as `??` entries;
- the implementation evidence is the one additional expected `??` entry;
- no symlink, reparse point, non-regular file, alternate stream, extra child,
  or case-colliding path exists in the authorized directories;
- the disposable path and directory are absent for PASS; and
- every candidate hash matches a fresh independent read.

On Windows, the complete non-index content representation for each new file is
`git diff --no-index --no-ext-diff -- NUL <literal-path>`; exit `1` means a
new-file diff and is expected. On POSIX, `/dev/null` replaces `NUL`. For
whitespace checking, `git diff --no-index --check -- NUL <literal-path>` (or
`/dev/null`) must return exit `1` with no output; any output or other exit is a
failure. Red Team runs these per file and also reads/hashes every row directly.
Ordinary `git diff --check` remains required for tracked state but is never
represented as covering the untracked candidate.

### Stage 2: exact implementation review

After Stage 1 validations pass, Architecture routes the thirteen-row frozen
candidate and evidence to the existing Red Team task. Red Team receives one
new, exactly named audit path at that time. Until that independent
implementation PASS, there is no Git, DreamHost, browser-account, staging,
production, or deployment authority.

### Stage 3: separately reviewed read-only hosting inventory

Only after implementation PASS may Architecture write a separate bounded plan
for a read-only static-hosting inventory. That plan must receive independent
Red Team PASS before any signed-in DreamHost/browser read. It defines exact
panel routes, permitted observations, secret/account-data handling, tab
lifecycle, evidence schema/path, and stop conditions. It may not mutate hosting,
DNS, certificate, credentials, files, or settings and may not reuse or revive
the v15 capability procedure.

The complete inventory evidence receives a second independent review. Only an
evidence-integrity and capability PASS may inform a later exact
deployment/rollback plan bound to final reviewed public hashes, exact domain,
web root, remote inventory/delta, upload mechanism, prior-state backup, HTTPS,
headers, rollback, and a human production checkpoint. Each later plan remains
separately reviewed. If a writable existing static target and valid HTTPS cannot
be established read-only, the release stops at the reviewed local artifact.

## Acceptance And Stop Gates

### Required automated checks

Implementation runs and records exact commands, exit codes, and outputs for:

```powershell
python -B -m unittest discover -s website\static-concierge\tests -p "test_*.py" -v
node --test website\static-concierge\tests\test_prompt_builder.mjs
python scripts\verify_release.py
git diff --check
```

The Python tests independently verify:

- the exact public-file allowlist, referenced assets, and size budgets;
- the complete closed HTML/CSS/JavaScript/SVG source/egress policy above;
- local links, exact external-anchor attributes, unique IDs, label/control
  relationships, declared language, page titles, viewport, and required
  privacy/authority/high-stakes copy;
- no root PNG/video is present in or referenced by the public tree; and
- the exact product-intake file identity bound by this plan.

The Node tests independently verify:

- required-idea and every UTF-16 length boundary without truncation;
- lone-high, lone-low, valid surrogate pair, CRLF/CR normalization, well-formed
  Unicode preservation, blank-field placeholder, exact section order, and no
  initial terminal LF;
- delimiter collisions in every input and at the first, middle, and last line
  of an edited candidate;
- deterministic candidate/envelope bytes for identical normalized inputs;
- end-to-end extraction of the envelope using the unchanged product-intake
  grammar, strict equality of extracted candidate, and identical UTF-8 length
  and SHA-256 for leading LF, trailing LF, non-ASCII, HTML-looking,
  Markdown-looking, URL-looking, and prompt-injection-looking candidates;
- approval invalidation after every candidate/input edit, regeneration,
  clear-all, validation error, clipboard failure, and download failure;
- refusal of a stale/mismatched snapshot before site copy/download;
- exact Clipboard API argument;
- exact filename, MIME, Blob UTF-8 bytes, hidden-anchor attributes/click count,
  and object-URL cleanup on success plus every injected failure branch; and
- absence of DOM, clock, randomness, locale, storage, and network dependencies
  from the pure builder module.

### Required browser and human checks

Implementation serves only `website/static-concierge/public` on localhost and
records, using only fixed synthetic ideas:

- keyboard-only completion, candidate editing, checkbox transitions,
  site-copy denial/success, native-copy disclosure, site download, and
  clear-all flow;
- screen-reader-oriented labels, descriptions, errors, focus order, result
  announcement, and decorative mascot treatment;
- 320 CSS-pixel layout, 400% zoom, long well-formed Unicode content, and no
  lost controls;
- normal and `prefers-reduced-motion` states;
- clipboard denial with candidate retention;
- exact downloaded envelope bytes/hash/filename followed by exact cleanup;
- JavaScript-disabled fallback explaining the manual sections and that no
  Yakherd-compatible envelope can be generated without JavaScript;
- initialization and synthetic `pageshow` clearing of the current document,
  with truthful browser/OS retention disclosure;
- absence of prompt text in URL, site storage, cookies, and runtime requests;
- the exact before/after Performance Resource Timing allowlist for every flow;
  and
- Chromium plus one available second browser engine, or an explicit recorded
  stop if no second engine is available.

`tests/accessibility_checklist.md` records every target above as PASS, FAIL, or
NOT TESTED with evidence. NOT TESTED blocks implementation PASS.

### Immediate stop gates

- Any idea, answer, candidate, or envelope reaches an unauthorized request,
  URL, site storage, cookie, log written by site code, executable context, or
  third-party resource.
- Any public source violates the closed source/egress policy or produces a
  runtime request outside the exact initial asset allowlist.
- Any file, directory, symlink, reparse point, alternate stream, temp artifact,
  or path outside the exact Stage 1 boundary is required or appears.
- Any dependency install, package manager, transpiler, bundler, framework,
  remote asset, or backend becomes necessary.
- The builder invents an answer, silently truncates or repairs input, accepts an
  ill-formed string/delimiter collision, or changes the approved candidate in
  the extracted handoff.
- A site-provided copy/download runs without an exact current approval snapshot,
  or a required invalidation transition leaves either site control enabled.
- Download bytes/filename/MIME differ, an object URL is not revoked exactly
  once after creation, or the exact disposable artifact is not cleaned for
  PASS.
- Copy or privacy language claims to prevent native copying or guarantee
  browser/OS erasure.
- Required automated, intake-bridge, source-policy, accessibility, privacy,
  keyboard, reduced-motion, reflow, browser, temp-cleanup, non-index diff, or
  byte-budget evidence is missing or fails.
- The implementation touches a package/release byte, existing plan/audit,
  root image/video, Git state, DreamHost/browser account, external network, or
  any path outside the exact write boundary.

## Evidence And SSOT Outputs

The Stage 1 implementation evidence record contains:

- reviewed plan path, byte length, and SHA-256;
- authorizing plan-audit path, verdict, byte length, and SHA-256;
- exact created directory and file lists;
- path, regular-file type, byte length, and SHA-256 for every durable file other
  than the evidence record itself;
- the evidence record's own identity supplied in the frozen Architecture
  handoff and independently verified by Red Team;
- exact untracked-path and non-index-diff results without staging;
- disposable download creation/hash/cleanup result and final absence, or exact
  retained-failure state;
- runtime versions used without installing them;
- exact automated commands, exit codes, and outputs;
- completed accessibility/browser/resource-request matrices;
- deviations, failures, and residual risks;
- explicit confirmation that no external network, DreamHost, secret, package,
  existing audit/plan, root media, Git, deployment, or release mutation
  occurred; and
- branch, HEAD, upstream, dirty state, staged paths, tracked diff, and
  ahead/behind.

The evidence record does not grant its own acceptance. Red Team independently
reviews every frozen byte. Existing dynamic-concierge records remain preserved
and are referenced only as history, not merged into this plan's authority
chain.

## Forbidden Scope

- Continuing, repairing, retrying, or reviewing the v15 preflight cycle.
- Creating a capability evidence skeleton or using the DreamHost panel/browser
  under v3-v15 authority.
- OpenAI or other model/provider integration, adaptive interrogation, prompt
  scoring, contradiction resolution, secret detection, or content moderation.
- PHP, server code, API routes, databases, authentication, email capture,
  analytics, telemetry, cookies, persistent drafts, accounts, payments, rate
  limiting, cron, queues, or background work.
- Automated Codex task creation, deep links, local installation, repository
  creation, GitHub OAuth, GitHub mutation, Git commits/pushes, SFTP/SSH, or
  DreamHost read/deployment in Stages 0-2.
- A ZIP bundle, signature, approval receipt, hash claim in the visitor artifact,
  provenance schema, automatic product-intake promotion, or modification of the
  audited installer/template.
- Production publication or claims about live TLS, headers, uptime, privacy,
  accessibility, performance, or browser compatibility before later live
  evidence passes its own gates.

autonomous next action: the existing Red Team task independently reviews this exact v2 static-concierge plan and writes only the authorized v2 plan-audit record; Implementation, v15, Git, DreamHost/browser, and every live/deployment path remain parked pending that verdict.
