# Historical planning and source records

The current release is Yakherd 3.0.0. Use [START_HERE.md](../../START_HERE.md),
[AGENTS.md](../../AGENTS.md) and the
[installed templates](../../packages/yakherd_v3/template/) for current work.

The records listed below describe earlier candidates, observations and
instructions. Statements such as "current", "unreleased", "blocked" or
"authorize" apply to their original context. Preserving these records does
not adopt their old startup rules, restart their work, or grant authority.
Their original content and source hashes are retained.

- The `2026-07-21_*` and `2026-07-22_*` documents in `docs/` preserve the
  concierge/website proposals, build directives and release preparation.
  Their corresponding records remain in `docs/audits/yakherd/`.
- [The beginner audit](../Yakherd%20Audit%20for%20Absolute%20Beginners.md)
  describes the earlier V1 experience. Its exported citation tokens belong
  to the original conversation; they are not independently usable web links.
- [The V1 1.5 candidate review](../audits/yakherd/2026-07-28_yakherd_1.5.0_finite_review_ledger_red_team.md)
  and [deferred hardening note](../TODO.md) preserve the finite-review work.
  This candidate was not made the public package version during cleanup.
- [The source-pack work record](../2026-09-24_ssot_instruction_work.md),
  [its review](../audits/yakherd/2026-09-24_ssot_instructions_red_team.md),
  [source-only starters](../ssot-starter/HISTORY.md) and
  [TRAVOLTA handoff](../handoffs/TRAVOLTA_SSOT_RESUME.md) preserve the
  pre-installer transition. The handoff is not a request to resume TRAVOLTA.
- [The pre-3.0 snapshot inventory](pre-3.0/inventory.json) records the original
  paths and SHA-256 values of 96 source/media files present before cleanup.
  Previously modified tracked files are retained in
  [the exact working-tree patch](pre-3.0/tracked-working-tree.patch), based on
  commit `735bd78d2790070470308d3af881a6b565d9efa3`. It reconstructs an earlier
  candidate; do not apply it over the current release.
- The old source-only [startup guide](pre-3.0/START_HERE.md),
  [process](pre-3.0/docs/SSOT_PROCESS.md) and
  [migration guide](pre-3.0/docs/SSOT_MIGRATION.md) are archived separately
  because the published 3.0 versions now own their original paths.

The original ten-second [Yakherd video](../../yakherd.mp4) is retained as a
media asset. It is not validation or release evidence.

The 2026-10-30 cleanup fast-forwarded local `main` from the old 1.4 checkout to
the already published 3.0 commit
`243bd15393f42f2e90412f42961f864575822def`, rather than replacing the released
installer with the older local 1.5 candidate. Both package trees, their hash
bindings and the runtime source remain unchanged from that published commit.
Interrupted test output and machine-local snapshots remain outside commits.
Separate YakherdMT branches/worktrees retain their own work and history.
