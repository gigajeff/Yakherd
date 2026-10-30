# Yakherd.dev Concierge Composite Plan v7 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus incorporated v5, v6, and the v7 runtime amendment
- Verdict: **FAIL**

## Exact Candidate And Precedence

The reviewed composite is exactly:

1. frozen v3
   `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
   `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
2. incorporated v5
   `docs/2026-07-21_yakherd_dev_concierge_website_plan_v5.md`, SHA-256
   `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
3. incorporated v6
   `docs/2026-07-21_yakherd_dev_concierge_website_plan_v6.md`, SHA-256
   `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
4. `docs/2026-07-21_yakherd_dev_concierge_website_plan_v7.md`, 17,715 bytes,
   399 lines, SHA-256
   `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`.

The preserved v6 FAIL audit is
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v6.md`,
SHA-256
`fcd340de3a67298d2dff0b36926225993941c0a6f863ab32e56b0d773f3f9b25`.
Every supplied hash matches the reviewed bytes. Root `AGENTS.md` was reviewed at
SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team role prompt at SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

Precedence is clear. V7 replaces v6 Appendix A and its PHP identity, scopes the
v6 tuple to successful quiescent states, adds a failure object, replaces every
clean/partial panel branch and cached-Authorization claim, and adds an Error Logs
proof (`v7:21-25`). All other v6 corrections remain; v6 continues to delete all
v5 cron authority. No contradictory lower-precedence cron, PHP, client-cache, or
deployment action survives as authority.

No DreamHost or network access was used for this document review.

## Appendix A Independent Reproduction

The literal Appendix A bytes were independently joined with LF line endings and
one terminal LF and encoded as UTF-8 without BOM. They reproduce exactly:

- byte length: `7131`;
- SHA-256:
  `7cdefa7718f84da1fc3266f9dea62b795724a49ff9c4b7b089e5a52249c2545e`.

Both values match `v7:31-40`. The exact POST body `{"run":true}` remains 12
UTF-8 bytes. The Appendix identity passes; the verdict follows from the strict
failure/evidence semantics below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — The mandatory `failure_state` cannot represent ordinary clean capability failures

V7 says **every failed attempt** has a `failure_state` whose `failure_classes`
array is nonempty and may contain only eleven listed values (`v7:65-99`). Those
values describe panel enable outcomes, retained fixture/work state, PHP error-log
visibility/rows, password-record cleanup, and browser restart. They do not
describe the capability checks that can fail while cleanup and all retained-state
classes are clean.

The literal Appendix supplies a direct counterexample. If
`curl_setopt_array(...)` returns false, the probe correctly does not call
`curl_exec`, returns bounded `503` data with
`openai_options_installed=false`, and can then complete fixture, work, panel,
password-record, tab, browser, access-log, and error-log cleanup successfully
(`v7:54-59`, `v7:342-395`). None of the allowed failure-class values is true, but
the array is required to be nonempty. The required object is therefore
impossible to construct without lying or using a forbidden enum.

The same contradiction occurs for clean failures of PHP version, a required
extension/function, `path_binding`, filesystem primitives, an unexpected OpenAI
status, response/time bound, Basic Auth/HTTP/header behavior, manifest or remote
download hash, access-log observation, and other gates that leave no retained
path or client failure. A caught generic PHP runtime error with a zero-row Error
Logs result also has no runtime-error enum. Certificate or panel/File Manager
precondition failures are likewise not modeled if the evidence contract applies
to the whole attempt.

Two cleanup outcomes are missing too. `staging_tabs_closed=false` must be a typed
failure under `v7:131-137`, but there is no tab-closure failure class. A normal
cleanup whose panel disable fails while both valid host files remain has
`panel_inventory=both_enabled`, but no `panel_disable_failed`/retained-enabled
class; `panel_retained_partial` does not truthfully describe both files.

Because only a typed `failure_state` can preserve a failed attempt at the sole
evidence path (`v7:94-103`, `v7:173-187`), these routine failures cannot be
recorded under the candidate's own strict schema. This blocks independent live
capability review even though the underlying remote/client behavior is otherwise
fail closed.

### P2 — Medium

#### P2-1 — Two nested failure-inventory types are not exact schemas

The top-level field names are finite, but `fixture_inventory` is described as an
array of relative names “with” type/mode/length/hash booleans without defining
whether each member is a string or object or listing exact member keys and types
(`v7:82-88`). `work_inventory` is simultaneously described as one of four string
values and as carrying additional safe metadata, without defining an object
shape that can contain both. Unknown fields are rejected, so an implementer
cannot add metadata keys safely.

The document calls this a strict evidence object, but two reviewers can produce
incompatible structures while following the prose. The exact failure-state
serialization/container within the Markdown evidence is also not stated. This
does not affect the already-correct canonical holding/probe manifests, but it
prevents strict validation of the new failure evidence.

#### P2-2 — `error_channel_contained=true` does not require successful output buffering

Appendix A calls `ob_start()` before installing the shutdown function, error
handler, or request-local display/log suppression, but it ignores `ob_start`'s
boolean result (`v7:208-230`). `error_channel_contained` is later set to true
solely because execution reached the result object after the two `ini_set`
checks (`v7:251-280`). A normal `200` can therefore attest containment without
proving that the output buffer—the mechanism relied on to discard accidental
output before every response—was actually installed.

An `ob_start` warning/failure also occurs before the warning-to-exception handler
and before `display_errors=0`/`log_errors=0`, exactly outside the boundary v7
claims is established “before any” work (`v7:42-52`). The later zero-row panel
check may detect a logged event, but it does not make the in-process containment
boolean truthful or prevent early displayed output. The buffer-start result must
be checked and logically required for any normal result; bootstrap failure needs
a generic, non-path-bearing disposition that cannot self-attest success.

#### P2-3 — A nonzero Error Logs query may expose the forbidden row merely by rendering results

The Error Logs route appropriately restricts hostname, time, fixed path,
zero/nonzero outcome, retention, and no-copy behavior, and makes unavailable or
nonzero results typed failures (`v7:139-171`). However, it does not require that
the panel expose a count/match boolean without rendering the matching row. In a
normal search UI, applying the time/path filter can display the row—including a
filesystem path or message—to the in-app browser before Architecture chooses not
to open or copy it. A browser-tool snapshot can then place that content in the
tool transcript, contradicting `v7:158-160`.

The finite route must first establish a count-only/redacted-results capability.
If the UI necessarily renders row content, it must become
`php_error_log_unobservable` without performing a query that exposes the row, or
the plan must identify another already-authorized human-only boolean channel that
cannot reveal row text. The current “never copied” rule is weaker than “never
displayed or enters the tool transcript.”

### P3 — Low / Observations

#### P3-1 — cURL installation and 200 logic are corrected

V7 records the strict boolean result of `curl_setopt_array`, short-circuits before
`curl_exec` when false, avoids `curl_getinfo` claims in that branch, and exposes
`openai_options_installed` in bounded result JSON (`v7:342-380`).
`openai_tls_unauthenticated` depends on `openai_direct_bounded`, which depends on
successful option installation, so any HTTP `200` logically requires the option,
fixed URL, no-proxy/no-redirect, TLS, timeout, 4096-byte body, and status gates
even though `$all` names the terminal dependent boolean rather than repeating
all of them (`v7:382-395`). V6 P1-1 is closed at the transfer boundary.

#### P3-2 — Runtime warning/throwable handling is materially fail closed after bootstrap

After startup, V7 installs a warning-to-exception handler that discards the
original message/file/line, requires request-local display and logging off,
catches every `Throwable`, discards buffers, and emits only fixed generic JSON
(`v7:42-52`, `v7:208-264`, `v7:396-398`). Filesystem, cURL, and JSON failures do
not interpolate a path, trace, source, configuration value, provider body, or
exception text. The shutdown handler covers an uncompleted fatal path with the
same fixed body. P2-2 is the remaining bootstrap-attestation gap, not a finding
that later filesystem/cURL/JSON branches deliberately expose data.

#### P3-3 — Credential lifecycle and cached-header claim are corrected

One affirmative checkpoint authorizes one credential and exactly one enable
submission with no retry. Success, timeout, clean failure, recovered partial, and
unresolved partial outcomes all require password-record deletion, staging-tab
closure, browser restart, and evidence booleans (`v7:105-129`). The unobservable
post-disable request and cached-Authorization inspection are removed; no header
or derived credential byte is inspected or claimed (`v7:131-137`). The missing
failure enum for tab closure and retained-enabled disable failure is part of
P1-1, not an authority to skip cleanup.

#### P3-4 — Successful state, cron removal, manifests, work recovery, and evidence path remain closed

V7 correctly limits the v6 three-class tuple to successful quiescent states and
keeps unknown/mismatched retained paths protected (`v7:65-103`). V6's private
work path, exact modes/hash recovery, strict ASCII/no-escape manifest bytes,
base64 preimages/timestamps, finite File Manager operations, and sole capability
evidence path remain incorporated. Every cron path/source/job/action remains
withdrawn, with final cron deferred to a later byte-bound deployment review.

The sole live evidence path remains
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`. Only a
complete successful preflight followed by fresh independent capability PASS may
unpark the unchanged v3 Section 9 local Implementation task. Implementation has
no DreamHost, network, credential, cron, SSH, Git, staging, provider-secret, or
production authority (`v7:173-187`). No dependency cycle, unlisted remote write,
new network destination, delete expansion, or deployment-authority leak was
found.

