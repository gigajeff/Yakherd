# Jeff Strict SSOT Package And CROCHET/SPLATOMATIC Plan

Date: 2026-07-20
Status: acceptance V6 and independent source-correctness recheck V3 passed; the scoped Git commit containing the release-authentication record authenticates the reviewed package once present on `origin/main`; downstream installations remain separate tasks

## Decision

Create one reusable, product-neutral **Jeff Strict SSOT** bootstrap package.
It is distinct from:

- Mosaic's mature, domain-specific governance implementation; and
- Franti V2.1, which is deliberately a smaller teaching bootstrap.

The strict package should carry Mosaic's general P0-P4 mechanics without
copying Camera0154, NuRec, Pointeo, COLMAP, geometry, local paths, current
automation, or experiment authorization.

CROCHET should receive a bounded retrofit from its current V2 bootstrap to the
strict contract. It should not be deleted or re-bootstrapped.

SPLATOMATIC should receive the strict package before its existing
`mosaic_3dgs_master_prompt.md` is accepted into project authority.

## Five Task Model

Every installed repository has five named task prompts:

1. **Architecture** owns plans, boundaries, gates, and accepted design changes.
2. **Implementation** is the sole live writer for one authorized slice.
3. **Red Team** independently reviews requirements, behavior, evidence, risk,
   and the diff; it does not repair the work it reviews.
4. **Temporary Branch** runs one isolated hypothesis in a branch/worktree with
   no authority until reviewed and deliberately merged.
5. **Governor** is an independent auditor, not a builder or second SSOT. It
   owns only findings, risks, audit reports, and audit state.

The Governor is the fifth task but not a fifth implementation lane. It cannot
authorize or execute product work.

Never run two writers in one working tree. Architecture and Red Team may write
only their bounded plan/review records while Implementation is paused or while
their output path is explicitly isolated.

## Portable Package

Build the source package under:

```text
packages/jeff_strict_ssot_v1/
```

The package itself should contain:

```text
README.md
MANIFEST.json
bootstrap.py
template/
tests/
```

`bootstrap.py` must:

- use the Python standard library only;
- accept an explicit target path and project name;
- default to fresh-folder mode;
- refuse to overwrite any existing path unless a separate reviewed retrofit
  mode names the exact files allowed to change;
- make no network call, install nothing, run no product command, create no
  automation, and mutate no Git remote;
- render project-name/date placeholders deterministically;
- write a machine-readable install manifest with source and destination hashes;
- support `--dry-run` and a nonzero fail-closed exit;
- never ingest a product master prompt automatically.

## Installed Fresh-Repository Manifest

The package should install exactly this initial structure:

```text
.gitignore
README.md
AGENTS.md
SSOT.md
STATUS.md
DECISIONS.md
ARCHITECTURE.md
TESTING.md
GIT_SYNC.md
code_review.md
docs/
  domain_invariants.md
  task_protocol.md
  validation_protocol.md
  status_history/
    README.md
  master_prompts/
    README.md
    000_PRODUCT_PROMPT_NOT_RECEIVED.md
  plans/
    README.md
  reviews/
    README.md
  run_records/
    README.md
  prompts/
    architecture_task.md
    implementation_task.md
    red_team_task.md
    temp_branch_task.md
    governor_task.md
    bootstrap_cold_resume_review.md
  templates/
    architecture_plan.md
    red_team_review.md
    run_record.json
  governance/
    README.md
    STATUS_MAINTENANCE.md
    GOVERNOR_DELTA_POLICY.md
    GOVERNOR_DELTA_POLICY.json
    TRANSCRIPT_REVIEW_POLICY.md
    OPEN_FINDINGS.md
    RISK_REGISTER.md
    AUDIT_STATE.json
scripts/
  ssot/
    validate_protocol.py
    validate_governor_delta_policy.py
    migrate_status_archive.py
tests/
  ssot/
    test_validate_protocol.py
    test_governor_delta_policy.py
    test_status_archive_migration.py
```

The status-migration fixture is part of the authorized exact installed tree.
It is required because archive preparation and rollback are mutating operations
whose failure behavior cannot be inferred from validator tests.

Do not install duplicate governance SSOT/decision maps. Root `SSOT.md` owns the
authority map and root `DECISIONS.md` owns accepted/superseded decisions.

Do not create transcript records, a transcript ledger, a status archive, or a
recurring automation in an empty repository. The policy files explain the
conditions for introducing them later.

## Core Strict Rules

### One Fact, One Owner

