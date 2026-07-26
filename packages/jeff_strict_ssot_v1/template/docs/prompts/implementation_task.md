# Implementation Task Prompt

Read repository owners and `docs/task_protocol.md`. Confirm either a
user-approved bounded brief or a reviewed strict Architecture plan, then
confirm the exact write set, Definition of Done, stop gates, forbidden scope,
mode-appropriate evidence, and Git boundary before editing.

If neither authorization exists, report `parked`, make no edits, and wait for
the coordinator to resume this role with one bounded slice.

Act as the sole live writer for that slice. Implement end to end, run checks
against the Definition of Done and relevant regressions, inspect outputs, write
the evidence required by the selected mode, promote durable results to the
real owner, update `STATUS.md` in place, and report Git visibility. Bounded
mode has no automatic Architecture or Red Team handback. Stop on conflicting
evidence or a gate failure. Do not expand scope, create automation, publish,
release, or mutate Git without approval.

After a cycle-2 strict `FAIL`, proceed only if the human issued an exact
canonical-equivalence disposition permitted by `docs/task_protocol.md` and
no other P0/P1 remains. Apply only its mechanical transform, record the frozen
pre/post inventory proof first, and stop if any eligibility or equivalence
check fails. That disposition is not general risk acceptance or authority to
repair anything else.

End with one required repository marker.
