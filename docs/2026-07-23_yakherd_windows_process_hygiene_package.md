YAKHERD COMPLETE WINDOWS PROCESS-HYGIENE PACKAGE
Generated: 2026-07-23

PURPOSE

This is the complete handoff for Yakherd. It combines:

1. the full incident description;
2. the complete proposed Yakherd-native solution;
3. the full long-form Codex process-hygiene prompt;
4. the token-optimized prompt;
5. the ultra-compact Yakherd-backed prompt;
6. the implementation architecture;
7. the acceptance-test matrix;
8. the migration requirements for repositories already given temporary instructions;
9. the context that mosaic_colmap, SPLATOMATIC, and CROCHET have already received partial mitigation instructions;
10. the requirement not to refresh or rewrite unrelated SSOT content.

IMPORTANT MIGRATION CONTEXT

The following repositories already contain some temporary process-hygiene instructions:

- mosaic_colmap
- SPLATOMATIC
- CROCHET

Yakherd must treat these repositories as partially mitigated. Do not force a complete SSOT refresh. Preserve the temporary protections until native enforcement exists, then replace duplicated prompt text with the smallest Yakherd policy reference only after proving that native enforcement is active and equivalent or stronger.

======================================================================
FULL YAKHERD WINDOWS PROCESS-HYGIENE SPECIFICATION
======================================================================

# Yakherd Native Windows Process Hygiene and Responsiveness Policy

**Date:** 2026-07-23
**Status:** Proposed Yakherd feature and immediate Codex mitigation
**Working name:** `Y-PROC-1` / Local Execution Hygiene

## Instruction to Yakherd

Treat this document as a product-design and implementation task.

Inspect the current Yakherd repository and determine how to make the policy below a **native, enforceable part of Yakherd**, rather than relying primarily on repeated natural-language prompting. Produce the smallest reliable implementation that:

1. preserves normal build and test throughput;
2. keeps Windows responsive during heavy local work;
3. prevents uncontrolled process fan-out;
4. guarantees cleanup of task-owned process trees on completion, failure, cancellation, timeout, or agent stop;
5. does not kill unrelated user processes; and
6. can be inherited by every Yakherd-governed Codex repository with only a very small instruction stub.

Do not overengineer the first usable version. Prefer a narrow execution governor, deterministic cleanup, tests, and clear observability over a large general orchestration framework.

---

# 1. Incident summary

During a Codex task on a Windows workstation, the machine became nearly unusable:

- mouse movement and window interaction lagged by seconds;
- CPU reached 92–100%;
- memory, disks, and GPU were not the limiting resources;
- two Microsoft C/C++ compiler processes each consumed roughly 36–38% CPU;
- the ChatGPT/Codex process group contained approximately 118–140 processes;
- the process group retained approximately 7.2–7.7 GB of memory;
- many `Node.js JavaScript Runtime` and `node_repl.exe` processes existed;
- multiple Codex command runners, Console Window Hosts, PowerShell processes, CMake, Ninja, Git, and compiler processes were visible;
- closing the visible Codex task/window did not terminate the ChatGPT/Codex host or all descendants;
- many descendants remained after the task was apparently closed.

The important observation is that this was **not primarily a GPU, disk, or RAM exhaustion problem**. It was a combination of:

1. CPU saturation by compiler/build work;
2. excessive process fan-out;
3. weak ownership and lifecycle control over child processes;
4. possible overlapping local execution pipelines;
5. abandoned or idle REPL/runtime processes;
6. insufficient cleanup when a task was stopped or the UI was closed; and
7. heavy work running at a priority that allowed it to degrade desktop responsiveness.

This is a process-governance problem.

---

# 2. What must not be done

The permanent solution must **not** simply limit every build to two workers.

A two-worker limit would preserve responsiveness but materially reduce throughput on larger systems. The correct distinction is:

- **Allowed:** one finite top-level build or test pipeline using normal internal parallelism.
- **Disallowed:** several top-level build systems, test runs, package installs, subagents, REPLs, watchers, or command runners executing locally at the same time without coordination.

