# Jeff Strict SSOT V1 Package Red Team Recheck V2

- Date: 2026-07-20
- Review mode: context-isolated, fail-closed, current local bytes only
- Evidence class: review
- Verdict: `fail`
- Authority effect: none; package use and downstream package-use tasks remain blocked

## Scope And Boundary

Reviewed the current local bytes of:

- `AGENTS.md` and `STATUS.md`;
- `docs/2026-07-20_jeff_strict_ssot_package_and_crochet_splatomatic_plan.md`;
- `docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_implementation.md`;
- both prior package Red Team reviews;
- every regular file under `packages/jeff_strict_ssot_v1/`, including seven
  existing `.pyc` files; and
- every regular file under
  `test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v5/`.

No package source was repaired. No network, installation, Git mutation,
product compute, or automation was run. `L:\dev\CROCHET` and
`L:\dev\SPLATOMATIC` were not inspected or modified. Their current filesystem
state is therefore intentionally unverified by this review; downstream use is
failed closed regardless.

## P0 Findings

None.

## P1 Findings

### P1-1: Retrofit can certify a tampered commit and can delete the concurrent replacement during rollback

Each retrofit output is hashed only immediately after its own replacement
(`packages/jeff_strict_ssot_v1/bootstrap.py:484-514`). After the loop, the
transaction is marked `committed_verified` and its journal/backups are deleted
without re-reading the complete allowlisted output set
(`packages/jeff_strict_ssot_v1/bootstrap.py:515-517`). A non-throwing writer
can therefore alter an earlier output after its per-file check and before the
commit, and `write_retrofit()` still returns success.

The error path is also not conservative. For every previously replaced path,
rollback unconditionally deletes a path whose reviewed prior state was
`absent`, or unconditionally replaces it from backup, without first proving
that the destination still contains the package-written bytes
(`packages/jeff_strict_ssot_v1/bootstrap.py:526-541`). A concurrent edit made
after replacement is consequently deleted or overwritten. Existing regression
tests cover a change before replacement and exceptions after replacement, but
not a non-throwing post-verification change or rollback preservation of such a
change (`packages/jeff_strict_ssot_v1/tests/test_bootstrap.py:272-317`).

Reproducible bounded evidence from a temporary target under the package parent:

1. Use allowlist `[JEFF_STRICT_SSOT_INSTALL.json, README.md]`, with the install
   manifest expected `absent` and `README.md` hash-guarded.
2. At `after_replace:JEFF_STRICT_SSOT_INSTALL.json`, overwrite that file with
   `external-after-verified-write` and return normally.
3. The call returned successfully, retained those tampered bytes, and removed
   the transaction journal:

   `{"success_returned": true, "tampered_install_bytes": "external-after-verified-write", "journals": 0}`

4. Repeat the overwrite, then raise at `before_replace:README.md`.
5. Rollback deleted the concurrent install-manifest replacement and reported a
   clean rollback:

   `{"error": "later failure", "external_install_preserved": false, "journal_state": "rolled_back_after_failure"}`

This leaves the original retrofit P1 only partially repaired and directly
blocks the planned CROCHET retrofit.

Required fix: retain expected rendered hashes for the whole allowlist, verify
the complete commit set immediately before committing, and during rollback
restore/delete a destination only if it still exactly matches the
package-written bytes. Preserve changed destinations, mark rollback incomplete,
and retain the recovery journal. Add both non-throwing fixtures.

### P1-2: Decision-state parsing accepts ambiguous duplicate fields and rejects valid multi-generation supersession

