# Yakherd.dev Static Concierge Plan v2 — Independent Red Team Review

- Date: 2026-07-21
- Candidate: `docs/2026-07-21_yakherd_dev_static_concierge_plan_v2.md`
- Verified candidate identity: 39,363 bytes; 752 lines; SHA-256
  `9355aa673fbc7c5e80427d4f7cdba67d54f1bd3a14fcab99c7cafaf89667efed`
- Prior FAIL audit: 14,266 bytes; 250 lines; SHA-256
  `c4ec34394032c6ef4fd7bc881e30da3ead426226f10a119ce561b67e6d794457`
- Verdict: **FAIL**

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — The exact temporary-directory state is impossible in this checkout and has unsafe ownership branches

The plan authorizes `.tmp/`, one acceptance directory, and one disposable file
(`docs/2026-07-21_yakherd_dev_static_concierge_plan_v2.md:484-496`,
`:514-516`). Its preflight then uses a plural subject to require both `.tmp` and
the acceptance directory to contain no child other than the permitted artifact
(`:518-522`). This cannot hold:

- the preserved `.tmp/` in this exact checkout currently has 64 children; and
- even in a new empty `.tmp/`, its direct child would be the acceptance
  directory, not the nested permitted artifact.

The same overbroad completion rule rejects every extra child in authorized
directories (`:555-565`). Exact Stage 1 must therefore stop before its required
download observation. It may not delete or relocate the preserved `.tmp`
children to make the plan pass.

The ownership and recovery rules also permit destructive ambiguity. The plan
requires the final file to be absent but does not require the acceptance
directory itself to be absent or created by this attempt before deleting that
directory (`:522-530`). A pre-existing empty user directory can therefore be
removed. If file deletion succeeds but directory deletion fails, the retained
state is an empty directory, contradicting the assertion that the artifact is
the only permitted retained failure (`:524-530`).

The required real-browser download is not bound to an exact available mechanism
that avoids browser/tool `.crdownload`, `.part`, profile, or tool-owned
temporary bytes (`:514-530`, `:647-670`). The plan says to stop if exact
destination control is unavailable, which is fail-closed, but it does not first
establish that the mandatory acceptance can be executed inside its literal
write boundary.

Finally, the twelve site/test files and implementation evidence have no
immediate pre-write absence, containment, ordinary-parent, and no-reparse
preflight (`:484-512`). Completion-time untracked/type checks
(`:546-565`) cannot prove that an already-untracked user file was not
overwritten or that a pre-existing redirecting parent was not traversed. The
word `create` does not define whether Implementation may edit only files it
created during its attempt or how a partial implementation is retained. The
non-index diff and all-file hash design are good, but they do not establish
source ownership.

#### P1-2 — The dependency-free “closed” source/egress verifier remains semantically open

The candidate now defines a substantially stronger static policy, but calls it
closed and mechanically verified using `html.parser`, `ElementTree`, and direct
source inspection (`static_concierge_plan_v2.md:373-388`). The JavaScript part
is still a blacklist plus a semantic assertion (`:419-443`), not a closed
lexical grammar or complete operation allowlist. For example, the written bans
do not mechanically reject:

- global `open(...)` or newer navigation APIs;
- `dispatchEvent(new MouseEvent(...))` on one of the existing external anchors;
- `Object.assign(existingImg, {src: ...})` or `Reflect.set(...)`, which can put
  visitor text in a same-origin URL without a `.src` or `.href` source token;
  or
- prototype/destructuring forms that invoke a property without the listed dot
  spelling.

Those examples violate the prose invariant, but the plan does not define how
the promised dependency-free verifier recognizes them. The catch-all that only
listed egress-capable operations are permitted (`:437-443`) is the property to
be proved, not an exact proof procedure. The CSP also remains specified as “at
least” rather than an exact value (`:375-379`), while the HTML attribute policy
does not freeze every security-relevant attribute value.

The CSS scan is likewise not closed: it rejects literal `url(` and `@import`
but does not define comment/escape normalization or a property/function
allowlist (`:444-445`). Escaped `u\72l(...)` or a dormant same-origin
`image-set(...)` can evade those literal checks. `img-src 'self'` permits such a
request.

Runtime Resource Timing and DevTools observations cover only enumerated,
exercised flows (`:455-463`, `:647-670`). They cannot close an input-dependent,
viewport-dependent, or otherwise dormant branch, and Resource Timing does not
itself cover every top-level/browser navigation. The exact observer, clean
browser/profile boundary, top-level navigation treatment, and browser-generated
housekeeping request treatment are not frozen. Static inspection and runtime
sampling are complementary, but this combination still cannot support the
plan's absolute no-egress assurance as written.

### P2 — Medium

#### P2-1 — Checkbox deselection is missing from the exact approval-transition table

