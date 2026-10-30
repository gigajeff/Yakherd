# Yakherd.dev Concierge Composite Plan v11 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, v7, v8, v9, v10, and the v11 amendment
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
8. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v11.md`, 8,779
   bytes, 175 lines, SHA-256
   `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`.

The preserved v10 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v10.md`,
SHA-256
`10fe29cac12625b09e19c609ecde0e08fa9b3dda69f07732547e70c22fee9ec8`.
Every supplied identity matches the reviewed bytes. Root `AGENTS.md` remains
SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team prompt remains SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is finite. V11 adds owner state to every v10 fixture/work child,
replaces the pre/post-submit client lifecycle and both success/failure client
evidence, and changes the failure schema identity; every other v10 safeguard
remains (`v11:22-31`). No lower-precedence three-boolean client record,
version-2 failure shape, executable, cron, retry, deployment, Git, or
Implementation authority survives.

No DreamHost or network access was used for this document review.

## Unchanged Appendix A Reproduction

V11 changes no executable byte (`v11:22-27`). I independently extracted the
literal v8 PHP fence, joined its lines with LF, added one terminal LF, and encoded
it as UTF-8 without BOM. It reproduces exactly:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

The source identity passes. The verdict follows from the exact human/browser
observation boundary below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — `DESTROYED_BY_NAVIGATION` is a PASS assertion that the permitted observation cannot prove

V11 permits `panel_fields=DESTROYED_BY_NAVIGATION` for both pre-submit and
post-submit cleanup and accepts it for capability PASS (`v11:62-85`,
`v11:123-140`). The only evidence the human may provide is that the old form is
not present in the current view. Architecture may not inspect history, DOM,
network state, field values, or password-manager state (`v11:97-115`).

Current-view absence does not prove that navigation destroyed the controls or
their values. The page may remain in browser history, session restoration, or a
back-forward cache. V11 expressly acknowledges that back-forward caching may
exist and requires a later restart because navigation is not sufficient clearing
evidence (`v11:111-115`). Yet the canonical client object still records the
stronger literal `DESTROYED_BY_NAVIGATION`, and v11 declares that literal a
successful panel-field result (`v11:117-121`, `v11:129-135`).

The combined mandatory tab closure and browser restart can safely dispose of the
unobserved residual state, but they do not make the earlier causal assertion
true. A strict evidence enum must describe the observation actually made. As
written, a PASS requires the human to certify destruction while the plan permits
only current-view absence and explicitly forbids the observations that could
distinguish destruction from caching. This is an impossible positive evidence
claim, not a cosmetic label, because the token is embedded and independently
validated as a PASS value.

#### P1-2 — The human-only boundary returns control on a signed-in account overview before the panel tab closes

V11 correctly yields the browser for all password-form inspection and prohibits
Architecture screenshots, DOM, network, history, value, and password-manager
inspection (`v11:111-113`). However, the human is told to navigate to a
“non-secret DreamHost home overview” **before returning control**, after which
the still-open panel tab is closed (`v11:105-113`).

“Non-secret” is not equivalent to account-neutral or machine-identifier-free. A
signed-in hosting overview can render account identity, domains, site users,
server names, unrelated sites, notifications, or credential-bearing navigation.
V11 supplies no count-only/redacted mode, fixed identifier-free page, no-read
close operation, or prohibition on Architecture/browser-tool capture after
control returns. The inherited File Manager and evidence rules specifically
exclude credential-bearing URIs, dedicated username/home/server values, and
unrelated account facts (`v6:198-233`); the handback reopens that exposure at the
last client-cleanup step.

The tab must be closed, or moved to a demonstrably account-neutral browser-local
state, while the human-only/no-capture boundary is still active. Returning
control on an unverified signed-in account page makes tool-transcript privacy
depend on UI content that the candidate neither binds nor safely observes.

### P2 — Medium

No P2 finding.

### P3 — Low

No P3 finding.

