# Independent Red Team Review — Yakherd Concierge V1 Static-Only Build Directive

Date: 2026-07-21
Review target: `docs/2026-07-21_yakherd_concierge_v1_build_directive_static_only.md`
Observed identity: 17,487 bytes; 319 lines; SHA-256 `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`
Verdict: **FAIL**

The candidate is a useful product directive, but it is neither completed product intake nor a bounded Architecture authorization. It also contains unresolved release-bridge, browser-byte, deterministic-ZIP, privacy, source-policy, acceptance, repository, and deployment requirements. No Implementation handoff is authorized.

## Prioritized findings

### P0

No P0 finding was identified in this static design review.

### P1 — The required authority chain has not occurred

Evidence:

- The candidate itself says it becomes authoritative only after product intake, conversion by Architecture into a bounded plan, and independent Red Team PASS (`docs/2026-07-21_yakherd_concierge_v1_build_directive_static_only.md:5-8`).
- The intake contract requires the raw prompt and an exact provenance record under `docs/master_prompts/`, byte/hash verification, an explicit owner decision, and only then Architecture extraction (`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:6-35`).
- The candidate was preserved from attachment text by normalizing CRLF/CR to LF. That is a valid identity for this review target, but it is not the contract's raw, no-whitespace-normalization intake operation (`packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md:15-30`).
- Architecture is required to produce a bounded plan with alternatives, stages, evidence, gates, and forbidden scope (`packages/jeff_strict_ssot_v1/template/docs/prompts/architecture_task.md:3-17`). The directive supplies product requirements, not an exact implementation slice.
- Implementation must remain parked unless a reviewed Architecture authorization names the exact write set, tests, evidence, stop gates, forbidden scope, and Git boundary (`packages/jeff_strict_ssot_v1/template/docs/prompts/implementation_task.md:3-14`).

No installed raw prompt/provenance pair, owner promotion, bounded Architecture plan, exact implementation evidence path, or exact Stage 1 write set was found. Reviewing the directive cannot manufacture those missing authority records. This alone blocks Implementation.

### P1 — The repository and writer boundary is unresolved

Evidence:

- R-01 requires a separate `yakherd-web` repository and forbids placing the site in the audited Yakherd engine repository (`candidate:94-96`).
- X-02 says the site must not create a GitHub repository or touch Git (`candidate:75-78`), while the Definition of Done requires committed, staged, and live bytes (`candidate:294-297`).
- The named Implementation task currently points at `L:\dev\YAKHERD`, not an identified separate checkout. This review has no authority to create a repository or worktree.
- The directive names page concepts and a few logical resources (`candidate:29-38`, `candidate:108-122`, `candidate:142-143`, `candidate:163-164`) but does not enumerate exact destination paths for every HTML, CSS, JavaScript, JSON, text, SVG, image, header, test, fixture, license, and evidence file.

There is no exact repository identity, parent path, branch/worktree, all-new-path inventory, non-wildcard write set, no-overwrite/symlink rule, or single-writer checkout handoff. X-02/X-04 may sensibly describe runtime product behavior, but the directive does not expressly scope them that way; as written they also conflict with the requested implementation, testing, and publication lifecycle.

### P1 — The required public-release five-file bridge is not presently buildable

Evidence:

- B-02 requires the exact `product_intake.md` contract from a pinned public release (`candidate:184-187`). B-05 also requires that release's `START_HERE.md` (`candidate:198-201`). A-04 requires a fresh-install end-to-end bridge test (`candidate:278-280`).
- B-08 does not freeze a release. It selects the newest public tag at build time and again leaves room for a newer tag at ship time (`candidate:209-211`).
- The local repository has tags `v1.1.0` and `v1.1.1`; `v1.1.1` resolves to `f8d3890a58ff750e919ee088c1b904ad0e30c639`. Neither tag contains the package `product_intake.md` or `START_HERE.md` needed by B-02/B-05.
- Those resources exist in the current package version `1.2.0`, but `CHANGELOG.md:5-20` explicitly marks 1.2.0 as unreleased. The current `product_intake.md` is 2,614 bytes with SHA-256 `c1582bcc7918eeb547bcae8d4ceec14cfbe36267ed7313131012b0ba95c32604`; those bytes are not bound to a public tag in the local evidence.
- Network access was forbidden for this review, so a different remote/public state could not be substituted for committed evidence.

