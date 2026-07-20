# Jeff Strict SSOT V1 Package Implementation

Date: 2026-07-20
Status: clean acceptance V6 and independent source-correctness recheck V3 passed; reviewed Git/release authentication pending
Authority effect: package candidate evidence only

## Scope

Implemented only:

`packages/jeff_strict_ssot_v1/`

The package contains its README, package manifest, standard-library bootstrap,
source templates, package tests, and durable acceptance runner. It creates the
exact product-neutral root/docs/scripts/tests structure authorized by
`docs/2026-07-20_jeff_strict_ssot_package_and_crochet_splatomatic_plan.md`.

No file under `L:\dev\CROCHET` or `L:\dev\SPLATOMATIC` was read or changed by
this implementation task. No product prompt was ingested.

## Implemented Boundaries

- Fresh mode accepts only a nonexistent or empty target and refuses every
  overwrite.
- Dry-run performs full package/template/target preflight and writes nothing.
- Retrofit mode requires `reviewed: true`, an exact sorted allowlist, expected
  SHA-256 or `absent` state for every allowed path, target identity, and an
  allowlisted install manifest.
- Template rendering replaces project/date placeholders deterministically.
- `JEFF_STRICT_SSOT_INSTALL.json` records package-manifest hash and per-file
  source-template/rendered hashes.
- Bootstrap and installed runtime utilities use Python's standard library only.
- Bootstrap performs no network access, dependency installation, product
  command, automation creation, product-prompt ingestion, or Git mutation.
- The pure protocol validator has no subprocess, product import, network, Git,
  or write surface.
- Status migration is a separate mutating tool with exact-byte archive,
  indexed hash evidence, and hash-guarded rollback.
- The installed Governor remains inactive and non-authoritative.

## Acceptance Evidence

Superseded pre-review evidence root:

`test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v2/`

Superseded repaired-candidate evidence root:

`test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v3/`

Current repaired-candidate evidence root:

`test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v6/`

Aggregate index:

`test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v6/acceptance_aggregate.json`

Results:

- acceptance status: `passed`;
- commands: `9` with expected exit sequence `0,0,0,0,0,0,0,2,0`;
- installed payload files hash-verified: `42`;
- exact installed regular-file tree: `43/43`;
- installed hash mismatches: `0`;
- installed missing/unexpected files: `0/0`;
- dry-run target created: `false`;
- repeated dry-run stdout/stderr: byte-identical;
- package tests: `21 passed`;
- generated-repository tests: `27 passed`;
- generated protocol validator: `passed`, zero errors/warnings;
- generated Governor validator: `passed`, zero errors;
- structured command evidence records validated: `9/9`;
- second fresh install: refused with nonzero exit;
- positive reviewed/hash-guarded retrofit: passed and left a non-allowlisted
  product file byte-identical;
- exact-case, Windows junction/reparse, traversal, concurrent-state change,
  injected write-phase rollback, temporary cleanup, source tampering, status
  line/byte caps, owner path, decision reciprocity, evidence limits/hashes,
  quiet-write, and archive/rollback hash failures have negative tests.

Each executed acceptance command has its own schema-conforming
`NN_run_record.json` with exact argv, environment, exit code, bounded raw
stdout/stderr paths and hashes. `acceptance_aggregate.json` is explicitly an
index, not a command run record.

The earlier `acceptance_v1` record is superseded test evidence because the
package subsequently added archive/rollback and standard-library checks.

## Limitations

- The fresh repaired-candidate recheck also failed with four P1 findings.
- No real product repository has installed or adopted it.
- CROCHET retrofit and SPLATOMATIC installation remain separate future tasks.
- This validates protocol mechanics, not any future product.
- No Governor activation, cadence, or automation is authorized.
- No Git staging, commit, push, branch, remote, or publication occurred.

## Next Gate

Acceptance V5 and current source bytes must receive another context-isolated
Red Team review. Only a `pass` or fully resolved `pass_with_fixes` may promote
V1 for use. A reviewed Git commit/release must then authenticate
`RELEASE.json` before downstream installation.

## First Independent Review