The target behavior is maximum useful throughput while Windows remains interactive.

Likewise, Yakherd must not solve this by globally killing every `node.exe`, `python.exe`, compiler, or shell process. That could destroy unrelated work. Cleanup must be based on verified task ownership.

---

# 3. Root-cause model

The exact Codex defect may vary, but Yakherd should defend against the entire class of failures.

## 3.1 Unbounded top-level concurrency

Multiple agents or tool calls may independently launch CPU-heavy operations. Each individual command may look reasonable while the combined workload saturates all logical processors and floods the scheduler.

## 3.2 Internal parallelism multiplied by external parallelism

A single Ninja, MSBuild, test runner, or package manager may already parallelize internally. Launching several such commands concurrently multiplies the worker count.

Example:

- three agents each start one Ninja build;
- each Ninja build creates 12 workers;
- the host sees up to 36 compiler jobs plus shells, runners, loggers, and antivirus activity.

## 3.3 Detached, interactive, or indefinite processes

REPLs, development servers, file watchers, `cmd /K`, PowerShell `-NoExit`, `Start-Process` without waiting, background jobs, and daemon modes can outlive the task that created them.

## 3.4 Missing process-tree ownership

A parent process can exit while descendants remain. Name-based cleanup is unsafe because unrelated processes may have the same executable name.

## 3.5 Incomplete cancellation semantics

A UI stop, agent stop, timeout, exception, or application close may not traverse and terminate every descendant.

## 3.6 CPU priority inversion at the user-experience level

Even legitimate work can make Windows unusable when all cores are saturated at normal priority. Heavy local jobs should yield promptly to desktop interaction without being artificially serialized internally.

---

# 4. Proposed Yakherd-native solution

## 4.1 Introduce a mandatory local execution broker

All Yakherd-governed local commands should pass through one execution entry point, conceptually:

```text
yakherd exec <command>
```

or an equivalent internal API.

Agents must not directly create unmanaged local subprocesses when Yakherd execution governance is active.

The broker should own:

- process creation;
- task identity;
- process-tree containment;
- priority;
- timeout;
- output capture;
- cancellation;
- cleanup;
- post-run verification; and
- telemetry.

This is the central control point. A prompt alone cannot reliably provide these guarantees.

## 4.2 Use a Windows Job Object for every execution task

On Windows, launch each top-level command inside a dedicated Job Object configured with kill-on-close behavior, preferably using:

```text
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
```

Every descendant that can be assigned to the Job Object should be contained in it.

Required behavior:

- normal completion closes the job after verifying no children remain;
- cancellation terminates the job;
- timeout terminates the job;
- agent stop terminates the job;
- broker crash or controlling-handle close kills job members where Windows semantics permit;
- Yakherd restart reconciles any recorded task that may have escaped containment.

Do not rely only on parent PID traversal. Use the operating system’s process-containment mechanism where possible.

## 4.3 Maintain a task-owned process registry

For every process created, record at least:

- Yakherd task ID;
- PID;
- parent PID;
- process creation time;
- executable path;
- command line;
- working directory;
- Job Object identity;
- start time;
- intended lifecycle: finite or approved persistent;
- termination state;
- exit code; and
- cleanup result.

PID alone is insufficient because Windows can reuse PIDs. Ownership checks must include creation time and preferably executable path and task/job identity.

## 4.4 Permit one heavy local pipeline while preserving internal parallelism

Default policy:

- one CPU-heavy top-level local execution pipeline per workstation or configured resource pool;
- normal internal parallelism inside that pipeline;
- lightweight read-only commands may run concurrently when classified safe;
- additional heavy pipelines queue rather than overlap;
- parallel reasoning/subagents may continue, but their local heavy execution requests must use the shared broker and governor.

This separates **agent concurrency** from **host execution concurrency**.

Yakherd should not globally disable multi-agent reasoning as the permanent solution. It should coordinate the commands produced by those agents.

## 4.5 Run heavy jobs at below-normal Windows priority

