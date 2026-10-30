# Yakherd.dev Concierge Website Plan v13 - Closed Handback State Machine

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v13 candidate is frozen v3 plus incorporated v5, v6, v7, v8, v9,
v10, v11, v12, and this amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v10: `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
- v11: `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
- v12: `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`;
- v12 FAIL audit:
  `374172237157a0964227c002e1c9dbb39cecbb7ed9d959462391ca32f25f1bd4`.

V13 replaces v12 Sections 3 and 4 wherever they concern the browser handback,
client object, cleanup final-state derivation, and client/failure schema
identities. V12's truthful `FORM_ABSENT_CURRENT_VIEW` semantics remain. Every
owner, inventory, runtime, cURL, Error Logs, manifest, File Manager, evidence,
no-submit-retry, no-cron, and authority rule remains. V8 PHP remains exactly
7,279 bytes, SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

No DreamHost, browser, evidence-skeleton, credential, fixture, network,
Implementation, Git, cron, SSH, staging-release, provider-secret, live-model,
deployment, or production action is authorized until a fresh independent PASS
on this exact composite.

## 2. Replacement client schema and finite failure mapping

For both successful and failed evidence, `client_cleanup` has exactly seven
members: one schema member plus six state members.

- `schema_version`: integer `3`;
- `password_record`: `NOT_APPLICABLE`, `COMPLETE`, `FAILED`, or
  `UNOBSERVABLE`;
- `panel_fields`: `NOT_APPLICABLE`, `CLEARED`,
  `FORM_ABSENT_CURRENT_VIEW`, `FAILED`, or `UNOBSERVABLE`;
- `panel_tab`: `NOT_APPLICABLE`, `CLOSED`, or `FAILED`;
- `staging_tabs`: `NOT_APPLICABLE`, `CLOSED`, or `FAILED`;
- `browser_restart`: `NOT_APPLICABLE`, `COMPLETE`, or `FAILED`;
- `handback_check`: `NOT_APPLICABLE`, `MATCH`, `MISMATCH`, or
  `UNOBSERVABLE`.

Before credential-generator invocation all six state members are
`NOT_APPLICABLE`. Once the generator is invoked, password record, panel fields,
panel tab, browser restart, and handback check are applicable; staging tabs
remain `NOT_APPLICABLE` until any staging-origin tab is opened. After panel
enable is submitted all six are applicable. An applicable fact that cannot be
established is represented by its `FAILED` or `UNOBSERVABLE` value, never by
`NOT_APPLICABLE`.

The tab enums represent final state after the last authorized cleanup action,
not the history of individual close attempts. `panel_tab=CLOSED` exactly when
the human finally confirms that no DreamHost panel-origin tab remains, including
confirmation achieved by closing the whole in-app browser. Otherwise it is
`FAILED`. `staging_tabs=CLOSED` has the same rule for every staging-origin tab.
A failed direct close followed by a successful all-origin close therefore has
the one canonical final result `panel_tab=CLOSED`; the earlier failed attempt
does not create a second serialization.

The finite check-ID table adds `HANDBACK_BLANK`. Final failure mapping is:

- password record `FAILED` or `UNOBSERVABLE` -> `PASSWORD_RECORD_DELETE`;
- panel fields `FAILED` or `UNOBSERVABLE` -> `PANEL_FIELDS_CLEAR`;
- panel tab `FAILED` -> `PANEL_TAB_CLOSE`;
- staging tabs `FAILED` -> `STAGING_TABS_CLOSE`;
- browser restart `FAILED` -> `BROWSER_RESTART`;
- handback check `MISMATCH` or `UNOBSERVABLE` -> `HANDBACK_BLANK`.

Each mapped client failure also adds `CLIENT_STATE_INCOMPLETE` to
`failure_classes`. A valid applicable non-failing value adds neither the check
nor that class by itself. Unknown values, missing members, and an applicable
`NOT_APPLICABLE` are rejected. No actual URL, tab title, account identifier,
machine identifier, error string, or credential-derived value is evidence.

## 3. Exact cleanup and retry state machine

After the last authorized panel mutation, Architecture yields the browser. The
human performs the following exact sequence. Architecture takes no screenshot,
DOM snapshot, URL read, network read, history read, tab-list read, value read,
password-manager read, accessibility-tree read, or browser-state read during
steps 1-7.

1. Resolve `panel_fields` under v12's truthful current-view rules. Blank and
   confirm emptiness when the form is present; otherwise report only
   `FORM_ABSENT_CURRENT_VIEW`, `FAILED`, or `UNOBSERVABLE`. Never read or report
   either masked value.
2. Attempt to close the panel tab directly. This result is provisional and is
   not serialized yet.
3. Delete or discard the saved, pending, or ambiguously created password-manager
   item and retain only the password-record enum.
4. Perform one all-origin close sweep over every remaining DreamHost panel tab
   and every staging-origin tab. This sweep includes the original panel tab if
   step 2 did not close it. Derive provisional panel/staging enums from the
   resulting observed state using Section 2.
5. Restart the in-app browser once. If no DreamHost panel or staging origin is
   restored, set `browser_restart=COMPLETE` and continue to step 7. If either
   origin is restored, perform one restoration close sweep over all such tabs,
   update the provisional tab enums, and restart exactly once more.
