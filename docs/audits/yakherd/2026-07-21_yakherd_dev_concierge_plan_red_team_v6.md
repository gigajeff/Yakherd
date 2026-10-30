# Yakherd.dev Concierge Composite Plan v6 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5 plus the v6 closed-preflight correction
- Verdict: **FAIL**

## Exact Candidate And Precedence

The reviewed composite is exactly:

1. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
   `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
2. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v5.md`, SHA-256
   `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
3. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v6.md`, 23,035 bytes,
   483 lines, SHA-256
   `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`.

The preserved v5 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v5.md`,
SHA-256
`53e4e3b8cab1c75877450020124ab06833d7ec7d892d30ea406b395ce5dc0a48`.
All four supplied hashes match the bytes reviewed. Root `AGENTS.md` was reviewed
at SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team role prompt at SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

V6's precedence is sufficiently explicit: it replaces the v5 PHP source/hash,
manifest/evidence serialization, File Manager proof, work recovery, and
human/panel lifecycle where stated, and removes every v5 cron-preflight
statement, path, source, state, job, and cleanup action from authority
(`v6:24-32`, `v6:64-67`). V5 otherwise remains incorporated; frozen v3 remains
binding outside the expressly suspended hosting/deployment order. No cron source
from v5 may be materialized under this composite.

No DreamHost or network access was used for this document review.

## Appendix A Independent Reproduction

The literal bytes between the v6 Appendix A fence were independently joined with
LF line endings and one terminal LF and encoded as UTF-8 without BOM. The result
is exactly:

- byte length: `5632`;
- SHA-256:
  `70feca907ce39312667d3924c5def589344d944cd06c6187fc7dbcce51727f10`.

Both values match `v6:69-80`. The recovery payload
`yakherd-capability` plus LF independently reproduces 19 bytes and SHA-256
`feb9228339c4d4ce5ef36577560781a0c38ec3e34c0ba37d75d26e33f6bb9be7`,
matching `v6:161-165`. The request body `{"run":true}` is 12 UTF-8 bytes.
Appendix source identity therefore passes; the verdict follows from execution
and evidence semantics below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — cURL option installation is not checked, so the direct/TLS boundary is not fail closed

V6 requires proxy and redirect disabling, HTTPS-only protocol, peer/host
verification, fixed effective URL, bounded time/body, and status `401`
(`v6:173-196`). Appendix A calls `curl_setopt_array(...)` but discards its boolean
result and executes the transfer unconditionally (`v6:433-468`).

`curl_setopt_array` can fail when an option is unsupported or rejected and can
stop applying later options. A failure at or before `CURLOPT_PROXY`,
`CURLOPT_NOPROXY`, `CURLOPT_SSL_VERIFYPEER`, or `CURLOPT_SSL_VERIFYHOST` is not
represented in `$result`. The subsequent request can still return cURL success,
the fixed effective URL, zero redirects, a body within 4096 bytes, and status
`401`, causing both `openai_direct_bounded` and
`openai_tls_unauthenticated` to become true even though one or more required
controls were never installed.

The expected DreamHost/PHP versions make successful option installation
plausible, but a fail-closed capability probe must prove it. Ignoring the only
API result that reports whether the required control set was accepted defeats
the exact direct/no-proxy/TLS assertion and leaves v5 P1-5 unresolved.

#### P1-2 — Expected filesystem failure branches can emit or log absolute machine paths

The incorporated v5 contract says the probe emits only bounded JSON and no file
path or server/account identifier (`v5:276-280`). V6 likewise requires redacted
evidence and no username/home/server (`v6:230-233`). The replacement PHP performs
`chmod`, `fileperms`, `fopen`, `flock`, `rename`, `symlink`, `unlink`, and `rmdir`
operations on absolute paths without installing a warning-to-exception handler,
disabling display/log emission, or otherwise containing PHP warnings
(`v6:380-430`).

These functions can emit warnings containing the full resolved filename on the
very permission, type, race, or cleanup failures the preflight is designed to
exercise. Depending on host configuration, that path can be inserted into the
authenticated HTTP body and/or DreamHost PHP error logs, corrupting the claimed
JSON-only response and persisting the dedicated home/user path. The v5/v6 log
sequence inspects access-log fields but does not bound or purge PHP error-log
output caused by the probe.

Basic Auth prevents an unauthenticated visitor from seeing the response, but it
does not satisfy the plan's no-machine-identifier response/log contract. Failure
must remain generic and redacted, not first leak the path and then mark the gate
failed.

### P2 — Medium

#### P2-1 — The “complete” three-class state tuple excludes its own retained-failure states

Section 2 calls the tuple complete, but permits only panel-auth `absent/enabled`,
fixture `absent/holding/probe`, and work `absent` at every quiescent boundary
(`v6:45-62`). Later required branches can quiesce with one host-managed auth file,
contradictory panel status, a failed-retained fixture path, or a known/unknown
work directory that cannot be safely removed (`v6:150-171`, `v6:254-264`; v5's
incorporated failure rules at `v5:306-319`). Evidence is expressly required to
record `partial-panel` and `failed-retained` states (`v6:292-301`).

Those are correct fail-closed outcomes, but they have no value in the state model
that is claimed to be complete. Consequently an independent reviewer cannot map
every mutation ledger end state to the strict tuple or distinguish an authorized
retained failure from an unmodeled extra. The tuple must either be scoped to
successful boundaries or include exact typed retained-failure states and their
allowed inventories.

#### P2-2 — Two clean panel-failure branches do not finish the credential lifecycle explicitly

After any enable submission, `disabled + neither file` is called a clean
failed/no-change state, while a mixed state receives exactly one disable attempt
(`v6:254-264`). If that disable succeeds, the document does not explicitly say
that the capability fails with no retry and then requires the human to delete the
temporary password-manager item, close staging tabs, restart the browser, and
record the cleanup confirmation. Those actions are written explicitly only for
normal cleanup and for an unresolved partial state “as far as possible”
(`v6:263-273`).

The checkpoint summary says cleanup includes those actions (`v6:237-250`), but
the exact branch transition is missing. A plan that authorizes one masked
credential must close its client-side state after every success, clean failure,
timeout, ambiguity, recovered partial enable, and unrecovered partial enable;
none may imply a retry or leave the password-manager item live.

#### P2-3 — “No cached Basic Auth credential is sent” has no authorized observable proof

Normal cleanup closes tabs and restarts the in-app browser, then opens a fresh
staging request and says to confirm that no cached Basic Auth credential is sent
(`v6:266-273`). Once panel protection is disabled, the server no longer
challenges the request. Opening the page alone cannot show whether the browser
preemptively attached an `Authorization` header, and the incorporated access-log
proof deliberately does not record that header.

V6 authorizes no browser-network-inspector operation for this check. Inspecting a
present Basic header also risks displaying a password-derived base64 value,
which the checkpoint forbids the assistant/tool transcript from receiving. A
browser restart can be recorded as the prescribed cache-clearing action, but the
additional transmission-absence claim needs a concrete secret-safe boolean
observation or must not be represented as directly proven.

#### P2-4 — The PHP error channel is absent from the otherwise finite log evidence route

V6 correctly preserves minimized access-log fields and prohibits unrelated log
downloads, while Section 6 limits remote proof to the panel/File Manager
operations (`v6:198-233`; incorporated `v5:266-272`). No step identifies the PHP
error-log location/controller, checks whether the fixture can write to it,
records a no-warning result, or defines cleanup/retention for a probe-generated
warning. This is the evidence-side counterpart to P1-2: even after code-level
containment, the live gate needs a finite proof that the test did not put paths,
response JSON, or credentials in an application/error channel.

### P3 — Low / Observations

#### P3-1 — The private work path and bounded recovery are corrected

Appendix A now resolves `fixture`, `staging-public`, and `yakherd.dev`, requires
their exact parent/basename relationship, and derives the work path from
`dirname(__DIR__, 2)` (`v6:132-148`, `v6:380-415`). It creates the work directory
as mode `0700`, creates `first.bin` exclusively, verifies file/dir modes and
filesystem primitives, and requires cleanup for HTTP `200`. Section 4 permits
only exact type/owner/mode/target/length/hash-verified recovery with panel auth
retained on any mismatch (`v6:150-171`). The advertised recovery hash matches.

#### P3-2 — Cron authority and its dependency/race are fully removed from preflight

The successful state sequence contains no cron class. V6 unconditionally removes
the v5 cron manifest, sources, paths, panel job, schedule, and cleanup actions and
defers the final cron to the post-Implementation deployment amendment
(`v6:30-32`, `v6:58-67`, `v6:275-290`). No remaining v6 cron reference grants a
write, delete, test, or scheduler action.

#### P3-3 — Manifest byte semantics and independent preimages are corrected

The restricted printable-ASCII alphabet, rejection of quote/backslash/escapes,
literal slash, raw-ASCII key/path ordering, integer form, exact punctuation,
no-whitespace/BOM/newline rule, strict parser, and zero-field rule close the v5
JSON escaping ambiguity (`v6:82-110`). Both exact manifest preimages, timestamps,
byte lengths, SHA-256 values, self-hashes, and human-readable tables must be
preserved as unwrapped padded RFC 4648 base64 at the sole named evidence path and
independently decoded/reproduced (`v6:112-130`). A digest without its preimage is
correctly a capability FAIL.

#### P3-4 — File Manager and authority boundaries are materially closed

V6 names the only panel/File Manager operations, requires hidden-file display,
type/owner/mode/length/containment fields, forbids alternate verifiers and bulk,
recursive, archive, editor, WebDAV, overwrite, or guessed operations, and uses
individual downloads for local length/hash comparison (`v6:198-233`). If a
required field is unavailable, the gate stops. Panel root auth precedes every
fixture byte, and the child `.htaccess` contains no auth directive or arbitrary
production suffix.

A v6 plan PASS is expressly limited to the disposable preflight. A separately
reviewed live capability PASS is still required before unchanged v3 Section 9
local Implementation can be sent to the existing task; Implementation receives
no DreamHost, network, credential, Git, staging, or production authority
(`v6:292-307`). Final cron, SSH, manual staging auth, release publication, Git,
provider secret, staging release, rollback, and production remain deferred. No
new dependency cycle or deployment-authority leak was found.

#### P3-5 — No secret value or observed machine-specific identifier is present in the candidate

V6 contains symbolic `$HOME`/builder paths, fixed public hostnames and role names,
source hashes, and test payloads only. It contains no observed DreamHost
username/home/server, credential, password-derived value, private key, API key,
provider response, or personal data. P1-2 concerns what the live PHP runtime may
emit on failure, not a secret or machine identifier already present in the plan
bytes.

## V5 Finding Closure Status

| V5 finding | V6 status |
| --- | --- |
| P1-1 wrong work path/recovery | Resolved by the corrected private path, binding/modes, reproduced recovery hash, and exact retained-failure handling. |
| P1-2 cron manifest contradiction | Resolved by unconditional removal of every cron state/path/source/action. |
| P1-3 cron cleanup race | Resolved by removing cron from preflight and deferring it to a later byte-bound review. |
| P1-4 unverifiable manifest hashes | Resolved by preserving exact base64 preimages/timestamps at one named evidence path. |
| P1-5 proxy/body boundary | Partially resolved; the literal options are correct, but ignored `curl_setopt_array` failure leaves P1-1. |
| P2-1 JSON escaping ambiguity | Resolved by the strict ASCII/no-escape serializer and parser. |
| P2-2 File Manager/evidence path | Resolved by finite panel operations, individual downloads, local hashes, and the sole evidence path. |
| P2-3 credential/partial panel lifecycle | Improved but incomplete for clean/recovered enable failures and the unobservable cached-header assertion. |
| P2-4 literal runtime assertions | Work modes, proxy, redirects, response cap, and cron removal are corrected; warning/error-channel handling remains unresolved. |

## Required Blocking Revisions

Before another independent review, Architecture must provide a new exact,
hash-identified candidate that:

1. requires successful installation of every cURL option before `curl_exec`,
   treats a false/exception/unsupported option as a generic fail-closed result,
   and makes the option-set result independently testable without exposing
   configuration;
2. prevents every PHP warning/notice/exception from disclosing or logging an
   absolute path, username/home/server, source, response body, or configuration
   value on all filesystem, cleanup, cURL, and JSON failure branches, and defines
   a bounded error-log proof/retention disposition;
3. makes the state model exact for both successful and all authorized
   partial/failed-retained quiescent inventories, or expressly limits the tuple
   and gives every failure state a separate closed schema;
4. states the no-retry outcome and complete password-manager/tab/browser cleanup
   for clean failed enables and successfully recovered partial enables, as well
   as unresolved partial states; and
5. replaces the unobservable “no cached Authorization sent” assertion with an
   exact secret-safe authorized observation, or limits the claim to the recorded
   browser restart/session-clear action without inspecting credential-derived
   bytes.

V6, v5, v3, every earlier plan/audit/evidence record, package/release bytes, and
unrelated files must remain preserved. These findings do not authorize Red Team
to repair the candidate in place.

## Residual Risks And Mandatory Future Gates

After plan correction, live evidence must still prove staging TLS, root Basic
Auth before all content/error/method responses, exact hidden inventory,
File Manager byte/mode fidelity, PHP/runtime support, path binding, filesystem
primitives, generic error behavior, work cleanup/recovery, direct bounded
credential-free OpenAI TLS, minimized access/error logs, panel cleanup, human
credential deletion, browser session clearing, and final exact inventory. Any
ambiguity remains a capability FAIL.

The mandatory later deployment amendment must independently bind final cron,
SSH/host keys, manual staging authentication, production/staging Apache bytes,
immutable releases, manifests, atomic publication, A/B/source-independent
rollback, Git checkpoints, provider secret, canary, staging release, and
production. V6 grants none of those actions.

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
was this authorized v6 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v6 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review. Implementation may
not receive v6 as written; the unchanged v3 Section 9 local write set remains
parked. No DreamHost panel/File Manager mutation, human credential checkpoint or
creation, fixture materialization/upload, probe or network request, cron, SSH,
SFTP, release/deployment, Git action, provider secret, staging release, live
model request, or production action is authorized.

No previous plan PASS, hosting inventory, or partial v6 finding overrides v6's
own block (`v6:34-36`) or the requirement for a separate independent live
capability PASS before Implementation (`v6:303-307`).

autonomous next action: Architecture must issue a new exact candidate resolving every v6 P1/P2 finding; Implementation, DreamHost, Git, credentials, cron, staging, and production remain parked.