Decision fields are collected by a dictionary comprehension, so duplicate
field names silently collapse to the last value
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/validate_protocol.py:225-236`).
Appending a second `- Status: proposed` field to the installed bootstrap
decision produced no decision validation error, even though the record then
simultaneously says `accepted` and `proposed`.

The repaired state rules also require every decision that names a predecessor
to remain `accepted`, and require every named direct successor to be currently
`accepted` (`validate_protocol.py:461-476`). That makes an ordinary
three-generation history impossible: once DEC-0002 is superseded by DEC-0003,
DEC-0002 must retain `Supersedes: DEC-0001` but can no longer satisfy the
validator's accepted-state requirement. The tests cover duplicate IDs and one
successor transition, not duplicate fields or a superseded middle decision
(`packages/jeff_strict_ssot_v1/template/tests/ssot/test_validate_protocol.py:121-172`).

Reproducible bounded evidence from temporary copies of the V5 installed tree:

- duplicate `Status` fields: `{"duplicate_status_errors": []}`;
- fully reciprocal chain DEC-0001 -> DEC-0002 -> DEC-0003, with DEC-0001 and
  DEC-0002 superseded and DEC-0003 accepted:

  `{"three_generation_chain_errors": ["decision successor DEC-0002 must be accepted", "superseding decision DEC-0002 must be accepted"]}`

The first result is a fail-open state ambiguity; the second prevents the core
decision register from representing normal durable history.

Required fix: reject duplicate fields in each decision block; permit a decision
with predecessors to be either accepted or later superseded; require only the
current terminal successor to be accepted; and preserve exact reciprocal links
through arbitrary bounded chain length. Add duplicate-field and three-node
fixtures.

## P2 Findings

### P2-1: V5 omits existing bytecode files from its package-source census

The installed-tree census now compares every regular installed path without a
cache exclusion (`packages/jeff_strict_ssot_v1/tests/run_acceptance.py:136-144`),
and the V5 installed fixture is genuinely clean and exact at `43/43`.

However, the separately recorded `package_files` census still excludes every
path under `__pycache__` and every `.pyc`
(`packages/jeff_strict_ssot_v1/tests/run_acceptance.py:215-218`). The installer
also ignores those files while comparing the source-template tree to the
manifest (`packages/jeff_strict_ssot_v1/bootstrap.py:159-165`). Current local
bytes contain `55` package regular files while V5 records only `48`. The seven
omissions are:

- `__pycache__/bootstrap.cpython-313.pyc`;
- `template/scripts/ssot/__pycache__/migrate_status_archive.cpython-313.pyc`;
- `template/scripts/ssot/__pycache__/validate_protocol.cpython-313.pyc`;
- `template/tests/ssot/__pycache__/test_status_archive_migration.cpython-313.pyc`;
- `template/tests/ssot/__pycache__/test_validate_protocol.cpython-313.pyc`;
- `tests/__pycache__/run_acceptance.cpython-313.pyc`; and
- `tests/__pycache__/test_bootstrap.cpython-313.pyc`.

Thus the prior exact *installed-tree* finding is closed, but V5 is not an exact
snapshot of all current package bytes. `-B` prevents new bytecode writes; it
does not establish that existing bytecode was absent from every import path.

Required fix: produce acceptance from a bytecode-free package tree and make the
package-source census include every regular file, failing on any unexpected
cache/bytecode path instead of excluding it.

### P2-2: Evidence timestamp validation accepts a date-only value as a UTC timestamp

The evidence validator checks only that `timestamp_utc` is a string ending in
`Z`, replaces `Z` with `+00:00`, and calls `datetime.fromisoformat()`
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/validate_protocol.py:300-307`).
It does not require a time component or verify an aware UTC result. The bounded
probe supplied `timestamp_utc: "2026-07-20Z"`; validation returned no errors:

`{"timestamp_utc": "2026-07-20Z", "errors": []}`

The fixture suite checks an obviously malformed timestamp but not this reduced
date bypass (`packages/jeff_strict_ssot_v1/template/tests/ssot/test_validate_protocol.py:199-216`).

Required fix: parse an exact UTC date-time grammar, require a time component
and UTC-aware result, and add reduced-date/naive timestamp negative fixtures.

## P3 Findings

