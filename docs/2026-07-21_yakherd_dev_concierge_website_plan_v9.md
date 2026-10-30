# Yakherd.dev Concierge Website Plan v9 — Tri-State Evidence Amendment

Date: 2026-07-21

Status: proposed; blocked pending fresh independent Red Team PASS

## 1. Exact composite and precedence

The exact v9 candidate is frozen v3 plus incorporated v5, v6, v7, v8, and this
amendment. Their SHA-256 identities are:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v8 FAIL audit:
  `d895ce12b8c648a56a9e91da2a9aa388dcde8988511280ca4d17a2d0c00f6f3b`.

V9 replaces v8 Sections 3, 3.1, 3.2, 3.3, and their top-level failure-object
fields. It adds the attempt/evidence bootstrap in Section 5. V8's strict
serialization/embedding rule remains except for the new exact fields and enums.
V8's PHP Appendix identity and bytes remain unchanged: 7,279 bytes, SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.
Every incorporated cron action remains removed; every deployment action remains
withheld.

No DreamHost, credential, fixture, network, Implementation, Git, cron, SSH,
staging release, provider-secret, or production action is authorized until a
fresh independent PASS on this exact composite.

## 2. Attempt boundary and evidence bootstrap

An attempt does not start until:

1. v9 has an independent plan PASS;
2. Architecture creates the sole capability evidence file at
   `docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_capability.md` with
   `Status: IN_PROGRESS`, exact plan hashes, a non-secret UTC attempt ID, and no
   live claim; and
3. `python scripts/verify_release.py` and `git diff --check` pass with that
   skeleton present.

If skeleton creation/validation fails, no attempt starts and no live or client
action is authorized. The exact check ID is `EVIDENCE_FINALIZATION`, reported in
the Architecture task; the absent/unvalidated evidence file itself prevents any
independent PASS.

The attempt starts at the first read-only staging-certificate check. Certificate,
root, and File Manager failures therefore receive a normal failure object but
all credential/session cleanup fields are `NOT_APPLICABLE`.

The evidence body is assembled and strict-validated in one known OS temporary
directory before one final `apply_patch` update. If finalization fails, the
existing `IN_PROGRESS` skeleton is retained and is unconditionally capability
FAIL. Exactly one recovery update may replace it with a failure record containing
`EVIDENCE_FINALIZATION`; if that also fails, stop with the skeleton unchanged.
No incomplete skeleton or thread report can authorize Implementation.

## 3. Replacement top-level failure object

Every started attempt that does not pass has one object with exactly:

- `schema_version`: integer `2`;
- `capability_result`: literal `FAIL`;
- `failed_checks`: nonempty sorted unique array from Section 4;
- `failure_classes`: sorted unique array from Section 4; it may be empty;
- `panel_inventory`: `NONE`, `BOTH_ENABLED`, `HTACCESS_ONLY`,
  `HTPASSWD_ONLY`, `BOTH_STATUS_MISMATCH`, or `UNOBSERVABLE`;
- `fixture_inventory`: exact Section 3.1 object;
- `work_inventory`: exact Section 3.2 object;
- `local_temp_state`: `ABSENT`, `KNOWN_RETAINED`, or `UNOBSERVABLE`;
- `client_cleanup`: exact Section 3.3 object;
- `cleanup_utc`: RFC 3339 whole-second UTC or null; and
- `notes_present`: boolean only.

Unknown/missing keys and invalid/unsorted/duplicate values are rejected. The
canonical JSON/base64/SHA-256 evidence embedding remains v8 Section 3.4.

### 3.1 Exact fixture inventory and derivation

`fixture_inventory` has exactly `state`, `extra_entry_state`, and `entries`.
`state` is `ABSENT`, `KNOWN_EXPECTED_SUBSET`, `KNOWN_MISMATCH`, or
`UNOBSERVABLE`. `extra_entry_state` is `NONE`, `PRESENT`, or `UNOBSERVABLE`.

Entries are the same five v8 rows in the same order. Each row has exactly:

- `path`: the v8 exact path enum;
- `presence`: `PRESENT`, `ABSENT`, or `UNOBSERVABLE`;
- `type`: `ABSENT`, `DIRECTORY`, `REGULAR`, `SYMLINK`, `OTHER`, or `UNKNOWN`;
- `mode`: `NOT_APPLICABLE`, `UNKNOWN`, `OTHER`, `0444`, or `0755`;
- `byte_length`: nonnegative integer or null; and
- `sha256_state`: `MATCH`, `MISMATCH`, `UNOBSERVABLE`, or `NOT_APPLICABLE`.

