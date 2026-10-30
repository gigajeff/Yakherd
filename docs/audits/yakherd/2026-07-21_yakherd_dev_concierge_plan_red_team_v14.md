# Yakherd.dev Concierge Composite Plan v14 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5-v13 and the v14 amendment
- Verdict: **FAIL**

## Exact Candidate And Preservation Boundary

The reviewed amendment is
`docs/2026-07-21_yakherd_dev_concierge_website_plan_v14.md`, exactly 13,013
bytes and 285 lines, SHA-256
`cf7604e35d0a36b9c32d283e466d49ad9f6e4e9cfbc69fc63d36cb68c830637a`.

Its incorporated identities all match the reviewed bytes:

1. v3:
   `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
2. v5:
   `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
3. v6:
   `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
4. v7:
   `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
5. v8:
   `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
6. v9:
   `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
7. v10:
   `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
8. v11:
   `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
9. v12:
   `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`;
10. v13:
    `d9f2f008f0155e1e16b908c1939817363a2f94ec8aac587e34374f193158625f`.

The exhausted v13 live evidence remains 9,229 bytes and 129 lines, SHA-256
`01042dd7125ae8edccdc21fb8e4abb48c22f6228413bbc70a134fd28f3f5cecd`.
Its independent integrity-PASS/capability-FAIL review remains 11,827 bytes and
265 lines, SHA-256
`e0fc6bda5cad82f06c87feaf895eb6718482b9cc19694848d5bcc0ad0c7ffddb`.
V14 does not edit or retry either record (`v14:23-35`).

