# Yakherd.dev Concierge Website Plan v5 — Pre-Implementation Capability Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite candidate

This amendment incorporates the complete frozen v3 plan at
`docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
`e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`.
V3's plan-level PASS remains recorded at
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v3.md`,
SHA-256
`559c07266a1744d824951572af94b9e26396fb5686486eb4e5a5a03081cca37a`.

V4 and its review are preserved historical records but are not incorporated as
authority:

- v4 plan SHA-256:
  `7d654f6aaf02c603c3b0f2136a887064b7a8b08e92b022545dfcf20e85183379`;
- v4 FAIL audit SHA-256:
  `e2abae3cf21dd1754d4f93afdd84051389ed53d3aca757ea697d318a3c3a42b5`.

The exact v5 composite is the frozen v3 bytes plus this amendment. This file
replaces v3 Sections 10, 11, and 12 only where stated. Every other v3 product,
privacy, model, security, accessibility, package boundary, finite Section 9
repository write path, secret restriction, test, and stop condition remains
unchanged.

V5 deliberately withdraws the v4 staging-overlay design. It separates a small,
disposable pre-Implementation capability fixture from the future website
release. Final SSH access, release upload, staging protection, immutable release
publication, A/B rollback, production rollback, cron installation, and
production activation require a later, exact, hash-bound deployment amendment
after the real Implementation bytes exist. No v5 PASS can authorize those later
actions.

Until v5 receives a fresh independent PASS, no further DreamHost mutation,
fixture upload, credential entry, cron entry, Implementation, Git operation,
provider secret, staging deployment, or production action is authorized.

## 2. Preserved hosting baseline

The read-only and already-consumed hosting setup evidence is preserved at
`docs/audits/yakherd/2026-07-21_yakherd_dev_dreamhost_evidence.md`, SHA-256
`791ea693b00963c0a4fb8034b733d3da15d8bb5e36fc4c1b4ea6d8a320246fe4`.

The intended retained baseline is:

- `yakherd.dev` and `staging.yakherd.dev` are hosted by the same dedicated
  website user on the selected Shared Unlimited server;
- roots are `$HOME/yakherd.dev/public` and
  `$HOME/yakherd.dev/staging-public`;
- PHP 8.3 is selected;
- the production and staging certificate requests are allowed to complete; and
- no application, probe, `.htaccess`, `.htpasswd`, SSH key, cron entry, provider
  key, or application secret has been installed.

These hosting and certificate records are retained on both success and failure.
V5 does not authorize changing the dedicated user, server, PHP version, domain,
root, DNS, or production root.

## 3. Exact v5 authority boundary

A fresh v5 PASS authorizes Architecture to perform only the disposable
preflight in Sections 4–9 through the already signed-in DreamHost panel and its
File Manager. It does not authorize Shell/SSH enablement, an SSH key, SFTP, a
manual `.htpasswd`, the v4 overlay, a website release, a provider credential,
Git, or production.

The preflight exists only to establish facts needed before asking Implementation
to write website bytes:

- staging certificate validity;
- PHP 8.3 and required extensions/functions;
- same-filesystem file mode, lock, flush, symlink, realpath, and rename support;
- outbound TLS to the OpenAI API without a credential;
- Apache child `.htaccess`, headers, custom 404, and panel-managed Basic Auth;
- bounded request behavior and non-secret access-log fields;
- the panel's cron scheduler and PHP 8.3 CLI path; and
- exact cleanup of every disposable operator file and panel job.

Final symlink following, manual staging authentication, production-equivalent
Apache configuration, immutable releases, deploy locking, retained manifests,
A/B rollback, final cron, SSH host authentication, and secret installation are
not facts this disposable fixture can prove. They move to the mandatory later
deployment amendment in Section 10.

## 4. Closed preflight write and state set

Architecture must first wait for a valid certificate for
`staging.yakherd.dev`, then inspect the staging root without changing it. The
root must contain no operator path. If any unknown or pre-existing path exists,
Architecture stops without overwriting or deleting it and returns to review.

