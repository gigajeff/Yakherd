# Yakherd 3 usage

Requires Python 3.11 or newer. Runtime operations use only the standard library.

## New repositories

```text
yakherd setup [PATH] [--project-name NAME] [--dry-run]
yakherd doctor [PATH] [--json]
```

PATH defaults to the current directory; the project name defaults to its folder
name. Setup installs ten payload files plus a receipt. No existing payload path
may be overwritten. Unrelated files remain untouched. An existing v3 receipt
selects read-only validation; a legacy receipt selects an explicit migration
instruction. Failed setup never silently falls back to a destructive mode.

Open the resulting project and say `Start Yakherd` together with the product
request. The agent reads AGENTS/SSOT/BASELINE/NOW and works in one task. Clients
that do not discover AGENTS automatically must be told to read it. CLAUDE.md is
only an import adapter, not a second policy. Client permissions still apply.

Doctor returns exit 0 for structurally ready repositories, 1 for target
structure errors, and 2 for command/package/input errors. `--json` emits the
same findings as data. A scaffold warning is expected until the product request
has been adopted. Doctor executes no target scripts, fetches no external links
and makes no product-correctness claim.

## Migration

```text
yakherd migrate plan TARGET --replacements DIR --output PLAN.json
yakherd migrate preview PLAN.json
yakherd migrate apply PLAN.json --plan-sha256 SHA256
```

See [the migration and recovery guide](SSOT_MIGRATION.md) before use. Plan and
preview are non-mutating with respect to the target. Apply requires reviewed
content, exact hash approval and unchanged target bytes. The plan, replacement
directory and target must have the documented separate locations. Do not
publish plans/backups containing project-specific or private data.

Legacy V1 `retrofit` plans are not v3 adoption plans. The v3 public `retrofit`
command reports the new migration path rather than reinterpreting an old plan.
The low-level engine remains available through `yakherd package-help`; ordinary
users should use setup and the content-preserving migration workflow.

## Finite Windows execution

```text
yakherd exec [--heavy|--light] --timeout SECONDS -- COMMAND [ARG ...]
yakherd process status
yakherd process cleanup --task TASK_ID --dry-run --verify
yakherd process resume --task TASK_ID
```

Heavy is the default and preserves internal worker counts while serializing
independent heavy pipelines. Use `--light` only for finite low-CPU work.
No REPLs, watchers, detached daemons or persistent leases are enabled by setup.
Cleanup requires coherent ownership plus Job membership and never targets a
process by name or PID alone. Preserve existing applicable process controls
when migrating. The broker fails closed on unsupported operating systems;
the remaining harness commands are cross-platform.

## Source checkout and troubleshooting

Replace `yakherd` with `python -B yakherd.py` when running from source. Verify
`--version` before following these v3 instructions. A missing/broken profile,
unresolved transaction or contradictory launcher should be repaired at its
actual owner. Do not restore a five-role startup to satisfy an old validator.
Current structure checks do not waive genuine product or data-integrity defects.