The visible contract says site controls are enabled only while the review box
is selected (`static_concierge_plan_v2.md:130-134`). The detailed invalidation
list handles edits, regeneration, clear, validation, and export failures but
does not name unchecking the review box (`:320-340`). The Node transition list
also omits it (`:625-645`); the browser phrase “checkbox transitions” has no
expected-state mapping (`:647-654`). Export revalidation will prevent an actual
unchecked export, but an unchecked box can leave an enabled-looking control and
resident approval snapshot until that control is attempted. This contradicts
the beginner-facing state promise.

#### P2-2 — The automated acceptance does not bind DOM-facing assertions to exact production handlers

The pure module is required to export validation, candidate, envelope, and
export-spec functions (`static_concierge_plan_v2.md:221-226`). Node tests are
then required to prove approval-event invalidation, Clipboard calls, anchor
mutation/click count, and cleanup branches (`:625-645`). Those behaviors are
DOM-facing production-handler behavior, but the plan names no production export,
dependency-injected handler seam, or dependency-free DOM harness. A test can
otherwise model or reimplement the intended transition instead of exercising
the shipped handler. The same ambiguity applies to cleanup-operation failures:
sequential `removeAttribute` then `revokeObjectURL` in one `finally` does not
guarantee revocation if the first cleanup operation throws (`:349-356`).

The plan must identify the exact shipped functions and injected capabilities
under test, including checkbox deselection, in-flight/stale async copy results,
anchor cleanup failure, and revoke failure, without adding a DOM package or an
unlisted module.

#### P2-3 — Browser-controlled privacy and test side effects are not fully frozen

The revised lifecycle disclosure is honest and `autocomplete="off"` is required
(`static_concierge_plan_v2.md:358-371`). However, the first-release goal still
says all idea processing occurs in the loaded page (`:19-23`), while the source
policy merely allows a `spellcheck` attribute without requiring
`spellcheck="false"` (`:402-404`). Browser spelling/grammar services may be
outside page control just like extensions and input methods. The literal
beginner promise should be scoped to site code, and the form policy should
disable browser assistance where possible while disclosing that browsers may
ignore preferences.

The required real site-copy success can also overwrite or synchronize the
operator's clipboard (`:101-108`, `:647-660`). The plan does not say whether
this observation uses an injected browser fake or a real OS clipboard, nor does
it authorize a human checkpoint for that client-state mutation. Reading the old
clipboard to restore it could itself expose unrelated sensitive data. The test
must use a defined isolated/fake boundary or obtain explicit informed approval
without reading prior clipboard contents.

### P3 — Low

#### P3-1 — Edited candidates have no final size ceiling

Form inputs are bounded, but the edited candidate validator rejects only empty,
CR, malformed-surrogate, and delimiter-collision states
(`static_concierge_plan_v2.md:203-208`, `:298-301`). A pasted arbitrarily large
edited candidate can therefore drive snapshot duplication, envelope creation,
Clipboard, Blob, hashing, and DOM work. This is a local availability/usability
risk rather than a server cost risk. Freeze a final edited-candidate limit and
test its exact boundary, or disclose and justify the unbounded local behavior.

## Prior-Finding Closure Matrix

| Prior required area | V2 result |
| --- | --- |
| Intake envelope, delimiter collisions, candidate/envelope distinction, extraction/hash fixture | Resolved by lines 221-340 and 625-637; unchanged intake identity also matches. |
| Native-copy truthfulness and approval equality/invalidation | Partially resolved; native copying and snapshot equality are honest, but checkbox deselection remains unspecified. |
| Site-controlled lifecycle language and browser/OS disclosure | Substantially resolved; the residual spellcheck/first-screen wording issue is P2. |
| Parent/durable/temp paths, cleanup, retained failure, untracked table, non-index review | Not resolved because the `.tmp` state is impossible and pre-write ownership/no-overwrite is incomplete. Non-index diff and file hashes are resolved. |
| Closed dependency-free HTML/CSS/JS/SVG egress policy and runtime observations | Not resolved; SVG and much of HTML are closed, but JavaScript/CSS proof and runtime coverage remain open. |
| Lone-surrogate rejection and edited envelope/download byte fidelity | Resolved at the deterministic contract level by lines 221-356 and 625-643. |
| Unconditional high-stakes warning | Resolved by lines 142-145 and automated-copy checks. |
| Download/SVG/external-link rules | SVG/link and nominal download rules are resolved; exact browser-temp and cleanup-failure behavior remain open. |
| Separately reviewed read-only hosting inventory | Resolved by lines 584-600; it grants no current live authority. |

## Verdict

**FAIL** for the exact 39,363-byte v2 candidate identified above.

V2 is a material improvement. It closes the intake envelope, native-copy
truthfulness, site-controlled lifecycle language, surrogate handling,
unconditional high-stakes warning, most exact-diff evidence, SVG/external-link
policy, and hosting-inventory sequencing. The impossible temporary-state gate
and non-closed egress verifier are nevertheless blocking P1 defects. The plan
cannot safely or reproducibly authorize Stage 1 as written.

