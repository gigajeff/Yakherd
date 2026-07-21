# Git Continuity

Git is transport and review evidence, not the owner of product truth.

- Shared local tasks see uncommitted files in the same working tree.
- Other machines, cloud tasks, and remote reviewers see only committed and
  pushed state.
- Review the exact staged list; never use blind `git add .`.
- Human approval is required before staging, commit, push, remote changes,
  history rewriting, destructive checkout/reset, or branch deletion.
- First-time GitHub setup follows `docs/GITHUB_SETUP.md`. The coordinator must
  show the authenticated login, destination, visibility, exact staged paths,
  commit message, remote, and first-push intent at one explicit checkpoint.
- Never print or store an authentication token. Never replace an existing
  remote or history merely to make onboarding succeed.
- Capture branch, HEAD, upstream, dirty state, ahead/behind, and remote
  visibility with explicit external commands in a structured run record.
- The pure SSOT validator must never invoke Git.
