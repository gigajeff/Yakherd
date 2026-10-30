# Independent Red Team Review — Yakherd Concierge V1 Pre-Intake Bounded Plan

Date: 2026-07-21

Review target:

- path: `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan.md`
- observed bytes: `68774`
- observed lines: `1391`
- observed SHA-256: `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029`

Bound direction:

- path: `docs/2026-07-21_yakherd_concierge_v1_build_directive_static_only.md`
- observed bytes: `17487`
- observed SHA-256: `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`

Prior review:

- path: `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_build_directive_red_team.md`
- observed bytes: `19030`
- observed SHA-256: `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`
- verdict: `FAIL`

## Prioritized findings

### P0

No P0 finding was identified.

### P1 — The finalized tree cannot rerun its own required verifier

The exact Gate I command set runs `python -B scripts\verify_static.py` (`candidate:1206-1217`). That verifier must fail unless product paths 1-61 exist and the sole evidence path, path 62, is absent (`candidate:1223-1227`). The evidence path is then exclusively created as the last Gate I file (`candidate:1267-1309`). The resulting final tree therefore necessarily violates the precondition of its required verifier.

This is not just a transient implementation detail. Gate S is defined as the later independent security/parser review of the exact implementation bytes and deterministic archive evidence (`candidate:252-255`), yet no read-only final-state mode is specified for the verifier. Red Team cannot rerun the exact Gate I command on the final tree without moving, deleting, or ignoring an authorized evidence file. Such a mutation or substitution is not authorized.

The failure lifecycle is also incomplete. The evidence schema can name `FAIL`, but the plan says an implementation failure stops and asks Architecture for recovery, and an evidence-create/read-back failure is reported in chat (`candidate:1284-1305`). It does not define one durable structured failure record capable of representing a partial path set, retained parent directories, failed command, and final inventory. This conflicts with the Implementation role's requirement to preserve structured evidence (`packages/jeff_strict_ssot_v1/template/docs/prompts/implementation_task.md:10-14`) and leaves retained mutations dependent on transcript state.

This P1 blocks PASS even though the evidence correctly avoids embedding its own byte length or hash.

### P1 — The exact seven-day and deletion success copy exceeds site control

The plan correctly discloses browser, extension, operating-system, crash-recovery, form-restoration, backup, and synchronization boundaries (`candidate:1121-1129`, `candidate:1184-1204`). Its exact state machine, however, checks expiry only on initial read and reducer transitions (`candidate:1158-1161`) and explicitly has no timer, unload handler, or background operation (`candidate:1167-1173`). A closed or never-revisited origin can retain the localStorage value beyond seven days.

The exact success message nevertheless says `Saved in this browser for up to seven days` (`candidate:1171`). The exact deletion success says `Browser copy deleted and verified` after only a current-key `getItem` null observation (`candidate:1162-1165`, `candidate:1175-1177`). Those statements contradict the otherwise accurate retained-platform boundary: the application can verify the current origin key observation, not an upper bound on browser retention or deletion of every browser-managed copy.

These are beginner-facing privacy promises, not cosmetic labels. They must be lifecycle-true on closed, idle, restored, backed-up, and never-revisited paths.

### P1 — The dependency-free Node 20+ acceptance contract does not bind ES-module semantics

The selected application uses browser ES2020 JavaScript modules and literal relative imports (`candidate:91-100`, `candidate:410-416`, `candidate:465-469`). Production modules use `.js` paths (`candidate:293-303`). The write set expressly forbids a package manifest (`candidate:347-351`). Gate I nevertheless declares any Node 20+ runtime sufficient and runs `.mjs` tests using one exact `node --test` command (`candidate:1206-1217`), while requiring the tests to invoke shipped handlers and reducer code rather than replicas (`candidate:803-810`, `candidate:1253-1261`).

The plan supplies no package `type`, command-line module-mode flag, exact Node minor/runtime identity, or other reviewed mechanism that makes the shipped `.js` files unambiguously ES modules throughout the declared Node 20+ range. A `.mjs` test file does not by itself freeze how an imported ambiguous `.js` file is parsed. Consequently the exact no-dependency command is not a reproducible acceptance contract for all permitted prerequisites.

Gate I cannot depend on an unstated runtime-version behavior or an unlisted manifest/flag.

### P1 — The golden archive oracle is created by the implementation it is supposed to check

Gate P must freeze the complete input fixture after Gate R supplies public release identities (`candidate:998-1026`). It does not freeze expected dependent file or ZIP output identities. Instead, the sole Implementation writer creates the four dependent golden files, golden ZIP, Python verifier, JavaScript implementation, and `golden_identity.v1.json`; the Python code then records the archive identity that same implementation produced (`candidate:1028-1035`, `candidate:1212-1216`).

