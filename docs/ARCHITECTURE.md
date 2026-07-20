# Yakherd Architecture

## Distribution Layer

The repository provides branding, public documentation, CI, release tooling,
and the `yakherd.py` convenience launcher. This layer does not alter target
repositories directly; it delegates to the audited package.

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

`SSOT.md` maps authority. `DECISIONS.md` owns durable decisions. `STATUS.md`
is a compact current-state index, not an append-only history. Domain owners and
run records carry detailed evidence.

## Trust Chain

The release tag authenticates `RELEASE.json`. `RELEASE.json` binds the
installer and manifest. `MANIFEST.json` binds every installed template. The
installation receipt binds rendered outputs and destination paths.
