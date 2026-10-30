# Yakherd.dev Concierge Composite Plan v8 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, v7, and the v8 amendment
- Verdict: **FAIL**

## Exact Candidate And Precedence

The reviewed composite is exactly:

1. frozen v3, SHA-256
   `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
2. incorporated v5, SHA-256
   `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
3. incorporated v6, SHA-256
   `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
4. incorporated v7
   `docs/2026-07-21_yakherd_dev_concierge_website_plan_v7.md`, SHA-256
   `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
5. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v8.md`, 18,573 bytes,
   431 lines, SHA-256
   `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`.

The preserved v7 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v7.md`,
SHA-256
`635f87c89b541200c1bdfd6de29854815ffcc516540ca7e7a760899011c2062c`.
Every supplied hash matches the reviewed bytes. Root `AGENTS.md` was reviewed at
SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team role prompt at SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is clear. V8 replaces v7 Appendix A/PHP identity, the entire v7
`failure_state`, and the Error Logs route. V7's one-attempt/no-retry lifecycle
and cached-header removal remain; v6's manifests, work recovery, File Manager,
and deployment suspension remain; all cron authority remains removed
(`v8:19-23`). No contradictory lower-precedence PHP, failure object, log query,
cron, or deployment action survives.

No DreamHost or network access was used for this document review.

## Appendix A Independent Reproduction

The literal Appendix A bytes were independently joined with LF line endings and
one terminal LF and encoded as UTF-8 without BOM. They reproduce exactly:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

Both values match `v8:29-38`. The exact POST body `{"run":true}` remains 12
UTF-8 bytes. Appendix source identity passes; the verdict follows from the
failure-state representation below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — The strict inventories cannot represent the unobservable states they enumerate

V8 correctly adds `FILE_MANAGER_OBSERVABILITY` and allows fixture/work state and
type values of `UNKNOWN`. It also requires every failed attempt to embed one
strict object (`v8:56-78`, `v8:82-108`). However, both inventory schemas require
boolean presence facts even when the File Manager has become unavailable or the
path cannot safely be inspected:

- every fixture row requires `presence: boolean`, and
  `unknown_entry_present` is also a boolean (`v8:129-150`);
- the work directory and every child require `presence: boolean`, while
  `unknown_child_present` is also a boolean (`v8:152-169`).

Consider an authorized failure in which File Manager visibility is lost after a
probe or during cleanup. The truthful final state is `fixture.state=UNKNOWN`
and/or `work.state=UNKNOWN_RETAINED`, with `FILE_MANAGER_OBSERVABILITY` in
`failed_checks` and the corresponding retained class. Architecture cannot know
whether a particular path or unknown child is present. Yet `presence` cannot be
null/unknown, and the two “unknown present” fields cannot express unobservable.
Choosing `true` or `false` guesses remote state; setting `type=UNKNOWN` does not
repair the contradictory definite presence claim.

The same problem occurs if the UI exposes a known regular retained file but an
individual download/hash is unavailable: `FILE_MANAGER_TRANSFER` truthfully
fails, but the fixture rule says a known regular source file uses a boolean
`sha256_match` rather than allowing “unobserved” (`v8:147-150`). Marking the hash
false conflates a proven mismatch with no observation; marking it true invents
evidence.

V8 says unknown/missing keys and invalid values are rejected and that the
canonical object must compare to the mutation ledger (`v8:77-78`,
`v8:171-180`). There is therefore no legal truthful serialization for a failure
the schema expressly anticipates. This is the same evidence-completeness class as
v7 P1-1: the remote action remains fail closed, but the mandatory independent
failure evidence cannot be produced without lying.

### P2 — Medium

#### P2-1 — State derivation and the row null/type matrix remain underspecified

The field names and enums are much more precise, but the rules do not define the
invariants that derive `fixture_inventory.state` from its rows and
`unknown_entry_present`, or `work_inventory.state` from directory/children and
`unknown_child_present`. For example, it is not stated whether a symlink at
`fixture`, an extra hidden entry, or an unobservable known path is
`EXPECTED_SUBSET` versus `UNKNOWN`.

Several row combinations also remain legal in syntax but contradictory in
meaning. The fixture rules require null hash for directory/nonregular rows but do
not require null `byte_length`; they do not state the required mode/length/hash
combination for `UNKNOWN`, `SYMLINK`, `OTHER`, or a regular file whose download
failed. The work rules say length/hash fields “apply only” to regular files but
do not give the complete per-type null matrix; directory `owner_match` and child
`target_match` have only partial rules (`v8:136-169`).

Because the object is canonical and strictly parsed, these semantic invariants
must be just as finite as the keys. Otherwise two reviewers can accept different
objects for the same final inventory.

