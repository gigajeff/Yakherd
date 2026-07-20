# Jeff Strict SSOT V1 Package Fresh Red Team Recheck

- Date: 2026-07-20
- Review mode: context-isolated, read-only package review, fail-closed
- Evidence class: review
- Verdict: `fail`
- Authority effect: none; Jeff Strict SSOT V1 remains an unpromoted candidate

## P0 Findings

None.

## P1 Findings

### P1-1: The real CLIs still erase target/root case and reparse evidence before validating it

`bootstrap.py` resolves `args.target` before fresh or retrofit preflight
(`packages/jeff_strict_ssot_v1/bootstrap.py:546-560`). The later component
checks therefore inspect the junction destination and canonical casing, not
the path the operator supplied. The shipped case test calls
`validate_existing_chain()` directly and never exercises `run()`
(`packages/jeff_strict_ssot_v1/tests/test_bootstrap.py:209-218`). The junction
test similarly checks only a destination below an already accepted target
(`test_bootstrap.py:220-234`).

Two bounded Windows probes demonstrated the bypass through the actual CLI:

- retrofit dry-run accepted a junction as `--target`, returned exit `0`, and
  reported the junction destination as the target;
- retrofit dry-run accepted `mixedcasetarget` for the existing
  `MixedCaseTarget`, returned exit `0`, and silently reported canonical case.

Status migration has the same defect because both actions resolve `--root`
before `ensure_under()` and component validation
(`template/scripts/ssot/migrate_status_archive.py:158-165,271-275`). A bounded
probe passed a junction root to `prepare`; it returned `0`, replaced the real
`STATUS.md`, and created the archive through the alias.

This leaves the original exact-case/reparse requirements unresolved at the
operator boundary. Validate the raw absolute path component by component
before any resolution, reject a target/root that is itself a reparse point or
case alias, and then derive the resolved containment identity. Add CLI-level
case and target/root junction tests for fresh, retrofit, prepare, and rollback.

### P1-2: Fresh-install failure cleanup can leave a partial governance tree

Fresh writes add a destination to `created_files` only after writing, syncing,
and post-write hash verification succeed
(`packages/jeff_strict_ssot_v1/bootstrap.py:323-341`). If write, flush, fsync,
readback, or hash verification fails, cleanup does not know that the file was
created (`bootstrap.py:344-356`). The same ordering affects the install
manifest.

A bounded injected post-write-hash failure raised
`post-write hash mismatch: A.txt` but left the target and `A.txt` present. The
current `14` package tests have no fresh write-phase or install-manifest
failure injection. This violates fail-closed partial-write cleanup and was an
explicit gap in the first review.

Journal or register a path immediately when creation succeeds, clean partial
files on every write phase, and add failure tests for payload and install-
manifest open/write/flush/fsync/hash paths.

### P1-3: Status prepare can commit compact status after its archive evidence is corrupted

`prepare` writes the archive, index, and record, but immediately before
replacing `STATUS.md` it rechecks only the current status hash
(`template/scripts/ssot/migrate_status_archive.py:213-235`). The archive has
no post-write hash readback, and the archive/index/record set is not rechecked
as a unit before status replacement or transaction success.

A bounded probe changed the archive during the existing `after_archive`
injection point without raising. `prepare` returned `0`, compacted
`STATUS.md`, retained the tampered archive, and retained an index claiming the
original archive hash. The resulting state has discarded live history while
its recovery evidence is false.

Verify every output after writing and recheck the exact archive, index, and
record bytes immediately before status replacement and final commit. Add
tamper-and-continue races for every prepare and rollback output, not only
injections that throw.

### P1-4: Core validator contracts still have obvious state/evidence bypasses

The evidence validator explicitly accepts `exit_code: null`
(`template/scripts/ssot/validate_protocol.py:301-306`), although the evidence
contract requires the exact command exit code. A current acceptance record
changed only to `exit_code: null` produced zero validation errors. A draft
template may contain null, but supplied completion/test evidence may not pass
with an unknown result.

Decision validation enforces `successor => predecessor status superseded`, but
not the reverse (`validate_protocol.py:449-461`). Changing the bootstrap
decision from `accepted` to `superseded` while leaving `Superseded by: none`
also produced zero decision errors. It can likewise allow a non-accepted
successor to supersede a decision. This does not enforce the advertised
decision state transition.

Require an integer exit code for validated run evidence. Require every
`superseded` decision to name at least one reciprocal successor, and require a
superseding decision to be in an allowed effective state. Add negative tests
for both cases.

## P2 Findings

### P2-1: Acceptance's exact installed-file-set check contains exclusions

`run_acceptance.py` excludes every file under a directory named
`__pycache__` and every `.pyc` from the installed-file census
(`packages/jeff_strict_ssot_v1/tests/run_acceptance.py:136-144`). An arbitrary
unexpected file under that directory, or any unexpected `.pyc`, therefore
does not populate `installed_unexpected`. Acceptance uses `-B`, so the clean
fixture needs no cache exception. Compare every regular installed path to the
authorized set.

The current V3 fixture itself is clean: an independent census without those
exclusions found exactly `43` files, consisting of the `42` authorized
templates plus `JEFF_STRICT_SSOT_INSTALL.json`.

### P2-2: The regression suites do not prove several repaired boundaries

