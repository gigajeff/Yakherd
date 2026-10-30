# Yakherd.dev Concierge Website Plan v11 — Owner and Client Closure Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v11 candidate is frozen v3 plus incorporated v5, v6, v7, v8, v9,
v10, and this amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v10: `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
- v10 FAIL audit:
  `10fe29cac12625b09e19c609ecde0e08fa9b3dda69f07732547e70c22fee9ec8`.

V11 adds `owner_state` to every v10 fixture/work-child row, replaces v10's
client cleanup object and lifecycle for both pre- and post-submit outcomes,
replaces the inherited successful client evidence contract, and replaces the
failure object's version. Every other v10 rule remains. V8 PHP remains exactly
7,279 bytes, SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

No DreamHost, evidence skeleton, credential, fixture, network, Implementation,
Git, cron, SSH, staging release, provider-secret, or production action is
authorized until a fresh independent PASS on this exact composite.

## 2. Owner-state extension and aggregate rules

Every fixture row and every work-child row defined by v10 gains exactly one
field:

`owner_state`: `MATCH`, `MISMATCH`, `UNOBSERVABLE`, or `NOT_APPLICABLE`.

The exact normalization is:

- absent path: `NOT_APPLICABLE`;
- presence or type unobservable: `UNOBSERVABLE`;
- any known-present directory, regular file, symlink, or other type: observed
  `MATCH`/`MISMATCH`, or `UNOBSERVABLE` if File Manager cannot prove owner class.

`MATCH` means the operator item is owned by the capability-proven dedicated
website user; it records no username. Host-managed root auth files remain outside
these operator rows and keep their separate panel-owned class.

V10 Section 2 aggregate precedence applies to `owner_state` exactly like mode,
length, hash, and target: any owner `UNOBSERVABLE` derives the aggregate
unobservable state even when another fact proves mismatch. With full visibility,
fixture `KNOWN_EXPECTED_SUBSET` and work `KNOWN_RECOVERABLE` each require owner
`MATCH` for every present row. Owner `MISMATCH` with no unobservable fact derives
`KNOWN_MISMATCH` or `KNOWN_RETAINED` and forbids recovery deletion.

The canonical failure row key order is the raw-ASCII key order required by v6;
the strict parser requires this new field and rejects its absence or any old
v9/v10 row shape.

## 3. Replacement five-field client object

For both successful and failed evidence, `client_cleanup` has exactly:

- `password_record`: `NOT_APPLICABLE`, `COMPLETE`, `FAILED`, `UNOBSERVABLE`;
- `panel_fields`: `NOT_APPLICABLE`, `CLEARED`,
  `DESTROYED_BY_NAVIGATION`, `FAILED`, `UNOBSERVABLE`;
- `panel_tab`: `NOT_APPLICABLE`, `CLOSED`, `FAILED`;
- `staging_tabs`: `NOT_APPLICABLE`, `CLOSED`, `FAILED`;
- `browser_restart`: `NOT_APPLICABLE`, `COMPLETE`, `FAILED`.

Applicability remains v10: all N/A before generator invocation; once invoked,
password record, panel fields, panel tab, and restart apply; staging tabs apply
once any staging-origin tab is opened; after submit all five apply because the
staging protection tests necessarily open the staging origin.

### 3.1 Pre-submit cleanup

V10's pre-submit sequence remains. `panel_fields=CLEARED` requires the human to
blank both masked fields without exposing their value and to confirm only that
both controls are empty. If the panel navigates away and destroys the form before
that action, use `DESTROYED_BY_NAVIGATION` only when the human confirms the old
form is no longer present. Unobservable form/control state is
`UNOBSERVABLE`, never an assumed clear.

### 3.2 Post-submit cleanup for every outcome

After a panel-enable submit, the same exact post-submit cleanup runs for success,
timeout, panel error, clean enable failure, recovered partial, retained partial,
and every later probe failure:

1. Complete the last authorized panel operation first: on the normal path,
   disable staging protection and verify panel/files absent; on a partial path,
   perform at most the one already-authorized disable attempt and final
   inventory. No panel mutation follows this point.
2. If the original password fields are still present in the panel history/form,
   the human blanks both controls without reading or reporting the value and
   confirms only emptiness: `CLEARED`.
3. If the submit/result/disable navigation destroyed the original controls, the
   human confirms only that the original form is absent:
   `DESTROYED_BY_NAVIGATION`. The assistant does not inspect value/history.
4. If existence/emptiness cannot be confirmed, use `UNOBSERVABLE`; if a known
   present field cannot be blanked, use `FAILED`.
5. Navigate the panel tab to the non-secret DreamHost home overview and close
   that tab. Confirm `CLOSED`; otherwise `FAILED`.
6. Have the human delete/discard the saved or pending password-manager item;
   close every staging-origin tab; restart the in-app browser. Record only the
   corresponding enums.

For steps 2–4 Architecture yields the browser and performs no screenshot, DOM,
network, history, value, or password-manager inspection. The human navigates to
the neutral overview before returning control and reports only the enum. Browser
restart remains mandatory even when the form was destroyed by navigation, so a
back-forward cache is not treated as cleared state.

This sequence applies even when host-managed auth files remain after failed
disable; client cleanup never edits those files and never authorizes a retry.
Any failed/unobservable applicable field adds the exact v10 failed-check and
`CLIENT_STATE_INCOMPLETE`. Both `CLEARED` and `DESTROYED_BY_NAVIGATION` satisfy
panel-field success; they do not claim the same observation.

## 4. Replacement successful client evidence

The inherited three-boolean successful-client record is deleted. Success uses
exactly the same five-field `client_cleanup` object from Section 3 under the
Markdown heading `Client cleanup (canonical JSON)`.

For capability PASS, its exact values are:

- `password_record=COMPLETE`;
- `panel_fields=CLEARED` or `DESTROYED_BY_NAVIGATION`;
- `panel_tab=CLOSED`;
- `staging_tabs=CLOSED`; and
- `browser_restart=COMPLETE`.

The object is serialized with v8/v9's strict ASCII canonical JSON rules,
embedded with exact byte length, lowercase SHA-256, and unwrapped padded RFC 4648
base64, then decoded/validated independently. Missing/N/A/failed/unobservable
success fields reject capability PASS. Failure evidence embeds the same object as
its required top-level `client_cleanup` member.

No lower-precedence three-boolean client evidence, free-form panel cleanup field,
or alternate success schema remains valid.

## 5. Unique failure schema identity

The complete canonical failure object resulting from v9 plus v10 plus v11 has
exactly `schema_version: 3`. Values `1` or `2` are rejected for this composite.
Every v11 owner field and five-field client object is mandatory under version 3;
the v9 and v10 incompatible version-2 shapes are historical candidate schemas
and cannot be used in v11 live evidence.

The evidence skeleton records composite schema ID
`yakherd-capability-failure-v3`. The failure object's canonical JSON/base64/SHA
embedding and all other strict rules remain.

## 6. V10 finding closure and authority

- **P1-1:** every operator fixture/work child carries owner match, mismatch,
  unobservable, or N/A, participates in aggregate precedence, and gates recovery.
- **P1-2:** one post-submit cleanup sequence covers every outcome after the last
  required panel operation, including disappeared controls and retained host
  state.
- **P2-1:** PASS and FAIL use one strict five-field client object; the inherited
  three booleans are deleted.
- **P2-2:** the structurally final failure object is uniquely version 3 and bound
  by a composite schema ID.

Every incorporated runtime, cURL, Error Logs, manifest, File Manager, evidence,
one-attempt/no-retry, no-cron, and authority safeguard remains. Only complete
successful evidence followed by fresh independent live capability PASS may
unpark unchanged v3 Section 9 in the existing IMPLEMENTATION task. No DreamHost
deployment, cron, SSH, Git, staging release, provider secret, live model request,
or production action is granted.
