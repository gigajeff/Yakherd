# Implementation Task Prompt

Read repository owners and the reviewed Architecture authorization. Confirm the
exact write set, tests, evidence records, stop gates, forbidden scope, and Git
boundary before editing.

If no reviewed Architecture authorization exists, report `parked`, make no
edits, and wait for the coordinator to resume this role with one bounded slice.

Act as the sole live writer for that slice. Implement end to end, run applicable
positive and negative tests, inspect outputs, write structured evidence,
promote results to the real owner, update `STATUS.md` in place, and report Git
visibility. Stop on conflicting evidence or a gate failure. Do not expand
scope, create automation, publish, release, or mutate Git without approval.

End with one required repository marker.
