# Yakherd.dev Concierge Composite Plan v4 — Independent Red Team Review

- Review date: 2026-07-21
- Role: independent Red Team
- Candidate: frozen v3 plan plus the v4 DreamHost staging amendment
- Verdict: **FAIL**

## Reviewed Identity And Boundary

The reviewed composite is exactly:

- `docs/2026-07-21_yakherd_dev_concierge_website_plan_v4.md`, SHA-256
  `7d654f6aaf02c603c3b0f2136a887064b7a8b08e92b022545dfcf20e85183379`;
- incorporating frozen
  `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
  `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- with prior v3 plan PASS
  `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v3.md`,
  SHA-256
  `559c07266a1744d824951572af94b9e26396fb5686486eb4e5a5a03081cca37a`;
- and DreamHost evidence
  `docs/audits/yakherd/2026-07-21_yakherd_dev_dreamhost_evidence.md`, SHA-256
  `791ea693b00963c0a4fb8034b733d3da15d8bb5e36fc4c1b4ea6d8a320246fe4`.

The four supplied hashes match the bytes reviewed. Root `AGENTS.md` was also
reviewed at SHA-256
`0699b05f2630ef4cc8e9233ab7c766c17980fe55c85e0d52d2d77b033ace718b`,
and the package Red Team role prompt at SHA-256
`69a057321f05c27bca98f0e011478fd6fc7e1e5d7f603ad6f90602cb7891e3c0`.

The frozen v3 product-neutral package boundary, finite repository write set,
OpenAI/provider-secret checkpoint, Git checkpoint, production checkpoint, and
package/release exclusion were treated as incorporated requirements, not as
reopened authority. This review did not use the network or DreamHost.

## Prioritized Findings

### P0 — Critical

No P0 finding.

### P1 — High

#### P1-1 — The pre-Implementation capability sequence has no authorized overlay source

V4 records that no application, probe, or `.htaccess` byte exists on the host
(`v4:34-39`). It nevertheless requires the capability stage to create and test
the Section 4 overlay before uploading the probe (`v4:54-71`, `v4:81-86`). The
only permitted overlay builder source is an **already verified production
release** and its retained production manifest (`v4:103-120`). That release can
only be produced by the v3 Section 9 Implementation write set, but Implementation
is explicitly parked until the complete capability gate and probe deletion pass
(`v3:699-703`, `v4:187-195`).

This is a hard dependency cycle. The composite provides no finite, hash-bound
pre-Implementation holding release from which the capability overlay can be
built, while `v4:84-85` requires the target to return to an undefined “empty
protected holding state.” The exact sequence therefore cannot be executed as
written without inventing unreviewed remote bytes, changing the gate order, or
starting Implementation before it is authorized.

#### P1-2 — The temporary PHP probe is forbidden by the overlay's own closed manifest

The probe may be uploaded only after protection is proven and must then be tested
through the overlay (`v4:69-71`, `v4:81-84`, `v4:163-171`). However, the overlay
must contain every copied production entry, with the retained overlay manifest as
the sole extra metadata file, and its verifier rejects every extra path
(`v4:143-169`). The combined staging `.htaccess` is declared the only intentional
staging/production byte difference (`v4:181-185`). The frozen v3 deploy mapping
has no capability-probe entry (`v3:833-860`).

Consequently the probe cannot be present when `v4:170-171` tests it: adding it
makes the overlay invalid, while omitting it prevents the required PHP runtime,
filesystem, egress, log, and deletion evidence. The plan does not define a
separate protected probe namespace or a manifest transition that could resolve
this contradiction.

#### P1-3 — The Basic Auth prefix can be overridden by an accepted production suffix

V4 prepends `Require valid-user` and then appends the production `.htaccess`
bytes (`v4:122-141`). Its rejection set covers only six literal forms. It does
not reject or structurally isolate other Apache authorization directives. For
example, a production suffix containing top-level `Require all granted` passes
the stated rejection list; Apache treats multiple uncontained `Require`
directives as an implicit any-of authorization section, so the accepted suffix
can make the staging route public. Authorization containers, `AuthMerging`, and
case/spacing variants are likewise not bounded by the stated rule.

The four sample 401 probes in `v4:163-173` cannot establish that arbitrary
static, API, method, rewrite, error, and nested-path configurations remain
protected. This defeats the amendment's fail-closed staging premise even though
the `.htpasswd` itself is outside the web root and mode-gated. The same
literal-only rule is also insufficient to make production rejection of all
semantically equivalent overlay authentication artifacts unconditional.