#### P3-5 — No secret value or observed machine-specific identifier is present in the candidate

V7 contains symbolic paths, fixed public hosts/role names, source hashes, enum
labels, and test payloads only. It contains no observed DreamHost
username/home/server, password or derived value, private key, API key, provider
body, unrelated log row, or personal data.

## V6 Finding Closure Status

| V6 finding | V7 status |
| --- | --- |
| P1-1 unchecked cURL options | Resolved by strict result capture, short-circuit, result visibility, and dependent 200 logic. |
| P1-2 PHP path/error disclosure | Substantially resolved after bootstrap by output discard, warning conversion, display/log suppression, generic catch/shutdown, and zero-row proof; unchecked buffer bootstrap remains P2-2. |
| P2-1 incomplete retained-failure tuple | Success tuple is correctly scoped, but the replacement failure schema omits routine clean failures and has ambiguous nested types (P1-1/P2-1). |
| P2-2 incomplete clean/recovered credential branch | Behavioral cleanup/no-retry is resolved; its tab-closure and retained-enabled failure classes are missing from the evidence enum. |
| P2-3 unobservable cached Authorization claim | Resolved by deleting the claim and post-disable request and recording only secret-safe cleanup actions. |
| P2-4 missing PHP error-channel evidence | A finite zero-row/error-retention route is added, but nonzero result rendering is not yet guaranteed transcript-safe (P2-3). |

