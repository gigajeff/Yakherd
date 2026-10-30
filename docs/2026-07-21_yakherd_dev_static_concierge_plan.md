# Architecture Plan: Yakherd.dev Static Concierge First Release

- Date: 2026-07-21
- Status: proposed
- Owner: `docs/2026-07-21_yakherd_dev_static_concierge_plan.md`
- Supersedes: the v1-v15 dynamic-concierge candidates as the active first-
  website-release scope only
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
processing occurs in the loaded browser page. The visitor can review, copy, or
download the resulting plain-text prompt and receives honest next-step guidance
for taking it into Yakherd.

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
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v13.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability_red_team.md`
- `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v14.md`
- `packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md`
- `packages/jeff_strict_ssot_v1/template/docs/prompts/architecture_task.md`
- `packages/jeff_strict_ssot_v1/template/docs/task_protocol.md`

The v13 plan PASS, exhausted v13 capability FAIL, v14 plan FAIL, unreviewed v15
draft, and every earlier plan and audit remain immutable historical evidence.
Nothing in this plan changes their bytes or retroactively changes a verdict.
The v15 preflight/retry path is parked indefinitely and receives no skeleton,
browser action, DreamHost action, retry, or further Red Team cycle under this
release scope.

## Invariants And Boundaries

### Product and authority boundary

- The page produces a **candidate master prompt**. It is not authoritative
  until the visitor reviews it and later supplies it to the governed Yakherd
  product-intake workflow.
- The page never claims that a prompt, architecture, implementation, review,
  repository, backup, or deployment has been created.
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
- Site JavaScript must not use `fetch`, `XMLHttpRequest`, `WebSocket`,
  `EventSource`, `sendBeacon`, `WebTransport`, or any equivalent network API.
- Site JavaScript must not use cookies, `localStorage`, `sessionStorage`,
  IndexedDB, Cache API, or browser history/query/hash state for visitor input.
- No input is placed in a URL. No HTML form submission exists. All action
  buttons have `type="button"`, and CSP sets `form-action 'none'` and
  `connect-src 'none'`.
- Clipboard access is user-initiated and optional. If unavailable or denied,
  the result remains selectable and downloadable; denial is not an error that
  loses the prompt.
- Download uses a browser-created UTF-8 text Blob and a temporary object URL.
  The object URL is revoked after the user-initiated download.
- Refreshing, closing, or navigating away clears the working state. The page
  says this plainly before idea entry and beside the result.
- Normal host access logs may record the page request and network metadata, but
  the site sends no idea, answer, or generated prompt to the host. The privacy
  page states both facts without promising anonymity.

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
- The generated result is an editable plain-text `<textarea>`. The visitor must
  select `I reviewed this draft and want to use it as my candidate master
  prompt` before copy or download is enabled.
- `Clear everything` clears all inputs, the output, validation messages, and
  approval state in the current page without a reload.
- External links are visibly labeled as leaving Yakherd.dev, never initiate an
  account or mutation, and are limited in this slice to:
  `https://github.com/gigajeff/Yakherd` and
  `https://pypi.org/project/yakherd/`.
- High-stakes medical, legal, financial, security-critical, or safety-critical
  ideas receive a general visible warning that the generated prompt is only a
  planning aid and requires qualified human review. This release performs no
  domain classification and makes no safety conclusion.

### Accessibility and presentation boundary

- Target WCAG 2.2 AA for the implemented experience, with semantic landmarks,
  explicit labels and instructions, useful heading order, keyboard-only
  operation, visible focus, associated errors, a polite result status region,
  sufficient contrast, and no color-only meaning.
- The layout must remain usable at 320 CSS pixels and 400% zoom without loss of
  content or two-dimensional page scrolling.
- Every pointer target is at least 24 by 24 CSS pixels unless an allowed WCAG
  exception is documented in evidence.
- Animation is decorative, never communicates the only copy of state, and is
  disabled when `prefers-reduced-motion: reduce` is active.
- The visual motif is a friendly original SVG yak. An idea card moves toward
  the yak and a prompt card appears behind it when the visitor generates a
  result. Text describes the state independently; the mascot SVG is decorative
  and hidden from the accessibility tree.
- Copy may be playful (`Feed the yak`, `Fresh prompt`) but must not shame the
  visitor, sexualize the theme, obscure the result, or substitute humor for a
  privacy/authority disclosure.
- No existing multi-megabyte PNG is copied into the website release. The full
  public tree must remain at or below 250,000 bytes before transfer encoding,
  and no individual public file may exceed 100,000 bytes.

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
   groups:
   `audience`, `outcome`, `must_haves`, `boundaries`, `platform`, `data_safety`,
   `success`, and `unresolved`.