The target release, intake contract bytes, README/START_HERE bytes, archive/install identity, and bridge fixtures therefore are not frozen. The handoff design also lacks a collision rule for a user prompt containing `MASTER PROMPT START`, `MASTER PROMPT END`, or an equivalent delimiter line. B-02's reference to unspecified required “metadata” does not define byte-exact framing around the approved prompt. The stop condition at `candidate:314-319` is currently met.

### P1 — The runtime source contract contradicts the committed data-file design

Evidence:

- I-01 requires the question tree in `interview.v1.json` (`candidate:140-143`), and D-01 requires `prompt_template.v1.txt` (`candidate:161-164`).
- S-02 allows first-party assets while loading, then requires no request after load (`candidate:51-53`).
- The prescribed CSP is `default-src 'none'` with only script, style, and image exceptions; it does not allow `connect-src 'self'` (`candidate:263-266`). A browser `fetch()` of JSON or text is consequently blocked by the stated policy.
- No alternative byte-exact loading mechanism, initial-load ordering, integrity binding, failure behavior, or closed source allowlist is specified. Treating JSON as JavaScript or embedding either resource would change another explicit requirement unless Architecture reviews that choice.

The directive cannot simultaneously require those runtime files, that CSP, and unspecified loading behavior. Runtime request observation in A-02 (`candidate:272-275`) is useful evidence but cannot prove the absolute absence of every network-capable source or output sink. The plan needs a closed, mechanically checked HTML/CSS/JS/SVG source and egress policy, including navigation, forms, links, imports, media, workers, preload/prefetch, WebSocket/EventSource, beacon, and dynamically created URLs.

### P1 — Prompt approval and ZIP determinism are under-specified

Evidence:

- D-02 calls a JavaScript textarea's contents “whatever bytes are in that editor” (`candidate:163-166`). Browsers expose UTF-16 strings, not user-authored bytes; textarea newline handling and lone-surrogate encoding require an explicit normalization/rejection contract before UTF-8 bytes exist.
- D-03 revokes approval after editing (`candidate:167-171`) but does not bind approval to a stored byte snapshot/hash and require equality at copy/download time on every edit, undo, paste, programmatic, navigation, restore, and storage transition.
- B-01 promises exact UTF-8 bytes with preserved line endings (`candidate:181-183`) without defining how the editor, persistence, JSON, copy, download, and bridge paths preserve or reject their edge cases.
- B-07 calls its input list complete but omits bundle-affecting values such as `yakherd_target_release`, `prompt_edited_by_user`, high-stakes acknowledgment, and any exact question/template/pattern identities (`candidate:188-211`).
- B-03 says `generated_at` is ISO-8601 UTC but does not freeze one exact lexical grammar and range (`candidate:188-194`).
- B-06 freezes several ZIP properties but not their numeric header values or all canonical fields and limits (`candidate:202-205`). Missing decisions include general-purpose flags beyond the UTF-8 bit, version-needed, host/version-made-by values, internal/external attributes, local/central field equality, disk fields, comments, EOCD fields, ZIP64 rejection/limits, maximum entry/archive sizes, and failure behavior.

No independently reproducible CRC fixture, five-file golden archive, canonical JSON Unicode/number contract, or browser-independent byte-construction algorithm is named. The manifest correctly avoids self-reference by hashing the other four files (`candidate:195-197`), but that does not close the archive-byte contract.

### P1 — Privacy, anonymity, persistence, and secret-residue promises are not truthful enough

Evidence:

