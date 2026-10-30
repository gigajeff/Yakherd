# Yakherd.dev Concierge Website Plan v8 — Exhaustive Failure Evidence Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v8 candidate is frozen v3 plus incorporated v5, v6, v7, and this
amendment. Their identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v7 FAIL audit:
  `635f87c89b541200c1bdfd6de29854815ffcc516540ca7e7a760899011c2062c`.

V8 replaces v7 Appendix A and PHP identity, replaces the entire v7
`failure_state` schema, and replaces the Error Logs observation route. V7's
credential one-attempt/no-retry lifecycle and removal of cached-Authorization
inspection remain. V6's manifests, private work recovery, File Manager route,
and withheld deployment authority remain. Every cron action remains removed.

No DreamHost, credential, fixture, network, Implementation, Git, cron, SSH,
staging release, provider-secret, or production action is authorized until this
exact composite receives a fresh independent PASS.

## 2. Replacement PHP identity and bootstrap

V7 Appendix A is replaced by Appendix A here:

- destination `fixture/capability.php`;
- byte length `7279`;
- SHA-256
  `34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`;
- mode `0444`, `application/x-httpd-php`, LF-only UTF-8 without BOM, one final
  LF.

Bootstrap now performs only three suppressed, non-path operations before the
generic runtime boundary: request-local `display_errors=0`, request-local
`log_errors=0`, and `ob_start`. It captures all three results. If either
configuration call or buffer start fails, it performs no path, cURL, provider,
JSON, header-derived, or credential work; it emits only the fixed generic body
and exits. The `@` operators suppress bootstrap warnings while no handler exists;
the calls contain no machine-specific operand. If buffer start succeeds, all v7
shutdown, warning-to-exception, catch, buffer-discard, and generic response rules
apply.

`error_channel_contained` equals the conjunction of all three captured bootstrap
results and is required for HTTP `200`. A normal result cannot self-attest output
containment without a successfully installed buffer. V7's strict cURL option
success/short-circuit and every incorporated direct-egress/filesystem control
remain unchanged.

## 3. Replacement exhaustive failure schema

Every started preflight that does not achieve capability PASS embeds exactly one
`failure_state`. A human declining the credential checkpoint is not a started
attempt and creates no remote/client credential state.

The top-level object has exactly:

- `schema_version`: integer `1`;
- `capability_result`: literal `FAIL`;
- `failed_checks`: a nonempty array of unique check IDs, sorted by raw ASCII;
- `failure_classes`: an array of unique retained-state class IDs, sorted by raw
  ASCII; it may be empty for a completely cleaned failure;
- `panel_inventory`: one exact enum from below;
- `fixture_inventory`: the exact object in Section 3.2;
- `work_inventory`: the exact object in Section 3.3;
- `password_record_deleted`, `staging_tabs_closed`, and `browser_restarted`:
  booleans;
- `cleanup_utc`: RFC 3339 whole-second UTC or null; and
- `notes_present`: boolean only; no free-form note exists inside the object.

Unknown/missing keys, duplicate/unknown enum values, unsorted arrays, or a blank
`failed_checks` array are rejected.

### 3.1 Finite check and retained-state IDs

`failed_checks` may contain only:

- `ACCESS_LOG_OBSERVATION`, `ACCESS_LOG_PRIVACY`;
- `AUTH_BEFORE_UPLOAD`;
- `BROWSER_RESTART`;
- `CERTIFICATE`;
- `CURL_OPTIONS`;
- `CUSTOM_404`, `DIRECTORY_LISTING`, `HTTP_HEADERS`, `HTTP_STATUS`;
- `ERROR_CHANNEL`, `ERROR_LOG_OBSERVATION`, `ERROR_LOG_ZERO`;
- `FILE_MANAGER_OBSERVABILITY`, `FILE_MANAGER_TRANSFER`;
- `FINAL_INVENTORY`;
- `FILESYSTEM_PRIMITIVES`;
- `FIXTURE_CLEANUP`;
- `HOLDING_HTTP`, `HOLDING_MANIFEST`, `HOLDING_REMOTE_BYTES`;
- `LOCAL_VALIDATION`, `MANIFEST_EVIDENCE`;
- `OPENAI_DIRECT_BOUNDARY`, `OPENAI_STATUS`, `OPENAI_TLS`;
- `PANEL_DISABLE`, `PANEL_ENABLE`;
- `PASSWORD_RECORD_DELETE`;
- `PATH_BINDING`;
- `PHP_BOOTSTRAP`, `PHP_EXTENSIONS`, `PHP_FUNCTIONS`, `PHP_RUNTIME`,
  `PHP_VERSION`;