6. If the second restart restores no protected-origin tab, set
   `browser_restart=COMPLETE` and continue. If either restart cannot complete or
   the second restart restores any DreamHost panel or staging origin, set
   `browser_restart=FAILED` and perform exactly one terminal close-only sweep.
   There is no third restart. Recompute both final tab enums after that sweep.
   If either final absence cannot be confirmed, attempt to close the whole
   in-app browser once; confirmed whole-browser closure makes both applicable
   tab enums `CLOSED`, while inability to confirm it leaves the corresponding
   enum `FAILED`. Do not reopen the browser merely to create a handback.
7. If a browser is open and both applicable tab enums are `CLOSED`, open and
   select exactly one `about:blank` tab, make no further navigation, and return
   control for the single equality-only operation in Section 4. If the browser
   is closed or a tab enum is `FAILED`, return control to the Codex task without
   reopening or exposing browser content; Section 4 then produces
   `UNOBSERVABLE`.

The two restart attempts and the terminal close-only sweep exhaust this cleanup
authority. Close sweeps are client cleanup, not another credential, panel
submit, panel-disable, fixture, or probe retry. There remains exactly one
credential, at most one panel-enable submit, at most one panel-disable attempt,
and no capability retry.

After Section 4 returns `false` or `null`, Architecture immediately yields
again and the human closes the entire in-app browser once without reporting any
page value. Confirmed whole-browser closure normalizes both applicable final tab
enums to `CLOSED`; inability to confirm it leaves the corresponding enum
`FAILED`. `handback_check` remains the result already produced, and no second
handback check is authorized.

## 4. Equality-only handback verifier

The handback comparison is one atomic read-only browser operation. It must run
exactly as follows against the already selected tab and existing `iab` browser
binding:

```javascript
var handbackProbeV13 = await (async () => {
  try {
    var selectedHandbackTabV13 = await iab.tabs.selected();
    if (selectedHandbackTabV13 == null) return null;
    var equalHandbackV13 = await selectedHandbackTabV13.playwright.evaluate(
      () => globalThis.location.href === "about:blank"
    );
    return equalHandbackV13 === true
      ? true
      : (equalHandbackV13 === false ? false : null);
  } catch {
    return null;
  }
})();
nodeRepl.write(handbackProbeV13);
```

The operation calls neither `tab.url()` nor any tab-list, DOM, history, log,
network, screenshot, or page-content API. Its page expression returns only a
boolean. Its catch clause does not bind, print, or rethrow an error. The outer
tool result is exactly `true`, `false`, or `null`; the operation is not retried.
No unexpected URL or error text can enter the tool transcript or evidence.

Map `true` to `handback_check=MATCH`, `false` to
`handback_check=MISMATCH`, and `null` or any non-boolean result to
`handback_check=UNOBSERVABLE`. Before applicability only, use
`NOT_APPLICABLE`. Architecture performs no other browser operation after the
human-only boundary during this attempt.

## 5. Canonical bytes, schema identities, and PASS

V6 raw-ASCII key sorting controls every canonical object. For the version-3
client object, the literal serialized key order is exactly:

1. `browser_restart`;
2. `handback_check`;
3. `panel_fields`;
4. `panel_tab`;
5. `password_record`;
6. `schema_version`;
7. `staging_tabs`.

There is no conceptual, insertion, or "leading field" order. Any other byte
order is rejected before byte length, SHA-256, or base64 evidence is accepted.
All inherited strict ASCII/no-escape, array ordering, lowercase SHA-256,
unwrapped padded RFC 4648 base64, decoded-table, and independent-validation
rules remain.

The client composite schema ID is `yakherd-capability-client-v3`. The complete
failure object is exactly `schema_version: 5` with schema ID
`yakherd-capability-failure-v5`; it contains the mandatory version-3 client
object. Client versions 1 or 2, failure versions 1-4, stale schema IDs, missing
`handback_check`, and old panel-field enums are rejected. The evidence skeleton
records both exact schema IDs before live work.

Capability PASS requires client version 3 with:

- `password_record=COMPLETE`;
- `panel_fields=CLEARED` or `FORM_ABSENT_CURRENT_VIEW`;
- `panel_tab=CLOSED`;
- `staging_tabs=CLOSED`;
- `browser_restart=COMPLETE`; and
- `handback_check=MATCH`.

Any client failure produces the exact mapping in Section 2 and cannot authorize
Implementation. Successful evidence embeds the same canonical client object
under `Client cleanup (canonical JSON)`; failed evidence embeds it as the
mandatory `client_cleanup` member of the version-5 failure object.

## 6. V12 finding closure and authority

- **P1-1:** handback has one field, a finite result alphabet, one failed-check
  mapping, one failure-class disposition, and an equality-only atomic verifier
  that never returns the compared URL.
- **P1-2:** direct-close precedence is final-state based; first restoration gets
  one close/restart; second restoration or restart failure gets one listed
  terminal close-only sweep and deterministic tab normalization without a third
  restart or hidden action.
- **P2-1:** the seven canonical client keys have one literal raw-ASCII order.

Only complete capability evidence followed by fresh independent live capability
PASS may unpark unchanged v3 Section 9 in the existing IMPLEMENTATION task. No
DreamHost deployment, cron, SSH, Git, staging release, provider secret, live
model request, or production action is granted.
