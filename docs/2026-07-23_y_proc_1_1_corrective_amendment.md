YAKHERD CORE 1.3 CORRECTIVE AMENDMENT
Y-PROC-1.1 — PROCESS IDENTITY, CLEANUP SEVERITY, AND NON-DEADLOCKING RESUME

Context

Y-PROC-1 Core 1.3 was implemented and passed its original tests, but real use in
CROCHET and mosaic_colmap exposed two policy defects:

1. CROCHET permanently blocked work because a tracked process record was
   internally inconsistent:
   - image name: vctip.exe
   - recorded parent: nvidia-smi.exe
   - reported command line: python.exe -m unittest ...
   Ownership could not be established, yet the hygiene rule treated the record
   as a blocker.

2. mosaic_colmap retained bare numeric PIDs after the original processes exited.
   Windows reused those PIDs, and cleanup then attempted actions against
   unrelated or protected process identities.

These are defects in Yakherd Core’s process identity and cleanup-severity model.
Correct them natively in process_hygiene.py, Y-PROC-1.md, tests, hooks, status
output, reconciliation, and documentation.

Do not deploy to downstream repositories in this task. Modify and validate
Yakherd Core only.

======================================================================
1. PROCESS IDENTITY MUST BE A COHERENT SNAPSHOT
======================================================================

A tracked process identity must contain:

- PID
- process creation timestamp
- executable path
- executable image name derived from that path
- command line
- parent PID
- parent creation timestamp when available
- Yakherd task ID
- execution/session ID
- Job Object identity or verified membership
- observation timestamp
- lifecycle classification

PID is only an address used to look up a live process. PID is never identity.

Before any terminate, signal, ownership assertion, or blocking decision,
Yakherd must re-query the current process and compare it with the original
identity snapshot.

Minimum verified ownership requires:

- PID matches;
- creation timestamp matches;
- executable path matches;
- task or Job Object ownership matches when available.

Command line and parentage are supporting evidence, not sole proof.

======================================================================
2. REJECT INTERNALLY INCONSISTENT RECORDS
======================================================================

Add an identity-coherence validator.

Examples of incoherence:

- image name says vctip.exe but executable path or command line identifies
  python.exe;
- executable path and image name disagree;
- command line is attributed to a different executable;
- parent metadata belongs to a different creation epoch;
- Job Object membership conflicts with the recorded task;
- one observation combines fields captured from different process instances.

An incoherent record must be classified:

    ownership_record_inconsistent

It must never be used to terminate a process or block unrelated work.

Record the defect, preserve diagnostic metadata, remove it from the actionable
cleanup set, and continue unless an independently verified hazard exists.

======================================================================
3. FORMAL PROCESS-STATE MACHINE
======================================================================

Replace binary “remaining/not remaining” logic with these states:

- VERIFIED_LIVE_OWNED
- VERIFIED_EXITED
- PID_REUSED_UNRELATED
- OWNERSHIP_UNVERIFIED
- OWNERSHIP_RECORD_INCONSISTENT
- APPROVED_PERSISTENT
- CLEANUP_WARNING
- CLEANUP_BLOCKER

Required transitions:

A. PID absent:
   -> VERIFIED_EXITED
   -> remove active tracking record promptly

B. PID present, creation time differs:
   -> PID_REUSED_UNRELATED
   -> never signal or terminate the current process
   -> remove stale active tracking record

C. PID present, executable path differs:
   -> PID_REUSED_UNRELATED or OWNERSHIP_UNVERIFIED
   -> never signal or terminate
   -> remove from actionable cleanup set

D. original creation time/path were never recorded:
   -> OWNERSHIP_UNVERIFIED
   -> do not terminate
   -> do not block unless a separately verified concrete hazard exists

E. fields are internally contradictory:
   -> OWNERSHIP_RECORD_INCONSISTENT
   -> do not terminate
   -> do not block unrelated work

F. PID, creation time, executable identity, and task ownership all match:
   -> VERIFIED_LIVE_OWNED
   -> cleanup may proceed

