# Yakherd.dev Static Concierge Plan — Independent Red Team Review

- Date: 2026-07-21
- Candidate: `docs/2026-07-21_yakherd_dev_static_concierge_plan.md`
- Verified candidate identity: 22,120 bytes; 469 lines; SHA-256
  `c00f32e8f50d174e9cf1c149dfc13849705fc5bd41fad0ef5262304315b7cc67`
- Verdict: **FAIL**

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — The exported candidate is not directly consumable by the unchanged Yakherd intake contract

The plan says the result becomes authoritative only after it is supplied to the
governed product-intake workflow and tells the beginner to give the text to the
Architecture task (`docs/2026-07-21_yakherd_dev_static_concierge_plan.md:61-63`,
`:191-194`). The exact generated artifact starts with `MASTER PROMPT`, contains
no intake envelope (`:213-248`), and copy/download exports only the current
textarea string (`:255-260`). The unchanged intake contract instead accepts
only text between literal `MASTER PROMPT START` and `MASTER PROMPT END` lines
and requires a resend when those delimiters are absent
(`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:8-13`).

This is a fail-closed rejection rather than an authority bypass, but it breaks
the promised beginner handoff. Merely adding an outer wrapper is also
insufficient: the current builder preserves an answer or later edit containing
a complete delimiter line, which can make boundary extraction ambiguous or
premature. The acceptance plan tests builder formatting but has no end-to-end
fixture against the unchanged intake grammar (`static_concierge_plan.md:374-383`).

#### P1-2 — The review checkbox is neither enforceable as written nor bound to the current draft

The result must be an editable textarea and remain selectable
(`static_concierge_plan.md:88-90`, `:110-112`, `:255-257`). Native keyboard,
context-menu, accessibility-tool, or browser copy therefore remains possible
before the checkbox. The absolute stop condition that copy cannot occur without
the checkbox is not implementable (`:418-419`).

The plan also does not require approval to be synchronously invalidated after a
textarea edit, regeneration from changed answers, or validation transition.
Consequently an implementation can satisfy the literal checkbox test while
exporting bytes different from the draft the visitor acknowledged. This is a
candidate-authority truthfulness defect, even though the plan correctly avoids
claiming a signed or authoritative artifact.

#### P1-3 — The non-persistence promise exceeds the site's control and its tests

The plan correctly bans site use of storage and history APIs
(`static_concierge_plan.md:81-87`), but then states categorically that refresh,
close, or navigation clears working state (`:93-94`). A static page does not
control browser form restoration, back-forward cache, crash/session restore,
autofill, clipboard synchronization, downloaded files, extensions, or input
methods. In particular, navigating through an allowed external link and using
Back can restore an in-memory document without the site having used a storage
API (`:115-118`).

The proposed observation covers reload/close but not back/forward restoration
and still cannot prove universal tab-close or session erasure
(`:400-403`). The privacy copy must distinguish "the site does not persist or
transmit this text" from browser-, OS-, clipboard-, and download-controlled
retention. Site-controlled lifecycle safeguards may be tested, but they cannot
support the current unconditional erasure promise.

#### P1-4 — The exact write and exact-diff boundary is incomplete for an all-new implementation

Stage 1 authorizes only thirteen file paths and forbids every other path
(`static_concierge_plan.md:294-313`). At review time `website/` and all four
required descendant directories do not exist, so creating the listed files
necessarily creates unlisted directory entries. The required successful browser
download and durable screenshot evidence also need either process-owned
temporary outputs, exact artifact paths, or an explicitly defined in-record
embedding; none is authorized (`:385-403`, `:428-437`). No cleanup or retained-
failure disposition is defined for those outputs.

Every Stage 1 file will initially be untracked. Ordinary `git diff` and the
required `git diff --check` do not include untracked contents, staging is
forbidden, and the plan does not define a non-index representation for the
"exact implementation diff" (`:310-313`, `:320-325`, `:351-358`). Evidence
hashes are required only for public files, not for every file in the reviewed
write set (`:428-442`). The later Red Team therefore lacks one deterministic,
complete, non-Git-mutating candidate boundary.

#### P1-5 — The core no-network claim is broader than the specified verification method