Separate code paths and a later Gate S review reduce risk, but they do not make the Gate I expected result independent. A shared misreading of the specification can make the builder, parser, generated golden, and recorded identity agree. The problem is amplified by two omissions:

- `golden_identity.v1.json` has no exact schema, canonical key set, nested types, or independently bound bytes in the candidate (`candidate:1028-1035`); and
- the final-state verifier contradiction above prevents Gate S from reproducing the exact required verification without an unreviewed exception.

The post-intake plan must bind an independently reproducible oracle and complete golden-identity contract before the product writer starts. Implementation must not define its own expected PASS bytes.

### P2 — UNKNOWN and restored values are not fail-closed for high-stakes screening

Question 11 permits `UNKNOWN`, and the `Make my prompt now` path records unanswered values as `UNKNOWN` (`candidate:526-540`). The high-stakes flag is true only for `YES` or a term match (`candidate:1109-1119`). A beginner who selects or inherits `UNKNOWN` with no matching keyword sees the useful unconditional warning but does not enter the acknowledgment gate.

The persistence schema makes this less exact: a restored `ANSWERED` row permits a validated scalar value but does not explicitly restrict question 11 to `YES`, `NO`, or `UNKNOWN` (`candidate:1131-1156`). The general statement that invalid types/ranges are rejected does not define normalization for an invalid choice string. The candidate therefore leaves both the unknown-risk policy and a corrupted/mutated stored choice capable of ambiguous handling.

### P2 — Optional persistence can retain secret-shaped input before the first scan

Raw answers, editor text, and the initial draft may be written to localStorage on every successful transition (`candidate:1131-1174`). The first required secret scan occurs only during approval (`candidate:740-760`). A beginner can therefore enable saving, paste a credential, and have it retained before seeing the secret warning.

The privacy copy explains that optional storage may persist, and the detector is correctly described as best-effort, but it does not disclose this ordering or require a scan before persistence. The plan must explicitly bind the pre-scan storage behavior and beginner warning rather than imply that the pre-download detector protects browser storage.

### P2 — Two public claims remain broader than the specified product behavior

First, the product boundary says the site does not “create or access a GitHub repository” (`candidate:58-68`), while the site intentionally advertises and allows user navigation to the Yakherd GitHub repository and release (`candidate:445-463`, `candidate:617-625`). The intended boundary appears to be no user-repository/API access, but the beginner-facing statement does not say that.

Second, the plan calls its list the permitted “browser-initiated requests” (`candidate:410-424`). The application can constrain its source and deliberate requests, but it cannot universally control user-agent, extension, captive-portal, favicon-probing, or platform behavior. The later wording correctly narrows the claim to what site code intentionally transmits (`candidate:491-501`, `candidate:1189-1204`); that narrower boundary must govern the exact request claim and acceptance interpretation.

### P2 — Gate I evidence syntax is not fully canonical despite claiming an exact record

The candidate names one schema ID and a list of required information (`candidate:1267-1297`), but it does not define the exact top-level keys, nested row keys/types/enums, ordering of path and command rows, bounded-output summary values, failure-state normalization, or partial-inventory representation. Canonical JSON serialization alone does not make an underspecified object canonical.

Gate P says its future plan must have its own exact evidence boundary (`candidate:220-236`). That later plan must supply the complete evidence schema and reject alternate shapes; it cannot merely copy the current prose list.

### P3 — Prior blockers that are materially closed

The candidate makes substantial, useful corrections:

- Gate A/R/B/P/I sequencing is explicit, serial, and fail-closed; this plan cannot authorize product code (`candidate:109-267`, `candidate:1374-1391`).
- `v1.2.0` is fixed rather than a moving release, and actual public artifact identities are mandatory before later gates (`candidate:11-22`, `candidate:120-165`, `candidate:823-860`).
- The separate `L:\dev\yakherd-web` root, current-task exclusion, single-writer rule, no-overwrite behavior, and non-wildcard Gate I file list are strong (`candidate:167-199`, `candidate:269-374`).
- The content-module design resolves the prior CSP/data-loading conflict, and the source/egress policy is much more testable (`candidate:83-107`, `candidate:395-507`).
- The textarea/UTF-8/no-normalization model, delimiter collision rule, approval snapshot, native-copy disclosure, and exact v1.2 handoff framing are well defined (`candidate:721-865`).
- Canonical JSON and ZIP32 Store-only header fields, limits, CRC, and manifest self-reference avoidance are otherwise precise (`candidate:895-1035`).
- All nine literal fixture length/SHA-256 pairs at `candidate:1012-1022` independently reproduced exactly.
- Browser/OS/accessibility, Git, host inventory, staging, deployment, DNS, production, and publication are separated from local implementation (`candidate:239-267`, `candidate:1206-1265`, `candidate:1311-1358`).
- DreamHost/v15 remains parked (`candidate:70-81`, `candidate:1383-1391`).