G. explicitly leased process:
   -> APPROVED_PERSISTENT
   -> exclude from ordinary finite-task cleanup

======================================================================
4. STALE PID REUSE IS NORMAL, NOT A CLEANUP FAILURE
======================================================================

A stale PID that now points to another process is not:

- a leftover task process;
- a cleanup failure;
- a blocker;
- a reason for human intervention;
- a reason to restart Windows.

It is a normal PID-reuse event.

Yakherd must:

1. classify it as PID_REUSED_UNRELATED;
2. discard the stale actionable record;
3. avoid querying or acting on the replacement process beyond the minimum
   identity comparison needed to establish mismatch;
4. continue the task.

Completed process records must be retired promptly. Do not retain numeric PIDs
as active cleanup targets after verified process exit.

======================================================================
5. CLEANUP WARNING VERSUS CLEANUP BLOCKER
======================================================================

A cleanup anomaly must not automatically stop all future work.

Classify as CLEANUP_BLOCKER only when all of the following are true:

1. the process is positively VERIFIED_LIVE_OWNED; and
2. cleanup failed; and
3. the process creates a concrete current hazard.

Concrete hazards include:

- meaningful ongoing CPU, GPU, disk, network, or memory consumption;
- a file, directory, executable, database, port, mutex, device, or build-tree
  lock required by the next action;
- duplicate execution of the same job;
- risk of corrupting active repository or product state;
- direct interference with the command about to run;
- an uncontrolled process capable of continuing to mutate outputs.

Classify as CLEANUP_WARNING when:

- ownership is unverified;
- the record is inconsistent;
- PID reuse occurred;
- the process is idle and not interfering;
- cleanup telemetry is incomplete;
- a harmless process may remain but no concrete hazard is established.

CLEANUP_WARNING must not create a global execution embargo.

======================================================================
6. EXPLICIT USER RESUME SEMANTICS
======================================================================

When the user explicitly says “resume”, “continue”, or equivalent:

- resume automatically after resolving or downgrading non-hazardous warnings;
- do not repeatedly request the same human authorization;
- do not require Windows restart for an ambiguous, stale, reused, inconsistent,
  or harmless process record;
- preserve uncommitted work;
- continue from the last safe checkpoint.

User authorization may override CLEANUP_WARNING.

User authorization must not override a verified, active, concrete
CLEANUP_BLOCKER without a clear explanation of the danger.

======================================================================
7. JOB OBJECTS ARE PRIMARY; PID SCANS ARE SECONDARY
======================================================================

Use Windows Job Object membership as the primary process ownership boundary.

PID/creation/path records are supporting identity evidence and reconciliation
metadata.

Do not reconstruct ownership later solely from:

- ancestry;
- parent PID;
- executable name;
- command-line similarity;
- temporal proximity.

Parentage alone is not authoritative because parent processes can exit and PIDs
can be reused.

If a process is not verified as a member of the task Job Object and no coherent
creation identity exists, ownership is unproven.

======================================================================
8. SAFE TERMINATION PROTOCOL
======================================================================

Before termination:

1. re-query live process identity;
2. compare creation timestamp;
3. compare executable path;
4. verify Job Object/task ownership;
5. validate identity-field coherence;
6. classify state;
7. terminate only VERIFIED_LIVE_OWNED processes.

After termination:

1. wait for exit with bounded timeout;
2. re-query identity;
3. distinguish:
   - original process still alive;
   - original process exited;
   - PID already reused;
4. never interpret a newly reused PID as failed termination.

Do not use process-name-wide kills.

======================================================================
9. STATUS AND REPORTING CHANGES
======================================================================

yakherd process status must separately report:

- verified live owned processes;
- approved persistent processes;
- stale PID reuse events;
- ownership-unverified records;
- inconsistent identity records;
- cleanup warnings;
- cleanup blockers.

Do not report:

    TRACKED_REMAINING count=1

without also reporting the classification and ownership confidence.

Preferred output:

    VERIFIED_LIVE_OWNED=0
    PID_REUSED_UNRELATED=1
    OWNERSHIP_UNVERIFIED=0
    OWNERSHIP_RECORD_INCONSISTENT=0
    CLEANUP_WARNING=1
    CLEANUP_BLOCKER=0

