# Yakherd.dev Concierge Composite Plan v12 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, v7, v8, v9, v10, v11, and the v12 amendment
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
7. incorporated v10, SHA-256
   `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
8. incorporated v11, SHA-256
   `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
9. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v12.md`, 6,616
   bytes, 131 lines, SHA-256
   `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`.

The preserved v11 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v11.md`,
SHA-256
`2e9ec79771fd01eb9419c3dba5ac3aba20ded7017900ac95d7e25fd0368fc18d`.
Every supplied identity matches the reviewed bytes. Root `AGENTS.md` remains
SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team prompt remains SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is finite. V12 replaces only v11's form-destruction enum/claim and
human-only handback, then changes the client/failure schema identities; every
other owner, inventory, runtime, cURL, Error Logs, manifest, File Manager,
evidence, no-retry, no-cron, and authority rule remains (`v12:23-32`). No stale
destruction enum, signed-in nominal handback, older schema, executable, retry,
deployment, Git, or Implementation authority survives.

No DreamHost, browser, or network access was used for this document review.

## Unchanged Appendix A Reproduction

V12 changes no executable byte (`v12:23-28`). I independently extracted the
literal v8 PHP fence, joined its lines with LF, added one terminal LF, and encoded
it as UTF-8 without BOM. It reproduces exactly:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

The source identity passes. The verdict follows from the new handback failure and
canonical-client branches below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — A non-blank handback has neither a secret-safe observation nor a legal failure representation

V12 correctly defines `FORM_ABSENT_CURRENT_VIEW` as only the current-view fact
the human can observe and couples its PASS use to panel-tab closure and completed
restart (`v12:34-54`). It also keeps Architecture out of browser state until the
human reports an `about:blank` handback (`v12:56-78`).

The verification failure branch is not closed. Architecture's first browser
operation reads the current URL and, if it is not literal `about:blank`, v12 says
“the client cleanup is `FAILED`” (`v12:80-82`). But `client_cleanup` is a strict
six-field object, not an enum. None of its fields represents handback URL state
(`v12:89-111`; `v11:62-71`), and the finite allowed check table has no handback-
URL check. V10 added only `PANEL_FIELDS_CLEAR` and `PANEL_TAB_CLOSE`; the other
client mappings remain password record, staging tabs, and browser restart
(`v10:171-180`; `v8:80-115`). V12 neither adds a check nor says which existing
field becomes `FAILED`.

Therefore an otherwise complete cleanup followed by an unexpected URL cannot
produce the required nonempty, allowlisted `failed_checks` plus one truthful
canonical client object without inventing a mapping. Marking
`browser_restart=FAILED` would contradict an observed successful restart;
marking a tab field failed would contradict the human's completed closure.

The read itself also breaks the privacy guarantee on precisely this failure
path. A wrong handback may be a credential-bearing File Manager URI, signed-in
panel path, account-specific URL, or restored staging URL. “URL-only” still
places that unexpected URL in the browser-tool result unless the candidate binds
an equality-only boolean operation that never returns the actual value. V12
simultaneously forbids any such identifier/history entry from entering a tool
transcript (`v12:74-82`). The current rule can detect the violation only by
exposing the value it promises not to expose.

#### P1-2 — The one-retry restoration and repeated-close failure branches do not reach one deterministic safe final client state

The nominal sequence closes all protected-origin tabs, restarts the browser, and
permits exactly one restoration retry (`v12:63-72`). Two adverse branches remain
incomplete:

1. If the direct panel-tab close in step 2 fails, step 4 orders another close of
   every remaining DreamHost-origin tab. V12 does not state whether a successful
   second close changes `panel_tab` from `FAILED` to `CLOSED`, or whether the
   original failed operation permanently controls the enum. The same final state
   can therefore serialize two different client objects, one PASS-capable and
   one blocking.
2. If the second restart restores a DreamHost/staging tab, v12 sets
   `browser_restart=FAILED` but authorizes no final closure of the newly restored
   tab (`v12:68-70`). Step 6 nevertheless requires the human to confirm that no
   such origin is open before handback. Satisfying it needs an unlisted extra
   close; omitting that close leaves a signed-in/protected-origin tab open and
   makes the required confirmation false. `staging_tabs`/`panel_tab` final enums
   are also undefined after this second restoration.

These are cleanup actions, not panel-submit retries, but the plan still needs one
finite final-state rule. A failed attempt must either reach a safe neutral
handback with truthful final tab enums or remain wholly human-controlled with an
exact evidence/finalization disposition. It cannot rely on an unlisted third
cleanup action while claiming the listed sequence is exact.

### P2 — Medium

#### P2-1 — “Leading” client `schema_version` conflicts with inherited raw-ASCII canonical key order

V12 says the canonical five-field object gains one **leading** field,
`schema_version`, while retaining strict ASCII canonical JSON (`v12:89-97`,
`v12:113-116`). The inherited serializer emits every object key in ascending raw
ASCII byte order (`v6:89-104`). For the six client keys, that order begins with
`browser_restart`; `schema_version` sorts after the `panel_*` and
`password_record` keys and before `staging_tabs`.

