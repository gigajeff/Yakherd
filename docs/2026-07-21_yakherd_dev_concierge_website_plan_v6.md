# Yakherd.dev Concierge Website Plan v6 — Closed Preflight Correction

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v6 candidate is:

1. frozen v3 plan
   `docs/2026-07-21_yakherd_dev_concierge_website_plan_v3.md`, SHA-256
   `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
2. v5 preflight amendment
   `docs/2026-07-21_yakherd_dev_concierge_website_plan_v5.md`, SHA-256
   `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
3. this v6 correction.

The v5 FAIL audit is preserved at
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v5.md`,
SHA-256
`53e4e3b8cab1c75877450020124ab06833d7ec7d892d30ea406b395ce5dc0a48`.

This file supersedes every v5 cron-preflight statement, the v5
`capability.php` bytes/hash, v5 manifest/evidence serialization wording, v5
File Manager proof wording, v5 work-path recovery, and v5 human/panel lifecycle
where specified below. V5 otherwise remains incorporated. Frozen v3 remains
unchanged except where v5 and v6 expressly suspend its hosting/deployment order.

V6 removes cron from the disposable preflight; it does not try to repair a
concurrent scheduler in a test that does not need one. The final cron is still a
mandatory part of the post-Implementation, byte-bound deployment amendment.

No further DreamHost action, fixture materialization/upload, credential action,
Implementation, Git, provider secret, staging deployment, or production is
authorized until this exact composite receives a fresh independent PASS.

## 2. Replacement authority and state machine

A v6 PASS authorizes only the panel/File-Manager disposable preflight described
by incorporated v5 as corrected here. It authorizes no cron entry or cron file,
no Shell/SSH/SFTP/key, no manual password file, no website release, no Git, no
provider credential, and no production action.

The complete quiescent remote state is a tuple with three independently bounded
classes:

- **panel-auth class:** either `absent` (neither host-managed root file) or
  `enabled` (exactly regular root `.htaccess` and `.htpasswd`, created/owned by
  the DreamHost panel); their contents are outside operator source and the
  `.htpasswd` is never read or hashed;
- **fixture class:** `absent`, `holding`, or `probe`, verified only within exact
  subtree `$HOME/yakherd.dev/staging-public/fixture`; and
- **work class:** `absent` at every quiescent boundary; it may contain only the
  exact runtime paths in Section 4 while the authenticated probe request is
  executing.

The only successful sequence is:

`(enabled, absent, absent)` → `(enabled, holding, absent)` →
`(enabled, probe, absent)` → `(enabled, holding, absent)` →
`(enabled, absent, absent)` → `(absent, absent, absent)`.

The cron state, cron manifest, cron Appendix sources, `.capability-cron`
directory, `enabled`, marker, temp, lock, panel job, ten-minute schedule, and all
v5 cron cleanup steps are deleted from authority. Their v5 literal bytes are
historical candidate text and must not be materialized.

## 3. Exact fixture and manifest bytes

The incorporated v5 `.htaccess`, `index.html`, and `404.html` Appendix blocks
remain the exact source bytes and retain their advertised lengths/hashes. The
v5 PHP block and hash are replaced by Appendix A of this file:

- destination: `fixture/capability.php`;
- byte length: `5632`;
- SHA-256:
  `70feca907ce39312667d3924c5def589344d944cd06c6187fc7dbcce51727f10`;
- mode: `0444`;
- media type: `application/x-httpd-php`.

Only two local manifests exist: `holding` and `probe`. `holding` contains exactly
the incorporated three fixture rows. `probe` contains those same rows plus the
replacement PHP row. Verifiers are scoped to the exact fixture subtree and
reject every extra/missing path there. The independent panel-auth and work
classes are verified separately under Section 2; they are not silently ignored
manifest extras.

The manifest schema and zero-field self-hash remain v5 except canonical
serialization is replaced by this exact rule:

- every string must contain only printable ASCII bytes `0x20` through `0x7e`
  and must contain no quote (`0x22`), reverse solidus (`0x5c`), or solidus escape;
- the serializer rejects a string that would require JSON escaping;
- object keys are emitted in ascending raw ASCII byte order;
- arrays retain schema order, with entries sorted by raw ASCII
  `destination_path` bytes;
- integers are base-10 ASCII with no sign or leading zero, except integer zero;
- output uses literal `{`, `}`, `[`, `]`, `:`, and `,`, no whitespace, no BOM,
  and no terminal newline;
- UTF-8 encoding is therefore byte-identical to ASCII for every permitted
  manifest; and
- `state_sha256` is computed after replacing exactly its value with 64 ASCII
  zeroes and serializing under these rules.

`source_name`, path, class, hash, mode, media type, state, and timestamp values
all satisfy this restricted alphabet. A slash is always the literal byte `0x2f`;
`\/` is rejected. The strict parser rejects duplicate/unknown keys, unknown
fields, floats, negative integers, booleans/null, invalid UTF-8, alternate
escapes, alternate key/entry order, whitespace, BOM, or a final newline.

Immediately before each upload transition, Architecture generates that state's
manifest once and does not rewrite its `created_utc`. The sole capability
evidence file is:

`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`.

For both states, that evidence embeds:

- the state name, `created_utc`, exact byte length, lowercase SHA-256, and
  `state_sha256`;
- the exact canonical manifest bytes encoded as standard RFC 4648 base64 with
  padding and no line wrapping; and
- a decoded, human-readable field/entry table.

The independent capability reviewer must base64-decode the preserved bytes,
verify byte length/SHA-256, strict-parse, reproduce canonical bytes and the
zero-field self-hash, then compare all embedded rows with the Appendix source
hashes and redacted live evidence. A hash without its base64 preimage is a
capability FAIL.

## 4. Exact PHP path, runtime, and recovery

The replacement probe binds its path without emitting it. With
`capability.php` at `staging-public/fixture/`, it proves real paths and exact
basenames for `fixture`, `staging-public`, and `yakherd.dev`, then uses only
`dirname(__DIR__, 2) . '/.yakherd-capability-work'`.

The only runtime paths are:

- `$HOME/yakherd.dev/.yakherd-capability-work`, a real directory mode `0700`;
- regular `first.bin` and `second.bin`, mode `0600`; and
- symlink `link.bin` whose literal target is `second.bin`.

The program refuses a pre-existing work path, exclusively creates `first.bin`,
checks lock/write/flush/fsync/rename/symlink/realpath/modes, and attempts exact
cleanup in `finally`. `path_binding`, `filesystem`, and `cleanup` must all be
true for HTTP `200`.

After every probe invocation, Architecture uses the exact File Manager proof
operations in Section 6 to require the work class is absent. If the program
reports failed cleanup or any work path remains, keep panel auth enabled and
perform only this bounded recovery:

1. Inspect the exact work directory and its hidden entries without following a
   symlink. The directory itself must be a non-symlink directory, dedicated-user
   owned, mode `0700`, with no child other than `first.bin`, `second.bin`, or
   `link.bin`.
2. `link.bin`, if present, must be a symlink with literal target `second.bin`;
   delete that link only.
3. `first.bin` or `second.bin`, if present, must be a non-symlink regular file,
   dedicated-user owned, mode `0600`, byte length `19`, and SHA-256 of literal
   `yakherd-capability` plus LF
   `feb9228339c4d4ce5ef36577560781a0c38ec3e34c0ba37d75d26e33f6bb9be7`;
   delete each verified exact file only.
4. Remove the verified empty work directory and prove the path is absent.

If any owner, type, mode, target, length, hash, or child differs—or File Manager
cannot prove it—touch nothing at that work path, retain panel protection, record
only redacted relative names/booleans, and fail the capability. Panel auth is
never disabled while a work path remains.

## 5. Replacement direct-egress proof

Appendix A fixes the only URL to
`https://api.openai.com/v1/responses`, sends `{}` without `Authorization`,
cookie, idea, or personal data, and requires expected status `401`. It:

- permits only HTTPS and verifies peer and host;
- sets cURL proxy to the empty string and no-proxy to `*`, overriding configured
  proxy environment/system state;
- disables redirect following and permits zero redirects;
- requires the effective URL remain byte-identical to the fixed URL;
- caps connect time at five seconds and total time at ten seconds; and
- counts but never retains response-body chunks, aborting the transfer if the
  cumulative body would exceed `4096` bytes.

`openai_direct_bounded` and `openai_tls_unauthenticated` must both be true. A
write-abort, proxy, redirect, changed effective URL, TLS failure, timeout,
response over 4096 bytes, or status other than `401` fails closed. The JSON emits
only fixed check labels, booleans, and the status integer; it never emits body
bytes, URL changes, DNS/IP, proxy data, paths, or configuration values.

This proves only the shared host's narrow direct unauthenticated TLS capability.
The final relay still requires its v3 request/response bounds and later staging
tests; no provider credential or live model request is authorized.

## 6. Exact panel and File Manager proof route

No alternate remote verifier is permitted. Architecture must use only these
operations in the already signed-in DreamHost panel/File Manager:

1. Open the dedicated website user's File Manager from the staging-host setup
   screen without copying, recording, or exposing its credential-bearing URI.
2. Enable the File Manager's hidden-file display. Use its breadcrumb and file
   details/properties views to record redacted containment booleans, item names,
   regular/directory/symlink type, symlink target where required, owner-class,
   mode, and length. If any field is unavailable, stop; do not use a shell,
   script, alternate client, or guessed value.
   `$HOME/yakherd.dev` and its `staging-public` child must each be a real,
   non-symlink directory, dedicated-user owned, mode `0755`; the staging root
   must contain no path before panel auth. A mismatch fails without chmod or
   ownership repair.