## Required Fixes

1. Separate `.tmp` parent containment/type checks from the acceptance-directory
   inventory. Preserve unrelated `.tmp` children. Require the acceptance
   directory to be absent and exclusively created by the current attempt (or
   stop), represent every partial cleanup state, and delete only run-created
   exact paths. Bind the real-download observation to an available mechanism
   and its complete repository/workspace and browser-owned temporary lifecycle.
2. Add an immediate fail-closed pre-write inventory for every durable parent,
   directory, and file: repository containment, ordinary type, no
   symlink/reparse/alternate stream, target absence, exclusive creation, and
   explicit authority to modify only paths created by this attempt until the
   freeze. Define retained partial state without overwriting or deleting
   pre-existing user paths.
3. Replace the JavaScript/CSS semantic blacklist with a mechanically exact
   dependency-free grammar/operation allowlist or equally reproducible closed
   verifier. Freeze CSP and security-relevant attribute values, JavaScript
   global/member/property-write/call forms, CSS escape/comment processing and
   load-capable properties/functions, every allowed exception, and exact
   top-level/runtime observation boundaries. Test adversarial equivalent forms,
   not only the intended flows.
4. Add checkbox deselection to the atomic invalidation table and to exact Node
   and browser expected-state tests.
5. Identify an exact production-handler test seam for approval, copy, download,
   and nested cleanup behavior. The dependency-free tests must execute shipped
   logic rather than a duplicated test model and cover every cleanup and stale
   async branch.
6. Scope “all processing” to site code, require `spellcheck="false"` where
   supported, retain the browser-service disclosure, and define whether
   copy-success testing uses a fake/isolated clipboard or a human-approved real
   clipboard mutation without inspecting old clipboard contents.
7. Bound or explicitly justify the maximum edited-candidate size and add the
   corresponding acceptance boundary.

Any revision requires a new exact candidate and fresh independent review. Red
Team did not repair the candidate.

## Residual Risk

- A static page and local tests cannot control browser extensions, input
  methods, OS clipboard sync/history, downloaded copies, browser recovery, or
  every user-agent request. Corrected copy must disclose these boundaries.
- A generated envelope is untrusted visitor input and gains no Yakherd authority
  until unchanged product-intake preservation, provenance, extraction,
  promotion, and independent review complete.
- Local meta CSP and browser observations do not establish live TLS, headers,
  caching, clickjacking protection, 404 behavior, remote inventory, deployment,
  or rollback. Every hosting phase remains separately gated.
- Manual accessibility and two-engine checks are bounded observations, not
  universal conformance or compatibility proof.

## Exact Authority Effect

This FAIL permits only Architecture to create a new static-concierge plan
candidate and request fresh independent review. **Architecture may not send v2
or its Stage 1 write set to Implementation.** Implementation remains parked.
No browser, DreamHost, network, credential, evidence-skeleton, capability,
hosting inventory, PHP, API, Git, staging, production, publication, deployment,
or v15 authority is granted. The v15 path remains permanently parked for this
release.

## Validation, Git State, And Preservation

- Candidate identity independently matched: 39,363 bytes; 752 lines; SHA-256
  `9355aa673fbc7c5e80427d4f7cdba67d54f1bd3a14fcab99c7cafaf89667efed`.
- Prior FAIL audit identity independently matched: 14,266 bytes; 250 lines;
  SHA-256
  `c4ec34394032c6ef4fd7bc881e30da3ead426226f10a119ce561b67e6d794457`.
- Unchanged product-intake identity independently matched: 2,614 bytes;
  SHA-256
  `c1582bcc7918eeb547bcae8d4ceec14cfbe36267ed7313131012b0ba95c32604`.
- `python scripts\verify_release.py`: PASS, exit 0;
  `release_verification status=passed manifest_files=47 cache_paths=0`.
- `git diff --check`: PASS, exit 0, no output.
- Branch: `main`; HEAD: `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`;
  upstream: `origin/main`; ahead/behind: `0/0`.
- Baseline Git state had no staged paths and no tracked diff. The worktree was
  dirty only through preserved untracked records; this review adds only the
  authorized untracked v2 audit.
- Package/release bytes, v1/v2 static plans, the prior audit, every dynamic
  plan/audit/evidence record, and implementation state were not changed. The
  `website/` tree remained absent. Root media was not read, hashed, moved,
  modified, staged, or otherwise accessed; in particular, `yakherd.mp4` was not
  touched.
- No Git metadata mutation, DreamHost/browser/network access, credential or
  evidence-skeleton action, PHP/API work, implementation, hosting inventory,
  staging, production, deployment, or publication occurred.

autonomous next action: Architecture may create only a new static-concierge plan candidate and request fresh exact Red Team review; Implementation, v15, Git, hosting inventory, and every live/deployment path remain parked.