#### P2-2 — Pre-credential failures have no exact client-cleanup N/A semantics

V8 includes `CERTIFICATE`, `ROOT_INVENTORY`, and File Manager preconditions in
`failed_checks`, so failures before credential creation are intended to be
recordable. The top-level object nevertheless requires boolean
`password_record_deleted`, `staging_tabs_closed`, and `browser_restarted`, with
no null/not-applicable value or stated vacuous-truth rule (`v8:58-75`).

The incorporated sequence performs certificate/root inventory before the human
credential checkpoint. On such a failure, no password record or Basic Auth
browser session ever existed and v7's post-enable restart lifecycle does not run.
Setting the booleans false makes unrelated client cleanup appear failed; setting
them true claims deletion/restart actions that did not occur. V8 excludes only a
human declining the checkpoint from “started attempt” and does not define the
start boundary or N/A encoding for these earlier failures (`v8:58-60`).

#### P2-3 — The check table is finite but does not define exact mapping for all incorporated cleanup operations

The table now covers the previously missing runtime, cURL, panel-disable, tab,
manifest, HTTP, log, and retained-state cases, and `failure_classes` may correctly
be empty after full cleanup (`v8:80-127`). Two incorporated operations still lack
an exact named mapping:

- failure to delete the individually downloaded File Manager verification files
  or their OS temporary directory required by v6's finite transfer route; and
- failure to create/finalize the sole capability evidence document itself after
  the remote/client sequence.

`LOCAL_VALIDATION`, `FILE_MANAGER_TRANSFER`, and `MANIFEST_EVIDENCE` could be
interpreted to cover these, but V8 does not state which, whether multiple IDs are
required, or how a retained local temporary path is represented in
`failure_classes`/the mutation ledger. Similar ambiguity remains for an approved
checkpoint where the password manager cannot produce/prove the required entropy
before panel submission: `PANEL_ENABLE` is available but no mapping is stated.
An exhaustive strict table needs an explicit gate-to-ID mapping rather than
relying on broad inference.

### P3 — Low / Observations

#### P3-1 — Bootstrap and runtime containment are corrected

Appendix A uses only suppressed, machine-path-free `ini_set` and `ob_start`
operations before sensitive work; captures all three results; short-circuits to
fixed generic output on failure; and requires their conjunction as
`error_channel_contained` for normal `200` (`v8:40-54`, `v8:236-305`,
`v8:414-430`). After successful bootstrap, v7's shutdown, warning-to-exception,
buffer discard, display/log suppression, generic catch, and fixed response remain
effective. No filesystem, cURL, JSON, provider body, source, credential, or
machine path is used in the failed bootstrap branch.

#### P3-2 — Clean versus retained failure causes are properly separated at the top level

`failed_checks` is nonempty and finite; `failure_classes` describes only retained
or unobservable state and may be empty for a clean failure (`v8:62-127`). The
table includes the earlier missing PHP/runtime, cURL option, direct/TLS/status,
provider bound, panel disable, tab closure, manifest, HTTP/header, File Manager,
access/error-log, cleanup, and final-inventory gates. The canonical ASCII JSON,
SHA-256, padded unwrapped base64 preimage, and decoded table at the sole evidence
path create a reproducible independent review artifact (`v8:171-180`). P1-1 and
P2-1 concern unknown/null semantics inside that otherwise sound structure.

#### P3-3 — Error Logs observation is now secret-safe and finite

Architecture must prove count-only/redacted results before querying. Otherwise
it takes no snapshot or DOM/network read, yields entirely to a human who reports
only `zero`/`nonzero`, and never queries row-rendering mode itself. Lack of either
channel fails without a query; nonzero/unanswered results fail; no row body,
path, message, source, IP, credential, or unrelated event enters the tool
transcript/evidence (`v8:182-204`). The incorporated UTC window, fixed path,
retention/no-delete rule, and access-log separation remain.

#### P3-4 — Credential, cURL, cron, manifest, File Manager, and authority boundaries remain closed

V7's one affirmative checkpoint, one enable submission, one credential, no
retry, full password-record/tab/browser cleanup, and removal of cached-header
inspection remain incorporated. V7/v8 cURL requires strict option success and
short-circuits before transfer; the fixed URL, no-proxy/no-redirect, TLS/time,
effective URL, 4096-byte non-retained body, and status gates remain required for
`200`. V6 manifest preimages, private work path/recovery, and finite File Manager
route remain.

