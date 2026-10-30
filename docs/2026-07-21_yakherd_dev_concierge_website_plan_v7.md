# Yakherd.dev Concierge Website Plan v7 — Fail-Closed Runtime Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v7 candidate is frozen v3 plus incorporated v5 plus v6 plus this
amendment:

- v3 SHA-256:
  `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5 SHA-256:
  `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6 SHA-256:
  `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v6 FAIL audit SHA-256:
  `fcd340de3a67298d2dff0b36926225993941c0a6f863ab32e56b0d773f3f9b25`.

This file replaces v6 Appendix A and its PHP length/hash, scopes v6's successful
state tuple, adds a closed failure-state schema, replaces every clean/partial
panel failure branch, replaces the Basic Auth cache assertion, and adds the
bounded PHP error-channel proof. All other v6 corrections remain incorporated.
V6 continues to remove every v5 cron action and to withhold deployment authority.

No DreamHost, credential, fixture, network, Implementation, Git, staging
release, provider-secret, cron, SSH, or production action is authorized until a
fresh independent PASS on this exact composite.

## 2. Replacement PHP identity and fail-closed runtime

V6 Appendix A is replaced by Appendix A here:

- destination: `fixture/capability.php`;
- byte length: `7131`;
- SHA-256:
  `7cdefa7718f84da1fc3266f9dea62b795724a49ff9c4b7b089e5a52249c2545e`;
- mode `0444`, media type `application/x-httpd-php`, LF-only UTF-8 without BOM,
  one final LF.

Before any filesystem, cURL, header, or JSON work, the program starts an output
buffer, installs a generic shutdown response, installs a warning-to-exception
handler that discards the original message/file/line, and requires successful
request-local `display_errors=0` and `log_errors=0`. Every throwable reaches a
single generic `500` JSON body. Output buffers are discarded before every
response. No throwable/message/trace/source/path/configuration/provider body is
displayed or passed to PHP's default logger.

Normal results include `error_channel_contained=true` only after those controls
succeed. A normal `200` also requires that boolean. The generic error body is
exactly `{"ok":false,"error":"runtime"}` and contains no varying value.

The replacement records the return of `curl_setopt_array` as
`openai_options_installed`. It never calls `curl_exec` unless that return is
strictly true. A false return or exception/unsupported option produces either a
bounded `503` with `openai_options_installed=false` or the generic `500`; neither
can attest direct egress. A `200` requires `openai_options_installed`,
`openai_direct_bounded`, `openai_tls_unauthenticated`, and overall `ok` true.

The incorporated v6 URL, proxy, redirect, TLS, timeout, effective-URL,
4096-response-byte, provider-body-discard, private-path, filesystem, mode, and
cleanup requirements remain unchanged.

## 3. Successful and failed state schemas

V6 Section 2's three-class tuple is expressly the **successful quiescent state
machine only**. It is complete only when no failure has occurred. It must not be
used to describe retained failure.

Every failed attempt has a separate evidence object `failure_state` with exactly:

- `schema_version`: integer `1`;
- `capability_result`: literal `FAIL`;
- `failure_classes`: a nonempty sorted array drawn only from
  `panel_clean_enable_failure`, `panel_recovered_partial`,
  `panel_retained_partial`, `fixture_retained_known`,
  `fixture_retained_unknown`, `work_retained_known`,
  `work_retained_unknown`, `php_error_row`, `php_error_log_unobservable`,
  `password_record_cleanup_unconfirmed`, and
  `browser_restart_unconfirmed`;
- `panel_inventory`: exactly one of `none`, `both_enabled`, `htaccess_only`,
  `htpasswd_only`, `both_status_mismatch`, or `unknown`;
- `fixture_inventory`: an array containing only redacted relative names from
  `.htaccess`, `index.html`, `404.html`, and `capability.php`, with safe
  type/mode/length/hash booleans but no unknown path content;
- `work_inventory`: `absent`, `known_recoverable`, `known_retained`, or
  `unknown_retained`, plus only the exact safe metadata permitted by v6;
- `password_record_deleted`: boolean;
- `staging_tabs_closed`: boolean;
- `browser_restarted`: boolean; and
- `cleanup_utc`: RFC 3339 whole-second UTC or null when cleanup cannot finish.

Unknown/extra fields or enum values are rejected. Multiple failure classes may
coexist. Any `failure_state` makes capability FAIL permanently for that attempt,
is embedded in the sole v6 capability evidence path, and grants no retry,
Implementation, or next-stage authority. A new attempt requires a new
Architecture decision and fresh human credential approval after the previous
client state is cleaned.

Known retained fixture/work paths remain subject to v6's exact type/mode/hash
recovery rules. Unknown or mismatched paths are not touched and remain protected.
Host-managed auth bytes are never manually edited/deleted/read/hashed.

## 4. Complete one-attempt credential lifecycle

One affirmative v6 human checkpoint authorizes exactly one panel-enable
submission and one temporary credential. There is no automatic retry.

Every possible result executes client cleanup, including success, timeout,
panel error, `disabled + neither file`, partial state later recovered by the one
allowed disable attempt, and unresolved partial state:

1. Do not submit enable again.
2. Complete or attempt the exact remote disable/inventory branch already allowed
   by v6; never manually touch host files.
3. The human deletes the temporary password-manager record and explicitly
   confirms deletion.
4. Architecture closes every staging-origin tab and restarts the in-app browser.
5. Record the three client cleanup booleans in success evidence or the exact
   `failure_state`.

`disabled + neither file` immediately after enable is
`panel_clean_enable_failure`; it receives full client cleanup and FAIL, not a
retry. A mixed/ambiguous state that reaches `disabled + neither file` after the
single disable attempt is `panel_recovered_partial`; it receives full client
cleanup and FAIL, not a retry. An unresolved mixed state is
`panel_retained_partial`; it remains protected when possible, receives full
client cleanup as far as observable, and fails.

V6's statement that a fresh request proves no cached Basic `Authorization` was
sent is removed. V7 authorizes no credential/header/network-inspector
observation and makes no claim about a derived header. The only client cache-
clearing evidence is: all staging tabs closed, the in-app browser restart action
completed, and the human confirmed password-record deletion. Failure to confirm
any action is a typed failure class. No post-disable staging request is made for
cache inspection.

## 5. Bounded PHP error-channel evidence

The incorporated access-log inspection remains read-only. V7 adds one finite
error-log proof through the signed-in DreamHost Website Logs/Error Logs panel;
no File Manager log download, shell, alternate client, or broad log export is
authorized.

Immediately before the first authenticated probe request, Architecture records
UTC `error_window_start`. Immediately after the last probe response and work
inventory, it records `error_window_end`. Through the staging hostname's Error
Logs view, it restricts the view to that interval and searches only for the fixed
non-secret request path `/fixture/capability.php` and its timestamps. It records
only:

- whether the error-log view and interval/filter controls were available;
- count zero/nonzero, never a copied row;
- whether any row matched the fixed path/time window; and
- the documented host retention period.

No error-log line, absolute path, username/home/server, IP, agent, referrer,
message, stack, source, credential, body, or unrelated event enters evidence or
the tool transcript. Zero matching rows and an observable bounded interval are
required for capability PASS. An unavailable/unfilterable view creates
`php_error_log_unobservable`. Any matching row creates `php_error_row`; do not
open/copy it, do not attempt manual log deletion, finish safe fixture/client
cleanup, and block until the provider retention lifecycle removes it and a new
reviewed attempt is authorized.

Appendix A's `log_errors=0`, warning-to-exception conversion, output buffering,
generic catch/shutdown response, and the zero-row panel check jointly bound the
request/error channel. Access-log evidence separately proves bodies,
Authorization, credentials, and response JSON are absent under the incorporated
v5/v6 rules.

## 6. Corrected evidence and authority sequence

The sole capability evidence remains
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`. It includes
the v6 exact manifest preimages, the v7 PHP hash, all normal result booleans,
the bounded access/error-log booleans, remote/local-download evidence, the
successful final tuple or one typed `failure_state`, and the three client cleanup
booleans.