CPU-intensive build, test, compiler, linker, code-generation, indexing, and package-install tasks should normally run with:

```text
BELOW_NORMAL_PRIORITY_CLASS
```

Their child processes should inherit the appropriate priority where possible.

This should preserve most throughput because the work can consume otherwise-idle CPU, while Windows interaction, Desktop Window Manager, and foreground applications receive scheduling preference.

Do not automatically lower priority for latency-sensitive helper processes unless required.

## 4.6 Optional adaptive CPU budget, not a fixed two-worker limit

The initial implementation can preserve the build system’s normal parallelism and rely on:

- one heavy pipeline at a time; and
- below-normal priority.

If responsiveness is still unacceptable, add an adaptive resource policy:

- detect logical processor count;
- reserve approximately one or two logical processors for Windows;
- translate that into tool-specific worker flags only for tools Yakherd understands;
- avoid applying a worker cap when the tool is I/O-bound or already self-regulating;
- allow per-repository overrides.

For the observed 6-core/12-thread machine, a starting ceiling of roughly 10 workers would be more reasonable than 2, but this should be measured rather than hard-coded globally.

## 4.7 Ban unmanaged interactive and indefinite processes

Unless the user explicitly authorizes a persistent process, reject or require confirmation for:

- bare `node`, `node_repl.exe`, or another interactive Node invocation;
- bare `python` without a finite script or `-c`;
- `cmd /K`;
- PowerShell `-NoExit`;
- `Start-Process` without `-Wait`;
- `start` without `/WAIT`;
- `Start-Job`;
- watch modes;
- daemon modes;
- development servers;
- file watchers;
- `npm run dev`;
- `vite`;
- `nodemon`;
- `webpack serve`;
- `tsc -w`;
- `dotnet watch`;
- equivalent commands that intentionally remain alive.

A finite script executed by Node or Python remains allowed.

## 4.8 Persistent-process leases

Some tasks legitimately require a server or watcher.

Yakherd should support an explicit persistent-process lease containing:

- task ID;
- PID and process identity;
- exact command;
- purpose;
- working directory;
- owner;
- start time;
- lease expiry or “until explicitly stopped” state;
- health state; and
- exact stop command.

No persistent process should exist merely because an agent happened to detach it.

## 4.9 Deterministic stop and cleanup hooks

Integrate cleanup with Codex lifecycle hooks where available, particularly turn-level `Stop` and `SubagentStop` events.

The hook should call Yakherd’s cleanup/reconciliation command, not duplicate complex process logic in the hook itself.

Conceptually:

```text
yakherd process cleanup --scope current-turn --verify
```

Important limitation: a Stop hook is an additional enforcement path, not the sole owner of process state. Cleanup must also occur inside the execution broker’s `finally` path.

## 4.10 Startup orphan reconciliation

On Yakherd startup:

1. load the process registry;
2. inspect tasks not marked cleanly terminated;
3. verify process identity using PID plus creation time and other metadata;
4. terminate only verified Yakherd-owned leftovers;
5. report what was found and what was terminated;
6. never kill an ambiguous process automatically.

This addresses application crashes and abnormal shutdowns.

## 4.11 Observable execution status

Yakherd should expose a concise status command:

```text
yakherd process status
```

It should report:

- active finite tasks;
- queued heavy tasks;
- approved persistent tasks;
- task-owned PIDs;
- CPU and memory use;
- priority class;
- elapsed time;
- cleanup failures; and
- suspected orphans.

A cleanup command should support dry-run mode:

```text
yakherd process cleanup --dry-run
```

## 4.12 Safe emergency cleanup

Provide a scoped emergency command:

```text
yakherd process cleanup --all-owned --verify
```

It must kill only processes whose Yakherd ownership is verified.

Do not implement emergency cleanup as:

```text
taskkill /F /IM node.exe
```

or any other broad executable-name kill.

---

# 5. Minimal implementation versus later hardening

## 5.1 Minimum usable implementation

The first usable Yakherd implementation should contain:

