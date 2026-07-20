# Git Continuity

Git is transport and review evidence, not the owner of product truth.

- Shared local tasks see uncommitted files in the same working tree.
- Other machines, cloud tasks, and remote reviewers see only committed and
  pushed state.
- Review the exact staged list; never use blind `git add .`.
- Human approval is required before staging, commit, push, remote changes,
  history rewriting, destructive checkout/reset, or branch deletion.
- Capture branch, HEAD, upstream, dirty state, ahead/behind, and remote
  visibility with explicit external commands in a structured run record.
- The pure SSOT validator must never invoke Git.