Root `AGENTS.md` remains SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`.
No DreamHost, browser, or network operation was performed for this review.

## Unchanged Appendix A Reproduction

I independently extracted the literal v8 PHP fence, joined its lines with LF,
added one terminal LF, and encoded it as UTF-8 without BOM. It reproduces:

- byte length: `7279`;
- SHA-256:
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

V14 changes no executable fixture byte (`v14:34-39`).

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — Certificate-tab close failures are swallowed while the only evidence fields are forced to N/A

Both frozen wrappers can create a browser tab and then fail to close it:

- the signed-in certificate-panel wrapper catches a close failure, changes only
  `panel_status` to `UNOBSERVABLE`, and returns that one scalar
  (`v14:131-194`);
- the public navigation wrapper catches and discards close failures, then returns
  only `MISMATCH` or `UNOBSERVABLE` (`v14:196-230`).

Neither scalar says whether the tab actually closed. The panel wrapper therefore
cannot distinguish `(status unobservable, tab closed)` from `(status
unobservable, signed-in panel tab retained)`. The navigation wrapper likewise
cannot distinguish a cleaned failed navigation from a retained staging,
certificate-error, login, or redirect tab. “Closed exactly once” at
`v14:192-194` is also not a truthful final-state assertion when the sole close
attempt throws; only “close attempted once” is established.

V14 then requires every v13 client state field to remain `NOT_APPLICABLE` on a
certificate stop because the credential generator was not invoked
(`v14:232-245`). That contradicts the new actions: v14 itself has created panel
and/or staging tabs whose cleanup is now applicable. The mandatory failure
object has no other tab-cleanup field. `certificate_preflight` describes only
certificate observations, while `panel_inventory` describes host-managed auth
files, not browser tabs. Consequently a retained signed-in tab can serialize
with:

- `panel_tab=NOT_APPLICABLE` and/or `staging_tabs=NOT_APPLICABLE`;
- no `PANEL_TAB_CLOSE` or `STAGING_TABS_CLOSE` failed check; and
- no `CLIENT_STATE_INCOMPLETE` class.

This conflicts with v13's rule that an applicable fact may never be represented
as N/A and that tab-close failures receive those exact checks/classes
(`v13:53-83`). It also defeats v13's final-state tab semantics
(`v13:61-68`). The privacy-safe scalar output is not enough: on these branches a
signed-in or unexpected-origin tab may remain open with neither safe terminal
cleanup nor truthful evidence.

#### P1-2 — The valid navigation tab is deliberately retained before root inspection, but its binding and pre-credential cleanup lifecycle are undefined

On `VALID`, the navigation wrapper returns immediately without closing the tab
(`v14:200-225`), and v14 says that tab remains open for the downstream sequence
(`v14:228-230`). However `certificateNavigationTabV14` is declared with `var`
inside the async IIFE. It is function-scoped and unavailable after the wrapper
returns. Only the enum assigned to `certificateNavigationStateV14` survives.
The exact code does not export a tab binding or define a subsequent
`selected()`/claim operation. Reacquiring it therefore needs an unlisted tab
selection/list operation or another tab/navigation.

The lifecycle also has an earlier failure hole even if the implementation can
somehow use the selected tab. `(ACTIVE, VALID)` continues first to root and File
Manager inspection, before the credential checkpoint (`v14:247-252`; inherited
`v5:90-95,199-218`). If either of those read-only gates fails, the deliberately
open staging tab already exists, but v13's unchanged pre-generator client rule
still makes all client fields N/A (`v13:53-59`; `v14:239-245`). V14 provides no
close action, no preserved binding, no final tab state, and no failed-check/class
mapping for such a downstream pre-generator stop.

Thus the exact same live state can be serialized as clean N/A client state while
a v14-created tab remains open. The plan must close this path before it can
authorize a new attempt.

### P2 — Medium

#### P2-1 — The visible-body bound and status/window contract do not match the frozen evaluator

V14 says the panel evaluation “reads at most 2,000,000 characters”
(`v14:84-99`). The code first evaluates `document.body.innerText` in full and
only then rejects when `body.length > 2000000` (`v14:142-147`). This is an
acceptance bound, not a read bound. An arbitrarily larger visible body has
already been materialized before the check.

The window prose is also not byte-exact on boundary and conflict cases. The code
uses a start clamped to zero and `slice(start, start + 600)`, which returns fewer
than 600 characters near the end; the prose requires a 600-character window
beginning 200 characters before the target (`v14:86-89,148-155`). More
importantly, the prose independently defines `PENDING` and `FAILED` by their
keywords, so a window containing one keyword from each satisfies both branches.
The code silently gives `PENDING` precedence (`v14:156-170`). `add` is an
unbounded substring rather than a token and can match unrelated words or an
adjacent domain row inside the broad window, causing a false `ABSENT` or blocking
an otherwise active row.

False `PENDING`/`FAILED`/`ABSENT` remains fail-closed, and a false `ACTIVE` alone
cannot pass because the public scalar is also mandatory. Nevertheless this is a
new one-attempt gate: inconsistent prose/code and context-crossing substring
rules make the canonical certificate evidence non-reproducible and can exhaust
the sole attempt on an avoidable false failure. The body bound must be described
truthfully or implemented as an actual bound; window clipping, keyword/token
matching, and conflict precedence must have one exact rule.

#### P2-2 — The new evidence skeleton does not explicitly bind the certificate schema or the authorizing v14 review

The skeleton must record “the schema IDs in Section 5” (`v14:48-56`). Section 5
names `yakherd-capability-failure-v6` and preserves
`yakherd-capability-client-v3` (`v14:262-273`), but the new certificate schema ID
`yakherd-capability-certificate-v1` is defined only in Section 3
(`v14:67-76`). Under the literal instruction, the skeleton is not required to
record the certificate schema ID whose bytes gate the entire new attempt.

The skeleton also does not require the exact future independent v14 plan-PASS
record identity, even though that review is the authority prerequisite for
creating it. The previous live evidence preserved its authorizing plan-review
identity; the fresh boundary should remain self-auditing rather than relying on
thread history.

Finally, failed evidence contains the certificate object twice: once under
`Certificate checks (canonical JSON)` and again as
`certificate_preflight` inside the version-6 failure object (`v14:254-268`). The
candidate calls each the exact Section 3 object but does not explicitly require
the decoded objects and canonical preimages to be byte-identical. A strict
validator needs that equality rule to prevent two internally valid but
contradictory certificate records in one evidence document.

### P3 — Low

No P3 finding.

## Browser/API And Gate Pressure Test

The exact API names and ordinary exception containment are otherwise coherent:

- `iab.tabs.new()` produces a bound tab; `tab.goto()`,
  `tab.playwright.evaluate()`, and `tab.close()` are callable operations;
- both wrappers catch normal awaited failures without binding, printing, or
  rethrowing an error;
- each explicit output is an allowlisted scalar, and no body/window, URL,
  redirect target, account data, tab title, certificate diagnostic, or error
  object is written;
- the public equality expression returns only a boolean based on protocol and
  exact hostname, then normalizes non-booleans and exceptions to
  `UNOBSERVABLE`;
- no refresh, alternate panel route, URL read, tab-list read, screenshot, DOM
  snapshot, network/log/history read, or certificate-operation retry appears.

The panel gate's broad text heuristic may falsely classify its local row, but it
cannot by itself authorize continuation: only `ACTIVE` followed by `VALID` does
so (`v14:106-127`). A non-active panel scalar maps to `CERTIFICATE_PANEL`; a
public mismatch/unobservable scalar maps to `CERTIFICATE`. The certificate
object's field applicability and raw-ASCII order are otherwise total
(`v14:65-76,232-260`).

The ordinary transcript-containment claim is sound for caught promise
rejections. An execution-layer interruption before the explicit write remains
an operational residual and cannot establish an allowlisted scalar or PASS. It
does not repair the retained-tab/evidence gaps above.

## Schema, Inheritance, And Authority Recheck

The proposed certificate key order
`https_navigation,panel_status,schema_version` is correct raw-ASCII order. The
new top-level `certificate_preflight` position after `capability_result` and
before `cleanup_utc` is also correct. Failure version `6`, failure ID
`yakherd-capability-failure-v6`, certificate version/ID `1`/
`yakherd-capability-certificate-v1`, and unchanged client v3 are distinct from
stale versions (`v14:254-273`).

No regression was found in the inherited fixture/work row matrices, owner
states, unknown-first aggregation, PHP/bootstrap/runtime behavior, cURL direct
boundary, Error Logs channel, manifest/File Manager rules, credential
checkpoint, handback verifier, local-download lifecycle, no-cron rule, or
deployment boundary. No secret value, credential-derived value, account/user/
machine identifier, new remote filesystem path, package/release mutation, Git
authority, cron/SSH authority, provider-secret authority, or production
authority appears in v14.

Those correct lower layers do not override v14's own new-attempt block
(`v14:41-44`) or cure the new pre-generator browser-tab lifecycle.

## Required Blocking Revisions

Before another independent review, Architecture must issue a new exact,
hash-identified candidate that:

1. supersedes v13's applicability rule for v14-created tabs: `panel_tab` becomes
   applicable when the dedicated certificate-panel tab is created, and
   `staging_tabs` becomes applicable when the public navigation tab is created;
   other pre-generator client fields may remain N/A until their true boundaries;
2. makes every panel/navigation close result observable through a finite,
   allowlisted non-secret state, maps failed/unobservable final closure to
   `PANEL_TAB_CLOSE`/`STAGING_TABS_CLOSE` plus `CLIENT_STATE_INCOMPLETE`, and
   defines a bounded safe terminal cleanup for close failure without exposing a
   signed-in page, redirect, URL, or error and without retrying the certificate
   gate;
3. preserves an exact usable binding for the `VALID` staging tab or defines one
   explicit non-list/non-URL handoff operation, and requires that tab to be
   closed and truthfully recorded on every root/File Manager/other failure before
   credential-generator invocation;
4. aligns the panel evaluator and prose on the body-read versus acceptance cap,
   clamped/short window behavior, status conflict precedence, token matching,
   and cross-row ambiguity so one independent implementation derives one enum;
5. requires the fresh skeleton to bind all three schema IDs and the exact
   authorizing plan-review identity; and
6. requires the standalone certificate canonical object and the nested
   `certificate_preflight` object in failed evidence to be byte-identical and
   independently decoded/validated as the same observation.

The exhausted v13 evidence/review, v14 candidate, all prior plans/audits/evidence,
package/release bytes, Git state, DreamHost/browser/network state, and unrelated
files must remain preserved. Red Team is not authorized to repair v14.

## Residual Risks And Future Gates

After correction, a new plan PASS may authorize only a new validated skeleton
and one new disposable attempt. Live evidence must still demonstrate both exact
certificate signals, root/File Manager visibility, remote byte/mode/owner
fidelity, panel Basic Auth, bounded PHP/provider behavior, logs, manifests,
cleanup, client handback, and final empty state. Any missing scalar, ambiguous
inventory, retained tab, or incomplete evidence is capability FAIL.

Even a future capability PASS grants no Implementation by itself. Complete live
evidence still requires a separate fresh independent PASS before unchanged v3
Section 9 can be sent to Implementation. Deployment, cron, SSH/SFTP, Git, final
staging authentication/release, provider secret, live model, canary, production,
and publication remain subject to later byte-bound plans and independent gates.

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
The final audit SHA-256 is reported with the repository handoff so this record
does not attempt to contain its own digest.

No evidence, plan, prior audit, package/release byte, DreamHost/browser/network
state, credential, Git state, or website implementation byte was changed. The
PHP fence was hashed in process memory and was not materialized. The unrelated
`yakherd.mp4` was not read, hashed, moved, modified, staged, or otherwise
touched. The only write was this authorized v14 review.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v14 composite identified above.

This FAIL grants no new-attempt authority. Architecture may draft a corrected,
exact, hash-bound candidate and request fresh independent review, but may not
create `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability_v14.md`
or begin either certificate operation under v14. Implementation may not receive
v14; unchanged v3 Section 9 remains parked. No DreamHost/browser/network action,
credential, fixture, evidence skeleton, Git operation, cron, SSH/SFTP, final
staging auth/release, provider secret, live-model request, deployment, canary,
production, publication, or retry of the exhausted v13 attempt is authorized.

autonomous next action: Architecture must issue a new exact candidate resolving every v14 P1/P2 finding; the v13 attempt remains exhausted, and evidence-skeleton creation, browser/DreamHost access, Implementation, Git, credentials, SSH, cron, staging, provider-secret, live-model, deployment, and production remain parked.