## V10 Finding Recheck And Unchanged Safeguards

| Prior v10 blocker | V11 result |
| --- | --- |
| P1-1 owner gaps | **Resolved.** Every fixture/work-child row has exact owner normalization; unknown wins aggregate precedence, positive states require match, and mismatch forbids recovery deletion (`v11:33-60`). |
| P1-2 post-submit cleanup | **Structurally resolved.** Every named outcome reaches one post-submit sequence after the last panel operation, but the form-destruction proof and handback boundary above remain unsafe. |
| P2-1 success client schema | **Resolved.** PASS and FAIL use the same strict five-field object; PASS values and embedding are exact (`v11:123-144`). |
| P2-2 version ambiguity | **Resolved.** V11 requires version 3 plus `yakherd-capability-failure-v3` and rejects version 1/2 shapes (`v11:146-156`). |

The review found no other regression:

- type/mode/length/SHA/target/owner matrices now represent every named partial
  observation and apply conservative unknown-first aggregate precedence;
- owner match gates positive fixture/work verification and every permitted
  recovery deletion, while mismatch/unobservability remains protected;
- every generator and panel-submit outcome still has one credential, one
  possible submit, no retry, typed record/field/tab/restart failures, and
  mandatory password-manager/staging-tab/browser cleanup;
- the evidence skeleton precedes the first live check, in-memory finalization and
  its one recovery update remain bounded, and incomplete evidence cannot unpark
  Implementation;
- v8's bootstrap/runtime containment, strict cURL option short circuit, direct
  fixed no-proxy/no-redirect URL, TLS/status/time/body bounds, and secret-safe
  Error Logs route remain; and
- manifests, File Manager-only verification, local-download cleanup, no-cron,
  and all deployment/secret/Git/production gates remain unchanged.

No secret value or machine-specific identifier appears in v11's document bytes.
No new remote path, network target, write/delete action, alternate verifier,
dependency cycle, or authority leak was introduced. The finding concerns the
unbounded content visible when the future live browser is handed back.

## Required Blocking Revisions

Before another independent review, Architecture must issue a new exact,
hash-identified candidate that:

1. replaces the unprovable `DESTROYED_BY_NAVIGATION` claim with an exact enum and
   semantics limited to what the human can observe (current-view/form absence),
   and makes clear that only the combined panel-tab closure and completed browser
   restart dispose of unobserved history/back-forward state; and
2. keeps the human-only/no-screenshot/DOM/network boundary active through panel-
   tab closure, returning only `CLOSED`/`FAILED`, or otherwise binds a fixed
   browser-local, account-neutral handback plus a no-read close operation that
   cannot expose DreamHost account or machine identifiers.

V11, v10, v9, v8, v7, v6, v5, v3, all prior plans/audits/evidence,
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

No package/release byte, existing plan/audit/evidence byte, DreamHost state,
credential, Git state, or website implementation byte was changed. Appendix A
was hashed in memory and was not materialized. The unrelated `yakherd.mp4` was
not read, hashed, moved, modified, staged, or otherwise touched. The only write
was this authorized v11 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v11 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review, but may not create
the `IN_PROGRESS` capability skeleton or begin certificate/root checks under
v11. Implementation may not receive v11 as written; unchanged v3 Section 9
remains parked. No DreamHost panel/File Manager/Logs inspection or mutation,
human credential checkpoint or creation, fixture materialization/upload,
probe/network request, cron, SSH, SFTP, release/deployment, Git action, provider
secret, staging release, live model request, or production action is authorized.

No previous plan PASS, hosting evidence, partial v11 closure, or unchanged lower-
layer control overrides v11's own plan-review block (`v11:29-31`) or the separate
fresh independent live capability PASS required before Implementation
(`v11:170-175`).

autonomous next action: Architecture must issue a new exact candidate resolving every v11 P1 finding; Implementation, DreamHost, evidence-skeleton creation, Git, credentials, cron, staging, and production remain parked.
