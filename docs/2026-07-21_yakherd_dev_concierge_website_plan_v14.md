# Yakherd.dev Concierge Website Plan v14 - Fresh Certificate-Gated Attempt

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and preserved exhausted attempt

The exact v14 candidate is frozen v3 plus incorporated v5, v6, v7, v8, v9,
v10, v11, v12, v13, and this amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v10: `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
- v11: `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
- v12: `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`;
- v13: `d9f2f008f0155e1e16b908c1939817363a2f94ec8aac587e34374f193158625f`.

The exhausted v13 live record and its independent review are immutable inputs:

- v13 capability FAIL evidence:
  `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md`,
  SHA-256
  `01042dd7125ae8edccdc21fb8e4abb48c22f6228413bbc70a134fd28f3f5cecd`;
- evidence-integrity PASS / capability FAIL review:
  `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability_red_team.md`,
  SHA-256
  `e0fc6bda5cad82f06c87feaf895eb6718482b9cc19694848d5bcc0ad0c7ffddb`.

V14 does not retry or edit the v13 attempt. It creates one new attempt boundary
with a new evidence path and replaces only the certificate gate, evidence path,
and failure-schema identity. Every v13 runtime, owner, inventory, cURL, Error
Logs, manifest, File Manager, credential, cleanup, handback, no-cron, and
authority rule remains. V8 PHP remains exactly 7,279 bytes, SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

No DreamHost, browser, evidence-skeleton, credential, fixture, network,
Implementation, Git, cron, SSH/SFTP, staging-release, provider-secret,
live-model, deployment, or production action is authorized until a fresh
independent PASS on this exact composite.

## 2. New sole-attempt evidence boundary

After exact v14 plan PASS, Architecture may create exactly one new skeleton at:

`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability_v14.md`.

It must contain `Status: IN_PROGRESS`, the complete v3/v5-v14 hash chain, the
two immutable v13 live-record identities above, a new non-secret UTC attempt ID,
the schema IDs in Section 5, and no live claim. `python
scripts/verify_release.py` and `git diff --check` must pass before any live
action. Failure to create or validate the skeleton authorizes no live action.

The new attempt starts at the single panel-status operation in Section 3. It is
not a continuation of v13 and may occur only once. Any non-PASS certificate
result finalizes the v14 evidence as FAIL and stops before root/File Manager
inspection. The existing v9 in-memory finalization, one recovery update, and
unconditional incomplete-evidence block apply to the new path. The v13 evidence
and review are never edited or reused as a skeleton.

## 3. Exact two-signal certificate gate

The certificate gate has an exact canonical object with:

- `schema_version`: integer `1`;
- `panel_status`: `ACTIVE`, `PENDING`, `ABSENT`, `FAILED`, `UNOBSERVABLE`, or
  `NOT_APPLICABLE`;
- `https_navigation`: `VALID`, `MISMATCH`, `UNOBSERVABLE`, or
  `NOT_APPLICABLE`.

The raw-ASCII key order is exactly `https_navigation`, `panel_status`,
`schema_version`. The schema ID is `yakherd-capability-certificate-v1`.

### 3.1 Signed-in panel scalar

Architecture opens the fixed signed-in DreamHost Secure Certificates route:

`https://panel.dreamhost.com/index.cgi?tree=domain.secure`.

Without a screenshot, DOM snapshot, tab-list read, URL read, network read, or
page-content output, it executes exactly one read-only page evaluation. The
evaluation reads at most 2,000,000 characters of current visible body text,
requires exactly one literal occurrence of `staging.yakherd.dev`, examines only
the 600-character window beginning 200 characters before that occurrence, and
returns one enum:

- `ACTIVE` only if the lowercase window contains both `let's encrypt` and
  `settings`, and none of `pending`, `processing`, `failed`, `error`, `expired`,
  `temporary`, or `add`;
- `PENDING` if it contains `pending` or `processing`;
- `FAILED` if it contains `failed`, `error`, `expired`, or `temporary`;
- `ABSENT` if it contains `add` and does not meet `ACTIVE`;
- `UNOBSERVABLE` for missing/oversized body text, zero/multiple target
  occurrences, no exact branch, any non-enum result, navigation failure, or
  caught exception.

