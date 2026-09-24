# Yakherd SSOT 3.0 package

The default payload is ten files: five core owners (AGENTS, SSOT, BASELINE,
NOW, README), direct START_HERE instructions, the optional CLAUDE import
adapter, a small gitignore, a versioned profile and the Windows process policy.
The installer adds a hash-bound `YAKHERD_INSTALL.json` receipt.

`bootstrap.py` is a standard-library-only deterministic installer and
transaction engine derived from the V1 containment/rollback implementation.
`MANIFEST.json` pins every template; `RELEASE.json` pins the engine and manifest.
The reviewed Git commit authenticates the release file itself.

Fresh install is no-overwrite, including nonempty targets with unrelated files.
The public `yakherd migrate` command adds reviewed embedded replacement content,
before/after hashes, structural preflight, exact plan approval and retained
successful backups to the same transaction engine. Its behavior and recovery
limits are documented in [the migration guide](../../docs/SSOT_MIGRATION.md).

No installer operation invokes target Git, network access, dependency
installation, automation or product execution. `yakherd exec` is a separately
invoked process broker. Doctor reads target data with trusted distributed code
and checks structure only; project Markdown is expected to evolve.

The legacy package is retained separately for provenance and regression tests.
Legacy receipts and plans are never relabeled as v3 installations.