The fresh review at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_review.md`
returned `fail`. Its blocking findings are:

- P1-1: retrofit reparse/containment, TOCTOU, and rollback gaps;
- P1-2: status migration traversal and partial-transaction gaps;
- P1-3: exact-casing/reparse, decision, and evidence-validator bypasses;
- P2: exact-tree mismatch, nonconforming acceptance records, incomplete safety
  tests/determinism checks, and no installer-enforced template hash baseline;
- P3: conflict/link scanner false-positive cases.

The package remains unpromoted. Acceptance V2 and V3 are superseded candidate
evidence; V5 is the current passing candidate evidence.

## Bounded Repair

The repaired package now adds:

- component-by-component exact-case and reparse/junction rejection;
- cooperative locks, expected-state rechecks immediately before replacement,
  post-write hashes, verified backups, transaction journals, rollback, and
  failure-injection coverage for retrofit and status migration;
- strict date, containment, hash, evidence-schema, evidence-size, decision
  uniqueness/state/owner/reciprocity, conflict-marker, and balanced-link
  validation;
- an explicitly authorized status-migration fixture in the exact installed
  tree;
- deterministic rendered timestamps and repeated dry-run evidence;
- `MANIFEST.json` source hashes for all 42 templates; and
- `RELEASE.json`, which binds the bootstrap and manifest. The reviewed Git
  commit/release remains the external authentication boundary for that release
  record.

## Fresh Recheck

The fresh review at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_recheck.md`
returned `fail`. Its blocking findings are:

- P1-1: the real bootstrap and status-migration CLIs resolve raw target/root
  paths before exact-case and reparse-point validation;
- P1-2: a failed fresh install can leave a partially created governance tree;
- P1-3: status migration can replace live status after archive evidence is
  corrupted; and
- P1-4: null evidence exit codes and incomplete decision-supersession rules
  can pass validation.

The review also requires exact installed-file census without cache exclusions,
CLI-level and non-throwing race regression coverage, correct long-fence
parsing, final committed migration state, and external Git/release
authentication after a passing recheck. No downstream package-use task is
authorized.

## Post-Recheck Bounded Repair

The current candidate adds:

- raw absolute target/root validation through the real fresh, retrofit,
  prepare, and rollback CLIs before path resolution, with Windows case-alias
  and junction tests;
- immediate fresh-install creation journaling plus cleanup tests at create,
  write, flush, fsync, post-hash, and install-manifest phases;
- exact archive/index/record/status commit-set verification before status
  replacement and final commit, non-throwing tamper race tests, conservative
  handling of externally changed status, and final `committed_verified`
  records;
- mandatory integer evidence exit codes, reciprocal accepted decision
  successor semantics, and negative tests;
- exact installed regular-file census with no `__pycache__` or `.pyc`
  exclusions; and
- fence parsing that tracks marker character and opening run length.

Acceptance V5 passed with `43/43` exact installed files, `42/42` payload
hashes, `26/26` generated tests, `19/19` package tests, and `9/9` structured
command records. Root governance validation, Governor policy validation,
`tests/test_reference_frames.py` (`9 passed`), JSON parsing, and scoped
`git diff --check` also pass. No product repository was inspected or changed.

## Independent Recheck V2

The review at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_recheck_v2.md`
returned `fail`. It found:

- P1-1: retrofit can certify an earlier allowlisted output that changes after
  per-file verification, and rollback can overwrite/delete that concurrent
  replacement;
- P1-2: duplicate decision fields are silently collapsed and the state rules
  reject a valid three-generation supersession chain;
- P2-1: acceptance omits existing source-package bytecode from its package
  snapshot; and
- P2-2: a date-only `timestamp_utc` value can pass evidence validation.

The package, CROCHET retrofit, and SPLATOMATIC bootstrap remain unauthorized.

## Post-Recheck V2 Bounded Repair

The current candidate adds:

- whole-allowlist retrofit verification immediately before commit;
- rollback that restores/deletes only package-written bytes and preserves an
  externally changed destination with a retained `rollback_failed` journal;
- decision parser rejection of duplicate fields and valid reciprocal
  multi-generation supersession semantics;
- exact UTC date-time evidence grammar with reduced-date/naive/offset negative
  fixtures; and
- exact package-source census with bytecode/cache rejection. Seven generated
  `.pyc` files were removed, and acceptance records all `48` current source
  files with zero cache paths.

Clean acceptance V6 passed with exact installed tree `43/43`, payload hashes
`42/42`, generated tests `27/27`, package tests `21/21`, and command records
`9/9`.

## Independent Recheck V3

The fresh context-isolated review at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_recheck_v3.md`
returned `pass` for current package source and acceptance V6, with no open
P0-P3 findings. It independently reconciled the `48`-file source snapshot,
`42/42` template hash chain, `43/43` installed tree, and all V2 repairs.

This pass does not authenticate local untracked bytes to GitHub or another
machine. Package use remains blocked until an intentional reviewed Git
commit/release authenticates `RELEASE.json` and the exact passing source.

## Scoped Release Authentication Authorization

Jeff authorized scoped staging, commit, and push of the reviewed package,
package governance records, and the package-specific `STATUS.md` decision. The
commit containing
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_release_authentication.md`
is the reviewed external authentication boundary once present on
`origin/main`. This authorization does not include unrelated dirty-worktree
files and does not authorize modifying CROCHET or SPLATOMATIC.

autonomous next action: stage, validate, commit, and push only the authorized package release scope.