3. Before every create/upload, refresh and prove the exact destination is absent
   and its parent has the expected type/owner/mode. Use only File Manager's
   create-directory, individual-file upload, rename, permissions, individual-
   file download, individual-file delete, and empty-directory delete controls.
   No overwrite, archive upload/extract, recursive action, bulk action, editor,
   WebDAV, or alternate root is allowed.
4. After setting modes, download each operator-supplied remote file individually
   into a new operating-system temporary directory outside the repository. Hash
   and length-check the downloaded bytes locally against Section 3, then delete
   only those local downloads and their known temporary directory. Do not
   download either host-managed auth file, any log, or any unrelated remote
   path.
5. The authenticated probe's `path_binding` boolean independently proves the
   resolved runtime parent chain. Both the File Manager containment facts and
   `path_binding=true` are required; neither substitutes for the other.

Evidence records UTC action times, redacted relative paths, operation class,
type/owner/mode/length booleans, and expected/observed SHA-256. It never records
the File Manager URI, dedicated username/home/server, credential, unrelated
path, or auth-file content.

## 7. Replacement human and panel-auth lifecycle

Before panel mutation, present a checkpoint bound to all of these facts:

- exact target `staging.yakherd.dev` and its staging root, never production;
- fixed non-secret login `yakherd-preflight`;
- exactly one new, non-reused, password-manager-generated credential with at
  least 128 bits of entropy;
- assistant never sees/transfers the password or derived value;
- DreamHost will create opaque root auth files; and
- cleanup deletes the temporary password-manager record, disables panel auth,
  verifies both host files absent, closes all staging-origin tabs, and restarts
  the in-app browser to clear Basic Auth session state.

The human must answer an explicit affirmative question. Silence, a general past
authorization, or merely being signed in is not approval for this secret step.
If approved, the human fills only the panel's masked password/confirmation
controls and later the browser's native masked Basic Auth prompt.

After the enable submission—whether it reports success, failure, timeout, or an
ambiguous state—Architecture immediately inspects both the panel status and the
hidden staging-root inventory:

- `enabled + both regular host-managed files` is the sole continue state;
- `disabled + neither file` is a clean failed/no-change state;
- any one-file, mixed, unknown, or contradictory state triggers exactly one
  panel **disable** attempt for that same root, followed by reinventory; and
- if disable cannot prove `disabled + neither file`, do not manually edit/delete
  host files, retain the partial state, clear the human/browser credential state
  as far as possible, record redacted facts, and fail the capability.

On normal cleanup, first reach `(enabled, absent, absent)`, then disable through
the same panel control and require `(absent, absent, absent)`. The human deletes
the temporary password-manager item and affirmatively confirms deletion.
Architecture closes every staging-origin tab and restarts the in-app browser;
after restart it opens a fresh staging request and confirms no cached Basic Auth
credential is sent and panel protection remains disabled. If restart/session
clearing or password-record deletion cannot be confirmed, capability fails even
when remote files are gone.

## 8. Corrected test, cleanup, and evidence sequence

The incorporated v5 protected-empty, holding, probe, post-probe holding, log,
and response tests remain, with these replacements:

1. There is no cron transition or test.
2. The exact POST body is 12 bytes; Appendix A reads at most 33 bytes. A valid
   `200` requires `php_83`, every required extension/function, `path_binding`,
   `filesystem`, `cleanup`, `openai_direct_bounded`,
   `openai_tls_unauthenticated`, and overall `ok` all true.
3. Work absence is verified after the request; Section 4 recovery runs on a
   known cleanup failure. Any unknown work state remains protected and blocks.
4. After probe deletion, reverify the preserved `holding` manifest bytes and
   state. Then delete only `404.html`, `index.html`, child `.htaccess`, and the
   empty `fixture` directory; verify fixture and work classes absent.
5. Perform the Section 7 panel/browser/password-manager cleanup last.

The exact evidence path from Section 3 records:

- both preserved manifest preimages and independent-verification fields;
- Appendix hashes and all local-download comparisons;
- the full authorized mutation ledger with created, verified, removed,
  retained-baseline, partial-panel, failed-retained, and final state;
