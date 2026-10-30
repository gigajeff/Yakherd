# Yakherd.dev Concierge Website Plan v12 — Truthful Browser Handback Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v12 candidate is frozen v3 plus incorporated v5, v6, v7, v8, v9,
v10, v11, and this amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v10: `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
- v11: `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
- v11 FAIL audit:
  `2e9ec79771fd01eb9419c3dba5ac3aba20ded7017900ac95d7e25fd0368fc18d`.

V12 replaces only v11's `DESTROYED_BY_NAVIGATION` enum/claim and the human-only
post-submit handback sequence. Because the client enum changes, V12 also assigns
unique schema identities in Section 4. Every owner, inventory, runtime, cURL,
Error Logs, manifest, File Manager, evidence, no-retry, no-cron, and authority
rule remains. V8 PHP remains 7,279 bytes, SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

No DreamHost, evidence skeleton, credential, fixture, network, Implementation,
Git, cron, SSH, staging release, provider-secret, or production action is
authorized until a fresh independent PASS on this exact composite.

## 2. Truthful panel-field enum

The five-field `client_cleanup` object remains v11 except `panel_fields` is now:

`NOT_APPLICABLE`, `CLEARED`, `FORM_ABSENT_CURRENT_VIEW`, `FAILED`, or
`UNOBSERVABLE`.

`DESTROYED_BY_NAVIGATION` is invalid and rejected everywhere.

- `CLEARED` means the human observed both masked controls in the current form,
  blanked them without reading/reporting values, and confirmed only emptiness.
- `FORM_ABSENT_CURRENT_VIEW` means only that the human confirmed the original
  password form was not present in the current panel view. It makes no claim
  about browser history, back-forward cache, process memory, or destruction.
- `UNOBSERVABLE` means the human could not establish either current-view state;
  it is never a PASS value.

`FORM_ABSENT_CURRENT_VIEW` is safe only as one element of the mandatory cleanup
sequence in Section 3. The strict validator accepts it for PASS only when the
same client object also has `panel_tab=CLOSED` and
`browser_restart=COMPLETE`. Otherwise it rejects PASS.

## 3. Human-only boundary through neutral handback

After the last authorized panel operation, Architecture yields the browser and
does not regain control during any client cleanup. The human performs, in order:

1. Report only `CLEARED`, `FORM_ABSENT_CURRENT_VIEW`, `FAILED`, or
   `UNOBSERVABLE` for the panel fields under Section 2.
2. Close the DreamHost panel tab directly. Do not navigate to or return control
   on any signed-in DreamHost page. Report only `CLOSED` or `FAILED`.
3. Delete/discard the saved or pending password-manager item and report only the
   password-record enum.
4. Close every staging-origin tab and every remaining DreamHost-origin tab.
5. Fully restart the in-app browser. If any DreamHost/staging tab is restored,
   close it without returning control and restart once more; a second restoration
   or inability to restart is `browser_restart=FAILED`.
6. Open exactly `about:blank`. Confirm no DreamHost/staging origin is open, then
   return control and report only the five client enums in plain text.

Throughout steps 1–6, Architecture performs no screenshot, DOM, network,
history, tab-list, value, password-manager, accessibility-tree, or browser-state
inspection and receives no page content. No signed-in overview, hostname detail,
account identifier, machine identifier, username, form field, credential-derived
value, or history entry may enter a tool transcript.

Architecture's first browser action after handback may only verify the current
URL is literal `about:blank`; it must not inspect page DOM or history. If the URL
is not `about:blank`, the client cleanup is `FAILED` and capability cannot PASS.

This same boundary applies after pre-submit cleanup and after every post-submit
outcome, including success, timeout, panel error, clean enable failure, recovered
partial, retained partial, or later probe failure. Host-managed remote state does
not change the human-only client sequence.

## 4. Final schema identities and PASS contract

The canonical five-field client object gains exactly one leading field:

`schema_version`: integer `2`.

It is the same six-field object in successful evidence and as the
`client_cleanup` member of failed evidence. Version `1` or an unversioned object
is rejected.

The complete failure object is now exactly `schema_version: 4` and has composite
schema ID `yakherd-capability-failure-v4`. Versions `1`, `2`, or `3` and earlier
client enums/shapes are rejected. All v11 owner fields and v10 observation fields
remain mandatory.

Capability PASS requires client schema version 2 with:

- `password_record=COMPLETE`;
- `panel_fields=CLEARED` or `FORM_ABSENT_CURRENT_VIEW`;
- `panel_tab=CLOSED`;
- `staging_tabs=CLOSED`;
- `browser_restart=COMPLETE`; and
- verified handback URL `about:blank`.

The strict ASCII canonical JSON, byte length, SHA-256, base64 preimage, decoded
table, and independent validation requirements remain. No v11
`DESTROYED_BY_NAVIGATION`, version-3 failure object, unversioned client object,
or signed-in-page handback can validate.

## 5. V11 finding closure and authority

- **P1-1:** the enum states only current-view absence; tab closure and restart
  are separate mandatory facts, so no destruction/history claim is inferred.
- **P1-2:** the no-capture boundary continues through panel-tab closure, all
  DreamHost/staging-tab closure, restart, and literal `about:blank` handback;
  control never returns on a signed-in account page.

Every v11 closure of owner state, post-submit branch coverage, shared PASS/FAIL
client evidence, and unique failure parsing remains under the new exact schema
versions. Only complete successful evidence followed by fresh independent live
capability PASS may unpark unchanged v3 Section 9 in the existing IMPLEMENTATION
task. No DreamHost deployment, cron, SSH, Git, staging release, provider secret,
live model request, or production action is granted.