## Required Blocking Revisions

Before another independent review, Architecture must provide a new exact,
hash-identified candidate that:

1. makes `failure_classes` exhaustive for every clean and retained capability
   failure, including PHP/runtime/required-feature, path/filesystem, cURL-option,
   direct-egress/status/bound, TLS/certificate, auth/HTTP/header, manifest/remote
   byte, File Manager, access-log, error-log, cleanup, panel-disable, tab closure,
   and other required gate failures, or supplies an exact bounded `failed_checks`
   sub-schema that truthfully represents each one;
2. defines the exact JSON/data shape, member keys, types, and allowed metadata for
   each `fixture_inventory` and `work_inventory` variant and the exact embedding
   of `failure_state` at the named evidence path;
3. verifies successful `ob_start`, includes output-buffer installation in the
   error-containment/200 dependency, and gives pre-handler bootstrap failure a
   generic, non-logging, non-disclosing fail-closed disposition; and
4. requires a count-only/redacted Error Logs result mode before querying, or
   treats a row-rendering UI as unobservable without allowing row text to enter a
   browser/tool transcript.

V7, v6, v5, v3, all earlier plans/audits/evidence, package/release bytes, and
unrelated files must remain preserved. These findings do not authorize Red Team
to repair the candidate in place.

## Residual Risks And Mandatory Future Gates

After correction, live evidence must still prove staging TLS, panel Basic Auth
before every content/error/method response, hidden inventory, File Manager
byte/mode fidelity, manifest preimages, PHP/runtime support, generic output/error
behavior, path/filesystem primitives, work cleanup/recovery, direct bounded
credential-free OpenAI TLS, minimized access/error logs, panel removal,
password-record deletion, tab closure, browser restart, exact final inventory,
and independent capability review. Ambiguity remains a capability FAIL.

The later deployment amendment remains mandatory for final cron, SSH/host keys,
manual staging authentication, production/staging Apache bytes, immutable
releases, manifests, atomic publication, A/B/source-independent rollback, Git,
provider secret, canary, staging release, and production. V7 grants none of those
actions.

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
was this authorized v7 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v7 composite identified above.

This FAIL grants no disposable-preflight authority. Architecture may draft a new
exact candidate and request fresh independent Red Team review. Implementation may
not receive v7 as written; unchanged v3 Section 9 remains parked. No DreamHost
panel/File Manager/Error Logs mutation or inspection, human credential checkpoint
or creation, fixture materialization/upload, probe/network request, cron, SSH,
SFTP, release/deployment, Git action, provider secret, staging release, live
model request, or production action is authorized.

No previous plan PASS, hosting inventory, or partial v7 finding overrides v7's
own block (`v7:27-29`) or the separate fresh independent live capability PASS
required before Implementation (`v7:173-187`).

autonomous next action: Architecture must issue a new exact candidate resolving every v7 P1/P2 finding; Implementation, DreamHost, Git, credentials, cron, staging, and production remain parked.
