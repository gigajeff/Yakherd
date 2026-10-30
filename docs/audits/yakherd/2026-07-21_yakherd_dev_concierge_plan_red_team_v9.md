# Yakherd.dev Concierge Composite Plan v9 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, v7, v8, and the v9 amendment
- Verdict: **FAIL**

## Exact Candidate And Precedence

The reviewed composite is exactly:

1. frozen v3, SHA-256
   `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
2. incorporated v5, SHA-256
   `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
3. incorporated v6, SHA-256
   `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
4. incorporated v7, SHA-256
   `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
5. incorporated v8, SHA-256
   `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
6. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v9.md`, 12,067
   bytes, 250 lines, SHA-256
   `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`.

The preserved v8 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v8.md`,
SHA-256
`d895ce12b8c648a56a9e91da2a9aa388dcde8988511280ca4d17a2d0c00f6f3b`.
Every supplied identity matches the reviewed bytes. Root `AGENTS.md` was
reviewed at SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team prompt at SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is finite. V9 replaces v8 Sections 3–3.3 and the corresponding
top-level failure fields, adds the attempt/evidence bootstrap, and leaves the v8
PHP, serialization/embedding, runtime, cURL, Error Logs, one-attempt, no-cron,
File Manager, and authority rules in force (`v9:20-30`). No lower-precedence
cron, cached-Authorization inspection, executable, retry, deployment, or
Implementation authority reappears.

No DreamHost or network access was used for this document review.

## Unchanged Appendix A Reproduction

V9 changes no executable byte (`v9:20-24`). I independently extracted the
literal v8 PHP fence, joined its lines with LF, added one terminal LF, and
encoded it as UTF-8 without BOM. It reproduces exactly:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

Those values match v9's identity and the inherited v8 declaration. Appendix
source identity passes; the verdict follows from the failure evidence and
credential lifecycle below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — Known presence with unobservable type or length still has no truthful row

V9 fixes total File Manager loss and makes presence, extra-entry/child, SHA,
target, and owner observations tri-state. A known regular source whose download
or hash fails can now use `sha256_state=UNOBSERVABLE` (`v9:80-125`), and the work
schema provides the corresponding target and owner states (`v9:127-179`). Those
are real closures.

The row model is still not total for partial File Manager loss, however:

- fixture `type=UNKNOWN` is legal only when `presence=UNOBSERVABLE`
  (`v9:97-108`), and a present regular file must have an observed nonnegative
  `byte_length` (`v9:103-105`);
- the work directory matrix has no `presence=PRESENT,type=UNKNOWN` case
  (`v9:134-144`); and
- each present regular work child likewise requires an observed nonnegative
  length, while the only `UNKNOWN` type row is the wholly unobservable row
  (`v9:146-167`).

The inherited File Manager contract explicitly says to stop when any details
field is unavailable and forbids an alternate verifier or guessed value
(`v6:198-225`). Therefore a started attempt can truthfully know that
`fixture/capability.php` or `first.bin` is present while losing the properties
view that distinguishes its type, or know it is regular while losing its length
field. V9 cannot encode either state: changing `PRESENT` to `UNOBSERVABLE`
discards a known fact, choosing a concrete type or length invents evidence, and
null length is illegal for a present regular row.

That is a mandatory failure branch, not a merely descriptive corner case. It can
force the evidence finalizer either to violate the schema or to lie after a live
mutation. The v8 P1 evidence-completeness defect is narrowed but not closed.

#### P1-2 — Pre-submit credential failures can retain a generated secret while all browser cleanup is N/A

The inherited procedure has the human generate a new secret and fill the panel's
masked password and confirmation controls before the panel-enable submission
(`v6:235-252`). V9 then requires all client fields to be `NOT_APPLICABLE` before
a password-manager record exists, and, after record creation but before submit,
makes only record deletion applicable; tab closing and browser restart remain
`NOT_APPLICABLE` (`v9:181-192`). Its generation/masking failure branches say only
that record cleanup becomes applicable if a record was created and that any
created record is cleaned/deleted (`v9:208-215`).

Two ordinary no-submit outcomes remain unsafe and unrepresentable:

1. the generator fills the masked panel fields but does not create/save a
   password-manager record before entropy proof fails; and
2. a record is created and later deleted, but masking proof fails while the
   generated value remains in the live panel form.

In both cases the remote enable is correctly not submitted, yet v9 supplies no
exact action or evidence field for clearing the panel fields, navigating away or
closing that panel tab, and disposing of any ambiguous pending password-manager
save. In the first case it affirmatively encodes every client action as
`NOT_APPLICABLE`; in the second it can report record cleanup `COMPLETE` while the
same secret remains in browser form state. A password-manager creation timeout
also has no exact conservative encoding for “record existence unobservable.”

This violates the complete one-credential lifecycle inherited from v7/v6 and
leaves credential-bearing client state outside the typed cleanup contract. The
fact that no panel submission occurred limits remote exposure but does not make
the local secret state safe.

### P2 — Medium

#### P2-1 — The claimed deterministic aggregate state still depends on an undefined “required fact” short circuit

Fixture state becomes `UNOBSERVABLE` when a presence/mode/SHA fact “required to
classify” the path is unknown; otherwise known mismatches fall through to
`KNOWN_MISMATCH` (`v9:110-125`). Work state uses the same undefined test for
directory and child facts before falling through to `KNOWN_RETAINED`
(`v9:169-179`).

The phrase does not define a validator. For example, a present fixture symlink
already proves a mismatch, but its permitted `mode=UNKNOWN` can either be treated
as irrelevant to that conclusion or as an unobservable required row fact. A real
work directory with mode `OTHER` already proves non-recoverability, while
`owner_state=UNOBSERVABLE` can likewise yield either `KNOWN_RETAINED` or
`UNOBSERVABLE_RETAINED` depending on short-circuit interpretation. The schema
needs an exact per-row priority/normalization rule and an exact aggregate
function; declaring the result deterministic does not make the two readings
equivalent.

#### P2-2 — The new evidence-assembly temporary workspace is outside the exact temp cleanup mapping

V9 newly requires the evidence body to be assembled and strict-validated “in one
known OS temporary directory” before the final patch (`v9:53-57`). Its explicit
local cleanup mapping covers an individual verification download or that
download's known temporary directory (`v9:216-219`). It does not define the
evidence workspace's exact file set, creation/no-overwrite rule, mode, cleanup
point, or the combined `LOCAL_TEMP_CLEANUP`/`local_temp_state` disposition if
that workspace cannot be removed.

The later assertion that retained local files contain only Appendix/manifest
bytes (`v9:229-232`) is also incompatible with a retained temporary evidence
body, which may contain the failure-object preimage and the rest of the redacted
evidence. `EVIDENCE_FINALIZATION` safely blocks capability, but it does not by
itself describe or authorize cleanup of this separately introduced local path.
The lifecycle must either avoid this additional file-backed workspace or include
it in the exact local mutation, cleanup, retention, and failure-state contract.

### P3 — Low

No P3 finding.

## V8 Finding Recheck And Unchanged Safeguards

| Prior v8 blocker | V9 result |
| --- | --- |
| P1-1 unobservable inventories | **Partly resolved.** Total loss and extra/hash/target/owner uncertainty are truthful; known-present unknown-type/length cases remain illegal. |
| P2-1 row matrices and deterministic derivation | **Not resolved.** The missing row states and undefined “required fact” priority prevent one independent validator. |
| P2-2 attempt boundary and pre-credential cleanup semantics | **Partly resolved.** The evidence skeleton and attempt start are ordered, but generated pre-submit form/record uncertainty is not cleaned or encoded. |
| P2-3 exact local/evidence/credential mappings | **Partly resolved.** New IDs cover the named cases, but the newly introduced evidence workspace is outside the local-temp lifecycle. |

The review found no regression in the unchanged controls:

- v8's bootstrap suppression, checked output buffer, runtime exception/shutdown
  boundary, fixed generic response, and `200` dependency remain unchanged;
- strict cURL-option installation and pre-`curl_exec` short circuit, direct
  no-proxy/no-redirect fixed URL, TLS/status/time bounds, and non-retained
  4,096-byte body ceiling remain unchanged;
- the secret-safe count/redacted-or-human-only Error Logs route, no cached
  Authorization inspection, one panel submission/no retry, canonical base64
  failure/manifest preimages, and File Manager-only verifier remain in force;
- the evidence skeleton precedes live checks and a retained `IN_PROGRESS`
  skeleton cannot authorize Implementation (`v9:32-58`); and
- no cron, SSH, Git, provider secret, staging release, deployment, live model, or
  production authority leaks through v9 (`v9:246-250`).

No secret value or machine-specific account, home, user, server, credential URI,
or identifier appears in v9. No dependency cycle exists between plan review,
skeleton creation, live evidence, capability review, and Implementation: the
sequence is ordered, but this FAIL stops it before skeleton creation.

## Required Blocking Revisions

Before another independent review, Architecture must issue a new exact,
hash-identified candidate that:

1. provides legal exact rows for known-present but type-unobservable fixture,
   work-directory, and work-child paths, and for present regular files whose
   byte length is unobservable; it must distinguish unknown from mismatch and
   N/A without discarding known presence;
2. replaces “facts required to classify” with one exhaustive per-type
   normalization and aggregate-state function, including precedence when one
   fact proves mismatch/retention while another fact is unobservable;
3. covers every pre-submit generated-secret state, including a value resident in
   panel fields with no saved record and ambiguous record creation; it must give
   exact field/tab/record cleanup actions, evidence enums/check IDs, and retained
   failure disposition without authorizing a second credential or submit; and
4. either removes the evidence-assembly file workspace or binds its exact local
   paths/files, no-overwrite creation, cleanup, retention, and
   `LOCAL_TEMP_CLEANUP`/`local_temp_state`/failure-class mapping consistently
   with the finalization recovery branch.

V9, v8, v7, v6, v5, v3, all prior plans/audits/evidence, package/release bytes,
Git state, DreamHost, and unrelated files must remain preserved. These findings
do not authorize Red Team to repair the candidate.

## Residual Risks And Mandatory Future Gates

After plan correction, the disposable live preflight must still prove staging
TLS, exact root/hidden inventory, panel Basic Auth before all content/error/method
responses, File Manager byte/mode/owner fidelity, canonical manifest and failure
preimages, PHP/bootstrap/runtime behavior, direct bounded credential-free OpenAI
TLS, bounded access/Error Logs, exact work/fixture/panel/client/local cleanup, and
the final empty state. Ambiguity remains capability FAIL.

Even a later preflight PASS grants no Implementation by itself. The complete
capability evidence must receive a separate fresh independent PASS before the
unchanged v3 Section 9 local-only write set can be sent to Implementation
(`v3:699-749`; `v9:246-250`). A later byte-bound deployment amendment and review
remain mandatory for SSH/keys/host keys, final staging authentication, immutable
releases, atomic activation, source-independent rollback, cron, Git, provider
secret, staging canary, and production.

## Validation And Preservation

Required documentation-only validation after writing this audit:

- `python scripts\verify_release.py`: PASS, exit `0`;
  `release_verification status=passed manifest_files=47 cache_paths=0`.
- `git diff --check`: PASS, exit `0`, no output.

Repository state at review completion: branch `main`, HEAD
`97b470f8342cfba619da8f13bd224b2c6c4e2e2a`, upstream `origin/main`,
ahead/behind `0/0`, no staged path, and no tracked diff. The pre-existing plans,
audits, evidence, beginner guide, and `yakherd.mp4` remain untracked; this new
authorized audit is the only additional untracked path. Package `MANIFEST.json`
remains SHA-256
`ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`,
and package `RELEASE.json` remains SHA-256
`312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`.
The final audit SHA-256 is reported with the repository handoff so the record
does not attempt to contain its own digest.

No package/release byte, existing plan/audit/evidence byte, DreamHost state,
credential, Git state, or website implementation byte was changed. Appendix A
was hashed in memory and was not materialized. The unrelated `yakherd.mp4` was
not read, hashed, moved, modified, staged, or otherwise touched. The only write
was this authorized v9 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v9 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review, but may not create
the `IN_PROGRESS` capability skeleton or begin certificate/root checks under v9.
Implementation may not receive v9 as written; unchanged v3 Section 9 remains
parked. No DreamHost panel/File Manager/Logs inspection or mutation, human
credential checkpoint or creation, fixture materialization/upload, probe/network
request, cron, SSH, SFTP, release/deployment, Git action, provider secret,
staging release, live model request, or production action is authorized.

No previous plan PASS, hosting evidence, partial v9 closure, or unchanged v8
control overrides v9's own plan-review block (`v9:28-30`) or the separate fresh
independent live capability PASS required before Implementation (`v9:246-250`).

autonomous next action: Architecture must issue a new exact candidate resolving every v9 P1/P2 finding; Implementation, DreamHost, evidence-skeleton creation, Git, credentials, cron, staging, and production remain parked.