- `POST_PROBE_HOLDING`;
- `PROBE_JSON`, `PROBE_MANIFEST`, `PROBE_METHOD_BODY`, `PROBE_REMOTE_BYTES`;
- `PROVIDER_RESPONSE_BOUND`;
- `ROOT_INVENTORY`;
- `STAGING_TABS_CLOSE`;
- `WORK_CLEANUP`.

These IDs exhaust every required v5/v6/v7/v8 preflight gate. A clean
`openai_options_installed=false` uses `CURL_OPTIONS`; an unexpected `401`/TLS/
bound condition uses the corresponding OpenAI/provider ID; a caught generic
runtime failure uses `PHP_RUNTIME`; a missing extension/function uses its exact
PHP ID; a normal disable failure uses `PANEL_DISABLE`; and tab close failure uses
`STAGING_TABS_CLOSE`. Multiple failed gates list every applicable ID.

`failure_classes` may contain only `PANEL_STATE_RETAINED`,
`FIXTURE_STATE_RETAINED`, `WORK_STATE_RETAINED`,
`CLIENT_STATE_INCOMPLETE`, or `LOG_EVIDENCE_INCOMPLETE`. It describes retained
or unobservable state, not the reason a check failed. A clean, fully cleaned
failure has an empty array and remains truthful because `failed_checks` is
nonempty.

`panel_inventory` is exactly `NONE`, `BOTH_ENABLED`, `HTACCESS_ONLY`,
`HTPASSWD_ONLY`, `BOTH_STATUS_MISMATCH`, or `UNKNOWN`. A normal disable failure
with both files is `BOTH_ENABLED`, includes `PANEL_DISABLE`, and includes
`PANEL_STATE_RETAINED`.

### 3.2 Exact fixture inventory

`fixture_inventory` has exactly `state`, `unknown_entry_present`, and `entries`.
`state` is `ABSENT`, `EXPECTED_SUBSET`, or `UNKNOWN`; the boolean
`unknown_entry_present` is true only when the UI reports an extra entry whose
name/content is deliberately not captured.

`entries` always has five rows, sorted in this exact order:
`fixture`, `fixture/.htaccess`, `fixture/404.html`,
`fixture/capability.php`, `fixture/index.html`. Each row has exactly:

- `path`: that exact enum;
- `presence`: boolean;
- `type`: `ABSENT`, `DIRECTORY`, `REGULAR`, `SYMLINK`, `OTHER`, or `UNKNOWN`;
- `mode`: `NOT_APPLICABLE`, `UNKNOWN`, `OTHER`, `0444`, or `0755`;
- `byte_length`: nonnegative integer or null; and
- `sha256_match`: boolean or null.

Absent rows use `type=ABSENT`, `mode=NOT_APPLICABLE`, and both nullable fields
null. Directory/nonregular rows use null hash. Known regular source files use
observed length and a boolean hash match. Unknown extra names never enter the
object.

### 3.3 Exact work inventory

`work_inventory` has exactly `state`, `unknown_child_present`, `directory`, and
`children`. `state` is `ABSENT`, `KNOWN_RECOVERABLE`, `KNOWN_RETAINED`, or
`UNKNOWN_RETAINED`.