The only host-managed state v5 permits is DreamHost panel Htaccess/WebDAV
protection applied to the exact staging root. The panel is known to create
server-owned root `.htaccess` and `.htpasswd` files and to overwrite a root
`.htaccess`. Therefore protection is enabled before any operator path exists,
no operator root `.htaccess` is ever created, and the tool is never used on the
production root or on a website release. The host-managed files are operational
authentication state, not fixture source. Their names, regular-file type,
owner-class, mode, creation/removal time, and panel-enabled state are recorded;
the `.htpasswd` contents, length, hash, and credential-derived values are never
read or recorded.

The complete operator-created remote path set is:

- `$HOME/yakherd.dev/staging-public/fixture/`, mode `0755`;
- `$HOME/yakherd.dev/staging-public/fixture/.htaccess`, mode `0444`;
- `$HOME/yakherd.dev/staging-public/fixture/index.html`, mode `0444`;
- `$HOME/yakherd.dev/staging-public/fixture/404.html`, mode `0444`;
- `$HOME/yakherd.dev/staging-public/fixture/capability.php`, mode `0444`, only
  during probe state;
- `$HOME/yakherd.dev/.capability-cron/`, mode `0700`;
- `$HOME/yakherd.dev/.capability-cron/cron.php`, mode `0500`;
- `$HOME/yakherd.dev/.capability-cron/enabled`, zero bytes, mode `0600`;
- `$HOME/yakherd.dev/.capability-cron/marker.txt`, mode `0600`, created only by
  the exact cron program; and
- `$HOME/yakherd.dev/.capability-cron/.marker.tmp-<decimal-pid>`, mode `0600`,
  created only transiently by the exact cron program and renamed or deleted in
  the same invocation.

The PHP web probe may also create only:

- `$HOME/yakherd.dev/.yakherd-capability-work/`, mode `0700`;
- its exact children `first.bin`, `second.bin`, and `link.bin` as specified by
  Appendix A.

It must remove those children and the directory in the same request. A
pre-existing work path causes a failed check and is never touched.

No wildcard, recursive upload, recursive delete, alternate path, symlinked
parent, overwrite of an existing operator path, or unlisted panel setting is
authorized. Resolved staging and site paths must remain beneath the capability-
proven dedicated home. File Manager must preserve the Appendix A LF-only UTF-8
bytes and exact modes; inability to prove that is a gate failure, not authority
to adapt the bytes.

## 5. Exact source bytes and canonical state manifests

Appendix A is the sole source authority for every operator-supplied preflight
file. Each fenced block denotes the exact UTF-8 bytes between the opening and
closing fence, with LF line endings and one final LF. The empty `enabled` file
has zero bytes. Before upload, Architecture materializes the blocks in an
operating-system temporary directory outside the repository and verifies:

| destination | bytes | SHA-256 |
| --- | ---: | --- |
| `fixture/.htaccess` | 354 | `3d78af579472accd7a9dcd88b8e3dd32b29ebaea8ec523e92d4d40dc18f7ac4c` |
| `fixture/index.html` | 129 | `eb3210806694aa07c2688a05901b6454ba61460ec99908832343a410856d8c15` |
| `fixture/404.html` | 95 | `a197e91834a3427a9321720a342903799b814132842796eb204e7fe915efdf4d` |
| `fixture/capability.php` | 4164 | `7df26e841c1fed7d9b17e2ee9719caee01d681547eeaee33590bc05b52acdd5f` |
| `.capability-cron/cron.php` | 489 | `9a26887f281ba1ebbce2bbe9b6a8c493e72bc5646c431495322af28f24f84c3b` |
| `.capability-cron/enabled` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Architecture creates a separate local canonical manifest for each state. A
manifest is UTF-8 canonical JSON: one object; keys sorted by Unicode code point;
no insignificant whitespace; JSON booleans/null only where explicitly allowed;
integers only; no floats; duplicate or unknown keys rejected; no BOM; no final
newline. Its object has exactly:

- `schema_version`: integer `1`;
- `fixture_version`: integer `1`;
- `state`: exactly `holding`, `probe`, or `cron`;
- `created_utc`: RFC 3339 UTC with whole seconds and `Z`;
- `state_sha256`: 64 lowercase hex characters; and
- `entries`: an array sorted by UTF-8 destination path bytes.