- X-07 says “Nothing leaves the browser, ever” (`candidate:82-83`) and P-03 says nothing typed leaves the browser (`candidate:237-239`), while the core feature writes a ZIP outside the browser and instructs the user to hand it to a local Yakherd process (`candidate:35`, `candidate:198-201`). The intended no-network promise is narrower than the text.
- X-06 calls the site “fully anonymous” (`candidate:81`), while X-10 permits host-level request measurement (`candidate:87-88`) and any ordinary host may process IP and request metadata.
- P-01 promises that closing a tab loses the session (`candidate:234`), which is not universally true under tab/session restoration, back-forward cache, crash recovery, memory snapshots, or browser-managed form restoration.
- P-02 leaves the storage system as `localStorage/IndexedDB` and states a seven-day expiry without specifying the selected store, origin/key/schema, clock basis, when expiry is enforced, migration/corruption/quota handling, verification, deletion verification, multi-tab behavior, or truthful retained-failure UI (`candidate:235-236`).
- G-01/G-03 describe best-effort secret detection (`candidate:218-228`) but do not identify exact pattern bytes, Unicode/index semantics for displayed spans, overlap ordering, false-positive handling, or how secrets are excluded from URLs, DOM attributes, error strings, logs, test artifacts, and retained evidence.

Browser, OS, clipboard, downloaded-file, password-manager, backup, sync, crash-recovery, and host-log boundaries need to be stated as user/platform boundaries rather than site-controlled deletion guarantees. These are beginner-facing trust claims and remain blocking.

### P1 — Acceptance and Definition of Done require ungranted and undefined capabilities

Evidence:

- S-04 forbids npm, build tooling, and build-time downloads (`candidate:56-57`).
- A-01 through A-08 nevertheless require Chromium, Firefox, WebKit, at least two operating systems, default extraction on Windows/macOS/Linux, a fresh Yakherd install, a screen-reader walkthrough, and an automated accessibility scanner (`candidate:272-286`).
- R-03 leaves the host undecided (`candidate:97-101`), while the Definition of Done requires staging and production to be live from committed bytes (`candidate:292-297`).
- S-07 requires behavior “identical to production” under `python -m http.server` (`candidate:61-64`), but the local server cannot reproduce HTTPS enforcement, host redirects, response headers, or response-only CSP such as `frame-ancestors` (`candidate:263-266`).

The directive does not identify already-available dependency-free test tools, browser/OS ownership, exact test commands, fixture bytes, evidence files, environment matrices, expected observations, human checkpoints, or stop/recovery branches. Nor does it authorize network, package installation, Git/GitHub, credentials, static-host configuration, DNS, staging, production, release, rollback, or publication. A live Definition of Done cannot be attached to a local-only implementation slice without separately reviewed gates.

### P2 — Asset, license, content, and header identities are not frozen

Evidence:

- T-04 identifies `yakherd2.png` only by an abbreviated digest and does not give a source path, byte length, destination, license/provenance, or copy policy (`candidate:115-116`). The tracked local file is 3,028,501 bytes with SHA-256 `e45c1c5449fff67c0ea4f2b4ed3af9e4886793939f89a449c9e996e1367a4383`, which matches the abbreviation but is not bound by it.
- R-02 leaves the website license open to a later override (`candidate:97`). Moving an asset to a separate public repository requires an explicit reviewed provenance/license decision.
- T-05 permits only `textContent` for user text (`candidate:117-118`), but an editable textarea normally requires its `.value` property. Safe non-HTML sinks need to be enumerated accurately rather than expressed as one impossible universal sink.
- The exact question tree, prompt template, no-JS fallback, secret patterns, high-stakes terms, SVGs, privacy copy, links, download policy, and host header/redirect bytes are not present or hash-bound.

External links and navigation are especially material to the zero-runtime-network and privacy claims, yet no exact link allowlist, `target`/`rel` rule, referrer behavior test, or user-initiated-navigation distinction is defined.

### P2 — Security-header and local-parity claims exceed what the named mechanisms can prove

Evidence:

- S-08 assumes a generic static headers/redirects file (`candidate:63-64`), but `_headers` syntax and behavior are host-specific.
- The CSP is said to be mirrored in a meta tag (`candidate:263-266`), but `frame-ancestors` is not enforceable from a meta-delivered CSP, and HTTPS enforcement, `X-Content-Type-Options`, and other response properties do not exist under the named dumb local server.
- A-08 therefore cannot prove literal behavioral identity (`candidate:286`). It can prove application-flow parity only after Architecture precisely separates response/transport properties from in-page behavior.

The directive also omits MIME, caching, compression, redirect, custom-error, directory-index, source-map, and public-file allowlist rules. These affect security, privacy, and byte-for-byte deployment verification.

### P3 — Sound retained boundaries

