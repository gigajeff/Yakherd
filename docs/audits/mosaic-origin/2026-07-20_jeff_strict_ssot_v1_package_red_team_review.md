# Jeff Strict SSOT V1 Package Fresh Red Team Review

- Date: 2026-07-20
- Review mode: fresh context-isolated, repository evidence only
- Evidence class: review
- Verdict: `fail`
- Authority effect: none; the package remains a candidate and may not become current or usable

## P0 Findings

None.

## P1 Findings

### P1-1: Retrofit writes can escape through reparse parents and can overwrite post-review changes

`bootstrap.py` joins each allowlisted name to the target and follows normal
filesystem resolution when checking it, but never proves that every destination
component remains beneath the target or rejects symlinks, junctions, and other
reparse points (`packages/jeff_strict_ssot_v1/bootstrap.py:145-164`). The write
path then creates parent directories, creates a temporary file in the resolved
parent, and replaces the destination without a containment or reparse check
(`packages/jeff_strict_ssot_v1/bootstrap.py:249-259`). An allowlisted path such
as `docs/task_protocol.md` therefore writes outside the repository when `docs`
is a junction to another directory and the reviewed expected hash matches the
external file.

The expected hash is checked only during preflight
(`packages/jeff_strict_ssot_v1/bootstrap.py:153-163`). The later write reads a
new backup and replaces the file without rechecking that hash
(`packages/jeff_strict_ssot_v1/bootstrap.py:249-259`). A change between those
operations is silently overwritten. The rollback block tracks replaced files
only; it does not remove newly created parent directories or a temporary file
left by a failed `os.replace` (`packages/jeff_strict_ssot_v1/bootstrap.py:246-268`).
This does not satisfy the package's reviewed-state, expected-hash, containment,
TOCTOU, rollback, or partial-write safety claims.

Required fix: reject reparse points in the target and every destination parent;
resolve and prove containment component by component; validate exact casing;
recheck each expected state immediately before replacement under an exclusive
target transaction/lock; verify each post-write hash; and journal all temporary
files, created directories, replacements, and rollback outcomes. Add bounded
Windows junction/symlink, race/state-change, injected-failure, temporary-file,
and created-directory cleanup tests.

### P1-2: Status migration has a path traversal and can leave an unrecorded partial migration

The migration tool builds the archive filename directly from unvalidated
`--date` input (`packages/jeff_strict_ssot_v1/template/scripts/ssot/migrate_status_archive.py:53-55,118-120`).
Unlike the candidate and record paths, the archive and index are not passed
through `ensure_under`. On Windows, a value containing enough backslash-separated
`..` components resolves the archive outside the repository. Archive parents
are also not checked for junction/reparse escape.

Preparation has no reviewed expected-current hash. It reads `STATUS.md`, then
writes archive, index, live status, and record as four independent replacements
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/migrate_status_archive.py:45-80`).
A concurrent status change can be lost, and a failure after replacing status
can leave compact status active without the required record. Rollback similarly
replaces status before writing its evidence record
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/migrate_status_archive.py:92-107`).

Required fix: parse and canonicalize `--date` as ISO `YYYY-MM-DD`; containment-
check archive, index, record, status, and all parent components; reject reparse
points; require an expected-current hash for prepare and recheck it immediately
before commit; implement a recoverable transaction/journal with cleanup and
post-write verification; and add traversal, junction, TOCTOU, and failure-at-
every-write tests for prepare and rollback.

### P1-3: The pure validator can pass repositories that violate its advertised core contracts

The required-path check uses `Path.is_file()` and labels the result "exact
casing" (`packages/jeff_strict_ssot_v1/template/scripts/ssot/validate_protocol.py:138-141`).
On the reviewed Windows fixture, both `AGENTS.md` and nonexistent-case
`agents.md` returned `is_file=True`; casing is therefore not enforced. Required
paths and owner paths also follow symlinks/reparse points without proving they
remain under the repository (`validate_protocol.py:138-149,188-195`).

Decision validation checks only that eight labels occur in each block
(`validate_protocol.py:197-204`). It does not validate unique IDs, status,
current-owner existence, exact owner links, or reciprocal predecessor/successor
supersession. Contradictory transitions therefore pass.

Evidence validation checks top-level field presence, schema/class, whether
`command` is a list, and whether each artifact has two keys
(`validate_protocol.py:112-130`). It does not validate UTC format, exit-code
type, environment identity, stdout/stderr structure, limitations, authority
effect, artifact path containment/existence/hash, or bounded file size/count.
Explicit evidence paths are resolved and read without repository containment
or a count/byte limit (`validate_protocol.py:240-241`). Fabricated or unbounded
evidence can pass or force unbounded reads.