Only CLEANUP_BLOCKER may automatically stop unrelated work.

======================================================================
10. LEGACY RECORD HANDLING
======================================================================

Existing process records created before Y-PROC-1.1 may lack creation timestamps,
paths, or Job Object identity.

For legacy records:

- never infer ownership from PID alone;
- classify missing-identity records as OWNERSHIP_UNVERIFIED;
- do not terminate them automatically;
- do not block work unless an independent concrete hazard is proven;
- archive or retire them after diagnostic reporting.

======================================================================
11. REQUIRED NEW TESTS
======================================================================

Add tests for all of the following:

1. Original process exits; PID is reused by an unrelated process.
   PASS: replacement is not signaled, terminated, or blocked on.

2. PID reused by a protected/system process.
   PASS: no cleanup action is attempted against the replacement identity.

3. Image name, executable path, and command line conflict.
   PASS: OWNERSHIP_RECORD_INCONSISTENT; no termination; no blocker.

4. Record says vctip.exe while command line identifies python.exe.
   PASS: inconsistent record detected automatically.

5. Original record lacks creation time.
   PASS: OWNERSHIP_UNVERIFIED; warning only unless concrete hazard proven.

6. Parent PID is reused.
   PASS: parentage does not establish ownership.

7. Verified owned child survives cancellation and consumes CPU.
   PASS: CLEANUP_BLOCKER until terminated or safely resolved.

8. Verified owned child survives but is idle and cannot affect subsequent work.
   PASS: cleanup warning or bounded exception, not global permanent deadlock.

9. User says resume after warning.
   PASS: task resumes without asking again.

10. User says resume while a verified process holds a required lock.
    PASS: Yakherd explains the concrete blocker and does not proceed unsafely.

11. Termination succeeds and the PID is immediately reused.
    PASS: cleanup is reported successful, not “still remaining.”

12. Completed records are retired before plausible PID reuse.

13. Job Object membership conflicts with ancestry inference.
    PASS: Job Object/task identity wins.

14. Repeated stress test with rapid PID reuse.
    PASS: no unrelated process receives terminate, signal, handle, or cleanup
    action.

15. Status output distinguishes warning classes from blockers.

======================================================================
12. CORRECT THE ORIGINAL ABSOLUTE RULE
======================================================================

Replace:

    terminate and verify zero task-owned descendants remain;
    do not report completion until verification succeeds

with:

    terminate every VERIFIED_LIVE_OWNED finite-task descendant; verify that no
    verified owned hazardous descendants remain. Classify PID reuse,
    unverified ownership, inconsistent records, and harmless anomalies
    explicitly. Only a verified concrete cleanup blocker may stop unrelated
    work.

The invariant is not “zero numeric PIDs remain.”

The invariant is:

    zero verified, task-owned, unapproved, hazardous processes remain.

======================================================================
13. DOCUMENTATION AND VERSIONING
======================================================================

Update:

- src/yakherd/process_hygiene.py
- packages/jeff_strict_ssot_v1/template/.yakherd/policies/Y-PROC-1.md
- implementation plan
- process-hygiene package
- Red Team audit
- installer/distribution manifests if required
- hook behavior
- status/cleanup command documentation
- acceptance tests

Version the correction as Y-PROC-1.1 or Yakherd Core 1.3.1.

Do not claim completion based only on unit tests. Run fresh Windows acceptance
tests exercising real process creation, cancellation, PID reuse, conflicting
identity metadata, and user-authorized resume.

======================================================================
14. REQUIRED COMPLETION REPORT
======================================================================

Report:

- root causes in the original Core 1.3 implementation;
- exact files changed;
- process-state model implemented;
- ownership proof requirements;
- cleanup warning versus blocker logic;
- explicit resume behavior;
- legacy-record behavior;
- tests added and results;
- independent Red Team result;
- final process status;
- confirmation that no downstream repository was modified;
- commit status, but do not commit or push unless separately authorized.