The trust boundary bans named APIs plus every "equivalent network API" and all
input-bearing URLs (`static_concierge_plan.md:81-87`). The automated requirement
only says Python tests will verify the absence of executable primitives in
public JavaScript, without defining a closed primitive/sink set or a parser
strategy (`:360-367`). Exercising the intended browser flows and observing no
request does not cover dormant or alternate branches (`:385-403`).

Top-level navigation, `window.open`, programmatically activated anchors,
computed property access, dynamic imports/workers, element constructors, and
active SVG/HTML attributes are examples of egress-capable surfaces not closed
by a list limited to `fetch`-like calls. CSP reduces this risk but does not
block every top-level navigation. With no dependency install and no JavaScript
parser authorized, the plan must define a small auditable source/primitive
allowlist or an exact dependency-free verifier plus complete active-content and
runtime-request checks. As written, the central privacy invariant is not exact
or reproducibly testable.

### P2 — Medium

#### P2-1 — The UTF-8 preservation contract omits malformed UTF-16

The validator accepts by JavaScript UTF-16 code-unit length and applies its
rules to every input (`static_concierge_plan.md:180-186`, `:201-208`), while the
builder promises preserved Unicode and deterministic UTF-8 bytes (`:250-253`).
Copy/download then claims to use the exact current JavaScript string in a UTF-8
Blob (`:255-259`). A JavaScript string may contain an unpaired high or low
surrogate; UTF-8 conversion replaces it with U+FFFD. A read-only Node check
confirmed a one-unit lone high surrogate encoded as `efbfbd` and did not round
trip equal. The plan neither rejects these strings nor defines replacement
semantics, and its Unicode test set does not name these boundaries (`:374-383`).

#### P2-2 — The high-stakes warning has no deterministic trigger

The plan conditionally promises that high-stakes ideas receive a warning while
also stating that the release performs no classification
(`static_concierge_plan.md:119-122`) and forbidding classification or content
moderation (`:449-458`). No field or acceptance case determines when the
warning appears. A fixed warning shown for every generated result would be
deterministic; the conditional requirement is not.

#### P2-3 — Download, SVG, and external-link security assertions need exact acceptance

The browser matrix asks only for download success and prompt retention
(`static_concierge_plan.md:385-403`). It does not independently compare the
edited textarea value to downloaded UTF-8 bytes, check the suggested filename
and MIME value, or prove object-URL revocation on success and failure
(`:91-92`, `:255-259`). The static checks also need an explicit safe SVG subset:
no script, event attribute, `foreignObject`, external reference, or active
navigation. For the two allowed off-site links (`:115-118`), the plan should
freeze safe opener/referrer behavior in local markup while leaving server
header proof to deployment (`:275-278`).

#### P2-4 — The later deployment gate lacks a separately authorized fact-gathering phase

Stage 3 requires a later plan already bound to the current DreamHost web root,
upload mechanism, remote inventory, and delta
(`static_concierge_plan.md:327-338`). Yet a plan PASS authorizes only local
Stage 1 (`:282-290`), Stages 0-2 forbid DreamHost access (`:310-325`), and the
v15 capability route is permanently parked (`:50-55`, `:340-345`). The static
separation is correct, but the future sequence must include a separately
reviewed read-only static inventory/evidence gate, or bind to fresh existing
evidence, before a byte-bound mutation/rollback plan can truthfully exist.

### P3 — Low

No independent P3 finding. The remaining low-risk presentation choices are
appropriate to decide and inspect in the exact implementation review.

## Verdict

**FAIL** for the exact 22,120-byte candidate identified above.

The static-only direction materially reduces the dynamic design's abuse, cost,
secret, provider-log, PHP, and rollback attack surface. Its package-neutral
boundary, single-writer intent, CSP baseline, explicit deferral of hosting, and
honest statement that the page creates only a candidate are sound. The P1
contract gaps nevertheless make the beginner handoff, review state, privacy
promise, write/diff boundary, and no-network proof insufficiently fail-closed.

## Required Fixes

1. Specify an exact intake-compatible handoff envelope, distinguish envelope
   bytes from candidate-prompt bytes, handle complete delimiter lines in the
   current edited value, and add an end-to-end extraction/byte/hash fixture
   against the unchanged `product_intake.md` contract.
