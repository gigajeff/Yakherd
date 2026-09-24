# Yakherd 3 architecture

## Distribution and ownership

The public `yakherd` CLI in `src/yakherd/` dispatches to the trusted v3 package
at `packages/yakherd_v3/` or its identical bundled copy in an installed wheel.
The canonical product process is [SSOT_PROCESS.md](SSOT_PROCESS.md). The actual
installed template is its single starter source; repositories own their adopted
local rules and do not silently inherit future upstream policy changes.

The legacy V1 package remains separate for provenance/regression checks. Its
five-role launcher and validators are not part of the v3 default payload.
The root [development protocol](task_protocol.md) governs changes to Yakherd
itself, including independent release review. It is not installed in products.

## Deterministic installation

The reviewed commit authenticates RELEASE.json; that binds bootstrap.py and
MANIFEST.json, which binds every template. The installer verifies those bytes,
renders a project name/date, checks paths and collisions, creates files without
overwrite, verifies output hashes and writes YAKHERD_INSTALL.json. It refuses
unsafe path aliases/reparse traversal and cleans its created files on failure.
Unrelated target files remain untouched.

No installer path invokes the network, target Git, product code, dependency
installation or automation. The Python runtime has no third-party dependencies.
The build system may use pinned development dependencies independently.

## Diagnostics

`diagnostics.py` uses trusted distributed code and the engine's path checks to
read a bounded set of target documents as data. It validates the v3 owner map,
required current-work sections, local links, placeholders and recognized stale
entry points. It does not execute target validators or require current Markdown
to match its installation hashes. Results describe structural readiness only.

## Migration transaction

`migration.py` creates self-contained, unreviewed plans from deliberately
prepared replacement content. Every plan binds the exact package manifest,
absolute target, relative allowlist, prior state and proposed UTF-8 bytes.
Apply needs reviewed=true plus the final plan SHA-256. Core owner/policy bytes
are pinned even when carried forward unchanged.

Before mutation, the merged candidate passes structural diagnostics. The v3
engine then reuses the proven V1 cooperative lock, verified backups, atomic
replacement, immediate pre-replacement state checks, final output checks and
rollback. Successful backups and their journal are retained for deliberate
recovery. Failed transactions keep a journal and block another migration until
reconciled. Conflicting external edits are preserved rather than overwritten
by rollback. Non-cooperating writers can still race OS path APIs; migration
is a coordinated maintenance operation, not a filesystem security sandbox.

The default migration writes SSOT owners, known adapters/profile/policy and
Markdown documentation only. Product code, Git configuration and source data
are not generic migration targets. Semantic preservation is a reviewer/agent
responsibility: deterministic checks cannot infer a product's full requirements.

## Process containment

The Windows Y-PROC-1 broker remains separate from installation. It atomically
assigns finite commands to kill-on-close Job Objects, applies below-normal
priority to heavy work and serializes top-level heavy pipelines while retaining
internal parallelism. Ownership binds PID, creation time, executable path,
command identity, task/session and Job membership. Cleanup verifies empty Jobs
and never relies on a process name or ancestry alone. Inconsistent legacy
records warn; a verified live hazard is required to block unrelated work.