If “leading” is a serialized-order requirement, it contradicts canonical ASCII
sorting. If it merely means the schema field is conceptually added, the word has
no ordering effect, but the candidate does not say so. The exact bytes, hash, and
base64 preimage can therefore be produced two ways by reasonable independent
implementers. V12 must bind the literal key order or explicitly state that raw-
ASCII sorting controls and “leading” is non-serial descriptive wording.

### P3 — Low

No P3 finding.

## V11 Finding Recheck And Unchanged Safeguards

| Prior v11 blocker | V12 result |
| --- | --- |
| P1-1 unprovable destruction | **Resolved on the nominal path.** `FORM_ABSENT_CURRENT_VIEW` claims only current absence and is accepted only with closed panel tab plus completed restart (`v12:34-54`). |
| P1-2 signed-in handback | **Resolved on the nominal path.** Human-only/no-capture control continues through direct panel/DreamHost/staging closure, restart, and `about:blank` handback (`v12:56-78`). The mismatch/retry branches above remain incomplete. |

The review found no other regression:

- every fixture/work child retains exact owner match/mismatch/unobservable/N/A,
  owner participates in unknown-first aggregate precedence, and positive/recovery
  paths require owner match;
- the shared successful/failed client object, post-submit outcome coverage,
  current-view field semantics, password-manager cleanup, one credential/one
  possible submit/no retry, and failure class mappings otherwise remain;
- the evidence skeleton precedes live work, in-memory finalization and its one
  recovery update remain bounded, and incomplete evidence cannot authorize;
- v8's bootstrap/runtime containment, strict cURL option short circuit, direct
  fixed no-proxy/no-redirect URL, TLS/status/time/body bounds, and secret-safe
  Error Logs route remain; and
- manifests, File Manager-only verification, local-download cleanup, no-cron,
  and every deployment/secret/Git/production gate remain unchanged.

No secret value or machine-specific identifier appears in v12's document bytes.
No new remote path, external network target, write/delete action, alternate
verifier, dependency cycle, or next-stage authority leak was introduced. The P1
privacy finding concerns an unexpected future live handback URL.

## Required Blocking Revisions

Before another independent review, Architecture must issue a new exact,
hash-identified candidate that:

1. gives the handback comparison one exact client field/result, allowlisted
   failed-check mapping, failure class disposition, and updated schema identities,
   and performs the comparison through a bound equality-only boolean route that
   cannot return/log an unexpected URL or identifier;
2. defines final enum precedence when direct panel-tab close fails but the later
   all-origin close succeeds, and defines a safe final-close/neutral-handback or
   no-handback evidence branch after second restoration/restart failure without
   an unlisted retry; and
3. removes the client key-order ambiguity by explicitly binding the six canonical
   keys to inherited raw-ASCII order (or replacing that rule with one exact
   alternative) before any length/hash/base64 evidence is generated.

V12, v11, v10, v9, v8, v7, v6, v5, v3, all prior plans/audits/evidence,
package/release bytes, Git state, DreamHost, and unrelated files must remain
preserved. These findings do not authorize Red Team to repair the candidate.

## Residual Risks And Mandatory Future Gates

After plan correction, the disposable live preflight must still prove staging
TLS, exact root/hidden inventory, panel Basic Auth before all content/error/method
responses, File Manager byte/mode/owner fidelity, canonical manifest/failure/
client preimages, PHP/bootstrap/runtime behavior, direct bounded credential-free
OpenAI TLS, bounded access/Error Logs, exact work/fixture/panel/client/local
cleanup, and the final empty state. Any ambiguity remains capability FAIL.

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

No package/release byte, existing plan/audit/evidence byte, DreamHost/browser/
network state, credential, Git state, or website implementation byte was changed.
Appendix A was hashed in memory and was not materialized. The unrelated
`yakherd.mp4` was not read, hashed, moved, modified, staged, or otherwise touched.
The only write was this authorized v12 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v12 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review, but may not create
the `IN_PROGRESS` capability skeleton or begin certificate/root checks under
v12. Implementation may not receive v12 as written; unchanged v3 Section 9
remains parked. No DreamHost/browser/File Manager/Logs inspection or mutation,
human credential checkpoint or creation, fixture materialization/upload,
probe/network request, cron, SSH, SFTP, release/deployment, Git action, provider
secret, staging release, live model request, or production action is authorized.

No previous plan PASS, hosting evidence, partial v12 closure, or unchanged lower-
layer control overrides v12's own plan-review block (`v12:30-32`) or the separate
fresh independent live capability PASS required before Implementation
(`v12:126-131`).

autonomous next action: Architecture must issue a new exact candidate resolving every v12 P1/P2 finding; Implementation, DreamHost, browser, evidence-skeleton creation, Git, credentials, cron, staging, and production remain parked.