- R-05 and §16 keep DreamHost and the v15 capability path parked (`candidate:102`, `candidate:301-308`).
- S-01/S-03 and the deferred-relay rule provide a clear static/no-third-party direction (`candidate:49-60`, `candidate:301-305`).
- X-08 accurately says the website cannot confer governed approval (`candidate:84-85`).
- B-04 avoids manifest self-reference (`candidate:195-197`).
- H-01 provides a useful beginner-facing non-authority disclaimer (`candidate:247-251`).

These strengths survive, but do not offset the P1/P2 blockers.

## Verdict

**FAIL.** The exact directive is not a completed product intake or a sufficiently bounded Architecture plan, and its implementation/acceptance/deployment contract is not internally complete or presently feasible from the named released Yakherd bytes.

## Required fixes before fresh review

Architecture may prepare a new candidate only after the authority owner:

1. Completes the unchanged product-intake capture, provenance, byte/hash verification, and owner-promotion chain without treating this review as intake.
2. Produces a bounded local-only Stage 1 plan for an exact separate repository/worktree, with a non-wildcard all-new write set, single-writer/no-overwrite rules, exact evidence paths, commands, fixtures, stop gates, and forbidden scope.
3. Freezes one actually public Yakherd release and the exact install/archive, README, START_HERE, intake-contract, delimiter, collision, and five-file bridge bytes; or fails closed until such a release exists.
4. Resolves the CSP/data-loading contradiction and specifies a closed, testable source/egress/output-sink/navigation policy.
5. Defines one byte model for editor, approval snapshot, storage, copy, download, handoff, UTF-8, line endings, lone surrogates, canonical JSON, CRC-32, and every canonical ZIP header/limit; supplies independent golden fixtures.
6. Rewrites privacy, anonymity, tab-close, expiry, deletion, clipboard/download, browser/OS, host-log, and handoff claims to distinguish site-controlled behavior from platform/user behavior, with explicit retained-failure states.
7. Freezes full asset/content/license/provenance identities and all exact paths, including headers, links, templates, questions, patterns, fixtures, tests, and evidence.
8. Separates dependency-free local implementation acceptance from later browser/OS, fresh-install, accessibility, Git/GitHub, hosting, DNS, staging, deployment, rollback, production, and publication gates, each with separate capability evidence and authority.

Red Team has not supplied design choices or repaired the directive; the items above state the missing review predicates.

## Residual risk

Even after a revised plan resolves these blockers, deterministic ZIP behavior needs an independent parser/byte-level gate, beginner privacy copy needs adversarial browser-lifecycle testing, accessibility needs qualified manual coverage in addition to automation, and the exact public release/hosting state must be re-bound at the later release/deployment gate. A static-only design materially reduces server/API risk but does not remove browser, supply-chain, hosting-log, archive-parser, or social-handoff risk.

## Authority effect

This FAIL authorizes only a revised product-intake/Architecture candidate and a fresh independent Red Team review. It does **not** authorize contacting or un-parking Implementation, creating `yakherd-web`, installing dependencies, using browsers or the network, mutating Git/GitHub, changing package/release bytes, accessing DreamHost/v15, creating evidence skeletons, using credentials, configuring a host or DNS, staging, deploying, publishing, or starting any product implementation. The existing Implementation task remains parked at `L:\dev\YAKHERD`.

## Validation and preservation

- Candidate identity independently matched: 17,487 bytes; 319 lines; SHA-256 `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`.
- Repository at review baseline: branch `main`; HEAD `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`; upstream `origin/main`; ahead/behind `0/0`; staged paths `0`; tracked-diff paths `0`. The candidate and this audit are untracked documentation records.
- `python scripts\verify_release.py`: PASS (`release_verification status=passed manifest_files=47 cache_paths=0`).
- `git diff --check`: PASS. `git diff --cached --check` also passed; a non-index whitespace check of this untracked audit reported no errors after cleanup.
- Package/release files, prior plan/audit/evidence records, root media, Git state, website/implementation bytes, DreamHost, browsers, network, dependencies, repositories, credentials, staging, production, and publication were not changed. `yakherd.mp4` was not read, hashed, moved, or touched.

autonomous next action: Architecture may prepare a newly intake-bound, bounded static-concierge plan for fresh independent review; Implementation remains parked.