1. one local execution broker;
2. Windows Job Object containment;
3. below-normal priority for heavy commands;
4. one-heavy-pipeline concurrency control;
5. finite-command enforcement;
6. PID plus creation-time process registry;
7. cancellation and timeout cleanup;
8. end-of-task zero-leftover verification;
9. status and dry-run cleanup commands; and
10. automated Windows tests.

This is sufficient to solve the observed class of failure without turning Yakherd into a general cluster scheduler.

## 5.2 Later hardening

Only after the minimum implementation works:

- adaptive per-tool worker budgeting;
- CPU-rate control;
- dynamic responsiveness monitoring;
- repository-specific resource pools;
- cross-repository global scheduling;
- richer persistent-process lease management;
- UI integration;
- process telemetry history;
- recovery from unusual child-process breakaway behavior.

---

# 6. Required acceptance tests

Yakherd must test at least the following on Windows.

## 6.1 Normal finite command

A process creates nested children and exits normally.

**Pass condition:** all descendants exit; registry shows clean completion; no unrelated process is touched.

## 6.2 Internal parallel build

A single Ninja/MSBuild/CMake build creates many compiler workers.

**Pass condition:** internal workers are allowed; only one top-level heavy pipeline runs; Windows remains usable; cleanup is complete.

## 6.3 Two agents request heavy builds simultaneously

**Pass condition:** one runs and one queues, or policy explicitly budgets them without oversubscription.

## 6.4 Cancellation

The user stops the agent during compilation.

**Pass condition:** the entire task-owned process tree terminates promptly.

## 6.5 Timeout

A process intentionally hangs.

**Pass condition:** timeout terminates all task-owned descendants and reports the reason.

## 6.6 Parent exits before child

The parent launches a child and exits.

**Pass condition:** Job Object ownership still permits cleanup.

## 6.7 Interactive REPL attempt

An agent tries to launch bare Node or Python.

**Pass condition:** rejected, converted to a finite invocation, or explicitly approved.

## 6.8 Watch/server attempt

An agent starts a persistent server without permission.

**Pass condition:** blocked pending explicit lease approval.

## 6.9 Approved persistent process

A server is explicitly approved.

**Pass condition:** PID, command, purpose, working directory, and stop method are recorded; it is not killed by ordinary finite-task cleanup.

## 6.10 Broker crash or forced app close

Terminate the controlling Yakherd/Codex process abnormally.

**Pass condition:** Job Object kill-on-close handles members where possible; startup reconciliation finds and safely handles any verified leftovers.

## 6.11 PID reuse safety

Simulate a stale registry entry whose PID now belongs to another process.

**Pass condition:** Yakherd does not kill it because identity no longer matches.

## 6.12 Unrelated Node process

Start an unrelated user-owned Node process before the test.

**Pass condition:** Yakherd cleanup leaves it untouched.

## 6.13 Repeated stress test

Run hundreds of short commands, cancelled builds, and nested child trees.

**Pass condition:** process and handle counts return to baseline; no monotonic leak is observed.

---

# 7. Immediate long-form Codex instruction

Until Yakherd enforces this natively, use the following instruction in active Codex threads.