`directory` has exactly `presence`, `type`, `mode`, and `owner_match`.
`presence`/`owner_match` are booleans or `owner_match` is null when absent or
unobservable. `type` is `ABSENT`, `DIRECTORY`, `SYMLINK`, `OTHER`, or `UNKNOWN`.
`mode` is `NOT_APPLICABLE`, `0700`, `OTHER`, or `UNKNOWN`.

`children` always has exactly three rows sorted `first.bin`, `link.bin`,
`second.bin`. Each row has exactly `path`, `presence`, `type`, `mode`,
`byte_length`, `sha256_match`, and `target_match`. Types are `ABSENT`, `REGULAR`,
`SYMLINK`, `OTHER`, or `UNKNOWN`; modes are `NOT_APPLICABLE`, `0600`, `OTHER`,
or `UNKNOWN`. The nullable length/hash fields apply only to regular files;
`target_match` is boolean only for a symlink and null otherwise. Unknown child
names set `unknown_child_present=true` and are not captured.

### 3.4 Exact serialization and embedding

The object uses v6's strict ASCII/no-escape canonical JSON rules, extended only
to emit booleans as literal `true`/`false` and null as literal `null`. It has no
self-hash. At the sole capability evidence path, a heading exactly
`Failure state (canonical JSON)` is followed by the canonical byte length,
lowercase SHA-256, unwrapped padded RFC 4648 base64 preimage, and one decoded
field table. The independent reviewer must decode, hash, strict-parse, and
compare it to the mutation ledger. Free-form failure prose may appear elsewhere
only with redacted non-machine-specific facts; it is not part of the object.

## 4. Replacement Error Logs observation

Before any Error Logs query, Architecture inspects only the view-mode controls
and help text. It must establish one of these secret-safe channels:

1. a panel aggregate/count-only or redacted-results mode that guarantees no row
   body, filesystem path, message, source, IP, agent, referrer, credential, or
   other row field will render; or
2. a human-only zero/nonzero observation. For this channel, Architecture yields
   the browser without taking a snapshot or reading DOM/network state. The human
   applies the reviewed hostname/time/fixed-path filter, does not copy/open a
   row, navigates away from results, and reports only `zero` or `nonzero`.

If neither channel is confirmed before query, no query is submitted;
`ERROR_LOG_OBSERVATION` fails and `LOG_EVIDENCE_INCOMPLETE` is recorded. If the
human does not answer exactly `zero`, or aggregate count is nonzero,
`ERROR_LOG_ZERO` fails. Row-rendering mode is never queried by Architecture; row
text may not enter the browser-tool transcript or evidence.

The incorporated v7 UTC window, fixed path, retention/no-delete disposition,
access-log separation, and zero-row PASS requirement remain. The initial human
credential checkpoint discloses that a later human-only zero/nonzero log check
may be required; each human action still requires an explicit answer.

## 5. Corrected evidence and authority

The sole capability evidence path remains
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`. It includes
the exact manifest preimages, Appendix hash, result booleans, mutation ledger,
access/error-log booleans, success tuple or canonical failure object, and client
cleanup booleans. A failed attempt is evidence for FAIL only and never authorizes
a retry or Implementation.

Only a complete successful sequence, validated exact evidence, and a later fresh
independent capability PASS can unpark the unchanged v3 Section 9 local write set
in the existing IMPLEMENTATION task. Every DreamHost deployment, cron, SSH, Git,
staging release, provider secret, live model request, and production action
remains blocked.

## 6. V7 finding closure

- **P1-1:** finite `failed_checks` represents every clean gate failure;
  `failure_classes` separately represents retained state and may be empty.
- **P2-1:** fixture/work objects, every nested row/key/type/enum/null rule, and
  canonical evidence embedding are exact.
- **P2-2:** display/log suppression and buffer-start results are captured before
  work, generic bootstrap failure does nothing sensitive, and buffer success is
  required by `error_channel_contained` and HTTP `200`.
- **P2-3:** count-only/redacted capability is required before an Architecture
  query; otherwise only a human-returned zero/nonzero boolean is allowed, with no
  tool snapshot or row text.

## Appendix A — replacement `fixture/capability.php`

```php
<?php
declare(strict_types=1);

