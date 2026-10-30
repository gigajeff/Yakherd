# Yakherd.dev Concierge Composite Plan v13 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, v7, v8, v9, v10, v11,
  v12, and the v13 amendment
- Verdict: **PASS**

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
7. incorporated v10, SHA-256
   `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
8. incorporated v11, SHA-256
   `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
9. incorporated v12, SHA-256
   `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`;
10. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v13.md`, exactly
    11,500 bytes and 228 lines, SHA-256
    `d9f2f008f0155e1e16b908c1939817363a2f94ec8aac587e34374f193158625f`.

The preserved v12 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v12.md`,
SHA-256
`374172237157a0964227c002e1c9dbb39cecbb7ed9d959462391ca32f25f1bd4`.
Every supplied identity matches the reviewed bytes. Root `AGENTS.md` remains
SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team prompt remains SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is finite. V13 replaces v12 Sections 3 and 4 only for browser
handback, the client object, cleanup final-state derivation, and client/failure
schema identities (`v13:24-28`). V12's truthful current-view panel-field rule
survives. Every lower owner, inventory, runtime, cURL, Error Logs, manifest,
File Manager, evidence, single-submit/no-retry, no-cron, and authority control
survives. No stale client/failure schema or older cleanup rule can validate.

No DreamHost, browser, or network action was used for this document review.

## Unchanged Appendix A Reproduction

V13 changes no executable byte (`v13:24-30`). I independently extracted the
literal PHP fence from v8, joined its lines with LF, added one terminal LF, and
encoded it as UTF-8 without BOM. It reproduces exactly:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

The executable identity is unchanged from the previously reviewed composite.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

No P1 finding.

V12's handback blocker is closed. `handback_check` has a total four-value enum,
and both adverse applicable values map to the new allowlisted
`HANDBACK_BLANK` check plus `CLIENT_STATE_INCOMPLETE` (`v13:39-59,70-83`). The
atomic operation obtains the selected tab, evaluates only equality against the
literal `about:blank`, normalizes every ordinary return to `true`, `false`, or
`null`, catches without binding or rethrowing an error, and explicitly writes
only that normalized scalar (`v13:138-170`). It never returns the compared URL,
tab metadata, a page value, or an error object. A normal selection/evaluation
rejection is therefore contained before the sole explicit output. There is no
retry or alternate verifier.

V12's cleanup-finalization blocker is also closed. Tab enums represent final
observed state, so a failed direct close followed by successful all-origin
closure has one result, `CLOSED` (`v13:61-68`). The first restoration receives
one close sweep and one second restart; a second restoration or failed restart
receives one terminal close-only sweep, optionally one whole-browser close, and
no third restart (`v13:101-129`). The tab enums are then recomputed from final
absence, while `browser_restart=FAILED` remains truthful. No panel mutation,
credential generation, enable submission, disable retry, fixture retry, or
probe retry is hidden in those cleanup actions.

### P2 — Medium

No P2 finding.

V12's canonical-order ambiguity is closed. V13 lists the seven keys in exact
ascending raw-ASCII order and rejects every alternate byte order before hashing
or base64 acceptance (`v13:174-191`). It assigns the client schema ID
`yakherd-capability-client-v3`, failure schema version `5`, and failure schema ID
`yakherd-capability-failure-v5`; client versions 1-2, failure versions 1-4,
missing `handback_check`, stale IDs, and old panel enums are rejected
(`v13:193-198`).

### P3 — Low

No P3 finding.

## Adverse-Path Pressure Test

