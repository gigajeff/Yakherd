# Yakherd.dev Concierge Composite Plan v10 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, v7, v8, v9, and the v10 amendment
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
6. incorporated v9, SHA-256
   `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
7. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v10.md`, 10,773
   bytes, 216 lines, SHA-256
   `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`.

The preserved v9 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v9.md`,
SHA-256
`89da8a1a9f446bf85c762d9ea513d6efd07d3ed1e914b984d18850eda9d4a3fa`.
Every supplied identity matches the reviewed bytes. Root `AGENTS.md` remains
SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team prompt remains SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is finite. V10 replaces v9 Sections 3.1–3.3 and the file-backed
evidence-assembly lifecycle, adds two client check IDs, and leaves every other
v9/v8 rule in force (`v10:21-30`). No lower-precedence executable, cron,
cached-Authorization inspection, retry, deployment, Git, or Implementation
authority reappears.

No DreamHost or network access was used for this document review.

## Unchanged Appendix A Reproduction

V10 changes no executable byte (`v10:21-25`). I independently extracted the
literal v8 PHP fence, joined its lines with LF, added one terminal LF, and encoded
it as UTF-8 without BOM. It reproduces exactly:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

The source identity passes. The verdict follows from the cross-layer inventory
and credential evidence contracts below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — Owner observability is required by the verifier but absent from fixture and work-child rows

V10 states that every inventory fact, including owner, has an independently
unobservable representation and that any unknown/unobservable field always wins
aggregate precedence (`v10:32-58`). The actual replacement schemas do not meet
that claim:

- each fixture row has presence, type, mode, length, and SHA fields, but no
  `owner_state` (`v10:60-71`); and
- each work child has presence, type, mode, length, SHA, and target fields, but no
  `owner_state` (`v10:99-130`). Only the work directory retains v9's owner field
  (`v10:101-105`; `v9:134-144`).

Owner is not optional inherited metadata. The sole File Manager verifier must
record owner-class and must stop rather than guess when any details field is
unavailable (`v6:198-233`). Bounded recovery may delete `first.bin` and
`second.bin` only after proving each regular file is dedicated-user owned, and
any owner mismatch or unobservability requires no touch and capability FAIL
(`v6:150-171`). Fixture upload verification likewise records type/owner/mode/
length facts (`v6:214-233`).

Two mandatory failure states therefore remain unserializable:

1. a fixture source is visibly regular with correct mode/length/hash while its
   owner field is unavailable; and
2. a retained `first.bin` has correct type/mode/length/hash but owner is
   mismatched or unobservable.

In the first case the aggregate cannot derive `UNOBSERVABLE` because the strict
row has no unknown owner trigger. In the second, the listed child fields satisfy
the recovery invariants even though the inherited recovery rule forbids delete.
An owner boolean in free-form evidence cannot repair the canonical object's exact
row or its deterministic aggregate derivation. V10 closes type/length
observability but still cannot truthfully compare every required inventory fact
to the mutation/recovery ledger.

#### P1-2 — Post-submit panel secret cleanup is applicable but has no exact action or normalization

V10 correctly makes the password record, panel fields, panel tab, and browser
restart applicable immediately when generation begins and supplies a complete
pre-submit failure cleanup (`v10:143-180`). It then declares all five client
fields applicable after panel-enable submission (`v10:157-161`), but the only
new field-clearing, panel-navigation, and panel-tab-closing procedure is expressly
limited to a **pre-submit** generation/masking failure (`v10:163-169`).

The inherited post-submit lifecycle covers success, timeout, panel error, clean
enable failure, recovered partial state, and unresolved partial state. Its normal
and failure cleanup deletes the password-manager record, closes staging-origin
tabs, and restarts the browser; it does not clear the panel password controls,
navigate the non-staging panel tab away, or close that tab (`v6:254-273`;
`v7:105-129`). V10 does not replace those post-submit steps.

Consequently, after a successful or ambiguous submit, the panel response may
leave the masked values in the form/history state, remove the controls, or retain
the tab for later disable/inventory work. V10 gives no exact time at which to
clear and close it, no safe sequencing around the required later panel cleanup,
and no normalization for controls that disappear after submission: `CLEARED`
would assert an unproved action, while `UNOBSERVABLE` permanently fails the
attempt. Browser restart may eventually destroy browser state, but it does not
truthfully prove the separately mandatory `panel_fields=CLEARED` result.

This leaves a possible generated-secret residue outside an executable cleanup
branch and can make a normal success impossible to encode. Applicability and
check IDs alone do not supply the missing post-submit action/state transition.

### P2 — Medium

#### P2-1 — The successful evidence contract still has only three booleans, not the new five-field client object

V10 replaces v9's `client_cleanup`, which is a required member of the canonical
**failure** object (`v9:60-78`; `v10:143-151`). It does not replace the successful
evidence schema inherited from v7/v8. That schema records exactly the password-
record, staging-tab, and browser-restart booleans (`v7:110-121`, `v7:173-180`;
`v8:206-213`). It has no defined location, key order, or type for
`panel_fields` or `panel_tab`.

V10's statement that successful clearing/closing records “only the enum”
(`v10:180-182`) does not identify whether those enums replace the three success
booleans, appear in a five-field success object, or are free-form fields. Thus a
successful live record cannot be strict-validated against one exact schema, and
the independent capability reviewer cannot distinguish omitted panel cleanup
from complete panel cleanup.

#### P2-2 — Incompatible failure shapes still share `schema_version=2`

V9 fixes the top-level failure object at `schema_version=2` (`v9:60-78`). V10
retains that top level while changing every fixture row, every work-child row,
the legal work-directory matrix, and the entire client-cleanup object
(`v10:21-23`, `v10:60-180`). A v9 failure object and a structurally incompatible
v10 failure object therefore claim the same schema version.

The plan hashes make a human review distinguishable, but the canonical object's
own version no longer identifies its required shape. That weakens deterministic
parsing and preserved-evidence provenance precisely where unknown/missing keys
are otherwise rejected. The amended failure schema needs a new exact version (or
an equally exact composite-schema discriminator) and corresponding canonical
validation rule.

### P3 — Low

No P3 finding.

## V9 Blocker Recheck And Unchanged Safeguards

| Prior v9 blocker | V10 result |
| --- | --- |
| P1-1 known-present unknown type/length | **Resolved for type and length.** `PRESENT+UNKNOWN` and `byte_length_state=UNOBSERVABLE` are legal. Required owner observations remain absent from fixture/work-child rows. |
| P1-2 pre-submit credential residue | **Resolved for pre-submit failure.** Generator invocation activates record/field/tab/restart cleanup with no retry. Post-submit cleanup remains incomplete. |
| P2-1 aggregate precedence | **Resolved for represented fields.** Unknown/unobservable always wins after matrix validation. Missing owner fields prevent that rule from being total. |
| P2-2 evidence workspace | **Resolved.** Evidence is assembled in process memory; only the previously bounded verification-download directory remains. |

The review found no regression in the unchanged controls:

- fixture and work type/mode/length/SHA/target matrices distinguish mismatch,
  N/A, and unobservability for every field they contain;
- the evidence skeleton still precedes the first live check, and failed
  in-memory finalization retains an unconditional blocking skeleton with one
  bounded recovery update (`v9:32-58`; `v10:184-198`);
- v8's suppressed bootstrap, checked output buffer, generic runtime boundary,
  strict cURL option short circuit, direct fixed no-proxy/no-redirect URL,
  TLS/status/time/body bounds, and secret-safe Error Logs route remain;
- manifest preimages, File Manager-only verification, one credential/one possible
  submit/no retry, local-download cleanup, and no-cron rules remain; and
- no DreamHost deployment, cron, SSH, Git, staging release, provider secret,
  live model request, production, or Implementation authority leaks through v10
  (`v10:200-216`).

No secret value or machine-specific account, home, user, server, credential URI,
or identifier appears in v10. No new unlisted remote path, network target,
delete operation, dependency cycle, or alternate verifier was introduced.

## Required Blocking Revisions

Before another independent review, Architecture must issue a new exact,
hash-identified candidate that:

1. adds owner state to every fixture and work-child row whose owner is observed
   or required for positive verification/recovery, with exact
   `MATCH`/`MISMATCH`/`UNOBSERVABLE`/`NOT_APPLICABLE` per-type normalization and
   Section 2 aggregate precedence;
2. defines the post-submit field/tab cleanup for every success, timeout, panel
   error, clean failure, recovered partial, and retained partial outcome,
   sequenced after the last required panel operation and before final browser
   disposal, including exact treatment when submitted controls disappear;
3. replaces the inherited successful three-boolean evidence contract with one
   exact placement/schema for all applicable client-cleanup results, including
   `panel_fields` and `panel_tab`, and strict-validates it before capability PASS;
   and
4. assigns the structurally changed canonical failure object a unique exact
   schema version/discriminator and updates its validation/embedding contract.

V10, v9, v8, v7, v6, v5, v3, all prior plans/audits/evidence, package/release
bytes, Git state, DreamHost, and unrelated files must remain preserved. These
findings do not authorize Red Team to repair the candidate.

## Residual Risks And Mandatory Future Gates

After plan correction, the disposable live preflight must still prove staging
TLS, exact root/hidden inventory, panel Basic Auth before all content/error/method
responses, File Manager byte/mode/owner fidelity, canonical manifest/failure
preimages, PHP/bootstrap/runtime behavior, direct bounded credential-free OpenAI
TLS, bounded access/Error Logs, exact work/fixture/panel/client/local cleanup, and
the final empty state. Any ambiguity remains capability FAIL.

Even a later preflight PASS grants no Implementation by itself. The complete
capability evidence must receive a separate fresh independent PASS before the
unchanged v3 Section 9 local-only write set can be sent to Implementation. A
later byte-bound deployment amendment and review remain mandatory for SSH/keys/
host keys, final staging authentication, immutable releases, atomic activation,
source-independent rollback, cron, Git, provider secret, staging canary, and
production.

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
was this authorized v10 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v10 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review, but may not create
the `IN_PROGRESS` capability skeleton or begin certificate/root checks under
v10. Implementation may not receive v10 as written; unchanged v3 Section 9
remains parked. No DreamHost panel/File Manager/Logs inspection or mutation,
human credential checkpoint or creation, fixture materialization/upload,
probe/network request, cron, SSH, SFTP, release/deployment, Git action, provider
secret, staging release, live model request, or production action is authorized.

No previous plan PASS, hosting evidence, partial v10 closure, or unchanged lower-
layer control overrides v10's own plan-review block (`v10:28-30`) or the separate
fresh independent live capability PASS required before Implementation
(`v10:211-216`).

autonomous next action: Architecture must issue a new exact candidate resolving every v10 P1/P2 finding; Implementation, DreamHost, evidence-skeleton creation, Git, credentials, cron, staging, and production remain parked.