- redacted HTTP statuses/header booleans/probe booleans/log-field booleans;
- explicit no-cron/no-SSH/no-Git/no-secret/no-website-deploy assertions; and
- final `(absent, absent, absent)` state, browser restart, and human credential-
  record deletion confirmation.

Architecture then runs `python scripts/verify_release.py` and
`git diff --check` and routes the exact evidence/hash to independent Red Team.
Only a fresh capability PASS may unpark the unchanged v3 Section 9 local write
set in the existing IMPLEMENTATION task. Implementation receives no DreamHost,
network, credential, Git, staging, or production authority.

## 9. V5 finding closure

- **P1-1:** the literal probe uses the declared private site sibling, proves
  parent binding/mode, and has exact known-artifact recovery.
- **P1-2/P1-3:** cron and every cron state/path/race are removed from this gate
  and remain blocked for the future deployment review.
- **P1-4:** exact manifest bytes and timestamps are preserved as base64 at one
  named evidence path for independent reproduction.
- **P1-5:** proxy and redirects are explicitly disabled, effective URL is fixed,
  provider response bytes are counted/capped without retention, and time/TLS/
  status remain bounded.
- **P2-1:** manifest strings cannot contain escapable characters; literal slash,
  exact ASCII serialization, ordering, and rejection rules close byte identity.
- **P2-2:** panel/File Manager inventory, details, individual download/hash,
  mode/type, containment, temporary-local cleanup, and evidence path are finite.
- **P2-3:** the checkpoint requires an explicit yes and includes every partial
  enable/disable branch plus password-manager and browser-session cleanup.
- **P2-4:** the probe chmods and verifies the work directory, explicitly fixes
  redirect/proxy behavior, caps egress bytes, and makes no unprovable no-shell
  cron claim.

## Appendix A — replacement `fixture/capability.php`

The exact bytes are UTF-8 without BOM, LF-only, with one final LF.

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
    'path_binding' => false,
    'filesystem' => false,
    'cleanup' => false,
    'openai_tls_unauthenticated' => false,
    'openai_direct_bounded' => false,
    'openai_http_status' => 0,
];

foreach ($extensions as $name) {
    $result['extensions'][$name] = extension_loaded($name);
}
foreach ($functions as $name) {
    $result['functions'][$name] = function_exists($name);
}

$fixtureRoot = realpath(__DIR__);
$stagingRoot = realpath(dirname(__DIR__));
$siteRoot = realpath(dirname(__DIR__, 2));
$result['path_binding'] = $fixtureRoot !== false && $stagingRoot !== false && $siteRoot !== false
    && dirname($fixtureRoot) === $stagingRoot
    && dirname($stagingRoot) === $siteRoot
    && basename($fixtureRoot) === 'fixture'
    && basename($stagingRoot) === 'staging-public'
    && basename($siteRoot) === 'yakherd.dev';
$work = ($siteRoot === false ? '' : $siteRoot) . '/.yakherd-capability-work';
$first = $work . '/first.bin';
$second = $work . '/second.bin';
$link = $work . '/link.bin';
$handle = null;

if ($result['path_binding'] && !file_exists($work) && !is_link($work)
    && mkdir($work, 0700, false) && chmod($work, 0700)) {
    try {
        clearstatcache(true, $work);
        $workMode = fileperms($work) & 0777;
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
            $result['filesystem'] = $workMode === 0700 && $linked
                && $resolved === realpath($second) && $mode === 0600;
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
    $received = 0;
    $ch = curl_init('https://api.openai.com/v1/responses');
    if ($ch !== false) {
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => '{}',
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_RETURNTRANSFER => false,
            CURLOPT_WRITEFUNCTION => static function ($curl, string $data) use (&$received): int {
                $length = strlen($data);
                if ($received + $length > 4096) {
                    return 0;
                }
                $received += $length;
                return $length;
            },
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_PROTOCOLS => CURLPROTO_HTTPS,
            CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_MAXREDIRS => 0,
            CURLOPT_PROXY => '',
            CURLOPT_NOPROXY => '*',
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_SSL_VERIFYHOST => 2,
        ]);
        $curlOk = curl_exec($ch) !== false;
        $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $effective = (string) curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
        $redirects = (int) curl_getinfo($ch, CURLINFO_REDIRECT_COUNT);
        curl_close($ch);
        $result['openai_http_status'] = $status;
        $result['openai_direct_bounded'] = $curlOk && $received <= 4096
            && $effective === 'https://api.openai.com/v1/responses' && $redirects === 0;
        $result['openai_tls_unauthenticated'] = $result['openai_direct_bounded'] && $status === 401;
    }
}

$all = $result['php_83'] && $result['path_binding'] && $result['filesystem'] && $result['cleanup']
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