These closures should be preserved in a revision.

## Verdict

**FAIL.** The exact candidate is a strong pre-intake architecture draft, but the final-evidence/verifier cycle, privacy retention claims, Node module/test contract, and implementation-authored golden oracle remain blocking. It cannot grant Gate R preparation authority in this form.

## Required revisions before fresh review

A revised pre-intake candidate must, without performing product intake or implementation:

1. Define a read-only verifier lifecycle that validates the finalized tree including its evidence record, and define one durable, canonical failure record for partial, command, evidence-create, and read-back failures without self-reference.
2. Make every retention and deletion message truthful for idle, closed, restored, never-revisited, backup, and current-key-only observations.
3. Bind one exact dependency-free module-loading/test contract across the declared Node runtime range, consistent with the no-package-manifest write set and direct testing of shipped modules.
4. Freeze an independent expected-output oracle before Gate I and define the complete canonical schema/identity for every golden record.
5. Define fail-closed `UNKNOWN` and restored-choice behavior for high-stakes screening, plus the exact relationship between secret scanning and optional persistence.
6. Narrow GitHub and browser-request promises to behavior the site code can actually control.
7. Supply the complete Gate I evidence key/type/enum/order/failure schema that the future post-intake plan must bind.

Red Team has not selected repair bytes or modified the candidate; these are review predicates only.

## Residual risk

After those revisions, later independent gates must still verify the public v1.2.0 supply chain, installed intake bridge, same-writer parser independence, ZIP behavior in multiple parsers/operating systems, browser request observations, clipboard/download/storage lifecycle, qualified accessibility behavior, host headers/logs/cache/error routing, staging rollback, and identical production bytes. A static/no-backend design reduces server and provider-secret risk but does not eliminate browser, archive-parser, public-host, supply-chain, or handoff risk.

## Authority effect

This FAIL authorizes only a revised pre-intake candidate and a fresh independent Red Team review. Gate R remains parked. It does not authorize package/release preparation or mutation, Git/tag/GitHub/PyPI, network/browser, credentials, `L:\dev\yakherd-web` creation, product intake, Implementation contact or work, dependencies, image operations, evidence skeletons, hosting/DNS/staging/deployment/production/publication, or DreamHost/v15 activity.

The owner's standing sequence remains binding: only after Gates R, B, and P succeed and the new standalone post-intake plan receives a separate independent PASS may its exact Gate I slice be sent to the sole Implementation task attached to `L:\dev\yakherd-web`. Two implementation writers must never target one checkout.

## Validation and preservation

- Candidate identity: PASS — 68,774 bytes; 1,391 LF-terminated lines; SHA-256 `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029`.
- Direction identity: PASS — 17,487 bytes; SHA-256 `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`.
- Prior-audit identity: PASS — 19,030 bytes; SHA-256 `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`.
- Candidate encoding check: PASS — strict UTF-8, LF-only, no BOM, one terminal LF, no trailing whitespace.
- Literal fixture reproduction: PASS — all nine rows at candidate lines 1012-1022 matched their advertised byte lengths and SHA-256 values.
- Current intended engine identities at candidate lines 146-161 matched the local files and HEAD `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`; local tags remain `v1.1.0` and `v1.1.1`, and `CHANGELOG.md:5` still marks `1.2.0` unreleased. No network observation was made.
- `python scripts\verify_release.py`: PASS (`release_verification status=passed manifest_files=47 cache_paths=0`).
- `git diff --check`: PASS.
- Non-index candidate/audit UTF-8/LF/BOM/trailing-whitespace check: PASS for both records.
- Baseline Git state: branch `main`; HEAD `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`; upstream `origin/main`; ahead/behind `0/0`; staged paths `0`; tracked-diff paths `0`.
- Only this authorized audit path was created. Package/release bytes, prior untracked records, Git state, product/implementation paths, release state, browsers, network, credentials, dependencies, images, evidence skeletons, GitHub/PyPI, hosting/DNS/staging/deployment/production/publication, and DreamHost/v15 were not changed. `yakherd.mp4` was not read, hashed, moved, or touched.

autonomous next action: Architecture may revise the pre-intake plan for fresh independent review; Gate R and all product work remain parked.