Each entry has exactly `source_name`, `destination_class`, `destination_path`,
`sha256`, `byte_length`, `mode`, and `media_type`. `destination_class` is exactly
`staging_public` or `site_private`. Paths are relative POSIX paths without an
empty, dot, dot-dot, backslash, control, absolute, or percent-encoded segment.
`mode` is a four-character string from the modes in Section 4. The media-type
mapping is exact: `.htaccess` uses `text/plain; charset=utf-8`; both HTML files
use `text/html; charset=utf-8`; both PHP files use
`application/x-httpd-php`; and `enabled` uses `application/octet-stream`.
`source_name` and `destination_path` are the exact relative destinations in the
Section 5 table and Appendix headings, except the cron paths have the literal
`.capability-cron/` prefix.
`state_sha256` is SHA-256 of the canonical manifest after replacing only that
field with 64 lowercase zeroes.

The `holding` manifest contains exactly the three fixture `.htaccess`, HTML, and
404 rows. The `probe` manifest contains those same rows plus
`capability.php`. The `cron` manifest contains exactly `cron.php` and `enabled`.
The host-managed root authentication files, runtime-created marker/temp files,
and web-probe work paths are governed state from Section 4 and are never
misrepresented as Appendix A source entries.

For every transition, a local verifier first verifies the Appendix source hash,
the strict manifest/self-hash, and the exact expected entry set. After upload it
verifies each remote operator path's regular-file type, owner-class, mode,
length, and SHA-256 and rejects any extra operator path. The manifest itself is
never uploaded. Evidence records its self-hash and the remote file hashes, not
personal account identifiers.

## 6. Authentication and credential procedure

Panel-managed protection is disposable preflight state, not the final staging
design. The exact procedure is:

1. Confirm the valid staging certificate and empty-root inventory.
2. Present a narrow human secret checkpoint stating that DreamHost will create
   one temporary Basic Auth credential for the staging preflight only.
3. The human uses a browser/password-manager generator to create a new,
   non-reused password with at least 128 bits of generated entropy and fills the
   panel's masked password and confirmation controls. The fixed non-secret login
   name is `yakherd-preflight`. The assistant never receives, displays, copies,
   logs, places in a URI, command argument, environment variable, repository,
   evidence file, or tool transcript the password or password-derived value.
4. Enable the panel protection only for the exact staging root. Do not select
   WebDAV, production, another directory, or another user.
5. Prove unauthenticated HTTPS requests to `/`, `/fixture/`, and a random
   nonexistent path return `401` before any operator file is uploaded. Then the
   human enters the credential only in the browser's masked Basic Auth prompt;
   the signed-in browser session is used for the remaining authenticated tests.

No SSH, shell history, argv, clipboard transfer, manual bcrypt file, assistant-
generated secret, reused credential, or alternate installation method is
allowed. If the panel cannot meet the entropy, masking, exact-root, or cleanup
contract, the gate fails. The final staging credential algorithm, cost, path,
and lifecycle remain unchosen and must be reviewed in the later deployment
amendment.

## 7. Closed transition and test sequence

The order is mandatory:

1. **Protected-empty:** complete Section 6 and verify `401` on `/`,
   `/fixture/`, a random 404, and both GET and POST to
   `/fixture/capability.php`. None may contain the holding marker, custom 404
   text, probe JSON, PHP source, a path, or an environment value.
2. **Holding:** create only `fixture/`, upload the three `holding` files, set
   modes, and verify the holding manifest. Unauthenticated requests to the same
   paths still return `401`. Authenticated `/fixture/` returns the exact holding
   marker; authenticated missing content returns the exact custom 404 with
   status `404`; both have `X-Yakherd-Capability: v1`, `Referrer-Policy:
   no-referrer`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and
   `Cache-Control: no-store, max-age=0`. Directory listing is denied.
3. **Probe:** upload only `capability.php`, set mode, and verify the probe
   manifest. Unauthenticated GET and POST remain `401` without probe output.
   Authenticated GET returns `405`; a POST with any body other than exact
   `{"run":true}` returns `400`; the exact 12-byte body returns `200` only when
   every Appendix A boolean passes and the unauthenticated OpenAI request returns
   `401`. The call sends no `Authorization`, cookie, user idea, or personal data,
   uses HTTPS-only cURL with peer/host verification, and discards the provider
   body. No other host is contacted.