Only a complete successful state sequence, generic-error-channel proof with zero
matching rows, exact remote empty state, panel auth removal, password-record
deletion, tab closure, browser restart, required validations, and a later fresh
independent capability PASS can unpark v3 Section 9 in the existing
IMPLEMENTATION task. Implementation still receives no DreamHost, network,
credential, cron, SSH, Git, staging, provider-secret, or production authority.

## 7. V6 finding closure

- **P1-1:** option installation is recorded and required before transfer and
  success; false/exception is generic fail closed.
- **P1-2:** request-local display/log suppression, warning-to-exception handling,
  output buffering, generic catch/shutdown, and bounded zero-row Error Logs proof
  prevent path/configuration disclosure from being certified.
- **P2-1:** the tuple is scoped to success and every retained/partial/client/log
  failure has a strict separate schema.
- **P2-2:** every enable outcome is one attempt, no retry, with explicit password-
  record/tab/browser cleanup and typed failure when incomplete.
- **P2-3:** the unobservable cached-header assertion and post-disable request are
  removed; only secret-safe cleanup actions are recorded.
- **P2-4:** the exact staging error-log view, time/path filter, zero/nonzero rule,
  non-copy rule, retention disposition, and unobservable/nonzero failure states
  close the error evidence route.

## Appendix A — replacement `fixture/capability.php`

```php
<?php
declare(strict_types=1);

ob_start();
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
    if (ini_set('display_errors', '0') === false || ini_set('log_errors', '0') === false) {
        throw new RuntimeException('runtime');
    }
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
    'error_channel_contained' => true,
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