$displayOff = @ini_set('display_errors', '0') !== false;
$logOff = @ini_set('log_errors', '0') !== false;
$bufferStarted = $displayOff && $logOff && @ob_start();
if (!$bufferStarted) {
    http_response_code(500);
    echo '{"ok":false,"error":"runtime"}';
    exit;
}
$GLOBALS['yakherd_completed'] = false;
register_shutdown_function(static function (): void {
    if (($GLOBALS['yakherd_completed'] ?? false) === true) {
        return;
    }
    while (ob_get_level() > 0) {
        ob_end_clean();
    }
    if (!headers_sent()) {
        header('Content-Type: application/json; charset=UTF-8');
        header('Cache-Control: no-store, max-age=0');
    }
    http_response_code(500);
    echo '{"ok":false,"error":"runtime"}';
});
set_error_handler(static function (int $severity, string $message, string $file, int $line): never {
    throw new ErrorException('runtime', 0, $severity);
});

function yakherdRespond(int $status, string $body): never
{
    while (ob_get_level() > 0) {
        ob_end_clean();
    }
    http_response_code($status);
    header('Content-Type: application/json; charset=UTF-8');
    header('Cache-Control: no-store, max-age=0');
    header('Pragma: no-cache');
    header("Content-Security-Policy: default-src 'none'; base-uri 'none'; frame-ancestors 'none'");
    header('Referrer-Policy: no-referrer');
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: DENY');
    $GLOBALS['yakherd_completed'] = true;
    restore_error_handler();
    echo $body;
    exit;
}

try {
    error_reporting(E_ALL);

    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        yakherdRespond(405, '{"ok":false,"error":"method"}');
    }

    $body = file_get_contents('php://input', false, null, 0, 33);
    if ($body !== '{"run":true}') {
        yakherdRespond(400, '{"ok":false,"error":"body"}');
    }

$extensions = ['curl', 'json', 'openssl', 'hash', 'filter'];
$functions = ['flock', 'symlink', 'rename', 'realpath', 'fsync'];
$result = [
    'php_83' => version_compare(PHP_VERSION, '8.3.0', '>='),
    'extensions' => [],
    'functions' => [],
    'error_channel_contained' => $displayOff && $logOff && $bufferStarted,
    'path_binding' => false,
    'filesystem' => false,
    'cleanup' => false,
    'openai_tls_unauthenticated' => false,
    'openai_direct_bounded' => false,
    'openai_options_installed' => false,
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
        $optionsInstalled = curl_setopt_array($ch, [
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
        $result['openai_options_installed'] = $optionsInstalled;
        $curlOk = $optionsInstalled && curl_exec($ch) !== false;
        $status = $optionsInstalled ? (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE) : 0;
        $effective = $optionsInstalled ? (string) curl_getinfo($ch, CURLINFO_EFFECTIVE_URL) : '';
        $redirects = $optionsInstalled ? (int) curl_getinfo($ch, CURLINFO_REDIRECT_COUNT) : -1;
        curl_close($ch);
        $result['openai_http_status'] = $status;
        $result['openai_direct_bounded'] = $optionsInstalled && $curlOk && $received <= 4096
            && $effective === 'https://api.openai.com/v1/responses' && $redirects === 0;
        $result['openai_tls_unauthenticated'] = $result['openai_direct_bounded'] && $status === 401;
    }
}

$all = $result['php_83'] && $result['error_channel_contained']
    && $result['path_binding'] && $result['filesystem'] && $result['cleanup']
    && $result['openai_tls_unauthenticated'];
foreach ($result['extensions'] as $passed) {
    $all = $all && $passed;
}
foreach ($result['functions'] as $passed) {
    $all = $all && $passed;
}
$result['ok'] = $all;
yakherdRespond(
    $all ? 200 : 503,
    json_encode($result, JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR)
);
} catch (Throwable $error) {
    yakherdRespond(500, '{"ok":false,"error":"runtime"}');
}
```