| Path | Deterministic final evidence |
| --- | --- |
| Nominal cleanup | All applicable client fields take the exact PASS values, including `handback_check=MATCH`; there is one shared seven-member client object (`v13:39-59,200-212`). |
| Selected page is not blank | The verifier returns only `false`; `handback_check=MISMATCH`, `HANDBACK_BLANK`, and `CLIENT_STATE_INCOMPLETE` block PASS. The human then performs the one listed whole-browser close without reporting the page value (`v13:131-136,162-170`). |
| Selection/evaluation is unavailable or non-boolean | The contained operation returns `null`; `handback_check=UNOBSERVABLE` has the same blocking check/class mapping and no retry (`v13:155-170`). |
| Direct panel close fails, later sweep succeeds | Direct-close history is provisional. Confirmed final absence yields only `panel_tab=CLOSED` (`v13:61-68,97-104`). |
| First restart restores a protected origin | One restoration sweep and exactly one second restart are authorized (`v13:105-109`). |
| Second restart restores a protected origin, or a restart fails | `browser_restart=FAILED`; one terminal close-only sweep follows. Final protected-tab absence is re-evaluated, with one whole-browser-close fallback and no third restart (`v13:109-129`). |
| Browser is closed or a protected-tab enum remains failed | The browser is not reopened for handback; the check is `UNOBSERVABLE`, and the applicable client failures prevent PASS (`v13:118-123,168-172`). |
| `false`/`null` after a provisional clean tab state | One final human-only whole-browser close establishes final tab absence or leaves the applicable tab enums `FAILED`; the already obtained handback result is preserved, so there is one truthful object and no second check (`v13:131-136`). |
| Failure before credential-generator invocation | All six client state fields are `NOT_APPLICABLE`; no handback fact is fabricated (`v13:53-59`; inherited `v9:34-51,208-227`). |
| Failure after generator invocation but before submit | Record, panel-field, panel-tab, restart, and handback cleanup are applicable; staging remains N/A until opened. No second credential or submit is allowed (`v13:53-59,125-129`; inherited `v10:153-182`). |
| Any post-submit success, timeout, error, partial state, or later probe failure | All six client facts are applicable and the same bounded post-operation cleanup/state machine runs; remote failure does not suppress client cleanup (`v13:53-59,85-136`; inherited `v11:87-121`). |
| Evidence finalization fails | The inherited `IN_PROGRESS` skeleton is capability FAIL; only the single recovery update is allowed, and neither a thread report nor incomplete evidence authorizes Implementation (`v9:34-58`; `v13:193-212`). |

`FORM_ABSENT_CURRENT_VIEW` remains a claim only about the visible form and can
satisfy PASS only with a closed panel tab and completed restart (`v12:34-54`;
`v13:200-207`). Password-record, field, tab, restart, and handback failures each
retain an exact finite check mapping. Applicable N/A, missing/unknown fields, and
stale shapes are rejected (`v13:53-83,193-212`).

## Inherited-Control Recheck

No regression was found in the incorporated controls:

- every fixture/work row has total presence/type/mode/length/hash/target/owner
  normalization; unknown or unobservable required facts win aggregate
  precedence even over known mismatch, and owner mismatch forbids recovery
  deletion (`v10:32-141`; `v11:33-60`);
- the attempt begins only after a validated `IN_PROGRESS` evidence skeleton and
  at the first read-only certificate check; evidence finalization, one recovery
  update, and incomplete-evidence blocking remain bounded (`v9:34-58`);
- v8's PHP bootstrap/output buffering, warning/throwable containment, generic
  response, display/log suppression, strict cURL-option short circuit, fixed
  direct no-proxy/no-redirect request, TLS/status/time/body bounds, and
  credential-free provider request remain byte-identical;
- the secret-safe Error Logs route, count-only/redacted-or-human-only channel,
  finite time/path observation, non-copy rule, and zero-row PASS requirement
  remain;
- exact manifest preimages, File Manager-only inventory/hash/mode/owner proof,
  individually bounded local downloads and cleanup, strict canonical
  JSON/base64/SHA evidence, single credential/submit/disable attempt, and exact
  remote recovery/delete gates remain; and
- cron, SSH, Git, final staging authentication/release, provider secret, live
  model, deployment, and production authority remain withheld (`v13:225-228`).

No secret value, account identifier, hostname detail, username, machine-specific
identifier, credential-derived value, new remote path, alternate network target,
new write/delete surface, dependency cycle, or authority leak appears in v13.