```text
## Mandatory local process hygiene

These rules are mandatory for every local task.

1. Use only one top-level local execution pipeline at a time. A single build or
   test command may use its normal internal parallelism. Do not cap builds to
   two workers unless I explicitly request that.

2. Do not launch multiple builds, test runs, package installations, or code
   generation commands concurrently.

3. Never start an interactive shell or REPL. Specifically:
   - Never start node or node_repl.exe without a finite script or `node -e`.
   - Never use JavaScript code mode or an interactive Node REPL.
   - Never start Python without a script or `-c`.
   - Never use `cmd /K`, PowerShell `-NoExit`, or any process that waits
     indefinitely for interactive stdin.

4. Never detach or background a process. Do not use:
   - Start-Process without `-Wait`
   - start without `/WAIT`
   - Start-Job
   - watch mode
   - daemon mode
   - persistent development servers
   - file watchers
   - npm run dev
   - vite, nodemon, webpack serve, tsc -w, dotnet watch, or equivalent
   unless I explicitly request a persistent process.

5. Parallel reasoning is allowed, but do not use subagents or parallel agents
   to execute local shell commands. Local execution must be serialized.

6. Run CPU-heavy build, test, compiler, linker, and code-generation commands
   at Windows BELOW_NORMAL process priority. Preserve the build system's
   normal internal parallelism.

7. Every command must be finite, remain attached to its initiating process,
   and have a reasonable timeout.

8. Track the PID of every process you create. Also track every descendant PID
   created by those processes.

9. Use try/finally cleanup semantics. On success, failure, cancellation,
   timeout, interruption, or user stop, terminate the entire descendant
   process tree created by the command.

10. Before completing every turn:
    - Enumerate all processes created during the turn.
    - Terminate any that remain.
    - Enumerate again and verify that zero task-owned processes remain.
    - Do not report completion until this verification succeeds.

11. Never terminate processes that existed before the task. Clean up only
    processes and descendants whose PIDs were created during this task.

12. If cleanup fails, stop all further work and report the remaining process
    names, PIDs, parent PIDs, command lines, and the attempted cleanup action.

13. If a task genuinely requires a persistent process, ask me first. After
    approval, report its PID, complete command line, purpose, working
    directory, and exact command required to terminate it.
```

---

# 8. Token-optimized temporary instruction

The long prompt is useful as a formal specification, but it should not be copied into every `AGENTS.md`.

## 8.1 Recommended compact standalone version

```text
LOCAL PROCESS HYGIENE: Use one finite top-level local execution pipeline at a
time; preserve normal internal build/test parallelism. Run CPU-heavy work at
Windows BELOW_NORMAL priority. Never launch REPLs, watchers, detached/background
jobs, or persistent servers without explicit approval. Track task-owned process
trees and, on success/failure/cancel/timeout/stop, terminate and verify zero
task-owned descendants remain. Never kill pre-existing or unrelated processes.
```

This captures the essential behavioral contract without imposing a two-worker cap.

## 8.2 Ultra-compact Yakherd-backed version

Once Yakherd enforces `Y-PROC-1` natively, the global instruction can be:

```text
All local commands must use Yakherd Y-PROC-1: one governed finite pipeline,
normal internal parallelism, below-normal heavy-job priority, no unapproved
persistent/background/REPL processes, and verified task-owned tree cleanup on
every exit path.
```

This is the preferred long-term form because enforcement lives in code rather than tokens.

## 8.3 Minimal repository-level reference

If a repository contains the policy document or Yakherd skill:

```text
For all local execution, obey Yakherd policy Y-PROC-1. Do not bypass its
execution broker or process-lifecycle enforcement.
```

---

# 9. Token-efficiency architecture

OpenAI’s Codex guidance supports keeping `AGENTS.md` small and using richer reusable mechanisms for detailed workflows. Yakherd should exploit that structure.

## 9.1 Put only the invariant in `AGENTS.md`

`AGENTS.md` should contain the compact policy identifier and core prohibition, not implementation detail.

## 9.2 Store the detailed policy in one Yakherd-managed location

Possible locations:

```text
.yakherd/policies/Y-PROC-1.md
```

or a Yakherd skill:

```text
.agents/skills/yakherd-process-hygiene/SKILL.md
```

A skill is suitable because only compact metadata is needed for discovery, while the full instructions and scripts can be loaded when local execution is involved.

## 9.3 Enforce with code and hooks

The prompt should describe intent. The broker, Job Object, registry, and hooks should guarantee behavior.

The most token-efficient instruction is the one that refers to a mechanism the agent cannot bypass.

## 9.4 Do not refresh unrelated SSOT content

This policy is orthogonal to each repository’s domain SSOT. It should be inherited globally or injected by Yakherd as an execution-layer policy, without forcing every agent to reread or rewrite the full repository SSOT.

---

# 10. Codex configuration notes

## 10.1 Multi-agent mode

Current Codex configuration exposes `features.multi_agent`, and it is enabled by default.

