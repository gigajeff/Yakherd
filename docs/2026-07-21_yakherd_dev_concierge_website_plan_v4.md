# Yakherd.dev Concierge Website Plan v4 — DreamHost Staging Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact Composite Candidate

This amendment incorporates by hash the complete v3 plan at
`docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
`e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`.
V3 received plan-level PASS at
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v3.md`,
SHA-256
`559c07266a1744d824951572af94b9e26396fb5686486eb4e5a5a03081cca37a`.

The exact v4 candidate is the frozen v3 bytes plus this amendment. This file
changes only v3's staging access-control topology and cron wall-clock wording as
specified below. Every other v3 requirement, finite write path, package boundary,
test, authority gate, secret checkpoint, Git checkpoint, production checkpoint,
stop condition, and production release/rollback byte remains unchanged.

Implementation, further capability mutation, probe upload, access-control
credential creation, provider secret, live model use, staging deployment, Git,
and production remain blocked until this composite candidate receives a fresh
independent PASS.

## 2. Capability Evidence and Failed Assumption

The authorized Section 10 inventory is recorded at
`docs/audits/yakherd/2026-07-21_yakherd_dev_dreamhost_evidence.md`, SHA-256
`791ea693b00963c0a4fb8034b733d3da15d8bb5e36fc4c1b4ea6d8a320246fe4`.

Hosting configuration succeeded for `yakherd.dev` and
`staging.yakherd.dev` on the same new dedicated website user and Shared Unlimited
server. The selected roots are `$HOME/yakherd.dev/public` and
`$HOME/yakherd.dev/staging-public`; PHP 8.3 is selected. Certificate issuance was
pending. No probe, application, `.htaccess`, `.htpasswd`, SSH key, cron, API key,
or application secret was uploaded or created.

Official DreamHost evidence establishes that Shared hosting uses Apache. The
panel Htaccess/WebDAV protection tool creates server-owned `.htaccess` and
`.htpasswd` files inside the current web root, makes them uneditable, and
overwrites any existing `.htaccess`. That contradicts v3's assumption that
staging Basic Auth can be host-managed outside an immutable symlinked release.
The failure was detected before probe exposure.

V4 forbids the panel Htaccess/WebDAV tool for staging. It uses an exact,
transactional staging-only overlay assembled from—but never mutating—the
production release.

## 3. Replacement for v3 Section 10 Staging-Protection Gate

After v4 PASS, Architecture may resume only the non-provider capability gate. It
must first:

1. wait for and prove a valid automatically renewing Let's Encrypt certificate
   for `staging.yakherd.dev`;
2. enable Bash Shell/SSH access for the already dedicated website user in the
   panel, without displaying/resetting its password;
3. install a dedicated public SSH key through a panel-authenticated route or
   other reviewed method without exposing private-key bytes;
4. prove the exact resolved home/server/user and that both configured roots are
   under that home;
5. create `$HOME/.config/yakherd` mode `0700` and a staging-only bcrypt
   `.htpasswd` at `$HOME/.config/yakherd/staging.htpasswd`, mode `0600`, regular
   file, dedicated-user owned, non-symlinked, containing one randomly generated
   `yakherd-probe` login; and
6. create the temporary staging overlay in section 4, then prove unauthenticated
   HTTPS requests to `/`, a nonexistent path, and the probe return 401 before any
   content/error body, while an authenticated operator request succeeds.

The staging credential is an operational secret but is not an OpenAI/provider
secret. It is generated for this staging gate, entered only into the signed-in
browser/SSH flow, never committed, logged, included in evidence, placed in a
manifest, reused, or copied from an existing credential. Only presence,
algorithm/cost, owner/mode, and successful 401/authorized behavior are recorded.
If mode `0600` is not readable by Apache on this exact host, the gate fails; it
must not be loosened silently.

The temporary non-secret PHP probe may be uploaded only after the 401 gate is
proven. Every v3 Section 10 runtime, filesystem, egress, header, log, and deletion
test still applies. The probe is deleted immediately after evidence collection,
the overlay is reverified, and its target is returned to an empty protected
holding state. The provider endpoint is contacted only without authorization to
prove TLS connectivity; no OpenAI key or model request is permitted.

The DreamHost panel cron replaces v3's literal `03:17 UTC` wording. It runs once
daily at an exact recorded Pacific server time with locking; the pruning code
uses UTC dates internally. The capability evidence records current server
timezone and daylight-saving behavior. The retention contract remains current
UTC date plus the prior seven UTC dates regardless of the wall-clock run time,
and every POST still performs cleanup. An interval over 26 hours or an inability
to prove the daily panel job fails the gate.

## 4. Replacement for v3 Section 11 Staging Topology