4. **Post-probe holding:** delete only `capability.php`, prove it is absent, and
   reverify the original holding manifest and authenticated/unauthenticated
   behavior. A partial or undeletable probe blocks the gate.
5. **Cron:** create the private cron directory and two Appendix files, set modes,
   and verify the cron manifest. In the panel create exactly one job named
   `yakherd-capability-preflight` using the literal PHP binary
   `/usr/local/php83/bin/php` and the capability-proven absolute path
   `<EXACT_RESOLVED_HOME>/yakherd.dev/.capability-cron/cron.php`, with no shell,
   variable, interpolation, redirection, argument, or second command. The angle
   brackets are builder notation; the panel receives the verified absolute path,
   which contains no whitespace or shell metacharacter. Schedule it every ten
   minutes. If that exact interval or command form is unavailable, stop. Within
   twenty-six minutes, require a regular non-symlink
   `marker.txt`, mode `0600`, containing one syntactically valid UTC whole-second
   timestamp and one LF. Record the panel server timezone/DST display and marker
   UTC time, not the home/user value.
6. **Logs and limits:** inspect only staging access-log rows caused by the test.
   Record redacted timestamps, methods, paths, statuses, and the documented
   retention/control facts. Prove request bodies, Basic Auth password,
   `Authorization`, cookies, and probe result JSON are absent. Do not copy
   unrelated rows, IP addresses, user agents, referrers, usernames, or existing
   account data. A provider response body is never retained. Confirm the probe's
   33-byte read ceiling and 10-second outbound timeout execute as designed.
7. **Cleanup:** execute Section 8 completely and prove final state before any
   capability PASS is recorded.

The probe is never publicly reachable without Basic Auth. Its JSON contains only
fixed check names, booleans, and the unauthenticated provider HTTP status. It
does not emit PHP configuration values, file paths, environment variables,
server/account identifiers, response bodies, credentials, file contents, or
source.

## 8. Exact success and failure recovery

Cleanup uses only individually named paths; recursive deletion is forbidden.
The retained hosting baseline in Section 2 is not rolled back.

Once panel protection is enabled, it remains enabled until every operator web
file is removed and absence is verified. On success or any later failure:

1. If the cron job exists, delete `enabled` first and prove it absent so any
   concurrent or undeleted job becomes a no-op.
2. Delete the exact panel cron job and confirm it is absent before deleting
   `marker.txt`, `.marker.tmp-<observed-decimal-pid>` if present, `cron.php`,
   and the now-empty `.capability-cron` directory, in that order. Unknown
   temp/PID paths are not deleted; they block and are reported.
3. Delete `capability.php` if present, then `404.html`, `index.html`, the child
   `.htaccess`, and the empty `fixture` directory, verifying each exact path is
   absent.
4. Through the same panel route, disable protection for the exact staging root.
   Confirm the panel reports disabled and the two host-managed root files are
   absent. Do not manually delete or change their ownership/modes.
5. Reinventory the staging root and exact private paths. Final preflight state is
   no operator path, no panel-auth file, no cron job, no cron marker/temp/lock,
   no web-probe work path, and the untouched hosting baseline.

If panel-job removal fails, keep `enabled` absent and retain `cron.php` as an
inert exact Appendix file; keep staging auth enabled, report the retained named
paths, and block Implementation. If an operator web path cannot be removed,
keep staging auth enabled, do not disable it, record only its redacted relative
path/hash, and block. If disabling panel protection fails after operator cleanup,
leave the host-managed files untouched and block. If an unknown path or symlink
appears, touch nothing further at that path, keep protection enabled when
possible, and return to Architecture. No failure authorizes SSH, broader delete,
permission loosening, or a replacement method.

The capability evidence must enumerate every authorized mutation as created,
removed, retained-baseline, or failed-retained; include all three manifest
self-hashes and Appendix file hashes; and assert the final inventory. Only a
complete final empty-state proof is a capability PASS.

## 9. Capability PASS and Implementation authority

After cleanup, Architecture writes one redacted capability evidence document,
runs `python scripts/verify_release.py` and `git diff --check`, and sends the
exact evidence/hash back for independent Red Team review. Architecture does not
self-certify the live probe.

Only a fresh independent capability PASS may unpark the unchanged v3 Section 9
Implementation write set. The task sent to the existing IMPLEMENTATION task is
limited to those exact paths, local tests, local manifest generation, and the
implementation evidence path. It has no DreamHost, network, secret, Git,
staging, or production authority.

