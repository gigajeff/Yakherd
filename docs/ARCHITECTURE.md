# Yakherd Architecture

## Distribution Layer

The repository provides branding, public documentation, CI, release tooling,
and the `yakherd` Python command. The PyPI wheel bundles the reviewed package
bytes and the source checkout exposes the same command through `yakherd.py`.
This layer does not alter target repositories directly; it delegates to the
audited package.

## Audited Package Layer

`packages/jeff_strict_ssot_v1/` is the reviewed V1 engine. Its installer:

1. validates its release and manifest hash chain;
2. resolves and validates the target path;
3. renders the product-neutral template;
4. performs dry-run or fail-closed installation;
5. verifies output hashes; and
6. writes a structured installation receipt.

Fresh mode permits only a nonexistent or empty target. Retrofit mode requires
a reviewed, exact-state plan and uses locking, backup, atomic replacement,
post-write verification, and a durable transaction journal.

## Installed Governance Model

The generated repository separates five task responsibilities:

- Architecture decides and records bounded plans.
- Implementation executes only approved scope and writes durable evidence.
- Red Team reviews independently and does not repair while reviewing.
- Temporary Branch isolates exploratory work from the main implementation.
- Governor audits state drift using bounded, delta-only reporting.

For Codex, `START_HERE.md` and
`docs/prompts/codex_team_launcher.md` are a client adapter that explicitly
requests five direct role agents under one non-authoritative coordinator. The
adapter creates role execution contexts; it does not change authority. Roles
without an activation gate report waiting, parked, or inactive rather than
becoming concurrent writers.

`SSOT.md` maps authority. `DECISIONS.md` owns durable decisions. `STATUS.md`
is a compact current-state index, not an append-only history. Domain owners and
run records carry detailed evidence.

`AGENTS.md` is the single authoritative repository-instruction file. Codex
loads it when the generated repository is its active project. The generated
`CLAUDE.md` contains only `@AGENTS.md`, using Claude Code's import mechanism to
load the same rules without maintaining a second copy. Claude Code may require
first-use approval for that local import, and the active context should be
verified before work. Other agents remain compatible when explicitly directed
to read `AGENTS.md`; discovery and client-side approval state are outside the
installer's trust boundary.

GitHub setup and product-prompt intake are also post-install, agent-guided
workflows. The installer only writes their reviewed instructions. It does not
authenticate an account, access the network, initialize Git, create a remote,
push, or ingest prompt content. Those actions remain behind explicit user and
review gates in the generated repository.

## Trust Chain

The release tag authenticates `RELEASE.json`. `RELEASE.json` binds the
installer and manifest. `MANIFEST.json` binds every installed template. The
installation receipt binds rendered outputs and destination paths.