None open from the prior reviews. The long-fence parser now tracks marker
character and opening run length correctly
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/validate_protocol.py:167-191`),
and its four-backtick regression fixture passed.

## Prior-Finding Recheck Matrix

- Raw CLI case/junction enforcement for fresh and retrofit: closed on current
  bytes. `run()` keeps the absolute spelling for component validation instead
  of resolving aliases (`packages/jeff_strict_ssot_v1/bootstrap.py:573-603`).
  Windows case-alias and junction production-entry fixtures passed.
- Raw CLI case/junction enforcement for prepare and rollback: closed on current
  bytes. Both actions validate the absolute root before use
  (`template/scripts/ssot/migrate_status_archive.py:195-205,331-338`). Both
  Windows action fixtures passed.
- Fresh cleanup at create/write/flush/fsync/hash/install-manifest phases: closed
  for the named injected phases. Created paths are registered immediately
  after creation (`bootstrap.py:320-389`); all ten phase fixtures and the
  post-write hash fixture passed.
- Status archive/index/record/status commit-set integrity: closed for the named
  non-throwing and throwing fixtures. Prepare re-verifies all existing members
  before status replacement and the full set before commit
  (`migrate_status_archive.py:265-293`); rollback does likewise
  (`migrate_status_archive.py:371-395`). Conservative status rollback and
  changed-output handling passed.
- Mandatory integer evidence exit code: closed. `null` and booleans are rejected
  (`validate_protocol.py:313-315`), and the negative fixtures passed.
- Decision supersession state/reciprocity: not closed; see P1-2.
- Exact installed tree with no cache exclusions: closed for the installed V5
  fixture at `43/43`; the package-source evidence remains incomplete under P2-1.
- Long Markdown fences: closed; the durable fixture and direct behavior passed.
- Final committed transaction state: closed for ordinary successful prepare
  and rollback. Durable records use `committed_verified`
  (`migrate_status_archive.py:244-253,362-370`), and both success assertions
  passed.
- Manifest/release hash chain: internally correct on current bytes.
  `RELEASE.json` matches current `bootstrap.py` and `MANIFEST.json`; the manifest
  matches all `42` template hashes; all installed rendered hashes match.
  External authentication remains unfulfilled as described below.
- Acceptance evidence and determinism: all nine record/stream/artifact hashes
  reconciled; exits are `0,0,0,0,0,0,0,2,0`; repeated dry-run stdout/stderr is
  byte-identical; the dry-run target is absent; the installed tree has no
  missing, unexpected, cache, bytecode, or reparse paths. P2-1 limits the
  package-source snapshot claim.

## Independent Checks

- Current package tests: `19/19` passed under bytecode-write suppression.
- Current generated-repository tests: `26/26` passed under bytecode-write
  suppression.
- Generated protocol validator: passed with `0` errors and `0` warnings.
- Generated Governor validator: passed with `0` errors.
- V5 run records: `9/9` schemas and all referenced stream/artifact hashes
  reconciled against current evidence bytes.
- Exact installed tree: `43` expected / `43` actual, with `42/42` rendered
  payload hashes and no reparse points.
- Source chain: `RELEASE.json` -> `bootstrap.py`/`MANIFEST.json` -> all `42`
  templates reconciled with zero mismatch.
- Direct bounded negative probes reproduced P1-1, P1-2, and P2-2.

These checks are protocol evidence only. They do not validate a product.

## Git And Reviewed-Release Boundary

This boundary is separate from source correctness and is not satisfied:

- branch: `main`;
- HEAD: `25fd63067d9bf997cd257ad96d399a6f6e9fabd8`;
- upstream: `origin/main@25fd63067d9bf997cd257ad96d399a6f6e9fabd8`;
- ahead/behind: `0/0`;
- working tree: dirty with extensive pre-existing/current local work;
- package, plan, implementation record, and package reviews: untracked at the
  reviewed HEAD;
- remote visibility: the candidate package and this local review are not
  inspectable by ChatGPT web or other remote reviewers.

Current internal hashes do not authenticate `RELEASE.json` externally. Even a
future source-correct package requires an intentionally reviewed commit/release
before downstream use.

## Verdict And Authorization

Verdict: `fail`.

Jeff Strict SSOT V1 may not be promoted or used for fresh installation or
retrofit. The CROCHET retrofit task and SPLATOMATIC installation/bootstrap task
may not be created. A bounded package-only repair must resolve both P1s and the
P2 evidence gaps, remove/strictly reject source-tree bytecode, regenerate clean
acceptance evidence, and receive another context-isolated Red Team pass. Only
then may an explicitly reviewed Git commit/release authenticate the package for
downstream use.

`STATUS.md` and the package plan were not modified because this review was
authorized to write exactly one durable record. Their existing operative block
remains correct, but promotion of this V2 result into broader project indexes
is still pending.

human action required: keep Jeff Strict SSOT V1, the CROCHET retrofit task, and the SPLATOMATIC bootstrap task blocked; authorize only a bounded package-repair and clean-acceptance task followed by a fresh independent recheck.