## 10. Mandatory post-Implementation deployment amendment

V3 Sections 11 and 12 are suspended after local implementation review and before
any Git or hosting deployment action. Once Implementation produces exact bytes
and an independent implementation-diff PASS, Architecture must create a new
candidate binding at least:

- the exact reviewed source commit candidate and deploy manifest bytes/hash;
- the exact production and staging Apache bytes, with staging authentication
  generated independently rather than prepended to an arbitrary production
  suffix, and a closed grammar/hash proof that no authorization directive can
  override it;
- unconditional case/spacing/semantic rejection of every staging-only auth
  artifact by production build, deploy, verification, promotion, and rollback;
- the exact remote source-to-destination map, owner/modes, incoming names,
  manifest schemas, canonical serialization/self-hash, fsync boundaries,
  incoming-to-immutable-final atomic rename, next-symlink creation, activation,
  A/B rollback, and source-independent recovery;
- the exact DreamHost account/server binding in a machine-local non-public
  operator record; Ed25519 public-key fingerprint; independently authenticated
  server host-key fingerprints; `known_hosts` path/mode; `authorized_keys`
  no-overwrite/owner/mode transition; and a finite rollback for Shell/key state;
- the final staging credential generator, at least 128 bits of entropy, exact
  password-hash algorithm/cost, masked non-echo/non-argv input, atomic exclusive
  file creation/replacement, owner/mode/path, rotation, deletion, and failure
  disposition;
- the final cron command, lock, timezone/DST behavior, UTC cleanup semantics,
  monitoring, disable path, and rollback;
- per-step success/failure inventories and individually named cleanup/retained
  state for upload, verification, activation, rollback, key, credential, cron,
  staging, and production; and
- separate user checkpoints for Git, provider secret, and production.

That future candidate requires a fresh independent Red Team PASS before Shell,
SSH key installation, Git staging/commit/push, release upload, staging
credential, staging deployment, provider secret, live model request, or
production. V5 grants none of those actions and makes no claim that the rejected
v4 overlay is reusable.

## 11. Resolution of v4 findings

- **P1-1:** the capability source is now the literal Appendix A fixture, not a
  nonexistent production release; the fixture is fully removed before
  Implementation.
- **P1-2:** holding and probe are two explicit closed manifest states; probe
  upload, verification, deletion, and reversion are ordered.
- **P1-3:** the disposable fixture has panel-owned root auth with no production
  suffix; final production-equivalent staging auth is withheld for an exact
  post-Implementation design/review.
- **P1-4:** v4 overlay publication is withdrawn. The future immutable release
  transaction is expressly blocked pending a byte-bound amendment.
- **P1-5:** v5 authorizes no SSH/key/manual password file. The only transient
  credential uses the exact panel route plus a masked human/password-manager
  step and has exact cleanup.
- **P2-1:** v4's overlay manifest is withdrawn. V5's disposable state manifest
  has an exact schema, canonicalization, row shape, sort rule, modes, path
classes, unknown-field rejection, and self-hash.
- **P2-2:** Sections 2 and 8 define retained baseline, ordered cleanup, inert
  failure state, inventory, and stop behavior for every v5 mutation.

## Appendix A — exact disposable fixture sources

### `fixture/.htaccess`

```apache
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /fixture/404.html
<IfModule mod_headers.c>
Header always set X-Yakherd-Capability "v1"
Header always set Referrer-Policy "no-referrer"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "DENY"
Header always set Cache-Control "no-store, max-age=0"
</IfModule>
```

### `fixture/index.html`

```html
<!doctype html><html lang="en"><meta charset="utf-8"><title>Yakherd capability holding</title><p>Yakherd capability holding.</p>
```

### `fixture/404.html`

```html
<!doctype html><html lang="en"><meta charset="utf-8"><title>Not found</title><p>Not found.</p>
```

### `fixture/capability.php`

