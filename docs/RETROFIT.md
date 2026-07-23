# Retrofit Safety

Retrofit is for an established repository whose existing SSOT and product
ownership must be preserved. It is not an automatic upgrade mode.

## Required Process

1. Inventory current owners, instructions, status, decisions, validation, Git
   state, and conflicting files.
2. Write a bounded retrofit proposal.
3. Obtain independent Red Team review.
4. Freeze a JSON plan with `reviewed: true`, an exact path allowlist, and an
   expected SHA-256 or `absent` state for every allowed destination.
5. Run `yakherd.py retrofit ... --dry-run`.
6. Review the dry-run and execute from an isolated task.
7. Validate every changed path and the transaction journal.

## Fail-Closed Conditions

Retrofit stops on path escape, reparse ambiguity, missing review, unexpected
destination state, concurrent change, lock conflict, hash mismatch, incomplete
rollback, or stale transaction state.

Never widen a failed plan in place. Re-inventory and review a new plan.

## Y-PROC-1 Preserve-First Migration

`mosaic_colmap`, `SPLATOMATIC`, and `CROCHET` already contain temporary
process-hygiene instructions and are partially mitigated. Do not refresh their
SSOT or remove that text merely because Y-PROC-1 exists in Yakherd 1.3.

A later migration must use an exact, reviewed, hash-pinned retrofit that:

1. proves the installed `yakherd exec` broker and owned-cleanup commands are
   active and equivalent or stronger;
2. allowlists only the compact policy owner/reference and the exact duplicate
   temporary text being replaced;
3. preserves every unrelated SSOT owner and product file; and
4. records each repository, removed text, replacement reference, and native
   control that now enforces it.

The intended replacement is:

> For all local execution, obey Yakherd policy Y-PROC-1. Do not bypass its
> execution broker or process-lifecycle enforcement.