The production release tree, retained production manifest, production
`$HOME/yakherd.dev/public` symlink, production deploy mapping, production
`.htaccess` bytes, activation, and rollback remain exactly v3. They never contain
staging authentication directives or hashes.

Staging uses:

- production source release:
  `$HOME/yakherd.dev/releases/<production_release_sha256>`;
- staging overlay root:
  `$HOME/yakherd.dev/staging-releases/<production_release_sha256>/<overlay_sha256>`;
- staging active symlink: `$HOME/yakherd.dev/staging-public`;
- staging next symlink: `$HOME/yakherd.dev/staging-public.next`;
- password file: `$HOME/.config/yakherd/staging.htpasswd`;
- staging overlay retained manifest:
  `private/staging-overlay-manifest.json`, mode `0444`.

The staging overlay builder obtains the stable deploy lock, creates a new empty
incoming directory under the exact staging-release parent, and copies every
production entry byte from the already verified production release. It verifies
all copied lengths/hashes against that release's retained
`private/release-manifest.json`. It never writes or links into the production
release and never uses the current source checkout as authority.

It rejects any production `.htaccess` containing `AuthType`, `AuthName`,
`AuthUserFile`, `Require valid-user`, `Satisfy`, or `Allow from`. It replaces only
the staging copy of `public/.htaccess` with these LF-only UTF-8 bytes followed
immediately by the exact production `.htaccess` bytes:

```apache
# Yakherd staging gate; never a production release byte
AuthType Basic
AuthName "Yakherd staging"
AuthUserFile <EXACT_RESOLVED_HOME>/.config/yakherd/staging.htpasswd
Require valid-user
ErrorDocument 401 default

<EXACT_PRODUCTION_HTACCESS_BYTES>
```

The two angle-bracketed items are builder notation, not literal deployed bytes.
`EXACT_RESOLVED_HOME` is the capability-proven absolute dedicated home with no
escaping, whitespace, symlink, or path traversal. The production suffix begins
at the byte immediately after the single blank line.

The canonical staging overlay manifest contains exactly:

- `schema_version`: `1`;
- `created_utc`;
- `production_release_sha256`;
- `production_manifest_sha256`;
- `auth_prefix_sha256` over the bytes through the single blank LF;
- `production_htaccess_sha256`;
- `combined_htaccess_sha256`;
- `overlay_sha256`;
- `entries`: every copied production entry with exact destination/hash/length,
  except `public/.htaccess`, whose row contains its combined hash/length and the
  two component hashes.

`overlay_sha256` uses the v3 zero-field self-hash rule. The directory name binds
both the production release and overlay hashes. The retained overlay manifest is
the only permitted extra metadata file and is not recursively listed as an
entry. It records no username, Basic Auth password/hash line, `.htpasswd` bytes,
or credential-derived value.

Before atomic staging activation, an independent verifier:

- reverifies the retained production manifest and every production entry;
- proves every staging entry except `.htaccess` is byte-identical to production;
- proves the combined `.htaccess` prefix/hash and byte-exact production suffix;
- proves `.htpasswd` safe metadata without reading or hashing its contents;
- rejects every missing/extra/symlink/special file and unsafe path;
- proves 401-before-content for `/`, `/api/health.php`, a 404, and the temporary
  probe, then proves authenticated expected behavior; and
- atomically renames `staging-public.next` over `staging-public` using the same
  capability-proven primitive and stable lock as production.

Staging A/B/rollback uses retained overlay manifests and is exercised after
removing access to the original A source and local manifest. Production rollback
continues to use only retained production manifests and never consumes a staging
overlay. A staging overlay can never be selected by the production deploy or
rollback script; path class and manifest schema mismatches fail closed.

The combined staging `.htaccess` is the only intentional staging/production byte
difference. Header, CSP, error, cache, PHP, privacy, model, accessibility, bundle,
and application tests still run against the exact copied production bytes; the
production suffix and subsequent production smoke tests prove the unoverlaid
Apache configuration. Any other delta returns to Architecture.

## 5. Authority Sequence

Fresh v4 Red Team PASS authorizes resuming only the capability actions in
sections 3 and 4. A complete capability PASS and probe-deletion evidence then
unparks the unchanged v3 Section 9 Implementation write set. Every later v3 gate
remains sequential and unchanged: Implementation evidence; independent diff
PASS; fresh Git approval; clean commit; non-provider staging tests; fresh
provider-secret approval; live canary; full staging acceptance; fresh production
approval; activation/rollback.

A failed certificate, Shell/key setup, `0600` Basic Auth read, overlay/hash/path
check, 401-before-content behavior, runtime/filesystem/header/egress/log/cron
probe, or deletion check blocks Implementation and requires another Architecture
decision. No partial capability result authorizes the next role.
