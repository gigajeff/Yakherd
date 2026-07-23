# Y-PROC-1: Windows Local Execution Hygiene

## Invariant

On Windows, every finite local command must run through `yakherd exec`.
Use one top-level heavy pipeline at a time, preserve normal internal build and
test parallelism, run heavy work below normal priority, and leave zero
verified, task-owned, unapproved, hazardous descendants on every exit path.
Never kill a process by executable name or interfere with a pre-existing or
unrelated process.

## Commands

Heavy is the safe default and is serialized across the current Windows user:

```powershell
yakherd exec --timeout 900 -- cmake --build build
```

Use `--light` only for a finite, low-CPU command that is safe to overlap:

```powershell
yakherd exec --light --timeout 60 -- git status --short
```

The broker does not reduce a build system's internal worker count. It uses
`CreateProcessW` with `PROC_THREAD_ATTRIBUTE_JOB_LIST` to create the command
inside a kill-on-close Windows Job Object before its first instruction,
applies `BELOW_NORMAL_PRIORITY_CLASS` to heavy work, and verifies that the job
is empty on exit, error, timeout, or interruption.

Inspect or safely clean only identity-verified Yakherd-owned work:

```powershell
yakherd process status
yakherd process cleanup --all-owned --dry-run --verify
yakherd process cleanup --task TASK_ID --verify
yakherd process resume --task TASK_ID
```

Y-PROC-1.1 records a coherent identity snapshot: PID, creation time, executable
path and derived image name, command line, parent PID/epoch when available,
task/execution/session IDs, named Job membership, observation time and
lifecycle. Job membership is the primary ownership authority. Cleanup never
uses broad executable-name matching, ancestry, name, or command-line proximity.

The status classes are `VERIFIED_LIVE_OWNED`, `VERIFIED_EXITED`,
`PID_REUSED_UNRELATED`, `OWNERSHIP_UNVERIFIED`,
`OWNERSHIP_RECORD_INCONSISTENT`, and `APPROVED_PERSISTENT` (leases remain
unsupported). PID reuse, incomplete legacy telemetry, and contradictions are
warnings: do not terminate, retain as active cleanup targets, or embargo other
work. A blocker requires all three: a live Job-verified owned process, failed
cleanup, and concrete process-bound hazard evidence. An explicit
`yakherd process resume --task TASK_ID` continues after warnings once; it never
waives a verified blocker.

Each `yakherd.process-task.v1.1` record contains the task and owner IDs, state,
classification, finite lifecycle, exact top-level argument vector and command
line, task working directory, broker identity, named Job Object identity,
priority, finite queue/run timeouts, timestamps, top-process identity, observed
job-member identities, exit code, termination reason, and cleanup verification.
Process identities include PID, parent PID, creation time, executable, CPU time,
working set, and priority class. Descendant command lines or working directories
that Windows cannot query safely are recorded as `null`; Job Object membership,
not incomplete telemetry, is the containment and cleanup authority.

## Finite-command boundary

The broker requires finite positive queue and execution timeouts and rejects
known interactive, detached, watcher, daemon, and development-server forms,
including bare Node or Python, `cmd /K`, PowerShell `-NoExit`, `Start-Job`,
`Start-Process` without `-Wait`, and direct or wrapped forms of `npm run dev`,
Vite, Nodemon, Webpack Serve, TypeScript watch, and `dotnet watch`. This
finite-command filter is a fail-closed guardrail for recognized forms, not
proof that an arbitrary opaque script cannot start persistent work; the Job
and timeout are the lifecycle backstop.

Approved persistent-process leases are not part of Y-PROC-1.1. A task that
needs a server or watcher must stop and request a separately scoped future
lease implementation; it must not bypass the finite broker.

## Codex lifecycle hook (explicit opt-in)

The broker's `finally` path and Job Object kill-on-close are the primary
cleanup boundary. When Codex exposes `CODEX_THREAD_ID`, the broker records it
as the task owner. Codex `Stop` and `SubagentStop` hooks can additionally
cancel active tasks whose owner matches the hook's `session_id`, verify their
Jobs empty, and fail closed without killing different-owner activity in the
same workspace:

```json
{
  "description": "Optional Y-PROC-1 cleanup defense in depth.",
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "yakherd process hook",
        "commandWindows": "yakherd process hook",
        "timeout": 30,
        "statusMessage": "Verifying Y-PROC-1 cleanup"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "yakherd process hook",
        "commandWindows": "yakherd process hook",
        "timeout": 30,
        "statusMessage": "Verifying Y-PROC-1 subagent cleanup"
      }]
    }]
  }
}
```

Add that definition to the trusted project's `.codex/hooks.json` only after
explicit human authorization and review it with Codex `/hooks`. Yakherd does
not install or trust hook automation automatically. Hooks are defense in depth;
specialized tool paths may not pass through normal hook coverage.

## Existing-repository migration

Do not refresh or rewrite unrelated SSOT content to adopt this policy.
`mosaic_colmap`, `SPLATOMATIC`, and `CROCHET` are already partially mitigated:
preserve their temporary process-hygiene text until native `yakherd exec` and
cleanup checks are proven active. A later reviewed, hash-pinned retrofit may
replace only that duplicate text with:

> For all local execution, obey Yakherd policy Y-PROC-1. Do not bypass its
> execution broker or process-lifecycle enforcement.

The migration record must identify the exact removed text and the native
control that replaces it. It must not modify any unrelated repository owner.

## Deferred scope

Adaptive worker budgets, CPU-rate controls, dynamic responsiveness monitoring,
resource pools, rich persistent leases, UI, and telemetry history are outside
Y-PROC-1.1. Add them only from measured evidence and a separate reviewed
scope.