The complete row matrix is:

- `presence=ABSENT` requires `type=ABSENT`, `mode=NOT_APPLICABLE`, null length,
  and `sha256_state=NOT_APPLICABLE`;
- `presence=UNOBSERVABLE` requires `type=UNKNOWN`, `mode=UNKNOWN`, null length,
  and `sha256_state=UNOBSERVABLE`;
- a present `fixture` directory uses `type=DIRECTORY`, null length, and
  `sha256_state=NOT_APPLICABLE`; mode is observed `0755`, `OTHER`, or `UNKNOWN`;
- a present known source path with `type=REGULAR` uses observed nonnegative
  length, mode `0444`/`OTHER`/`UNKNOWN`, and SHA state
  `MATCH`/`MISMATCH`/`UNOBSERVABLE`;
- a present `SYMLINK` or `OTHER` row uses null length,
  `sha256_state=NOT_APPLICABLE`, and mode `OTHER` or `UNKNOWN`; and
- `type=UNKNOWN` is legal only with `presence=UNOBSERVABLE`.

State derivation is deterministic:

- `UNOBSERVABLE` iff extra-entry state or any row presence/mode/SHA fact required
  to classify the observed path is `UNOBSERVABLE`/`UNKNOWN`;
- otherwise `ABSENT` iff extra-entry state is `NONE` and all five rows are
  absent;
- otherwise `KNOWN_EXPECTED_SUBSET` iff extra-entry state is `NONE`, `fixture`
  is a `0755` directory, every present source file is regular mode `0444` with
  exact expected length and SHA `MATCH`, and every other known row is absent;
- otherwise `KNOWN_MISMATCH`.

An extra entry that is known to exist but whose name is deliberately not
captured uses `extra_entry_state=PRESENT` and derives `KNOWN_MISMATCH`. Lost
visibility uses `UNOBSERVABLE`; it never guesses presence. A known regular file
whose individual download/hash cannot be observed uses
`sha256_state=UNOBSERVABLE` and derives `UNOBSERVABLE`, not `MISMATCH`.

### 3.2 Exact work inventory and derivation

`work_inventory` has exactly `state`, `extra_child_state`, `directory`, and
`children`. `state` is `ABSENT`, `KNOWN_RECOVERABLE`, `KNOWN_RETAINED`, or
`UNOBSERVABLE_RETAINED`. `extra_child_state` is `NONE`, `PRESENT`, or
`UNOBSERVABLE`.

`directory` has exactly `presence`, `type`, `mode`, and `owner_state`:

- presence: `PRESENT`, `ABSENT`, or `UNOBSERVABLE`;
- type: `ABSENT`, `DIRECTORY`, `SYMLINK`, `OTHER`, or `UNKNOWN`;
- mode: `NOT_APPLICABLE`, `0700`, `OTHER`, or `UNKNOWN`;
- owner state: `MATCH`, `MISMATCH`, `UNOBSERVABLE`, or `NOT_APPLICABLE`.

Absent requires `ABSENT`/`NOT_APPLICABLE`/`NOT_APPLICABLE`; unobservable
requires `UNKNOWN`/`UNKNOWN`/`UNOBSERVABLE`; present directory uses
`DIRECTORY`, observed mode, and observed owner state; a present symlink/other
uses that type, `OTHER`/`UNKNOWN` mode, and observed or unobservable owner state.

Children remain exactly `first.bin`, `link.bin`, `second.bin`, sorted. Each row
has exactly `path`, `presence`, `type`, `mode`, `byte_length`, `sha256_state`, and
`target_state`. The enum sets are:

- presence: `PRESENT`, `ABSENT`, `UNOBSERVABLE`;
- type: `ABSENT`, `REGULAR`, `SYMLINK`, `OTHER`, `UNKNOWN`;
- mode: `NOT_APPLICABLE`, `0600`, `OTHER`, `UNKNOWN`;
- SHA and target state: `MATCH`, `MISMATCH`, `UNOBSERVABLE`,
  `NOT_APPLICABLE`.

The complete child matrix is:

- absent: `ABSENT`, `NOT_APPLICABLE`, null length, both states
  `NOT_APPLICABLE`;
- unobservable: `UNKNOWN`, `UNKNOWN`, null length, both states
  `UNOBSERVABLE`;
- present regular: observed nonnegative length, mode `0600`/`OTHER`/`UNKNOWN`,
  SHA `MATCH`/`MISMATCH`/`UNOBSERVABLE`, target `NOT_APPLICABLE`;