The wrapper catches without binding/rethrowing an error and explicitly emits
only the enum. It does not emit the window, body, target count, error, current
URL, other domain, account value, username, machine value, or identifier. There
is no alternate panel route, second evaluation, refresh, or retry.

If the result is not `ACTIVE`, `https_navigation=NOT_APPLICABLE`, the new
allowlisted failed check is `CERTIFICATE_PANEL`, and the attempt stops. No
failure class is added by this clean certificate-status failure alone.

### 3.2 Public HTTPS scalar

Only after `panel_status=ACTIVE`, Architecture creates one new in-app-browser
tab and navigates once to `https://staging.yakherd.dev/`. It then performs one
read-only equality evaluation that returns:

- `VALID` only when the navigation completed without a caught error and the
  page has protocol `https:` plus hostname exactly `staging.yakherd.dev`;
- `MISMATCH` when navigation completed but either equality is false; or
- `UNOBSERVABLE` for navigation/evaluation failure, non-enum result, or caught
  exception.

The wrapper emits only the enum, never an error, URL, redirect target,
certificate diagnostic, page value, or identifier. It calls no DOM snapshot,
page-content, URL, tab-list, network, history, log, or screenshot API and is not
retried. `MISMATCH` or `UNOBSERVABLE` maps to existing `CERTIFICATE` and stops
before root/File Manager inspection. Only `(ACTIVE, VALID)` permits the
unchanged v13 attempt to continue to the read-only root inventory.

### 3.3 Frozen browser wrappers

Section 3.1 is implemented by exactly this one outer operation:

```javascript
var certificatePanelStateV14 = await (async () => {
  var certificatePanelTabV14 = null;
  var certificatePanelObservedV14 = "UNOBSERVABLE";
  try {
    certificatePanelTabV14 = await iab.tabs.new();
    await certificatePanelTabV14.goto(
      "https://panel.dreamhost.com/index.cgi?tree=domain.secure"
    );
    certificatePanelObservedV14 = await certificatePanelTabV14.playwright.evaluate(
      () => {
        var body = globalThis.document?.body?.innerText;
        if (typeof body !== "string" || body.length > 2000000) {
          return "UNOBSERVABLE";
        }
        var target = "staging.yakherd.dev";
        var first = body.indexOf(target);
        if (first < 0 || first !== body.lastIndexOf(target)) {
          return "UNOBSERVABLE";
        }
        var windowText = body
          .slice(Math.max(0, first - 200), Math.max(0, first - 200) + 600)
          .toLowerCase();
        var pending = windowText.includes("pending")
          || windowText.includes("processing");
        var failed = windowText.includes("failed")
          || windowText.includes("error")
          || windowText.includes("expired")
          || windowText.includes("temporary");
        var add = windowText.includes("add");
        var active = windowText.includes("let's encrypt")
          && windowText.includes("settings")
          && !pending && !failed && !add;
        if (pending) return "PENDING";
        if (failed) return "FAILED";
        if (active) return "ACTIVE";
        if (add) return "ABSENT";
        return "UNOBSERVABLE";
      }
    );
    if (!["ACTIVE", "PENDING", "ABSENT", "FAILED", "UNOBSERVABLE"]
      .includes(certificatePanelObservedV14)) {
      certificatePanelObservedV14 = "UNOBSERVABLE";
    }
  } catch {
    certificatePanelObservedV14 = "UNOBSERVABLE";
  }
  if (certificatePanelTabV14 !== null) {
    try {
      await certificatePanelTabV14.close();
    } catch {
      certificatePanelObservedV14 = "UNOBSERVABLE";
    }
  }
  return certificatePanelObservedV14;
})();
nodeRepl.write(certificatePanelStateV14);
```

The dedicated certificate-panel tab is closed exactly once before the scalar is
returned. Close failure normalizes the result to `UNOBSERVABLE` and authorizes
no retry.

