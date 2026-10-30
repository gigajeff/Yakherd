# Yakherd.dev Concierge Website Plan v15 - Total Certificate Tab Lifecycle

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v15 candidate is frozen v3 plus incorporated v5, v6, v7, v8, v9,
v10, v11, v12, v13, v14, and this amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v10: `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
- v11: `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
- v12: `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`;
- v13: `d9f2f008f0155e1e16b908c1939817363a2f94ec8aac587e34374f193158625f`;
- v14: `cf7604e35d0a36b9c32d283e466d49ad9f6e4e9cfbc69fc63d36cb68c830637a`;
- v14 FAIL audit:
  `aac3c53a625ec9d20cf8917366b27ed2776eb7325bc8c5dcac7891d9e28e7377`.

The exhausted v13 capability FAIL and its evidence-integrity PASS/capability-
FAIL review remain immutable at SHA-256
`01042dd7125ae8edccdc21fb8e4abb48c22f6228413bbc70a134fd28f3f5cecd`
and `e0fc6bda5cad82f06c87feaf895eb6718482b9cc19694848d5bcc0ad0c7ffddb`.

V15 replaces v14 Sections 2-5 for the new evidence bootstrap, certificate DOM
normalization, created-tab applicability, wrapper outputs/bindings, terminal
cleanup, and schema identities. Every other v13/v14 runtime, owner, inventory,
cURL, Error Logs, manifest, File Manager, credential, handback, no-cron, and
authority rule remains. V8 PHP remains exactly 7,279 bytes, SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

No DreamHost, browser, evidence-skeleton, credential, fixture, network,
Implementation, Git, cron, SSH/SFTP, staging-release, provider-secret,
live-model, deployment, or production action is authorized until a fresh
independent PASS on this exact composite.

## 2. New evidence bootstrap

After exact v15 plan PASS, Architecture may create exactly one new skeleton at:

`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability_v15.md`.

Before any live action, that skeleton must literally record:

- `Status: IN_PROGRESS` and a new non-secret UTC attempt ID;
- the complete v3/v5-v15 plan hash chain;
- the immutable v13 live evidence/review hashes from Section 1;
- the exact authorizing audit path
  `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v15.md`,
  its exact SHA-256, and verdict `PASS`;
- certificate schema ID `yakherd-capability-certificate-v2`;
- client schema ID `yakherd-capability-client-v4`;
- failure schema ID `yakherd-capability-failure-v7`; and
- no live capability claim.

`python scripts/verify_release.py` and `git diff --check` must pass with the
skeleton present. Failure to create, bind, or validate any literal above grants
no live action. The new attempt starts only at the first wrapper in Section 5
and may occur once. V9's in-memory finalization, one recovery update, and
incomplete-evidence block apply to the v15 path. No prior evidence is edited or
reused.

## 3. Certificate object and exact applicability

Successful and failed evidence use one certificate object with exactly:

- `schema_version`: integer `2`;
- `panel_status`: `ACTIVE`, `PENDING`, `ABSENT`, `FAILED`, `UNOBSERVABLE`, or
  `NOT_APPLICABLE`;
- `panel_tab_close`: `NOT_APPLICABLE`, `CLOSED`, `RECOVERED`, `FAILED`, or
  `UNOBSERVABLE`;
- `https_navigation`: `VALID`, `MISMATCH`, `UNOBSERVABLE`, or
  `NOT_APPLICABLE`;
- `navigation_tab_close`: `NOT_APPLICABLE`, `CLOSED`, `RECOVERED`, `FAILED`,
  or `UNOBSERVABLE`.

Its literal raw-ASCII key order is `https_navigation`,
`navigation_tab_close`, `panel_status`, `panel_tab_close`, `schema_version`.
Its schema ID is `yakherd-capability-certificate-v2`.

Before attempt start all four state fields are `NOT_APPLICABLE`. On successful
creation of the certificate-panel tab, `panel_status`, `panel_tab_close`, and
client `panel_tab` become applicable. If tab creation itself fails before a tab
exists, `panel_status=UNOBSERVABLE`, `panel_tab_close=NOT_APPLICABLE`, and client
`panel_tab=NOT_APPLICABLE`.