#### P1-4 — The staging overlay is never transactionally finalized as an immutable release

The builder creates an empty incoming directory and copies/verifies production
entries (`v4:115-120`), but the amendment never defines the incoming name, writes
and verifies the retained overlay manifest as part of that transaction, fixes all
entry/directory modes, flushes the result, or atomically renames the complete
incoming tree to
`staging-releases/<production_release_sha256>/<overlay_sha256>`. It jumps from an
incoming directory to verifying “staging entries” and atomically replacing only
the active symlink (`v4:143-173`). It also does not state how
`staging-public.next` is created and proven to resolve to that immutable,
fully-verified final directory.

This omits the decisive publication boundary that v3 explicitly requires for a
production release (`v3:874-880`). A mutable/partial incoming tree can therefore
become, or be mistaken for, the activation target. The retained-manifest A/B and
source-independent rollback claims (`v4:175-179`) are not executable until the
overlay has a defined immutable finalization transaction.

#### P1-5 — PASS would authorize an open-ended SSH/key and credential mutation route

The capability stage permits installing a dedicated public key through a
“panel-authenticated route or other reviewed method” (`v4:59-68`), then grants
those actions immediately on v4 PASS (`v4:187-191`). It does not bind the exact
SSH account/key algorithm/public-key fingerprint, host-key verification, target
path, owner/modes, no-overwrite behavior, or the bytes/state the panel or the
unspecified alternative may change. “Other reviewed method” has no identified
review record or checkpoint.

The Basic Auth credential path is fixed, but its creation is not: there is no
minimum entropy, exact bcrypt cost, non-echo/non-argv generation and installation
flow, atomic create/replace rule, or pre-existing-file disposition. A password
entered in an SSH command argument or ordinary shell history would contradict
`v4:73-77` while still satisfying the described action. This is not a finite
write set or a sufficiently exact secret-handling procedure for authority that
would mutate the live hosting account.

### P2 — Medium

#### P2-1 — The retained overlay manifest is not specified precisely enough for independent reproduction

V4 lists top-level fields, but does not define whether
`production_manifest_sha256` is the SHA-256 of the retained manifest's exact
stored bytes or its zero-field release self-hash. Its `entries` rows are described
only as destination/hash/length (`v4:143-161`), omitting an exact object schema,
sort rule, destination class, mode, media type, and strict unknown-field rule.
The inherited v3 production manifest defines those details expressly
(`v3:833-872`).

The ambiguity permits two independent builders to produce different canonical
JSON or to accept different metadata while claiming the same overlay semantics.
It also weakens source-independent verification of permissions and path class.
The cryptographic fields are useful, but hashing an underspecified record does
not make its meaning independently reproducible.

#### P2-2 — Capability failure cleanup and rollback are not bounded

The amendment defines probe deletion on the success path (`v4:81-85`) and says a
failed capability blocks Implementation (`v4:197-200`). It does not define the
permitted and required cleanup/rollback for a partially enabled Shell account,
installed public key, partial or pre-existing `.htpasswd`, incoming overlay,
`staging-public.next`, failed active swap, or temporary capability artifacts.
There is no post-failure inventory proving which account and filesystem state
remains.

Blocking the next role is necessary, but it is not a transaction or recovery
contract for mutations already made. This omission also leaves the exact remote
write/delete authority indeterminate.

### P3 — Low / Observations

#### P3-1 — No secret value or machine-specific account identifier is present in the reviewed documents

The reviewed v4 amendment uses symbolic `$HOME` paths and does not record the
DreamHost username, server identifier, password, private key, bcrypt hash line,
API key, or application secret. `yakherd-probe` is a fixed role username, not a
secret or observed machine/account identifier. The DreamHost evidence expressly
redacts personal account identifiers (`DreamHost evidence:10-25`).

#### P3-2 — Several individual gates are appropriately fail-closed but do not cure the P1 findings