Required fix: enumerate path components to enforce exact casing and repository
containment; reject reparse escapes; structurally parse owner and decision
records; enforce unique decision IDs, allowed states, existing current owners,
and reciprocal supersession; fully validate the run-record schema and artifact
hashes; and impose explicit evidence count and byte limits. Add negative tests
for each bypass, including Windows casing and reparse fixtures.

## P2 Findings

### P2-1: The installed tree exceeds the exact authorized tree

The authorized plan calls its installed structure exact and lists only
`test_governor_delta_policy.py` and `test_validate_protocol.py` under generated
tests (`docs/2026-07-20_jeff_strict_ssot_package_and_crochet_splatomatic_plan.md:76-135`).
The package manifest additionally installs
`tests/ssot/test_status_archive_migration.py`
(`packages/jeff_strict_ssot_v1/MANIFEST.json:48-50`). The validator mirrors the
authorized 41 paths and does not require this 42nd template
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/validate_protocol.py:15-57`).
The file is useful, but it was not in the exact authorized tree.

Required fix: explicitly amend/supersede the authorized tree to include the
migration fixture, then add it to `REQUIRED_PATHS`; otherwise remove it. Do not
resolve this by silently treating the manifest as retroactive authorization.

### P2-2: The acceptance record is not a conforming structured run record

The package contract requires environment identity, one exact command and exit
code, bounded stdout/stderr or exact raw-output paths, and artifact hashes
(`packages/jeff_strict_ssot_v1/template/docs/validation_protocol.md:12-26`). The
acceptance runner instead emits an aggregate `commands` array and omits the
top-level `command`, `exit_code`, `environment`, `stdout`, `stderr`, and
`artifacts` fields (`packages/jeff_strict_ssot_v1/tests/run_acceptance.py:129-152`).
The resulting record closes at line 591 without those fields
(`test_output/experiments/jeff_strict_ssot_v1_package_2026-07-20/acceptance_v2/acceptance_record.json:585-591`).
Passing it to the installed validator fails. The implementation report's claim
of a structured acceptance record is therefore overstated.

Required fix: write one schema-conforming record per command plus a separately
versioned aggregate, include machine/OS/runtime identity and bounded output
references/hashes, validate every generated record, and make acceptance fail if
record validation fails.

### P2-3: Acceptance and negative tests do not cover the named safety gates

The bootstrap tests cover ordinary fresh installs, ordinary overwrite refusal,
one unreviewed plan, and one positive allowlist case
(`packages/jeff_strict_ssot_v1/tests/test_bootstrap.py:54-158`). They do not test
path traversal, drive-qualified paths, symlinks/junctions/reparse points,
expected-hash TOCTOU, partial failures, rollback cleanup, target identity aliases,
or install-record failure. The generated tests cover only one Governor mutation,
two migration paths, and four protocol-validator mutations
(`packages/jeff_strict_ssot_v1/template/tests/ssot/test_governor_delta_policy.py:19-32`;
`test_status_archive_migration.py:26-75`; `test_validate_protocol.py:18-59`).

The acceptance runner verifies hashes named by the install manifest but never
rejects unexpected files in the installed tree
(`packages/jeff_strict_ssot_v1/tests/run_acceptance.py:105-124`). It runs dry-run
once and does not compare repeated dry-run output. Its determinism unit test
compares template files only and excludes `JEFF_STRICT_SSOT_INSTALL.json`
(`packages/jeff_strict_ssot_v1/tests/test_bootstrap.py:95-104`), whose timestamp
and absolute target are intentionally variable
(`packages/jeff_strict_ssot_v1/bootstrap.py:176-187`).

Required fix: add the missing negative/failure-injection fixtures, compare the
actual installed file set exactly to the authorized manifest, repeat dry-run and
compare bytes, and define/test deterministic versus intentionally variable
install-manifest fields.

### P2-4: Package source hashes are observed evidence, not an installer-enforced baseline

`MANIFEST.json` lists template paths and guarantees but contains no expected
template hashes (`packages/jeff_strict_ssot_v1/MANIFEST.json:1-60`). Bootstrap
computes source hashes from whatever bytes are present at installation time
(`packages/jeff_strict_ssot_v1/bootstrap.py:98-109`) and then records those same
observations. The acceptance record currently provides a complete independent
47-file snapshot, but it lives outside the distributable package. A changed
template can therefore be installed and blessed by a newly generated install
record without comparison to an approved package baseline.

Required fix: add an authorized per-template SHA-256 map to the package manifest
and verify every source byte before rendering. Define how `bootstrap.py` and the
manifest itself are authenticated by release evidence, and test tamper refusal.

## P3 Findings

### P3-1: Conflict and link scanning can false-positive on ordinary Markdown

The validator rejects any occurrence of seven `=` characters in every bounded
file, including legitimate prose or fenced examples
(`packages/jeff_strict_ssot_v1/template/scripts/ssot/validate_protocol.py:91-94,153-157`).
Its regular expression for Markdown links stops at the first closing parenthesis
(`validate_protocol.py:91,206-221`), so ordinary relative filenames containing
parentheses can be reported as broken.

Required fix: recognize conflict markers only as complete marker lines outside
fenced examples and use a bounded Markdown-aware link parser or a conservative
scanner with fixtures for escaped and parenthesized destinations.

## Verification Results

- Package tests: `8/8` passed with `python -B -m unittest discover -s packages\jeff_strict_ssot_v1\tests -p test_*.py -v`.
- Installed generated tests: `9/9` passed with `python -B -m unittest discover -s tests\ssot -v` from the installed fixture.
- Installed protocol validator: passed with zero errors and warnings.
- Installed Governor validator: passed with zero errors.
- Independently reconciled all `47` package-file hashes in the acceptance record.
- Independently reconciled all `42` source-template, rendered destination, and byte-count entries in `JEFF_STRICT_SSOT_INSTALL.json`.
- Installed fixture contains exactly `43` files: the `42` manifest templates plus the install record; no extras, missing files, or reparse points were found.
- All seven acceptance log hashes and the package-manifest hash match current bytes. Recorded exits are `0,0,0,0,0,0,2`.
- The current evidence proves protocol execution only. It is not product evidence.

## Cold-Resume Result

`pass` for information recovery, but not for package safety. From the installed
fixture alone, a fresh reviewer can recover the one-owner model and authority
map; bootstrap state and blocker; next authorization and forbidden actions;
decision/supersession fields; five task boundaries and the single-writer rule;
evidence classes and done gate; pure-validator prohibitions; inactive Governor
and delta modes; transcript neutrality; Git/remote visibility rules; and the
block on product implementation before reviewed intake. The fixture contains no
fabricated product fact, transcript record or ledger, status archive, active
Governor, cadence, automation, dependency, product technology, or accepted
product prompt.

The cold-resume text is coherent, but the validators do not reliably enforce
several recovered rules, as P1-3 documents.

## Verdict And Use Gate

Verdict: `fail`.

Jeff Strict SSOT V1 may not become current or usable for fresh installation or
retrofit. P1-1 through P1-3 must be repaired; P2-1 through P2-4 must be resolved;
the complete bounded suites and acceptance evidence must be regenerated; and a
new context-isolated Red Team must review the corrected package and fresh
fixture. A passing current-byte hash census does not waive these requirements.

## Residual Risks

- Standard-library filesystem APIs cannot make a multi-file retrofit fully
  atomic; the package must document its recoverable transaction model and the
  remaining crash window.
- Windows reparse behavior and case-insensitivity need platform-specific tests;
  non-Windows symlink tests are not sufficient evidence for Windows retrofit.
- A package-local hash map detects accidental/tampered template changes only
  when the manifest/bootstrap release identity is authenticated externally.
- Protocol validators can establish repository-contract consistency only, never
  product or domain correctness.

## Boundary Confirmation

This review read every file named by the Red Team prompt: all package templates,
both package test files, the acceptance record, all seven logs, and every file
in the installed fixture. It ran only bounded local Python/PowerShell checks and
the package/generated tests. It did not access the network, install dependencies,
run product commands, activate automation, mutate Git, repair package files,
modify `STATUS.md` or owners, or access/modify `L:\dev\CROCHET` or
`L:\dev\SPLATOMATIC`. The package source and acceptance runner contain no code
path that targets either product repository. Both retrofits remain explicitly
unapproved. Because the review boundary prohibited accessing those directories,
their historical byte-for-byte untouched state is record-supported, not
independently filesystem-verified by this review.

SSOT promotion is still pending because the package failed its independent
promotion gate and this bounded review was not authorized to update `STATUS.md`.

human action required: keep Jeff Strict SSOT V1 unpromoted and authorize a bounded package-fix task for the P1/P2 requirements above, followed by fresh acceptance evidence and a new context-isolated Red Team review.