The suites pass, but they do not exercise the actual bootstrap CLI with a
case-aliased or junction target, fresh write/manifest failure cleanup, status
root aliases, rollback TOCTOU/junction behavior, or output tampering that does
not throw. The passing helper-level and injected-exception cases therefore do
not close the bypasses above. Add those cases to the durable package/generated
fixtures and regenerate acceptance.

### P2-3: Release layering is internally consistent but not externally authenticated

Current `RELEASE.json` correctly binds current `bootstrap.py` and
`MANIFEST.json`; the manifest in turn binds all `42` template hashes, and
source-template tampering is refused. The package README also correctly states
that a reviewed Git commit or release must authenticate `RELEASE.json`
itself (`packages/jeff_strict_ssot_v1/README.md:41-46`).

That external boundary is not yet satisfied. The complete `packages/` tree,
plan, implementation record, prompts, and reviews are untracked at local HEAD
`25fd63067d9bf997cd257ad96d399a6f6e9fabd8`; `origin/main` is the same SHA.
GitHub/ChatGPT web therefore cannot authenticate or inspect the candidate.
Even after code repair and recheck, package use needs an intentionally
reviewed commit/release under the repository's human-approved Git boundary.

## P3 Findings

### P3-1: Conflict scanning still misclassifies valid longer fences

The scanner stores only the first three fence characters and treats any later
line starting with those three characters as a close
(`template/scripts/ssot/validate_protocol.py:167-180`). For a valid four-
backtick fence containing a literal line beginning with three backticks, it
incorrectly exits the fence and reports a following full-line `=======` as a
conflict marker. A bounded direct probe returned marker line `[3]` for that
case. Track fence character, opening run length, and valid closing syntax.

Balanced relative links containing nested parentheses worked in both the
shipped fixture and an additional nested-parentheses probe.

### P3-2: Successful migration records retain a pre-commit transaction label

Both migration actions persist and print
`transaction_state: commit_ready_before_status_replace` even after status was
successfully replaced and verified
(`template/scripts/ssot/migrate_status_archive.py:203-212,299-307`). Record the
final committed state after success so durable evidence does not describe a
completed command as still pre-replacement.

## First-Review Recheck Matrix

- Retrofit nested-path containment, expected-state rechecks, lock, backups,
  journal, post-write hashes, rollback, and ordinary temporary cleanup now
  exist, but raw target case/reparse enforcement still fails at the CLI and
  fresh partial-failure cleanup remains unsafe.
- Status strict date, lexical containment, expected-current hash, lock,
  journal, ordinary rollback, and injected write-phase handling now exist, but
  raw root reparse enforcement and commit-set integrity still fail.
- Required-path and owner exact casing/reparse checks, decision ID uniqueness,
  reciprocal references, evidence path/hash containment, and count/size
  constants now exist; null exits and incomplete decision-state semantics
  remain bypasses. Static inspection found no write, subprocess, Git, product
  import, or network path in `validate_protocol.py`.
- The amended architecture plan now explicitly authorizes the status-migration
  fixture. `MANIFEST.json` and validator `REQUIRED_PATHS` contain the same
  exact `42` paths.
- Acceptance V3 contains one conforming record for each of nine commands and
  a distinct aggregate index. All referenced stdout/stderr files and the one
  referenced install-manifest artifact exist and match their hashes.
- Repeated dry-run output is byte-identical, rendered timestamps are derived
  deterministically from the supplied date, and manifest fields differ only
  where target/retrofit identity requires it.
- Manifest/release integrity layering is correct on current bytes, subject to
  the unfulfilled external authentication boundary above.
- Full-line conflict handling is improved and balanced parenthesized links
  pass, but longer-fence handling remains incomplete.

## Independent Verification

- Current package tests: `14/14` passed.
- Current generated repository tests: `19/19` passed.
- Current generated protocol validator: passed with `0` errors and `0`
  warnings.
- Current Governor validator: passed with `0` errors.
- Independently reconciled all `9` run-record schemas, aggregate record hashes,
  referenced stream/artifact hashes, `48` non-cache package snapshot files,
  all `42` source/rendered install entries, and the exact `43`-file installed
  tree; reconciliation errors: `0`.
- Acceptance exits are exactly `0,0,0,0,0,0,0,2,0`; dry-run target is absent.
- No network, dependency install, Git mutation, product compute, or automation
  ran. No package source was repaired. Neither `L:\dev\CROCHET` nor
  `L:\dev\SPLATOMATIC` was inspected or modified.

## Verdict And Downstream Authorization

Verdict: `fail`.

Jeff Strict SSOT V1 may not become current or be used for retrofit or fresh
installation. Separate CROCHET retrofit and SPLATOMATIC fresh-install tasks
may not now be created. A bounded package-only repair must resolve every P1,
the acceptance bypass/test gaps, regenerate fresh acceptance evidence, and
receive another context-isolated Red Team pass. The reviewed release bytes
must then cross the stated external Git/release authentication boundary before
package use.

`STATUS.md` still says the fresh recheck is pending. This task was explicitly
limited to the one review record, so SSOT promotion is still pending and this
review must not be represented as current remote-visible state.

human action required: keep Jeff Strict SSOT V1 and both downstream package-use tasks blocked, and authorize a bounded package-only repair plus regenerated acceptance and another fresh Red Team recheck.