Certificate-before-credential testing, refusal to loosen `.htpasswd` from mode
`0600`, provider egress without authorization, UTC application retention,
Pacific cron/DST evidence, the 26-hour ceiling, separate staging release paths,
and production schema/path rejection are all directionally sound
(`v4:57-94`, `v4:98-113`, `v4:175-185`). DreamHost evidence supports Apache,
manual Basic Auth, Shell conversion, seven-day access-log retention, Pacific
cron time, and per-subdomain Let's Encrypt in principle
(`DreamHost evidence:27-50`). It explicitly does not yet prove the runtime,
filesystem, authentication, symlink, log, cron, TLS, or deletion behavior
(`DreamHost evidence:73-93`).

## Required Blocking Revisions

Before another Red Team review, Architecture must provide a new exact candidate
that:

1. removes the capability/Implementation dependency cycle by defining the exact,
   finite, hash-bound source and lifecycle of every pre-Implementation holding and
   probe byte;
2. makes the probe compatible with a closed manifest and states the exact
   401-before-upload, upload, authenticated-test, deletion, and post-deletion
   verification sequence;
3. makes the Basic Auth requirement non-overridable by the production suffix and
   defines semantic, case/spacing-safe rejection of every staging-auth artifact
   from production;
4. specifies the complete overlay build, canonical manifest, mode, verification,
   incoming-to-immutable-final rename, next-symlink, activation, A/B rollback, and
   source-independent recovery transactions;
5. replaces the open-ended SSH method with an exact, fingerprint-bound,
   host-authenticated, finite write/state transition and defines a non-echo,
   non-argv, atomic, strength-bounded bcrypt credential procedure; and
6. enumerates success and failure cleanup, rollback, retained state, and evidence
   for every authorized live-host mutation.

V1, v2, v3, v4, all prior audits/evidence, and package/release bytes must remain
preserved. A revision is a new candidate and requires a fresh independent review;
these findings do not authorize Red Team to repair the plan in place.

## Residual Risks

Even after the blocking revisions, live capability evidence must still prove the
certificate, Apache authorization phase and error behavior, `0600` readability,
SSH host/account binding, restrictive modes, `flock`, same-filesystem atomic
rename, symlink isolation, PHP/runtime limits, outbound TLS without credentials,
actual log fields/retention, cron interval/DST behavior, probe deletion, and
source-independent A/B rollback. Shared-host configuration drift, account
compromise, access-log privacy, DST/provider changes, and operator credential
handling remain residual operational risks rather than facts established by this
document review.

## Validation And Preservation

Required documentation-only validation after writing this audit:

- `python scripts\verify_release.py`: PASS, exit `0`;
  `release_verification status=passed manifest_files=47 cache_paths=0`.
- `git diff --check`: PASS, exit `0`, no output.

Repository state at review completion: branch `main`, HEAD
`97b470f8342cfba619da8f13bd224b2c6c4e2e2a`, upstream `origin/main`,
ahead/behind `0/0`, no staged path, and no tracked diff. The pre-existing plan,
audit, evidence, beginner guide, and `yakherd.mp4` paths remain untracked. Their
status was not changed. Protected plan/audit/evidence hashes remain the values
recorded above and in the preserved v3 audit; package `MANIFEST.json` remains
`ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`
and package `RELEASE.json` remains
`312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`.

No package/release byte, existing plan/audit/evidence byte, DreamHost state,
secret, Git state, or website implementation byte was changed. The unrelated
`yakherd.mp4` was not read, hashed, moved, modified, staged, or otherwise touched.
The only write was this authorized v4 review record.

## Verdict And Authority Effect

**Verdict: FAIL** for the exact v4 composite identified above.

This FAIL grants **no next-stage authority**. Architecture may draft a new,
hash-identified candidate and request fresh independent Red Team review.
Implementation may not receive or implement v4 as written. No further DreamHost
or network mutation is authorized: do not enable Shell, install an SSH key,
create or transfer a staging credential, create an overlay, upload/run a probe,
configure cron, deploy staging, create/transfer a provider secret, make a live
model call, or activate production. Git branch creation, staging, commit, push,
PR, publication, package/release mutation, and unrelated-file action also remain
unauthorized.

The prior v3 PASS remains a preserved historical record; it does not override
v4's own block (`v4:23-26`) or the DreamHost evidence's failed vhost-auth
assumption and instruction to return to Architecture (`DreamHost
evidence:85-93`). No partial finding or previously consumed inventory authority
unparks the capability probe or Implementation.

autonomous next action: Architecture must issue a new exact candidate resolving every P1/P2 finding; Implementation and all further DreamHost actions remain parked.