Temporary diagnostic:

```toml
[features]
multi_agent = false
```

This can reduce process fan-out while the native governor is absent. It is **not** the preferred permanent design because parallel reasoning is useful. Yakherd should instead coordinate local execution across agents.

## 10.2 Code mode

Current Codex configuration exposes:

```toml
[features.code_mode]
enabled = false
```

Code mode is documented as under development and off by default. Therefore, the observed `node_repl.exe` population must not be attributed to code mode without checking the actual configuration and command lines.

Explicitly setting it to false may still be useful as a diagnostic pin, but it is not a substitute for process ownership and cleanup.

## 10.3 Stop hooks

Codex supports lifecycle hooks including `Stop` and `SubagentStop`. Yakherd should use these as deterministic calls into its own cleanup mechanism.

Hooks must not contain broad process-name kills.

---

# 11. Immediate operator guidance

Until Yakherd is implemented:

1. use the compact standalone prompt in each currently active agent rather than refreshing the entire SSOT;
2. do not cap builds to two workers by default;
3. allow one top-level heavy build/test command with normal internal parallelism;
4. require below-normal priority for CPU-heavy work;
5. prohibit local heavy execution from parallel subagents;
6. prohibit detached, interactive, and persistent commands without approval;
7. require task-owned process-tree cleanup and verification;
8. use temporary `multi_agent = false` only when process fan-out continues and no governor exists;
9. inspect actual command lines before blaming code mode or a particular runtime; and
10. report any cleanup failure with PID, parent PID, creation time, executable path, and command line.

---

# 12. Required Yakherd deliverables

Yakherd should return:

1. a concise architecture decision;
2. the exact minimal implementation scope;
3. repository files to add or modify;
4. a Windows Job Object/process broker implementation;
5. task process-registry format;
6. concurrency and priority policy;
7. Stop/SubagentStop hook integration;
8. status, dry-run cleanup, and emergency owned-only cleanup commands;
9. unit and integration tests covering the acceptance matrix;
10. a compact `AGENTS.md` integration line;
11. a migration plan for existing Yakherd-governed repositories that does not require rewriting their SSOT; and
12. explicit exclusions and deferred hardening to prevent scope creep.

The implementation is not complete until cancellation, timeout, abnormal exit, and repeated stress testing prove that task-owned process and handle counts return to baseline without affecting unrelated processes.


======================================================================
COMPLETE HANDOFF AND TOKEN-OPTIMIZED MIGRATION GUIDANCE
======================================================================

# Yakherd Process-Hygiene Handoff

## Context

The following is the complete response provided after creating the Yakherd Windows process-hygiene specification.

The user has already applied some of the earlier process-hygiene instructions to these repositories:

- `mosaic_colmap`
- `SPLATOMATIC`
- `CROCHET`

Yakherd should therefore treat those repositories as **already partially mitigated** and avoid forcing a full SSOT refresh merely to introduce this policy. The desired migration is a minimal, token-efficient integration that can later replace the temporary repository-specific prompts with native Yakherd enforcement.

---

[Download the Yakherd Windows process-hygiene specification](sandbox:/mnt/data/yakherd_windows_process_hygiene_spec.md)

The document includes:

- The observed failure: 100% CPU, 118–140 descendants, abandoned Node/REPL processes, and incomplete shutdown.
- A Yakherd-native solution using a mandatory execution broker, Windows Job Objects, owned-process tracking, cleanup verification, priority control, and concurrency governance.
- A full acceptance-test matrix.
- The complete long-form Codex prompt from above.
- Compact and ultra-compact replacements.
- A deliberately limited MVP scope to avoid turning Yakherd into an oversized scheduler.

I removed the inappropriate **two-worker limit**. The intended policy is:

> One top-level heavy execution pipeline, with normal internal build parallelism, running at below-normal priority.

That should preserve most build speed while avoiding several independently parallelized builds multiplying into a workstation-wide process storm.

## Recommended prompt for your existing agents

