# Yakherd.dev Concierge Website Plan v10 — Total Observation Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v10 candidate is frozen v3 plus incorporated v5, v6, v7, v8, v9,
and this amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v9 FAIL audit:
  `89da8a1a9f446bf85c762d9ea513d6efd07d3ed1e914b984d18850eda9d4a3fa`.

V10 replaces v9 Sections 3.1, 3.2, and 3.3, replaces v9's evidence-assembly
temporary-workspace sentence and lifecycle, and adds the client check IDs in
Section 5. Every other v9 rule remains. V8 PHP remains exactly 7,279 bytes,
SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.
All cron and deployment authority remains removed/withheld.

No DreamHost, evidence skeleton, credential, fixture, network, Implementation,
Git, cron, SSH, staging release, provider-secret, or production action is
authorized until a fresh independent PASS on this exact composite.

## 2. Universal observation and aggregate precedence

Every inventory fact has an explicit observed, not-applicable, mismatch, or
unobservable representation. A listed path may be known present while type,
mode, length, hash, owner, or symlink target is independently unobservable.

Aggregate derivation uses this single ordered function; no short-circuit phrase
from v9 survives:

1. Validate the row shape and per-type matrix. An illegal combination rejects
   the object.
2. If any required field for any present or unobservable row is
   `UNOBSERVABLE`/`UNKNOWN`, or an extra-entry/child observation is
   `UNOBSERVABLE`, derive the aggregate unobservable state. This rule has
   precedence even when a different observed field already proves mismatch.
3. Otherwise every fact is observed. Derive `ABSENT` only under the exact absent
   rule; derive the expected/recoverable state only under every exact positive
   invariant; otherwise derive the known mismatch/retained state.

Thus a known symlink plus unknown mode is unobservable, not a known mismatch; a
known wrong mode plus unknown owner is unobservable, not known retained. This is
conservative and deterministic.

For this function, every normalized field that permits `UNKNOWN` or
`UNOBSERVABLE` is always required for visibility. No field becomes irrelevant
because another field already proves mismatch, and `NOT_APPLICABLE` is the only
value excluded from the visibility test.

## 3. Replacement fixture inventory

The v9 fixture object and state/extra-entry enums remain. Each of the same five
ordered rows now has exactly:

- `path`;
- `presence`: `PRESENT`, `ABSENT`, `UNOBSERVABLE`;
- `type`: `ABSENT`, `DIRECTORY`, `REGULAR`, `SYMLINK`, `OTHER`, `UNKNOWN`;
- `mode`: `NOT_APPLICABLE`, `0444`, `0755`, `OTHER`, `UNKNOWN`;
- `byte_length_state`: `VALUE`, `NOT_APPLICABLE`, `UNOBSERVABLE`;
- `byte_length`: nonnegative integer or null; and
- `sha256_state`: `MATCH`, `MISMATCH`, `NOT_APPLICABLE`, `UNOBSERVABLE`.

The complete normalization matrix is:

- absent: type `ABSENT`, mode `NOT_APPLICABLE`, length state
  `NOT_APPLICABLE` with null length, SHA `NOT_APPLICABLE`;
- wholly unobservable presence: type/mode `UNKNOWN`, length state
  `UNOBSERVABLE` with null length, SHA `UNOBSERVABLE`;
- known present but type unobservable: type/mode `UNKNOWN`, length state
  `UNOBSERVABLE` with null length, SHA `UNOBSERVABLE`;
- present directory: type `DIRECTORY`; mode observed or `UNKNOWN`; length state
  `NOT_APPLICABLE`/null; SHA `NOT_APPLICABLE`;
- present regular: type `REGULAR`; mode observed or `UNKNOWN`; length state
  `VALUE` with a nonnegative integer or `UNOBSERVABLE` with null; SHA
  `MATCH`, `MISMATCH`, or `UNOBSERVABLE`;
- present symlink/other: that type; mode observed or `UNKNOWN`; length state
  `NOT_APPLICABLE`/null; SHA `NOT_APPLICABLE`.

`type=UNKNOWN` is legal with either `presence=PRESENT` or
`presence=UNOBSERVABLE`; in both cases every dependent metadata field is
unobservable as specified. `byte_length_state=VALUE` requires an integer and is
legal only for a regular file; the other length states require null.

After matrix validation, apply Section 2. With complete visibility, `ABSENT`
requires all rows absent and no extra; `KNOWN_EXPECTED_SUBSET` requires the
exact v9 directory/file mode, expected length, and hash invariants with no extra;
all other fully observed combinations are `KNOWN_MISMATCH`.

## 4. Replacement work inventory

The v9 work object, aggregate states, extra-child enum, directory keys, child
paths, and ordering remain. The directory matrix changes only to allow
`presence=PRESENT,type=UNKNOWN`; that combination requires mode `UNKNOWN` and
owner state `UNOBSERVABLE`. Wholly unobservable presence uses the same dependent
values. Other directory rows retain v9's matrix.

Each child now has exactly:

- `path`, `presence`, `type`, `mode`;
- `byte_length_state`: `VALUE`, `NOT_APPLICABLE`, `UNOBSERVABLE`;
- `byte_length`: nonnegative integer or null;
- `sha256_state`; and
- `target_state`.

The complete child matrix is:

- absent: type `ABSENT`, mode `NOT_APPLICABLE`, length state
  `NOT_APPLICABLE`/null, SHA/target `NOT_APPLICABLE`;