2. Scope the checkbox to site-provided Copy and Download controls; state that
   native/manual copying is not an access control; clear approval and disable
   both controls on every output edit, regeneration, reset, and relevant error;
   test every transition.
3. Replace universal erasure language with a truthful site-controlled
   non-persistence boundary. Disclose possible browser/session/autofill,
   clipboard, downloaded-file, extension, and input-method retention; define
   and test bounded page lifecycle and form-attribute safeguards without
   claiming the browser erased state it cannot prove.
4. Authorize the exact missing parent directories and exact disposable
   download/screenshot mechanism, including cleanup and retained-failure
   handling. Define a non-index exact representation of every new Stage 1 file,
   an exact untracked-path allowlist, and byte length/SHA-256 for all thirteen
   files without staging.
5. Replace the open-ended "equivalent network API" proof with an exact,
   dependency-free source and active-content policy plus runtime observations
   that jointly cover JavaScript, HTML, CSS, SVG, all alternate flows, and every
   allowed exception.
6. Define rejection or explicit well-formed replacement semantics for unpaired
   UTF-16 surrogates before build, approval, copy, and download; add lone-high
   and lone-low surrogate tests and exact edited download-byte checks.
7. Make the high-stakes warning unconditionally visible for every result, or
   define a non-classifying explicit visitor control and its tests.
8. Split future hosting work into a separately reviewed, read-only static
   inventory/evidence gate followed by a fresh exact deployment/rollback plan.
   No implementation PASS may imply DreamHost read or mutation authority.

Any revision must receive a fresh independent review as a new exact candidate.
Red Team did not repair the plan.

## Residual Risks

- Even a corrected static page cannot control browser extensions, operating-
  system clipboard synchronization, downloaded copies, screenshots, input
  methods, crash recovery, or every browser retention policy. These remain
  disclosed client-boundary risks, not site guarantees.
- A generated candidate remains untrusted user-controlled input. It acquires no
  Yakherd authority until the unchanged preservation, extraction, owner
  promotion, and independent review gates complete.
- Meta CSP and local checks do not establish live TLS, response headers,
  clickjacking resistance, caching, 404 behavior, or host rollback. Those facts
  remain for the separately reviewed deployment sequence.
- Manual accessibility and two-engine observations provide bounded evidence,
  not universal WCAG or browser-compatibility proof.

## Exact Authority Effect

This FAIL authorizes only Architecture to produce a revised static-concierge
plan and request a fresh independent review. **Architecture may not send this
plan or any Stage 1 write set to Implementation as written.** Implementation
remains parked. No browser, DreamHost, network, credential, evidence-skeleton,
capability, PHP, API, Git, staging, production, publication, or deployment
authority is granted. The v15 preflight/retry path remains permanently parked
for this release.

## Validation, Git State, And Preservation

- Candidate identity independently matched: 22,120 bytes; 469 lines; SHA-256
  `c00f32e8f50d174e9cf1c149dfc13849705fc5bd41fad0ef5262304315b7cc67`.
- `python scripts\verify_release.py`: PASS, exit 0;
  `release_verification status=passed manifest_files=47 cache_paths=0`.
- `git diff --check`: PASS, exit 0, no output.
- Branch: `main`; HEAD: `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`;
  upstream: `origin/main`; ahead/behind: `0/0`.
- Baseline and post-review Git state have no staged paths and no tracked diff.
  The worktree is dirty from preserved pre-existing untracked records plus this
  one authorized untracked audit.
- Package/release bytes, the static candidate, all prior website plans/audits/
  evidence, and implementation bytes were not changed. The `website/` tree
  remained absent. No root media was read, hashed, moved, modified, staged, or
  otherwise accessed; in particular, `yakherd.mp4` was not touched.
- No Git metadata mutation, DreamHost/browser/network access, credential or
  evidence-skeleton action, PHP/API work, implementation, staging, production,
  deployment, or publication occurred.

autonomous next action: Architecture may revise only the static-concierge plan and request a fresh exact Red Team review; Implementation and every live or deployment path remain parked.