Only after literal `ACTIVE`, Section 3.2 is implemented by exactly this second
outer operation:

```javascript
var certificateNavigationStateV14 = await (async () => {
  var certificateNavigationTabV14 = null;
  try {
    certificateNavigationTabV14 = await iab.tabs.new();
    await certificateNavigationTabV14.goto(
      "https://staging.yakherd.dev/"
    );
    var originMatchesV14 = await certificateNavigationTabV14.playwright.evaluate(
      () => globalThis.location.protocol === "https:"
        && globalThis.location.hostname === "staging.yakherd.dev"
    );
    if (originMatchesV14 === true) return "VALID";
    try {
      await certificateNavigationTabV14.close();
    } catch {}
    return originMatchesV14 === false ? "MISMATCH" : "UNOBSERVABLE";
  } catch {
    if (certificateNavigationTabV14 !== null) {
      try {
        await certificateNavigationTabV14.close();
      } catch {}
    }
    return "UNOBSERVABLE";
  }
})();
nodeRepl.write(certificateNavigationStateV14);
```

The valid staging tab remains open for the incorporated authenticated/HTTP
sequence. A mismatch/unobservable tab receives one close attempt; close failure
does not alter or retry the already failing certificate result.

## 4. Complete certificate applicability and downstream stop rules

Before the v14 attempt starts, both certificate fields are
`NOT_APPLICABLE`. Once the panel operation starts, `panel_status` is applicable.
`https_navigation` becomes applicable only after `ACTIVE`; otherwise it remains
`NOT_APPLICABLE`. An applicable unavailable fact is `UNOBSERVABLE`, never N/A.

On any certificate stop, every v13 client state field remains
`NOT_APPLICABLE` because the credential generator was not invoked. The failure
object truthfully normalizes uninspected panel/fixture/work/root state using
v10/v11 unknown-first matrices, `local_temp_state=ABSENT`, and the exact
applicable certificate check. Required downstream root/File Manager/final
inventory checks that cannot be established may be listed exactly as in the
accepted v13 FAIL record without implying that their operations ran.

If `(ACTIVE, VALID)` is established, the certificate object is immutable for
the attempt. The preflight continues once through the incorporated root,
File Manager, checkpoint, panel-auth, fixture/probe, log, cleanup, evidence, and
handback sequence. No later failure authorizes another panel certificate read,
HTTPS navigation, credential, submit, disable retry, fixture retry, probe retry,
or capability retry.

## 5. Replacement evidence and failure schema identities

Successful and failed v14 evidence both embed the certificate object under the
heading `Certificate checks (canonical JSON)` with exact ASCII byte length,
lowercase SHA-256, unwrapped padded RFC 4648 base64, and decoded field table.
Capability PASS requires certificate version 1 with exactly
`panel_status=ACTIVE` and `https_navigation=VALID`.

The complete v14 failure object is the v13 version-5 object plus one mandatory
top-level `certificate_preflight` member containing the exact Section 3 object.
Its `schema_version` is `6` and schema ID is
`yakherd-capability-failure-v6`. In raw-ASCII top-level order,
`certificate_preflight` appears after `capability_result` and before
`cleanup_utc`. Failure versions 1-5, stale schema IDs, a missing certificate
object, invalid applicability, and alternate certificate bytes are rejected.

The client schema remains `yakherd-capability-client-v3`; no client member or
canonical order changes. V13's exact fixture/work row schemas, owner fields,
aggregate precedence, finite checks/classes, canonical JSON rules, mutation
ledger, local-download lifecycle, and authority rules remain.

## 6. Authority

An independent PASS on this exact plan may authorize only the one new v14
skeleton and one bounded v14 attempt. It does not itself establish a certificate
or any DreamHost capability. Only complete successful v14 evidence followed by
a separate fresh independent live-evidence PASS may unpark unchanged v3 Section
9 in the existing IMPLEMENTATION task.

No plan PASS or live capability result grants deployment, cron, SSH/SFTP, Git,
final staging authentication/release, provider secret, live-model request,
canary, production, or publication authority.