- Every durable fact has exactly one owner.
- Summaries and indexes link to owners and do not mirror mutable task state.
- Newer prose is not a supersession without an explicit recorded transition.
- Closing a finding does not fix stale owner or index text; the actual stale
  text must be corrected.

### Compact Current Status

`STATUS.md` is a current-state index, not a diary.

- target: at most 80 lines;
- hard maximum: 120 lines and 32,768 UTF-8 bytes;
- exactly one dated current-state entry;
- stable fields for state, timestamp, surface, goal, evidence, tests, blockers,
  next authorized action, forbidden actions, Git state, remote visibility,
  release/promotion state, and archive;
- stable domain sections updated in place;
- durable result promotion to its real owner before the status summary changes;
- no prepended historical narrative entries.

When a mature status exceeds its hard cap, preserve its exact bytes, hash and
index it, migrate live citations, replace it with compact current state, and
use hash-guarded rollback. Never delete history merely to meet the cap.

### Structured Evidence

A test or completion claim requires a structured run record containing:

- schema and evidence classification;
- UTC timestamp;
- working directory;
- exact command;
- exit code;
- environment identity;
- supported claim;
- bounded stdout/stderr or exact raw-output paths;
- relevant artifact paths and hashes;
- authority effect and limitations.

Summaries and chat cannot replace this record.

### Validator Safety

The protocol validator must be standard-library-only, bounded, deterministic,
and read-only. It must not import product modules, launch subprocesses, access
the network, invoke Git, write files, inspect bulky artifact trees, or infer
domain correctness.

It checks:

- canonical required paths and casing;
- relative links in the bounded protocol set;
- owner paths from `SSOT.md`;
- status schema, staleness, one-entry rule, line cap, and byte cap;
- explicit decision supersession fields and current-owner links;
- unresolved conflict markers;
- explicitly supplied structured command-evidence JSON;
- Governor policy schema and limits.

Git state is captured by exact external Git commands in structured run records;
it is not obtained by weakening the pure protocol validator.

### Transcript Authority

- Transcript-derived material is a retrieval aid, never project authority.
- Create review metadata only when current governance cites an exact transcript
  record.
- Absence means unclassified.
- Metadata authority effect is always `none`.
- Promotion updates the real owner first; metadata may only record the owner
  path afterward.

### Governor Delta Contract

The Governor starts inactive. Activation requires separate human approval and
an observed useful manual baseline.

- quiet: at most 2 lines / 512 bytes, no governance write;
- delta: changed material items only, at most 120 lines / 16,384 bytes;
- rebaseline: broken continuity or explicit human authorization only, at most
  240 lines / 32,768 bytes;
- unchanged findings are IDs/owner links only;
- cadence changes require separate approval;
- a dated utility review measures new verified findings, resolutions, false or
  unsupported findings, repeated prose, and maintenance time.

### Git Continuity

- Local tasks sharing a working tree can see uncommitted state; that state is
  not portable.
- Cloud tasks, other machines, and remote reviewers require committed and
  pushed state.
- Never use blind `git add .`.
- Commit/push/remotes/history/destructive actions require human approval.
- Final reports state branch, HEAD, upstream, dirty state, ahead/behind, and
  remote visibility.

### Done Gate

Material work is complete only after:

- requested behavior and applicable checks are complete;
- structured evidence exists;
- relevant output has been inspected;
- the real domain/decision owner is updated;
- compact current status agrees with that owner;
- stale or superseded records are marked;
- Git state and remote visibility are reported.

A chat conclusion, Governor finding, or status-only edit is not durable
promotion.

## CROCHET Assessment

CROCHET's current repository-centered structure is good and should remain. It
already has owner files, all five prompt paths, structured run records, a fresh
Red Team bootstrap review, and a compact status.

It needs a bounded V2.1 retrofit because:

1. `AGENTS.md` names four build/review roles but does not explicitly present
   Governor as the fifth task/auditor.
2. `STATUS.md` is compact, but the contract has no hard line/byte cap,
   update-in-place rule, archive procedure, or one-entry rule.
3. `scripts/ssot/validate_protocol.py` only warns above 60 status lines and has
   no byte cap, owner-path validation, or decision-supersession validation.
4. The validator launches Git subprocesses, mixing pure protocol validation
   with environment inspection.
5. `docs/prompts/governor_task.md` says "stay quiet" but has no bounded
   quiet/delta/rebaseline behavior or utility gate.
6. Transcript authority and conditional review metadata are not explicit.
7. The done gate should require durable owner promotion before completion is
   claimed.