- wholly unobservable presence: type/mode `UNKNOWN`, length state
  `UNOBSERVABLE`/null, SHA/target `UNOBSERVABLE`;
- known present but type unobservable: the same dependent values as wholly
  unobservable presence;
- present regular: mode `0600`/`OTHER`/`UNKNOWN`; length state `VALUE` with
  integer or `UNOBSERVABLE`/null; SHA `MATCH`/`MISMATCH`/`UNOBSERVABLE`;
  target `NOT_APPLICABLE`;
- present symlink: mode `OTHER`/`UNKNOWN`; length state
  `NOT_APPLICABLE`/null; SHA `NOT_APPLICABLE`; target
  `MATCH`/`MISMATCH`/`UNOBSERVABLE`;
- present other: mode `OTHER`/`UNKNOWN`; length state
  `NOT_APPLICABLE`/null; SHA/target `NOT_APPLICABLE`.

`type=UNKNOWN` is legal with known or unknown presence and always triggers the
Section 2 unobservable state. For a regular file, an unavailable length uses
`UNOBSERVABLE`/null without discarding known presence/type. An observed wrong
length remains `VALUE` with its integer and yields known retained only if no
other required fact is unobservable.

After matrix validation, apply Section 2. With complete visibility, `ABSENT`
requires absent directory/children/no extra; `KNOWN_RECOVERABLE` requires every
exact v9/v6 owner/mode/type/length/hash/target invariant; every other fully
observed combination is `KNOWN_RETAINED`.

## 5. Replacement generated-secret client lifecycle

V9's `client_cleanup` is replaced by an object with exactly:

- `password_record`: `NOT_APPLICABLE`, `COMPLETE`, `FAILED`, `UNOBSERVABLE`;
- `panel_fields`: `NOT_APPLICABLE`, `CLEARED`, `FAILED`, `UNOBSERVABLE`;
- `panel_tab`: `NOT_APPLICABLE`, `CLOSED`, `FAILED`;
- `staging_tabs`: `NOT_APPLICABLE`, `CLOSED`, `FAILED`;
- `browser_restart`: `NOT_APPLICABLE`, `COMPLETE`, `FAILED`.

Lifecycle is exact:

- before the credential generator is invoked, every field is
  `NOT_APPLICABLE`;
- once invoked, password record, panel fields, panel tab, and browser restart
  are applicable even if generation/entropy/masking fails and panel enable is
  never submitted; staging tabs remain `NOT_APPLICABLE` until a staging-origin
  tab is opened;
- after panel-enable submission, all five fields are applicable.

For any pre-submit generation/masking failure: do not submit, do not generate a
second credential, blank both masked panel inputs using the form controls
without reading them, navigate the panel tab away, close it, have the human
delete/discard any saved or pending password-manager item, close a staging tab
if one was opened, and restart the in-app browser. The human reports only the
enum results. A creation timeout/ambiguous save uses
`password_record=UNOBSERVABLE`, never a guessed `COMPLETE`.

Any failed/unobservable record or field cleanup, failed panel-tab/staging-tab
close, or failed restart adds `CLIENT_STATE_INCOMPLETE`. Check mappings are:

- record `FAILED`/`UNOBSERVABLE`: `PASSWORD_RECORD_DELETE`;
- fields `FAILED`/`UNOBSERVABLE`: new `PANEL_FIELDS_CLEAR`;
- panel tab `FAILED`: new `PANEL_TAB_CLOSE`;
- staging tabs `FAILED`: `STAGING_TABS_CLOSE`;
- restart `FAILED`: `BROWSER_RESTART`.

The permitted check-ID table adds `PANEL_FIELDS_CLEAR` and `PANEL_TAB_CLOSE`.
Successful clearing/closing records only the enum and never secret bytes. There
is still one credential, one possible submit, and no retry.

## 6. Replacement evidence assembly and local-temp lifecycle

There is no evidence-assembly filesystem workspace. The v9 sentence requiring
one is deleted. Architecture constructs strict manifest/failure JSON bytes,
hashes, base64, decoded tables, and the Markdown evidence body entirely in
process memory, then passes the final text directly to one `apply_patch` update
of the existing `IN_PROGRESS` skeleton.

Only v6's individually downloaded remote-verification files may exist in the
known OS temporary download directory. Its exact file set, individual cleanup,
`LOCAL_TEMP_CLEANUP`, `local_temp_state`, and `LOCAL_STATE_RETAINED` rules remain
v9. It never contains the evidence Markdown or failure object. If final evidence
patch/validation fails, the skeleton/finalization recovery and
`EVIDENCE_FINALIZATION`/`EVIDENCE_INCOMPLETE` rules remain, with no local evidence
file to clean or retain.

## 7. V9 finding closure and authority

- **P1-1:** known presence can coexist truthfully with unknown type or length;
  every dependent field has a total normalization.
- **P1-2:** generator invocation makes panel fields/tab/record/restart cleanup
  applicable even before submit, including pending/ambiguous manager state.
- **P2-1:** unobservable facts always win aggregate precedence after exact matrix
  validation; otherwise the state is computed from fully observed invariants.
- **P2-2:** the evidence workspace is removed; only the already-bound download
  directory exists locally.

Every v8/v9 runtime, cURL, Error Logs, manifest, one-attempt, no-cron, evidence,
and authority safeguard remains. Only a complete successful live evidence record
followed by fresh independent capability PASS may unpark unchanged v3 Section 9
inside the existing IMPLEMENTATION task. No DreamHost deployment, cron, SSH,
Git, staging release, provider secret, live model request, or production action
is granted.
