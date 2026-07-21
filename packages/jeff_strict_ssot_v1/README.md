# Jeff Strict SSOT V1

This package installs a product-neutral, repository-centered governance shell
for a new project. It carries the reusable SSOT mechanics validated in Mosaic
without copying Mosaic product rules, experiments, paths, or authorizations.

## What It Creates

The installed repository has:

- one authority map in `SSOT.md`;
- one decision owner in `DECISIONS.md`;
- one authoritative agent instruction file in `AGENTS.md`;
- a one-line `CLAUDE.md` adapter that imports `AGENTS.md` for Claude Code;
- compact current `STATUS.md` maintenance rules;
- five task prompts: Architecture, Implementation, Red Team, Temporary Branch,
  and Governor;
- a `START_HERE.md` beginner handoff and Codex prompt that launches all five
  role-agent threads under one non-authoritative coordinator;
- a byte-preserving, hash-recorded product master-prompt intake protocol;
- a GitHub account/repository setup guide with an explicit human checkpoint;
- standard-library, read-only protocol validators;
- structured run-record templates and validator fixtures; and
- no product stack, dependency, network, deployment, automation, or release
  choice.

## Coding Agent Compatibility

Codex loads `AGENTS.md` when the installed repository is opened as the project.
Claude Code loads `CLAUDE.md` in that project; the installed adapter contains
only `@AGENTS.md`, so both environments can receive the same repository rules
without duplicated authority. Start a fresh Claude Code session with the
installed repository as the project. On first use, approve the import only
after verifying it resolves to the repository's local `AGENTS.md`, then use
`/context` to confirm both files are active.
Other coding agents can use the package when they have filesystem, shell, Git,
and Python access and are explicitly instructed to read `AGENTS.md`.

In Codex, the user explicitly invokes `START_HERE.md` after opening the
generated repository. Codex can then create all five role agents. Creation is
not activation: Red Team runs the bootstrap gate, Architecture waits,
Implementation and Temporary Branch park, and Governor remains inactive. If
the client cannot create all five, startup is incomplete and must be reported
as such.

The adapter is behavioral guidance, not a security sandbox. Its bytes can be
validated, but client approval and loaded-context state cannot. The installer
and validators remain responsible for deterministic, fail-closed package
behavior.

## Fresh Install

Preview without writing:

```powershell
python packages\jeff_strict_ssot_v1\bootstrap.py `
  --target L:\dev\NEW_PROJECT --project-name NEW_PROJECT --dry-run
```

Install into a nonexistent or empty folder:

```powershell
python packages\jeff_strict_ssot_v1\bootstrap.py `
  --target L:\dev\NEW_PROJECT --project-name NEW_PROJECT
```

The installer refuses to overwrite any path. It writes
`JEFF_STRICT_SSOT_INSTALL.json` with package, source-template, rendered-output,
and destination hashes.

`MANIFEST.json` pins every source-template SHA-256 and the installer verifies
that baseline before dry-run or installation. `RELEASE.json` pins the
bootstrap and package-manifest hashes for release review. This is a layered
boundary: a reviewed Git commit or release must authenticate `RELEASE.json`
itself; no self-contained file can authenticate a malicious replacement of
itself and every verifier beside it.

## Retrofit Mode

Retrofit mode is deliberately fail-closed. It requires a separately reviewed
JSON plan with `reviewed: true`, an exact allowlist, and an expected SHA-256 or
`absent` state for every path it may change. Use it only from a dedicated,
reviewed retrofit task:

```powershell
python packages\jeff_strict_ssot_v1\bootstrap.py `
  --mode retrofit --retrofit-plan reviewed_retrofit_plan.json `
  --target L:\dev\EXISTING_PROJECT --project-name EXISTING_PROJECT
```

Retrofit writes use an exclusive cooperative lock, exact-state rechecks,
verified backups, atomic replacements, post-write hashes, and a transaction
journal. An interrupted or failed transaction leaves a journal and blocks a
new retrofit until a human reviews recovery. These controls detect package and
cooperating-writer races; Windows path APIs cannot eliminate every possible
non-cooperating process race, so retrofit remains a reviewed maintenance
operation rather than a general concurrent installer.

## Package Tests

```powershell
python -B -m unittest discover -s packages\jeff_strict_ssot_v1\tests -v
```

The package does not install software, access the network, invoke Git, ingest a
product prompt, create automation, or run product code.

The installed GitHub and prompt-intake documents govern later coding-agent
actions after explicit authorization; they do not give the installer those
capabilities.