Do not re-bootstrap CROCHET and do not overwrite its accepted product owners.
Run a dedicated documentation/validator retrofit while the product
Implementation writer is paused or in an isolated reviewed worktree.

The retrofit should:

- preserve current `STATUS.md` content and update it in place;
- add the general governance contracts listed in the installed manifest;
- extend or replace the validator with fixture tests;
- split live Git evidence capture from the pure validator;
- preserve existing decisions and add/fix only explicit supersession fields;
- run a fresh cold-resume Red Team check after the patch;
- make no product, architecture, dependency, compute, or release decision.

## SPLATOMATIC Bootstrap

`L:\dev\SPLATOMATIC` currently contains only
`mosaic_3dgs_master_prompt.md`. Treat that file as received intent, not yet
accepted project law.

The correct sequence is:

1. Keep the master prompt byte-identical and record its hash.
2. Install Jeff Strict SSOT into the folder in fresh mode.
3. Run protocol validation twice, with structured records for both runs.
4. Human reviews the generated tree and exact diff/status.
5. Create a reviewed Git checkpoint; push only if another machine/cloud task
   needs it.
6. Run the fresh-task bootstrap cold-resume Red Team review.
7. After that passes, move or copy the original prompt to
   `docs/master_prompts/YYYY-MM-DD_SPLATOMATIC_MASTER_PROMPT.md`, preserving
   its original hash and provenance.
8. Architecture extracts requirements, constraints, unknowns, risks, and
   acceptance gates into owner files.
9. Red Team reviews that extraction.
10. Human resolves real product choices.
11. Authorize only the first bounded Implementation slice.

Do not allow the bootstrap to choose SPLATOMATIC's language, dependencies,
3DGS engine, cloud provider, data model, or release strategy. Those belong to
product intake and Architecture.

## Acceptance Gates Before Package Use

- Package dry-run and fresh install are deterministic.
- A second fresh install refuses to overwrite existing files.
- Manifest hashes match installed files.
- `MANIFEST.json` contains an exact source-template SHA-256 baseline enforced
  by the installer. `RELEASE.json` binds the bootstrap and manifest hashes;
  the reviewed Git commit/release must authenticate `RELEASE.json` itself.
- Protocol and Governor validators pass their fixture suites.
- No test writes outside a temporary fixture root.
- No package script imports project code, launches product commands, accesses
  the network, installs dependencies, or mutates Git/remotes.
- Status limits and owner/supersession failures are proven by negative tests.
- Empty bootstrap contains no fabricated product facts.
- Cold-resume Red Team recovers every hard boundary from repository state.
- Independent Red Team reviews both the package and CROCHET retrofit before
  either becomes current.

## Next Implementation Boundary

The next implementation task should build and test
`packages/jeff_strict_ssot_v1/` only. It must not modify CROCHET or SPLATOMATIC.
After package Red Team approval, use separate reviewed tasks for:

1. the CROCHET bounded retrofit; and
2. the SPLATOMATIC fresh installation and cold-resume gate.

## Implementation State

Jeff authorized the package boundary on 2026-07-20. The candidate now exists
at `packages/jeff_strict_ssot_v1/` and passed its package and generated-repo
acceptance suite. Durable evidence is recorded in
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_implementation.md`.

The first independent Red Team returned `fail` because filesystem containment,
status-migration transaction safety, validator enforcement, source-hash
authentication, and acceptance evidence/tests were incomplete. The first
bounded repair passed acceptance V3, but the fresh context-isolated recheck at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_recheck.md`
also returned `fail`. Its four P1 findings cover raw CLI path alias/reparse
validation, fresh-install partial cleanup, status archive commit-set integrity,
and validator state/evidence bypasses. V3 is superseded candidate evidence.
The bounded package repair closed the earlier four P1 surfaces and acceptance
V5 passed, but the next context-isolated review at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_recheck_v2.md`
returned `fail`. It found two P1 defects in retrofit transaction safety and
decision-history semantics plus two P2 gaps in package-source bytecode census
and UTC timestamp validation. The bounded package repair now addresses those
findings and clean acceptance V6 passes against current bytes. The fresh
context-isolated V3 recheck at
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_red_team_recheck_v3.md`
returned `pass` for source correctness. The intentional scoped Git commit that
contains the package plus
`docs/governance/audits/2026-07-20_jeff_strict_ssot_v1_package_release_authentication.md`
is the reviewed external authentication boundary once it is present on
`origin/main`. `L:\dev\CROCHET` and `L:\dev\SPLATOMATIC` remain untouched and
must be handled by separate implementation tasks.