Every cron source/path/job/action remains removed. The sole live evidence path is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`. A plan PASS
could authorize only the disposable preflight; a later independent PASS on exact
live evidence is still required before unchanged v3 Section 9 local-only
Implementation. DreamHost deployment, cron, SSH, Git, staging release, provider
secret, live model use, and production remain blocked (`v8:206-219`). No new
dependency cycle, unlisted remote write/delete/network path, or downstream
authority leak was found.

#### P3-5 — No secret value or observed machine-specific identifier is present

V8 contains symbolic paths, fixed public hosts/role names, source hashes, enum
labels, and test payloads only. It contains no observed DreamHost
username/home/server, credential or derived value, private key, API key, provider
body, log row, or personal data.

## V7 Finding Closure Status

| V7 finding | V8 status |
| --- | --- |
| P1-1 missing clean failure classes | Substantially resolved by `failed_checks` plus empty clean `failure_classes`; unknown fixture/work presence remains unrepresentable (P1-1). |
| P2-1 ambiguous nested inventories | Row keys/enums are added, but unknown presence, state derivation, and complete null/type invariants remain unresolved (P1-1/P2-1). |
| P2-2 unchecked output buffer | Resolved by suppressed/captured bootstrap results and 200 dependency. |
| P2-3 unsafe nonzero Error Logs rendering | Resolved by pre-query count-only proof or a human-only no-snapshot/DOM/network-read channel. |

## Required Blocking Revisions

Before another independent review, Architecture must provide a new exact,
hash-identified candidate that:

1. lets fixture/work presence and unknown-entry/child facts represent
   unobservable state without guessing, and permits an unobserved hash for a
   known regular retained file while distinguishing it from a proven mismatch;
2. defines the exact state-derivation rules and complete per-type
   presence/mode/length/hash/target/owner null matrix for every fixture and work
   inventory row;
3. defines when a preflight attempt starts and gives pre-credential failures an
   exact N/A/vacuous encoding for password-record, tab, and browser cleanup
   fields; and
4. states the exact `failed_checks`/retained-state mapping for local verification
   temp cleanup, evidence-file creation/finalization, and pre-submit credential
   generation/masking failures.

V8, v7, v6, v5, v3, all earlier plans/audits/evidence, package/release bytes, and
unrelated files must remain preserved. These findings do not authorize Red Team
to repair the candidate in place.

## Residual Risks And Mandatory Future Gates

After correction, live evidence must still prove staging TLS, panel Basic Auth
before all content/error/method responses, hidden/root inventory, File Manager
byte/mode fidelity, canonical manifest/failure preimages, PHP/bootstrap/runtime
support, generic output/error behavior, path/filesystem primitives, exact work
cleanup/recovery, direct bounded credential-free OpenAI TLS, minimized access and
Error Logs, panel removal, client cleanup, final exact inventory, required local
validation, and fresh independent capability review. Ambiguity remains a
capability FAIL.

The later deployment amendment remains mandatory for final cron, SSH/host keys,
manual staging auth, production/staging Apache bytes, immutable releases,
manifests, atomic publication, A/B/source-independent rollback, Git, provider
secret, canary, staging release, and production. V8 grants none of those actions.

## Validation And Preservation

Required documentation-only validation after writing this audit:

- `python scripts\verify_release.py`: PASS, exit `0`;
  `release_verification status=passed manifest_files=47 cache_paths=0`.
- `git diff --check`: PASS, exit `0`, no output.

Repository state at review completion: branch `main`, HEAD
`97b470f8342cfba619da8f13bd224b2c6c4e2e2a`, upstream `origin/main`,
ahead/behind `0/0`, no staged path, and no tracked diff. The pre-existing plans,
audits, evidence, beginner guide, and `yakherd.mp4` remain untracked. Their Git
status was not changed. Package `MANIFEST.json` remains SHA-256
`ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`
and package `RELEASE.json` remains SHA-256
`312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`.

No package/release byte, existing plan/audit/evidence byte, DreamHost state,
credential, Git state, or website implementation byte was changed. Appendix A
was hashed in memory and was not materialized. The unrelated `yakherd.mp4` was
not read, hashed, moved, modified, staged, or otherwise touched. The only write
was this authorized v8 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v8 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review. Implementation may
not receive v8 as written; unchanged v3 Section 9 remains parked. No DreamHost
panel/File Manager/Logs mutation or inspection, human credential checkpoint or
creation, fixture materialization/upload, probe/network request, cron, SSH, SFTP,
release/deployment, Git action, provider secret, staging release, live model
request, or production action is authorized.

No previous plan PASS, hosting inventory, or partial v8 finding overrides v8's
own block (`v8:25-27`) or the separate fresh independent live capability PASS
required before Implementation (`v8:206-219`).

autonomous next action: Architecture must issue a new exact candidate resolving every v8 P1/P2 finding; Implementation, DreamHost, Git, credentials, cron, staging, and production remain parked.