## Required Fixes

None for plan PASS.

This PASS does not waive any live observation or evidence requirement. A failure
to obtain exactly the expected scalar from the handback operation—including an
execution-layer interruption outside the JavaScript catch—cannot establish
`MATCH`; it must remain `UNOBSERVABLE`/capability FAIL, must not be retried, and
must not be copied into evidence as diagnostic text.

## Residual Risks And Mandatory Future Gates

The disposable live preflight must still prove staging TLS, exact root/hidden
inventory, panel Basic Auth before all content/error/method responses, File
Manager byte/mode/owner fidelity, canonical manifest/failure/client preimages,
PHP bootstrap/runtime behavior, direct bounded credential-free OpenAI TLS,
bounded access/Error Logs, exact work/fixture/panel/client/local cleanup, and the
final empty state. Any unavailable or ambiguous fact is capability FAIL.

Browser transport/session failure remains an operational risk. V13 makes it
fail closed because only the literal `true` result produces `MATCH`; it does not
authorize reconnection, rediscovery, another read, or retry. Human cleanup and
the evidence disposition remain mandatory after `false`, `null`, or lack of an
acceptable scalar.

Even a successful preflight does not authorize Implementation. The complete
capability record must receive a separate fresh independent live-evidence PASS
before unchanged v3 Section 9 may be sent to the existing IMPLEMENTATION task.
A later byte-bound plan and independent review remain mandatory for SSH/keys/
host keys, final staging authentication, immutable releases, atomic activation,
source-independent rollback, cron, Git, provider secret, staging canary, and
production.

## Validation And Preservation

Required documentation-only validation after writing this audit:

- `python scripts\verify_release.py`: PASS, exit `0`;
  `release_verification status=passed manifest_files=47 cache_paths=0`.
- `git diff --check`: PASS, exit `0`, no output.

Repository state before the authorized write: branch `main`, HEAD
`97b470f8342cfba619da8f13bd224b2c6c4e2e2a`, upstream `origin/main`,
ahead/behind `0/0`, no staged path, and no tracked diff. The pre-existing plans,
audits, evidence, beginner guide, and `yakherd.mp4` were untracked. Package
`MANIFEST.json` was SHA-256
`ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`,
and package `RELEASE.json` was SHA-256
`312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`.
The final audit SHA-256 is reported with the repository handoff so the record
does not attempt to contain its own digest.

No package/release byte, prior plan/audit/evidence byte, DreamHost/browser/
network state, credential, Git state, or website implementation byte was
changed. Appendix A was hashed in memory and was not materialized. The unrelated
`yakherd.mp4` was not read, hashed, moved, modified, staged, or otherwise
touched. The only write was this authorized v13 review record.

## Verdict And Exact Authority Effect

**Verdict: PASS** for the exact v13 composite identified above.

This PASS grants only the narrow disposable capability-preflight authority
defined by the composite. Architecture may create and validate the sole
`IN_PROGRESS` evidence skeleton at
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`, then begin
the one disposable attempt with the read-only staging-certificate and root
checks. It may perform only the exact bounded panel/File Manager fixture,
credential, probe, log-observation, cleanup, and evidence actions in the passed
composite, subject to every human checkpoint and stop/failure branch. This PASS
does not itself assert that DreamHost has any capability.

Implementation may **not** receive v13 yet. The resulting complete live
capability evidence must receive a separate fresh independent Red Team PASS
before unchanged v3 Section 9 local-only Implementation may be unparked. No
deployment, cron, SSH/SFTP, Git mutation, final staging authentication or
release, provider-secret installation, live-model request, canary, production,
or publication authority is granted.

autonomous next action: Architecture may create and validate the sole IN_PROGRESS capability skeleton, then run exactly one disposable v13 preflight beginning with the read-only certificate/root checks; Implementation and every deployment, Git, SSH, cron, provider-secret, staging-release, live-model, and production action remain parked pending the separately reviewed live evidence.
