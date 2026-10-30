# Current SSOT instruction pack: work and review record

Work ID: SSOT-INSTRUCTIONS-2026-09-24.
User request: prepare canonical new-repository instructions reflecting the
latest MonAV/Mosaic SSOT process and help steer stopped TRAVOLTA before resume.

## Accepted scope

Create a product-neutral canonical process, self-contained starter files,
new-repository entry point, migration guide and concrete TRAVOLTA steering
prompt. Make the current-vs-legacy distinction discoverable in root docs.
The core owners are AGENTS, SSOT, BASELINE, NOW and README. Default to one
implementation task; remove mandatory startup roles and process-review loops
while preserving useful independent verification, evidence and real hazards.

Write boundary: root START_HERE.md; docs/SSOT_PROCESS.md;
docs/SSOT_MIGRATION.md; docs/ssot-starter/*.md;
docs/handoffs/TRAVOLTA_SSOT_RESUME.md; this record and its one review file;
small discovery/status edits to AGENTS.md, README.md, CHANGELOG.md,
docs/ARCHITECTURE.md and docs/USAGE.md.

Forbidden: changes to the existing package, installer, validators, release
bindings or prior unrelated work; mutation or resumption of TRAVOLTA; changes
to research sources, product code, remotes, publication, dependencies,
credentials or automation. The instruction pack is not a released installer.

Definition of Done: usable canonical/starter/migration instructions; a
TRAVOLTA prompt that explicitly supersedes the stale operational clauses while
preserving accepted product requirements; coherent links and clear release
status; release verification and diff checks pass; independent scoped review.

## Review discipline

This is governance-core documentation work under Yakherd's existing
development protocol, not a new startup gate imposed on product repos.
Use one review path:
`docs/audits/yakherd/2026-09-24_ssot_instructions_red_team.md`.
R0 checks the exact candidate against the accepted scope and concrete hazards.
Only P0/P1 block; any repairs follow the existing R0/C1/C2 development budget.
No review may add product requirements or reset that budget.

Pre-task copies of edited root docs and package hashes are retained locally at
`.tmp/ssot-canonical-20260924/` to separate this task from existing dirty work.

## R0 candidate and validation

Stage: R0 -> PASS; no repair wave used. Independent reviewer `ssot_review`
verified the frozen scope and found no P0/P1 blocker or canonical/starter
mismatch. Findings and review limits are recorded in the review path above.
Candidate scope is exactly the 14 files below. This record and the review file
are administrative evidence, not part of the instruction candidate.

| File | SHA-256 |
| --- | --- |
| `AGENTS.md` | `5bf1f9d94b871c2d8976221bf2f8086f33ef1ec2c59d1497934a5993f46f6455` |
| `CHANGELOG.md` | `54547ea87aa70e5b5b04e547294ea4ae49b255e76532226afbe24b3d0ba7bfcc` |
| `README.md` | `12b69d55b3a58ba95804cd0cf95fd850ae8e1409ba34461808bdf25ee11b5f41` |
| `START_HERE.md` | `324beb0dc7cb497061ae62a9c751ed72b6fb5a4df39d16c91d0faaf9dbd117c6` |
| `docs/ARCHITECTURE.md` | `0108eb13e372115e57e607723b83ac7fdab99aa1deb937baf8a7b1c58c374431` |
| `docs/SSOT_MIGRATION.md` | `14582272b28d467337ccc594e14d3744a961c5a1b93d174eb5f9f2c148d01079` |
| `docs/SSOT_PROCESS.md` | `7bb7444204e631440755c5dc1713c475501b6725f4f26b48e20db077b2264343` |
| `docs/USAGE.md` | `4c6f8fbd0a3f77c6ea2317611965738eaf0acec609aecf48c0ef2e6391c357fd` |
| `docs/handoffs/TRAVOLTA_SSOT_RESUME.md` | `62da72388be7d4369d21128da2a5d744cee10169f25da402347f278a6a8ed308` |
| `docs/ssot-starter/AGENTS.md` | `0783ad652b463694b9e6093ec49aebd8612fa42311231bc01e2e033deb6ed267` |
| `docs/ssot-starter/BASELINE.md` | `9e05e2cb635a42e7bfd4a69656e58a683607c15266b5f8c519c92aa7855442fd` |
| `docs/ssot-starter/NOW.md` | `c81e7797d4b95499735383ae31983416712822894415dacb2aff6e54af966bed` |
| `docs/ssot-starter/README.md` | `767ded325c02dd09118af17e6cecb1e87cc04d60ea085ab52c72308e9abfb85c` |
| `docs/ssot-starter/SSOT.md` | `9d7a7bde2da508b5d07dab911d2d796ecc831d398d050b35c3e00af2fd2993ea` |

Validation on 2026-09-24: all 19 local Markdown links resolve; all five starter
files adapt into an isolated example without unresolved placeholders or a
cross-checkout dependency. All 54 existing package files retain their exact
pre-task bytes. `python -B scripts/verify_release.py` passes (48 manifest
files, zero caches); `git diff --check` passes.

The finite validation pipeline ran through `yakherd exec --light --timeout 60`
with task-local process state. Its completed Job record reports
`job_already_empty`, zero remaining PIDs and no concrete hazards. This is
documentation/instruction validation, not product validation or an installer
release/acceptance claim. Detailed local evidence is in the snapshot directory.