On successful creation of the public navigation tab, `https_navigation`,
`navigation_tab_close`, and client `staging_tabs` become applicable. If that tab
cannot be created, `https_navigation=UNOBSERVABLE`,
`navigation_tab_close=NOT_APPLICABLE`, and client `staging_tabs` remains N/A.
An applicable unavailable close is never N/A.

Client schema version becomes `4`, schema ID
`yakherd-capability-client-v4`. Its seven keys, enums, and canonical order remain
v13; only applicability changes before the credential generator:

- `panel_tab` applies once the certificate-panel tab is created;
- `staging_tabs` applies once the public navigation tab is created;
- password record, panel fields, browser restart, and handback check remain N/A
  until the inherited generator/client boundary makes them applicable.

Final client tab enums use v13 final-state semantics. A successful wrapper or
human terminal close yields `CLOSED`; inability to establish final closure
yields `FAILED`. Final `FAILED` maps to `PANEL_TAB_CLOSE` or
`STAGING_TABS_CLOSE` plus `CLIENT_STATE_INCOMPLETE`.

## 4. Deterministic panel status evaluator

The panel evaluator does not claim a character read bound. It performs one DOM
evaluation, accepts at most 50,000 candidate elements, materializes visible text
only for leaf candidates and at most eight ancestors of the unique target leaf,
and rejects any accepted ancestor text over 2,000 characters after
materialization. These are element/acceptance caps, not a guarantee about the
browser engine's internal string allocation.

It queries exactly `a,span,td,div,p`, keeps only visible leaf elements whose
trimmed `innerText` is exactly `staging.yakherd.dev`, and requires exactly one.
Starting at its parent, it examines at most eight ancestors. For each ancestor:

1. Reject the entire observation if its visible text exceeds 2,000 characters.
2. Lowercase and collapse ASCII/Unicode whitespace to one ASCII space.
3. Extract lowercase ASCII domain tokens using
   `[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}`; reject the observation if any
   distinct token other than `staging.yakherd.dev` exists.
4. Compute four categories with ASCII letter boundaries:
   `PENDING` from token `pending` or `processing`; `FAILED` from token `failed`,
   `error`, `expired`, or `temporary`; `ACTIVE` from exact phrase
   `let's encrypt` plus token `settings`; and `ABSENT` from token `add`.
5. If zero categories are true, continue to the next ancestor. If exactly one
   is true, return it. If two or more are true, return `UNOBSERVABLE`.

If no ancestor returns a category, or any element count/leaf/domain/length rule
fails, return `UNOBSERVABLE`. This lower-to-higher ancestor order, token rule,
conflict rule, and stop precedence are exact. Adjacent rows containing another
domain force `UNOBSERVABLE`; no category wins a conflict.

## 5. Frozen wrappers and finite tab results

### 5.1 Panel wrapper

The first and only panel operation is:

```javascript
var certificatePanelTabV15 = null;
var certificatePanelResultV15 = await (async () => {
  var panelStatusV15 = "UNOBSERVABLE";
  var panelCloseV15 = "NOT_APPLICABLE";
  try {
    certificatePanelTabV15 = await iab.tabs.new();
    panelCloseV15 = "UNOBSERVABLE";
    await certificatePanelTabV15.goto(
      "https://panel.dreamhost.com/index.cgi?tree=domain.secure"
    );
    panelStatusV15 = await certificatePanelTabV15.playwright.evaluate(() => {
      var nodes = globalThis.document?.querySelectorAll("a,span,td,div,p");
      if (nodes == null || nodes.length > 50000) return "UNOBSERVABLE";
      var leaves = [];
      for (var i = 0; i < nodes.length; i += 1) {
        var node = nodes[i];
        if (node.childElementCount === 0
          && typeof node.innerText === "string"
          && node.innerText.trim() === "staging.yakherd.dev") {
          leaves.push(node);
          if (leaves.length > 1) return "UNOBSERVABLE";
        }
      }
      if (leaves.length !== 1) return "UNOBSERVABLE";
      var current = leaves[0].parentElement;
      var token = (text, word) => new RegExp(
        "(^|[^a-z])" + word + "([^a-z]|$)"
      ).test(text);
      for (var depth = 0; depth < 8 && current != null; depth += 1) {
        var visible = current.innerText;
        if (typeof visible !== "string" || visible.length > 2000) {
          return "UNOBSERVABLE";
        }
        var normalized = visible.toLowerCase().replace(/\s+/g, " ").trim();
        var domains = normalized.match(
          /[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}/g
        ) || [];
        if ([...new Set(domains)].some(
          (domain) => domain !== "staging.yakherd.dev"
        )) return "UNOBSERVABLE";
        var pending = token(normalized, "pending")
          || token(normalized, "processing");
        var failed = token(normalized, "failed")
          || token(normalized, "error")
          || token(normalized, "expired")
          || token(normalized, "temporary");
        var active = normalized.includes("let's encrypt")
          && token(normalized, "settings");
        var absent = token(normalized, "add");
        var categories = [pending, failed, active, absent]
          .filter((value) => value === true).length;
        if (categories > 1) return "UNOBSERVABLE";
        if (categories === 1) {
          if (pending) return "PENDING";
          if (failed) return "FAILED";
          if (active) return "ACTIVE";
          return "ABSENT";
        }
        current = current.parentElement;
      }
      return "UNOBSERVABLE";
    });
    if (!["ACTIVE", "PENDING", "ABSENT", "FAILED", "UNOBSERVABLE"]
      .includes(panelStatusV15)) panelStatusV15 = "UNOBSERVABLE";
  } catch {
    panelStatusV15 = "UNOBSERVABLE";
  }
  if (certificatePanelTabV15 !== null) {
    try {
      await certificatePanelTabV15.close();
      certificatePanelTabV15 = null;
      panelCloseV15 = "CLOSED";
    } catch {
      panelCloseV15 = "FAILED";
    }
  }
  return {panel_status: panelStatusV15, panel_tab_close: panelCloseV15};
})();
nodeRepl.write(JSON.stringify(certificatePanelResultV15));
```

Only the two finite enums enter the transcript. An absent/unparseable outer
result is treated as `panel_status=UNOBSERVABLE` and
`panel_tab_close=UNOBSERVABLE` because tab creation may have occurred.

Continuation requires both `panel_status=ACTIVE` and
`panel_tab_close=CLOSED`. Every other panel result adds `CERTIFICATE_PANEL` and
stops. For close `FAILED`/`UNOBSERVABLE`, Architecture yields without another
browser read. The human closes the entire in-app browser once and reports only
`COMPLETE` or `FAILED`. `COMPLETE` produces
`panel_tab_close=RECOVERED` and client `panel_tab=CLOSED`; `FAILED` produces
certificate close `FAILED`/`UNOBSERVABLE`, client `panel_tab=FAILED`,
`PANEL_TAB_CLOSE`, and `CLIENT_STATE_INCOMPLETE`. No browser reopen, panel
refresh, alternate route, status retry, or handback check follows; the attempt
ends.

### 5.2 Navigation wrapper and preserved binding

Only after the exact panel continuation tuple, the public operation is:

```javascript
var certificateNavigationTabV15 = null;
var certificateNavigationResultV15 = await (async () => {
  var navigationV15 = "UNOBSERVABLE";
  var navigationCloseV15 = "NOT_APPLICABLE";
  try {
    certificateNavigationTabV15 = await iab.tabs.new();
    navigationCloseV15 = "UNOBSERVABLE";
    await certificateNavigationTabV15.goto("https://staging.yakherd.dev/");
    var originMatchesV15 = await certificateNavigationTabV15.playwright.evaluate(
      () => globalThis.location.protocol === "https:"
        && globalThis.location.hostname === "staging.yakherd.dev"
    );
    navigationV15 = originMatchesV15 === true
      ? "VALID"
      : (originMatchesV15 === false ? "MISMATCH" : "UNOBSERVABLE");
  } catch {
    navigationV15 = "UNOBSERVABLE";
  }
  if (navigationV15 !== "VALID" && certificateNavigationTabV15 !== null) {
    try {
      await certificateNavigationTabV15.close();
      certificateNavigationTabV15 = null;
      navigationCloseV15 = "CLOSED";
    } catch {
      navigationCloseV15 = "FAILED";
    }
  } else if (navigationV15 === "VALID") {
    navigationCloseV15 = "DEFERRED";
  }
  return {
    https_navigation: navigationV15,
    navigation_tab_action: navigationCloseV15
  };
})();
nodeRepl.write(JSON.stringify(certificateNavigationResultV15));
```

