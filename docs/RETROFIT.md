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