- present symlink: null length, mode `OTHER`/`UNKNOWN`, SHA
  `NOT_APPLICABLE`, target `MATCH`/`MISMATCH`/`UNOBSERVABLE`; and
- present other: null length, mode `OTHER`/`UNKNOWN`, both states
  `NOT_APPLICABLE`.

State derivation is deterministic:

- `UNOBSERVABLE_RETAINED` iff directory/extra-child state or any required child
  fact is unobservable/unknown;
- otherwise `ABSENT` iff directory is absent, all children absent, and no extra
  child exists;
- otherwise `KNOWN_RECOVERABLE` iff directory is a dedicated-owner `0700` real
  directory, no extra child exists, and every present child exactly matches the
  v6 permitted type/mode/length/hash/target while absent children follow the
  absent matrix;
- otherwise `KNOWN_RETAINED`.

### 3.3 Exact client cleanup N/A semantics

`client_cleanup` has exactly `password_record`, `staging_tabs`, and
`browser_restart`. Each is `NOT_APPLICABLE`, `COMPLETE`, or `FAILED`.

- Before any password-manager record is created, all three are
  `NOT_APPLICABLE`.
- If a password record is created but no panel-enable submission occurs,
  `password_record` is `COMPLETE` or `FAILED`; tabs and restart are
  `NOT_APPLICABLE`.
- Once panel enable is submitted, all three are applicable and each is
  `COMPLETE` or `FAILED`, regardless of enable outcome.

Any `FAILED` client field adds its exact failed-check ID and
`CLIENT_STATE_INCOMPLETE`. `NOT_APPLICABLE` never claims an action occurred.

## 4. Replacement check/class table and exact edge mappings

V8's check IDs remain and add:

- `CREDENTIAL_APPROVAL`, `CREDENTIAL_GENERATION`, `CREDENTIAL_MASKING`;
- `EVIDENCE_FINALIZATION`;
- `LOCAL_TEMP_CLEANUP`.

V8's failure classes remain and add `LOCAL_STATE_RETAINED` and
`EVIDENCE_INCOMPLETE`.

Exact edge mappings are:

- a human declines after the attempt starts: `CREDENTIAL_APPROVAL`, no password
  record, all client fields `NOT_APPLICABLE`, clean remote state;
- generator cannot prove at least 128 bits: `CREDENTIAL_GENERATION`; if it
  created a record, password cleanup becomes applicable;
- masked fields cannot be proved before submit: `CREDENTIAL_MASKING`; do not
  submit panel enable; clean/delete any created record;
- an individual verification download or its known OS temporary directory
  cannot be deleted: `LOCAL_TEMP_CLEANUP`, `local_temp_state=KNOWN_RETAINED`, and
  class `LOCAL_STATE_RETAINED`; if visibility of that known temp location is
  lost, state `UNOBSERVABLE` with the same class;
- failure to build/strict-validate/update the final evidence:
  `EVIDENCE_FINALIZATION` plus `EVIDENCE_INCOMPLETE`; the `IN_PROGRESS` skeleton
  remains an unconditional block under Section 2;
- failure to preserve either canonical manifest preimage or failure-object
  preimage: both `MANIFEST_EVIDENCE` and `EVIDENCE_FINALIZATION`;
- password, tab, or restart cleanup failure uses its existing exact check ID and
  `CLIENT_STATE_INCOMPLETE`;
- all other gates retain v8's explicit mapping.

Local retained files contain only the non-secret Appendix/manifest bytes; their
exact known temporary directory is never broadened into recursive delete
authority. Cleanup remains individually named. No local cleanup failure changes
remote/client cleanup or authorizes another live attempt.

## 5. V8 finding closure and authority

- **P1-1:** every presence/extra/hash/target/owner observation is tri-state;
  unobservability never forces a guessed boolean or false mismatch.
- **P2-1:** complete per-type matrices and deterministic state derivation close
  contradictory/ambiguous inventories.
- **P2-2:** attempt starts after the evidence skeleton and before certificate
  inventory; exact client enums express pre-credential N/A without claiming work.
- **P2-3:** local-temp cleanup, evidence finalization/preimages, credential
  approval/generation/masking, and retained local/evidence state have exact IDs
  and dispositions.

The sole evidence path and all v8 runtime/log/manifest/credential safeguards
remain. Only complete successful evidence followed by a fresh independent live
capability PASS may unpark the unchanged v3 Section 9 local write set in the
existing IMPLEMENTATION task. No DreamHost deployment, cron, SSH, Git, staging
release, provider secret, live model request, or production action is granted.