`DEFERRED` is a transient wrapper result, not a certificate-schema value and is
rejected in final evidence. It means the exact globally bound
`certificateNavigationTabV15` remains available. The only continuation tuple
is `(VALID, DEFERRED)` with a non-null bound tab. Any other navigation result
adds `CERTIFICATE` and stops.

On a failed navigation close or absent/unparseable outer result, the same
human-only whole-browser close runs once. A confirmed terminal close maps the
final certificate close to `RECOVERED` and client `staging_tabs=CLOSED`; an
unconfirmed close maps final certificate/client states to `FAILED` or
`UNOBSERVABLE`/`FAILED`, adds `STAGING_TABS_CLOSE` and
`CLIENT_STATE_INCOMPLETE`, and stops. The certificate operation is never
retried.

### 5.3 Closing the deferred valid tab before the generator

If any root, File Manager, evidence, approval, or other gate stops the attempt
before credential-generator invocation, Architecture invokes exactly once:

```javascript
var deferredNavigationCloseV15 = await (async () => {
  if (certificateNavigationTabV15 === null) return "UNOBSERVABLE";
  try {
    await certificateNavigationTabV15.close();
    certificateNavigationTabV15 = null;
    return "CLOSED";
  } catch {
    return "FAILED";
  }
})();
nodeRepl.write(deferredNavigationCloseV15);
```

`CLOSED` sets final `navigation_tab_close=CLOSED` and client
`staging_tabs=CLOSED`. `FAILED`, `UNOBSERVABLE`, or absent scalar triggers the
one human whole-browser close and final mappings from Section 5.2. This cleanup
does not retry the failed downstream gate.

If the generator is invoked, the deferred tab passes into the incorporated v13
client lifecycle. The final observed staging-tab result sets both client
`staging_tabs` and certificate `navigation_tab_close`: normal closure is
`CLOSED`; whole-browser terminal recovery is `RECOVERED`; inability to confirm
closure is `FAILED`/`UNOBSERVABLE` and blocks PASS. Architecture never
reacquires the tab by list, URL, history, snapshot, or a second navigation.

## 6. Certificate checks, mappings, and evidence equality

Certificate PASS requires exactly:

- `panel_status=ACTIVE`;
- `panel_tab_close=CLOSED`;
- `https_navigation=VALID`; and
- final `navigation_tab_close=CLOSED`.

`RECOVERED` is safe final closure but is never certificate PASS. A non-PASS
panel status/close adds `CERTIFICATE_PANEL`. A non-PASS navigation/close adds
`CERTIFICATE`. Final client tab failure independently adds its exact tab-close
check and `CLIENT_STATE_INCOMPLETE`.

Successful and failed evidence embed the certificate object under
`Certificate checks (canonical JSON)` with exact byte length, lowercase
SHA-256, unwrapped padded RFC 4648 base64, and decoded table. Failed evidence
also includes the object as top-level `certificate_preflight` inside the
failure object. The strict validator must decode the standalone preimage,
canonicalize the nested parsed object, and require byte-for-byte equality,
identical decoded values, identical length, and identical SHA-256. Any mismatch
adds `MANIFEST_EVIDENCE` and `EVIDENCE_FINALIZATION` and leaves capability FAIL.

The complete failure object is v13's object plus mandatory
`certificate_preflight`; its `schema_version` is `7` and schema ID is
`yakherd-capability-failure-v7`. Raw-ASCII top-level placement remains after
`capability_result` and before `cleanup_utc`. Client version is `4`. Failure
versions 1-6, client versions 1-3, certificate version 1, stale IDs, invalid
applicability, `DEFERRED`, and unequal standalone/nested certificate bytes are
rejected.

## 7. Authority

An independent PASS on this exact plan may authorize only the exact v15
skeleton and one bounded attempt. It does not establish a certificate or any
DreamHost capability. Only complete successful v15 evidence followed by a
separate fresh independent live-evidence PASS may unpark unchanged v3 Section 9
in the existing IMPLEMENTATION task.

No plan PASS or live result grants deployment, cron, SSH/SFTP, Git, final
staging authentication/release, provider secret, live-model request, canary,
production, or publication authority.