4. Each optional value permits 0-3,000 JavaScript UTF-16 code units. The page
   refuses over-limit values; it never silently truncates them.
5. The visitor selects `Make my prompt now`. A brief optional yak animation
   runs, and the deterministic candidate appears in an editable textarea.
6. The visitor edits and reviews the candidate, selects the explicit review
   checkbox, then copies or downloads the exact textarea value.
7. The next-step panel explains that the visitor can keep the text privately,
   open the Yakherd technical repository, and give the text to the Architecture
   task when Yakherd asks for the master prompt. It does not imply that this
   handoff already occurred.

### Deterministic initial prompt contract

`assets/prompt-builder.js` exports a pure builder and a pure validator. It has
no DOM, clock, random, locale, storage, or network dependency.

For every input, normalization is exactly:

1. convert CRLF and remaining CR to LF;
2. apply JavaScript `String.prototype.trim()` to the whole value;
3. reject the idea if empty or over 8,000 UTF-16 code units;
4. reject any optional field over 3,000 UTF-16 code units; and
5. replace an empty optional field in the output with the exact sentence
   `Not decided yet - ask me before choosing.`

The initial output has the following exact headings and order, separated by one
blank line:

```text
MASTER PROMPT

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

The pure builder returns LF line endings and exactly one terminal LF. Identical
normalized input produces identical initial UTF-8 output bytes. Unicode input
is preserved. No answer is parsed as a heading, instruction, URL, HTML, or
Markdown by the page.

The result textarea starts with those exact bytes. Subsequent visitor edits are
allowed. Copy and download use the textarea's exact current JavaScript string,
with no added heading, metadata, normalization, or terminal newline. The
download filename is exactly `yakherd-master-prompt.txt` and MIME type is
`text/plain;charset=utf-8`. The page calls this a candidate, not a signed,
verified, hashed, approved, or installed Yakherd artifact.

### Static security policy

Every HTML page contains an early meta CSP with at least:

```text
default-src 'self'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; frame-src 'none'; img-src 'self' data:; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

