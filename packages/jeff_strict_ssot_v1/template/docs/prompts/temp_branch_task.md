# Temporary Branch Task Prompt

Run one named hypothesis in an isolated branch/worktree. Record the base SHA,
scope, write set, tests, evidence, and cleanup/merge boundary before work.

If no hypothesis and isolation boundary have been explicitly approved, report
`parked`, create no branch/worktree, make no edits, and wait.

Temporary output has no authority. Do not update main-tree owners, claim
promotion, merge, publish, or delete the worktree/branch without independent
review and explicit approval. Keep datasets, secrets, bulky artifacts, caches,
and machine-local tools out of Git.

End with one required repository marker.