```php
<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=UTF-8');
header('Cache-Control: no-store, max-age=0');
header('Pragma: no-cache');
header("Content-Security-Policy: default-src 'none'; base-uri 'none'; frame-ancestors 'none'");
header('Referrer-Policy: no-referrer');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo '{"ok":false,"error":"method"}';
    exit;
}

$body = file_get_contents('php://input', false, null, 0, 33);
if ($body !== '{"run":true}') {
    http_response_code(400);
    echo '{"ok":false,"error":"body"}';
    exit;
}

$extensions = ['curl', 'json', 'openssl', 'hash', 'filter'];
$functions = ['flock', 'symlink', 'rename', 'realpath', 'fsync'];
$result = [
    'php_83' => version_compare(PHP_VERSION, '8.3.0', '>='),
    'extensions' => [],
    'functions' => [],
    'filesystem' => false,
    'cleanup' => false,
    'openai_tls_unauthenticated' => false,
    'openai_http_status' => 0,
];

foreach ($extensions as $name) {
    $result['extensions'][$name] = extension_loaded($name);
}
foreach ($functions as $name) {
    $result['functions'][$name] = function_exists($name);
}

$work = dirname(__DIR__) . '/.yakherd-capability-work';
$first = $work . '/first.bin';
$second = $work . '/second.bin';
$link = $work . '/link.bin';
$handle = null;

if (!file_exists($work) && !is_link($work) && mkdir($work, 0700, false)) {
    try {
        $handle = fopen($first, 'x+b');
        if ($handle !== false && chmod($first, 0600) && flock($handle, LOCK_EX | LOCK_NB)) {
            $wrote = fwrite($handle, "yakherd-capability\n") === 19;
            $flushed = fflush($handle);
            $synced = function_exists('fsync') && fsync($handle);
            $unlocked = flock($handle, LOCK_UN);
            fclose($handle);
            $handle = null;
            $renamed = $wrote && $flushed && $synced && $unlocked && rename($first, $second);
            $linked = $renamed && symlink('second.bin', $link) && is_link($link);
            $resolved = $linked ? realpath($link) : false;
            clearstatcache(true, $second);
            $mode = file_exists($second) ? (fileperms($second) & 0777) : -1;
            $result['filesystem'] = $linked && $resolved === realpath($second) && $mode === 0600;
        }
    } finally {
        if (is_resource($handle)) {
            fclose($handle);
        }
        $ok = true;
        foreach ([$link, $first, $second] as $path) {
            if ((file_exists($path) || is_link($path)) && !unlink($path)) {
                $ok = false;
            }
        }
        if (is_dir($work) && !rmdir($work)) {
            $ok = false;
        }
        $result['cleanup'] = $ok && !file_exists($work) && !is_link($work);
    }
}

if (extension_loaded('curl')) {
    $ch = curl_init('https://api.openai.com/v1/responses');
    if ($ch !== false) {
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => '{}',
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_RETURNTRANSFER => false,
            CURLOPT_WRITEFUNCTION => static fn($curl, string $data): int => strlen($data),
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_PROTOCOLS => CURLPROTO_HTTPS,
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_SSL_VERIFYHOST => 2,
        ]);
        $curlOk = curl_exec($ch) !== false;
        $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
        $result['openai_http_status'] = $status;
        $result['openai_tls_unauthenticated'] = $curlOk && $status === 401;
    }
}

$all = $result['php_83'] && $result['filesystem'] && $result['cleanup']
    && $result['openai_tls_unauthenticated'];
foreach ($result['extensions'] as $passed) {
    $all = $all && $passed;
}
foreach ($result['functions'] as $passed) {
    $all = $all && $passed;
}
$result['ok'] = $all;
http_response_code($all ? 200 : 503);
echo json_encode($result, JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
```

### `.capability-cron/cron.php`

```php
<?php
declare(strict_types=1);

$root = __DIR__;
$enabled = $root . '/enabled';
$marker = $root . '/marker.txt';
$temporary = $root . '/.marker.tmp-' . getmypid();

if (!is_file($enabled) || is_link($enabled)) {
    exit(0);
}

$bytes = gmdate('Y-m-d\\TH:i:s\\Z') . "\n";
if (file_put_contents($temporary, $bytes, LOCK_EX) !== strlen($bytes)) {
    @unlink($temporary);
    exit(1);
}
if (!chmod($temporary, 0600) || !rename($temporary, $marker)) {
    @unlink($temporary);
    exit(1);
}
```

### `.capability-cron/enabled`

This file has exactly zero bytes.