There are no inline scripts, inline styles, inline event handlers, `eval`,
`Function`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`,
HTML-producing template insertion, or third-party resources. Dynamic user text
is assigned only through form-control `.value` or node `.textContent`.

Server-enforced response headers, TLS, caching, `frame-ancestors`,
`X-Content-Type-Options`, `Referrer-Policy`, and the deployed 404 response are
not claimed by local HTML. They belong to the later exact static-deployment
plan and live evidence.

## Staged Implementation

### Stage 0: independent plan review

Red Team reviews this exact file and may write only:

`docs/audits/yakherd/2026-07-21_yakherd_dev_static_concierge_plan_red_team.md`

A FAIL permits Architecture to revise only the plan and request another exact
review. It grants no Implementation or deployment authority. A PASS authorizes
only Stage 1 in the existing Implementation task.

### Stage 1: local static implementation

The sole Implementation writer may create or modify exactly these paths:

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

No wildcard path is authorized. The implementation must not modify any existing
plan, audit, root asset, package/release byte, root documentation, Git state, or
DreamHost state. It must not install a dependency or access an external
network. Localhost browser validation is allowed.

Implementation may use only Python's standard library, the already available
Node runtime and its built-in test runner, and browser primitives. If a usable
Node runtime is absent, it stops and records the missing prerequisite; it does
not install Node or add a package manager file.

### Stage 2: exact implementation review

After Stage 1 validations pass, Architecture routes the exact implementation
diff and evidence to the existing Red Team task. Red Team receives one new,
exactly named audit path at that time. Until that independent implementation
PASS, there is no build, Git, DreamHost, staging, or production authority.

### Stage 3: separate static deployment plan

Only after implementation PASS may Architecture write a short deployment plan
bound to:

- the exact reviewed public-file allowlist, byte lengths, and SHA-256 values;
- the exact DreamHost domain and already-configured web-root path;
- the exact upload mechanism available in the signed-in account;
- the pre-deploy remote inventory and exact delta;
- a retained prior-state backup and one bounded rollback procedure;
- HTTPS and response-header observations; and
- the exact human production checkpoint.

That later plan receives a fresh independent Red Team review. It must prefer a
simple static upload. It may not revive the v15 certificate/PHP capability
probe, create a dynamic endpoint, transfer a provider secret, configure cron,
or improvise SSH/Git deployment. If an existing writable target and valid HTTPS
cannot be established without account reconfiguration, the first release stops
at the reviewed local artifact rather than expanding scope.

## Acceptance And Stop Gates

### Required automated checks

Implementation runs and records exact commands, exit codes, and outputs for:

```powershell
python -B -m unittest discover -s website\static-concierge\tests -p "test_*.py" -v
node --test website\static-concierge\tests\test_prompt_builder.mjs
python scripts\verify_release.py
git diff --check
```

The Python tests must independently verify:

- the exact public-file allowlist and size budgets;
- no external subresource, automatic redirect, form submission, remote CSS
  URL, or unapproved external anchor;
- the CSP and no-inline-code contract on every HTML page;
- no executable network, storage, cookie, service-worker, dynamic-HTML, or
  eval-like primitive in public JavaScript;
- local link and referenced-asset integrity;
- unique IDs, label/control relationships, declared language, page titles,
  viewport, and presence of the required privacy/authority copy; and
- that the existing multi-megabyte root PNGs are not present in or referenced
  by the public tree.

The Node tests must independently verify:

- required-idea and every length boundary without truncation;
- CRLF/CR normalization, Unicode preservation, blank-field placeholder, exact
  section order, and exactly one terminal LF;
- deterministic output for identical normalized inputs;
- preservation of HTML-looking, Markdown-looking, URL-looking, and prompt-
  injection-looking text as ordinary returned string data; and
- absence of DOM, clock, randomness, locale, storage, and network dependencies
  from the pure builder module.

### Required browser and human checks

Implementation serves only `website/static-concierge/public` on localhost and
records:

- keyboard-only completion, editing, review, copy fallback, download, and
  clear-all flow;
- screen-reader-oriented labels, descriptions, error association, focus order,
  result announcement, and decorative mascot treatment;
- 320 CSS-pixel layout, 400% zoom, high zoom with long Unicode content, and no
  lost controls;
- normal and `prefers-reduced-motion` states;
- clipboard denial and download success without prompt loss;
- JavaScript-disabled fallback copy that explains how to draft the same
  sections manually;
- reload/close non-persistence and no prompt text in URL, browser storage,
  cookies, or observed network requests; and
- Chrome/Chromium plus one available second browser engine, or an explicit
  recorded stop if no second engine is available.

`tests/accessibility_checklist.md` records each WCAG target above as PASS, FAIL,
or NOT TESTED with evidence. NOT TESTED blocks implementation PASS.

### Immediate stop gates

- Any idea, answer, or prompt leaves the page through a request, URL, storage,
  cookie, log written by site code, or third-party resource.
- Any public file or path outside the exact allowlist is required.
- Any dependency install, package manager, transpiler, bundler, framework,
  remote asset, or backend becomes necessary.
- Any user text reaches an HTML-producing sink or executable context.
- The builder invents an answer, silently truncates input, changes visitor
  edits during copy/download, or differs for identical normalized inputs.
- Copy or download can occur without the review checkbox, or clear-all leaves
  user content or approval state behind.
- Required automated, accessibility, privacy, keyboard, reduced-motion,
  reflow, or byte-budget evidence is missing or fails.
- The implementation touches a package/release byte, existing plan/audit,
  root image/video, Git state, DreamHost, external network, or any path outside
  the exact write set.

## Evidence And SSOT Outputs

The Stage 1 implementation evidence record contains:

- reviewed plan path and SHA-256;
- authorizing plan-audit path, verdict, and SHA-256;
- exact created/modified path list;
- per-public-file byte length and SHA-256;
- runtime versions used without installing them;
- exact automated commands, exit codes, and outputs;
- the completed accessibility/browser matrix;
- screenshots containing only fixed synthetic ideas, never a real visitor idea;
- deviations, failures, and residual risks;
- explicit confirmation that no external network, DreamHost, secret, package,
  existing audit/plan, root media, Git, deployment, or release mutation
  occurred; and
- branch, HEAD, upstream, dirty state, staged paths, and ahead/behind.

The evidence record does not grant its own acceptance. Red Team independently
reviews the exact diff and evidence. Existing dynamic-concierge records remain
preserved and are referenced only as history, not merged into this plan's
authority chain.

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
  DreamHost deployment in Stages 0-2.
- A ZIP/intake bundle, signature, approval receipt, hash claim, provenance
  schema, automatic product-intake promotion, or modification of the audited
  installer/template.
- Production publication or claims about live TLS, headers, uptime, privacy,
  accessibility, performance, or browser compatibility before later live
  evidence passes its own gate.

autonomous next action: the existing Red Team task independently reviews this exact static-concierge plan and writes only the authorized plan-audit record; v15 and all DreamHost/Implementation/deployment activity remain parked pending that verdict.
