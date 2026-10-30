# Yakherd.dev Concierge Composite Plan v5 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plus the v5 pre-Implementation capability amendment
- Verdict: **FAIL**

## Exact Candidate And Review Boundary

The reviewed composite is exactly:

- `docs/2026-07-21_yakherd_dev_concierge_website_plan_v5.md`, 27,694 bytes,
  573 lines, SHA-256
  `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- incorporating frozen
  `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
  `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- pressure-tested against the preserved v4 FAIL audit
  `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v4.md`,
  SHA-256
  `e2abae3cf21dd1754d4f93afdd84051389ed53d3aca757ea697d318a3c3a42b5`;
- and DreamHost evidence
  `docs/audits/yakherd/2026-07-21_yakherd_dev_dreamhost_evidence.md`, SHA-256
  `791ea693b00963c0a4fb8034b733d3da15d8bb5e36fc4c1b4ea6d8a320246fe4`.

All four supplied hashes match the bytes reviewed. Root `AGENTS.md` was reviewed
at SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team role prompt at SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

V4 is historical evidence, not incorporated authority. Frozen v3 requirements
outside v5's stated replacements remain binding. No DreamHost or network access
was used for this document review.

## Appendix A Independent Byte Reproduction

The bytes between each literal fence were independently joined with LF line
endings and one terminal LF, encoded as UTF-8 without BOM, and hashed in memory.
The empty `enabled` file was hashed as zero bytes. Every advertised value matches:

| Appendix source | Reproduced bytes | Reproduced SHA-256 | Result |
| --- | ---: | --- | --- |
| `fixture/.htaccess` | 354 | `3d78af579472accd7a9dcd88b8e3dd32b29ebaea8ec523e92d4d40dc18f7ac4c` | PASS |
| `fixture/index.html` | 129 | `eb3210806694aa07c2688a05901b6454ba61460ec99908832343a410856d8c15` | PASS |
| `fixture/404.html` | 95 | `a197e91834a3427a9321720a342903799b814132842796eb204e7fe915efdf4d` | PASS |
| `fixture/capability.php` | 4,164 | `7df26e841c1fed7d9b17e2ee9719caee01d681547eeaee33590bc05b52acdd5f` | PASS |
| `.capability-cron/cron.php` | 489 | `9a26887f281ba1ebbce2bbe9b6a8c493e72bc5646c431495322af28f24f84c3b` | PASS |
| `.capability-cron/enabled` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | PASS |

The exact request body `{"run":true}` is also 12 UTF-8 bytes as claimed at
`v5:242-249`. Correct source hashes do not cure the execution findings below.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — The probe writes to an unlisted public-root path, not the declared private work path

Section 4 authorizes only
`$HOME/yakherd.dev/.yakherd-capability-work/` and its three children
(`v5:125-132`). Appendix A computes:

```php
$work = dirname(__DIR__) . '/.yakherd-capability-work';
```

`capability.php` is deployed in `staging-public/fixture/`, so `__DIR__` is
`$HOME/yakherd.dev/staging-public/fixture` and `dirname(__DIR__)` is
`$HOME/yakherd.dev/staging-public`. The literal probe therefore creates
`$HOME/yakherd.dev/staging-public/.yakherd-capability-work`, not the authorized
site-private sibling (`v5:469-472`).

This violates the closed remote path set, places runtime artifacts under the web
root, invalidates the stated private-path inventory, and makes the exact-empty
proof check the wrong location. Section 8 does not individually delete either
version of the work directory or `first.bin`, `second.bin`, and `link.bin` if the
probe's `finally` cleanup fails (`v5:282-319`). On such a failure, the plan has no
authorized recovery path to exact empty and can later disable panel auth without
an exact branch covering these known leftovers.

#### P1-2 — The `cron` state manifest rejects the still-required holding state

The mandatory sequence leaves all three holding files in place after deleting
the probe, then creates the cron files (`v5:250-265`). Yet the `cron` manifest is
defined to contain exactly only `cron.php` and `enabled` (`v5:185-190`), while
the per-transition verifier must verify every remote operator path and reject any
extra operator path (`v5:192-197`).

At the cron transition, the three holding paths are therefore either forbidden
extras or silently outside an undefined verifier scope. The plan defines neither
a composite `holding + cron` state nor independent, destination-class-scoped
closed-set verification. The runtime marker/temp exemption does not resolve the
already-present holding files. The claimed
`protected-empty → holding → probe → holding → cron → exact-empty` state machine
cannot pass its own strict manifest rule as written.

#### P1-3 — Cron deactivation is racy and the “concurrent job becomes a no-op” assertion is false

Cleanup claims that deleting `enabled` first makes any concurrent or undeleted
job a no-op (`v5:287-295`). The cron program checks `enabled` only once, before
constructing and renaming its marker (`v5:551-568`). An invocation that passes
that check immediately before cleanup can still create a temp file and replace
`marker.txt` after cleanup has deleted or verified those paths. There is no
stable lock shared by execution and cleanup, no process/journal check, no
quiescence interval after panel-job removal, and no second enabled check before
rename.

Consequently final exact empty can be observed transiently and then invalidated.
The plan also has no exact branch for inability to delete `enabled`; in that case
the job is neither made inert nor safely bounded. `file_put_contents` does not use
exclusive creation for `.marker.tmp-<pid>`, so an unexpected pre-existing exact
temp path can be overwritten despite the no-overwrite contract. These defects
break both success cleanup and failure recovery.

#### P1-4 — A future independent capability reviewer cannot verify the state manifests

The state manifests are local only and are never uploaded. Evidence records their
self-hashes, not their canonical bytes (`v5:158-197`). The capability evidence is
required to list the three self-hashes and Appendix file hashes, but not the
manifest bytes, entry rows, or each manifest's `created_utc` (`v5:316-326`). A
SHA-256 value without its preimage cannot prove to an independent reviewer that
Architecture used the required state, entries, path classes, modes, timestamps,
or zero-field self-hash procedure.

That leaves the local Architecture verifier as the only party able to inspect
the record even though `v5:323-326` correctly says Architecture may not
self-certify the live probe. The required fresh independent capability PASS
cannot be evidence-based under this preservation contract.

#### P1-5 — The egress probe does not prove the fixed direct OpenAI boundary it claims

The probe fixes the URL and enables peer/host verification, but it never disables
configured environment/system proxies (`v5:509-529`). A transfer through an
allowed proxy can therefore satisfy cURL success and upstream status `401` while
failing to prove the inherited v3 no-proxy egress property. This contradicts the
claim that no other host is contacted (`v5:242-249`) and can falsely certify the
network boundary needed by later Implementation.

The write callback discards provider bytes but accepts an unbounded number of
them until the ten-second timeout; the 33-byte ceiling applies only to the
incoming browser request, not the provider response (`v5:443-448`, `v5:509-529`).
Thus `v5:266-272` also cannot prove the inherited bounded-response behavior from
this fixture. No credential or user idea is exposed by this probe, but the
capability conclusion itself is unsound.

### P2 — Medium

#### P2-1 — The “canonical JSON” serialization still permits different valid bytes

V5 fixes keys, types, ordering, whitespace, newline, row shape, and self-hash,
but it does not define JSON string escaping (`v5:158-183`). All destination
paths contain `/`; both `/` and `\/` are valid JSON encodings of the same parsed
string under the stated rules. Escape choices for other characters are likewise
not closed. Independent builders can therefore serialize different bytes and
produce different `state_sha256` values while satisfying the written semantic
schema. The exact v3 canonical serializer is not explicitly incorporated for
these new local state manifests.

#### P2-2 — Root/path and remote File Manager proof operations are asserted but not closed

The plan requires empty-root discovery including hidden paths, regular-file and
symlink classification, owner-class, exact Unix modes, remote length/hash, exact
resolved home containment, and non-symlinked parents using only the panel and
File Manager (`v5:90-139`, `v5:192-197`). It does not specify the exact read-only
panel/File-Manager operations that prove those facts or whether a download is
authorized for hashing. The Appendix PHP probe does not verify its own resolved
parent/root or directory mode; it checks only the symlink it creates and the mode
of `second.bin` (`v5:469-505`). If the panel cannot expose a fact the plan says to
stop, but the evidence route must still be finite so Architecture cannot invent
an unreviewed remote verifier or alternate transfer method.

Section 9 also authorizes “one redacted capability evidence document” without
naming its exact repository path (`v5:321-326`). That is an unlisted local write
outside the otherwise finite v3 Section 9 set and conflicts with the amendment's
exact-authority premise.

#### P2-3 — The human credential checkpoint and partial panel failure lifecycle are incomplete

The secret creation route is materially safer than v4: HTTPS first, human-only
password-manager generation, at least 128 bits, masked fields, fixed username,
no argv/clipboard/tool transcript, and root-only panel enablement
(`v5:199-225`). However, the checkpoint never expressly requires an affirmative
human answer bound to the exact root, username, single credential, and cleanup
facts before panel mutation. It also does not require removal of the temporary
password-manager record or browser Basic Auth cache/session after panel cleanup.

Section 8 begins its recovery contract only “once panel protection is enabled”
(`v5:282-301`). A panel operation that partially creates one host-managed file
but returns failure or never reaches an enabled state has no exact inventory,
disable, retention, or human recovery branch. The no-manual-delete rule is safe,
but the partial state still needs a bounded disposition before any capability
PASS.

#### P2-4 — Several literal probe assertions are not fully tested by the literal code

The probe requests work-directory mode `0700` but neither `chmod`s nor verifies
the directory's exact mode. It does not explicitly disable redirects, though the
expected default is off, and it does not count/cap discarded provider bytes. The
cron command's phrase “with no shell” is also not a provable property of a normal
cron daemon invocation; the plan can prove only that the reviewed command string
contains no shell metacharacter, variable, redirection, or second command
(`v5:253-265`). These assertions must be made exact rather than inferred from
platform defaults.

### P3 — Low / Observations

#### P3-1 — V5 correctly removes several v4 authority hazards

The nonexistent-production-release dependency and v4 overlay are withdrawn;
Appendix A is a finite preflight source; holding and probe are separate manifest
states; panel root auth is installed before any operator byte; the child
`.htaccess` contains no authorization directive or arbitrary production suffix;
and unauthenticated GET/POST/error paths are tested before and after upload. The
v4 immutable-overlay, final auth, SSH/key, release, Git, provider-secret, and
production actions are explicitly deferred (`v5:31-41`, `v5:64-88`,
`v5:334-371`). Those are sound boundary improvements, but they do not cure the
P1/P2 defects in the disposable preflight.

#### P3-2 — No secret value or observed machine-specific identifier entered the candidate

V5 uses `$HOME` and builder notation rather than an observed user, home, server,
password, private key, password hash, API key, or credential-derived value. The
fixed `yakherd-preflight` name is a non-secret role login. Appendix A contains no
credential, personal data, or machine-specific path.

#### P3-3 — The intended post-capability Implementation boundary is narrow

V5 states that only a separately reviewed live capability PASS may unpark the
unchanged v3 Section 9 paths and that Implementation then receives local paths,
tests, local manifest generation, and its exact v3 evidence path only—no
DreamHost, network, secret, Git, staging, or production authority
(`v5:321-332`). It also suspends v3 deployment/promotion until a later byte-bound
amendment receives fresh review (`v5:334-371`). This is the correct intended
authority shape. Because the present candidate fails, that conditional authority
does not arise.

## V4 Regression Disposition

| V4 finding | V5 disposition |
| --- | --- |
| P1-1 nonexistent production source | Conceptually resolved by Appendix A, but the literal probe introduces the P1-1 unlisted-path defect. |
| P1-2 probe forbidden by overlay | Holding/probe states are separated, but the later cron state violates the same closed-set semantics in P1-2. |
| P1-3 overridable auth suffix | Resolved for this disposable fixture by panel root auth and a child file with no auth directives; final staging auth is correctly deferred. |
| P1-4 incomplete immutable overlay transaction | Withdrawn and correctly deferred; v5 grants no release/deployment authority. |
| P1-5 open SSH/manual credential route | SSH/manual auth is withdrawn; transient panel auth is narrower but still has P2-3 lifecycle gaps. |
| P2-1 underspecified manifest | Improved, but string bytes and independently reviewable manifest evidence remain unresolved in P1-4/P2-1. |
| P2-2 incomplete cleanup | Improved with named steps, but work-path recovery and cron quiescence/failure branches remain blocking. |

## Required Blocking Revisions

Before another independent review, Architecture must provide a new exact,
hash-identified candidate that:

1. makes the literal PHP work path equal the single authorized path, proves its
   exact parent/type/mode, and gives individually named, fail-closed recovery for
   every possible work child and cleanup failure;
2. defines a coherent closed state at the cron transition—either an exact union
   or explicitly scoped manifests/verifiers—so all concurrently retained holding,
   cron, host-managed, marker, temp, and work paths have one unambiguous status;
3. makes cron execution and cleanup share a race-free exclusion/quiescence
   protocol, uses no-overwrite temp creation, and defines exact branches for
   enabled/job/marker/temp deletion failures before exact-empty is asserted;
4. preserves or embeds the exact canonical manifest bytes and timestamps needed
   for independent self-hash/schema reproduction, closes JSON escaping, and
   names the sole capability-evidence repository path;
5. disables proxy use explicitly, fixes redirect behavior, caps received provider
   bytes while discarding them, and proves the literal HTTPS host/status boundary
   without credential or response retention;
6. defines the exact authorized File Manager inventory/download/hash/mode/type
   proof operations without an alternate verifier, and verifies the probe's own
   resolved parent and directory mode; and
7. requires explicit human approval of the bound secret checkpoint, closes
   password-manager/browser cleanup, and covers partial panel-auth creation or
   disable failure without manual host-file deletion.

V5, v4, v3, all earlier plans/audits/evidence, package/release bytes, and unrelated
files must remain preserved. These findings do not authorize Red Team to repair
the candidate in place.

## Residual Risks And Mandatory Future Gates

Even after plan correction, a live preflight must still prove valid staging TLS,
panel Basic Auth before all content/error/method responses, PHP/runtime support,
File Manager byte/mode fidelity, filesystem primitives, no-proxy OpenAI TLS with
no credential, minimized access-log evidence, actual cron scheduling, race-free
cleanup, removal of panel auth files, and exact final inventory. Any ambiguity
must produce a capability FAIL, not a partial PASS.

The later deployment amendment remains mandatory for SSH/host keys, final manual
staging auth, exact Apache production/staging bytes, release manifests, atomic
publication, A/B and source-independent rollback, final cron, Git, provider
secret, canary, and production. Shared-host behavior, panel drift, browser
credential caching, log privacy, account compromise, and operator error remain
residual operational risks.

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
bytes were hashed in memory and were not materialized. The unrelated
`yakherd.mp4` was not read, hashed, moved, modified, staged, or otherwise touched.
The only write was this authorized v5 review record.

## Verdict And Exact Authority Effect

**Verdict: FAIL** for the exact v5 composite identified above.

This FAIL grants no v5 preflight authority. Architecture may draft a new exact
candidate and request fresh independent Red Team review. Implementation may not
receive or implement v5 as written and the unchanged v3 Section 9 write set
remains parked. No DreamHost panel/File Manager mutation, credential checkpoint
or creation, fixture materialization/upload, probe, cron, network access, SSH,
SFTP, release/deployment, Git action, provider secret, live model request, or
production action is authorized.

No previous v3 plan PASS, consumed hosting inventory, or partial v5 finding
overrides v5's own block (`v5:39-41`) or the requirement for a fresh independent
live capability PASS (`v5:321-332`).

autonomous next action: Architecture must issue a new exact candidate resolving every v5 P1/P2 finding; Implementation, DreamHost, Git, secrets, staging, and production remain parked.