```text
LOCAL PROCESS HYGIENE: Use one finite top-level local execution pipeline at a
time; preserve normal internal build/test parallelism. Run CPU-heavy work at
Windows BELOW_NORMAL priority. Never launch REPLs, watchers, detached/background
jobs, or persistent servers without explicit approval. Track task-owned process
trees and, on success/failure/cancel/timeout/stop, terminate and verify zero
task-owned descendants remain. Never kill pre-existing or unrelated processes.
```

## Once Yakherd enforces it natively

Your `AGENTS.md` entry can shrink to:

```text
All local commands must use Yakherd Y-PROC-1: one governed finite pipeline,
normal internal parallelism, below-normal heavy-job priority, no unapproved
persistent/background/REPL processes, and verified task-owned tree cleanup on
every exit path.
```

The correct token-efficient architecture is to keep only that invariant in `AGENTS.md`, place the detailed policy and scripts in a Yakherd skill or policy file, and enforce cleanup through code and lifecycle hooks. Codex’s current documentation explicitly recommends keeping `AGENTS.md` small, supports progressively loaded skills, and provides `Stop` and `SubagentStop` hooks for deterministic validation or cleanup.

The specification also corrects one diagnostic assumption: multi-agent tools are currently enabled by default, but code mode is documented as off by default. Therefore, disabling multi-agent execution may be useful temporarily, while the `node_repl.exe` infestation should not be blamed on code mode without checking actual command lines and configuration.

---

## Yakherd migration requirement

Because `mosaic_colmap`, `SPLATOMATIC`, and `CROCHET` already contain temporary process-hygiene instructions, Yakherd should:

1. detect and preserve those temporary protections during implementation;
2. avoid rewriting or refreshing unrelated SSOT content;
3. introduce native `Y-PROC-1` enforcement centrally;
4. replace repository-local long prompts later with the one-line Yakherd reference;
5. verify that removing the duplicated prompt text does not weaken enforcement; and
6. provide a migration report listing which repositories were updated, what text was removed, and which native control now replaces it.

The intended end state is:

```text
For all local execution, obey Yakherd policy Y-PROC-1. Do not bypass its
execution broker or process-lifecycle enforcement.
```

No repository should need to carry the full long-form process-hygiene specification once Yakherd enforces the policy in code.


======================================================================
FINAL REQUIRED END STATE
======================================================================

Yakherd must implement this as enforceable execution infrastructure, not merely as prose.

The target repository-level instruction is:

For all local execution, obey Yakherd policy Y-PROC-1. Do not bypass its
execution broker or process-lifecycle enforcement.

The target behavior is:

- one governed finite top-level local execution pipeline at a time;
- normal internal build and test parallelism preserved;
- CPU-heavy work run at Windows BELOW_NORMAL priority;
- no unapproved REPLs, watchers, detached jobs, background jobs, or persistent servers;
- task-owned process-tree tracking;
- deterministic cleanup on success, failure, cancellation, timeout, interruption, agent stop, subagent stop, and abnormal shutdown;
- zero verified task-owned descendants remaining at task completion;
- no broad process-name killing;
- no interference with pre-existing or unrelated user processes;
- startup orphan reconciliation;
- observable status and dry-run cleanup;
- Windows Job Object containment where technically possible;
- migration of mosaic_colmap, SPLATOMATIC, and CROCHET without unrelated SSOT refreshes.

Do not report this work complete until the Windows acceptance tests demonstrate that process and handle counts return to baseline after repeated builds, cancellations, timeouts, nested child trees, and abnormal exits.
# Y-PROC-1 source package (superseded in part by Y-PROC-1.1)

> **Correction:** The original Core 1.3 package below is preserved as source
> evidence. Its PID-ownership and cleanup-severity portions are amended by
> [Y-PROC-1.1 corrective amendment](2026-07-23_y_proc_1_1_corrective_amendment.md).
> Core 1.3.1 treats PID reuse, incomplete legacy identity, and contradiction as
> warnings; only a failed cleanup of a live Job-verified task process with
> concrete hazard evidence blocks unrelated work.
