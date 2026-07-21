# GitHub Project Setup

This is an agent-guided publication procedure, not installer behavior. Reading
this file authorizes no Git or network mutation by itself.

## Required Human Checkpoint

Before the first Git mutation or GitHub write, the coordinator must present and
receive one explicit approval for:

- the authenticated GitHub login;
- the exact `OWNER/REPOSITORY` destination;
- visibility: `private` is suggested, while `public` and `internal` require an
  explicit choice;
- whether this directory may be initialized as a Git repository if needed;
- the exact initial paths to stage and the proposed commit message; and
- creation of `origin` and the first push.

Approval for this checkpoint does not authorize later releases, deployments,
force pushes, remote changes, history rewrites, or branch deletion.

## Coordinator Procedure

1. Confirm the bootstrap cold-resume Red Team review passed and the governance
   shell has no unresolved critical finding.
2. Inspect local state without mutation: repository root, current Git state,
   existing remotes, and whether `gh` is available.
3. Check the active account with
   `gh auth status --active --hostname github.com`. Never add `--show-token`,
   print a credential, or ask the user to paste a token into chat or a file.
   If authentication is missing, ask the user to complete the normal browser or
   connector authorization flow, then recheck.
4. Resolve the destination with the user. When no owner is specified, GitHub
   CLI uses the active authenticated user; do not assume that is the intended
   account without showing it first.
5. Scan the proposed initial file set for secrets, caches, generated acceptance
   output, bulky artifacts, and machine-local state. Stop if any are present.
6. Request the single required checkpoint above. Do not combine it with a
   product, deployment, or release approval.
7. If approved and no Git repository exists, initialize one with the agreed
   default branch. If Git already exists, preserve its history and configuration.
8. Stage only the explicit reviewed paths, then show the staged path list and
   staged diff. Never use `git add .` or an equivalent blind recursive stage.
9. Create the approved initial commit. If an `origin` already exists or the
   destination repository already exists, stop and reconcile rather than
   overwriting or silently retargeting it.
10. Create and push the repository using the approved owner, name, and
    visibility. For GitHub CLI, the bounded shape is:

    ```text
    gh repo create OWNER/REPOSITORY --private --source=. --remote=origin --push
    ```

    Replace `--private` only with the visibility the user explicitly approved.
11. Verify and report branch, HEAD, upstream, dirty state, ahead/behind, remote
    URL, and whether the reviewed commit is visible on GitHub.

## Stop Conditions

Stop without mutation if the account is wrong, authorization is unavailable,
the destination or visibility is ambiguous, an unexpected remote/history
exists, a secret may be staged, the review gate failed, or the user declines
the checkpoint.

GitHub CLI documents account inspection in
[gh auth status](https://cli.github.com/manual/gh_auth_status) and creation from
an existing local repository in
[gh repo create](https://cli.github.com/manual/gh_repo_create).
