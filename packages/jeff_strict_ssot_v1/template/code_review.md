# Code And Protocol Review Checklist

Lead with correctness findings ordered by severity.

- Does the change stay inside its authorized slice?
- Does each durable fact have exactly one owner?
- Are owner changes and supersession explicit in `DECISIONS.md`?
- Was the real owner updated before `STATUS.md`?
- Is `STATUS.md` one dated current entry, updated in place, within both caps?
- Does structured evidence name exact commands, exit codes, environment,
  supported claims, paths, hashes, limitations, and authority effect?
- Does protocol validation remain bounded, deterministic, standard-library
  only, read-only, and free of subprocess, product imports, network, Git, and
  writes?
- Are transcript records treated as authority-neutral retrieval aids?
- Is Governor output limited to findings/risks and the active delta policy?
- Are product choices absent until reviewed product intake?
- Are network, dependencies, automation, release, deployment, destructive
  actions, and Git publication separately authorized?
- Do tests include negative cases for the changed invariant?
- Does the final report state Git and remote visibility accurately?
- Does the result end with one required repository action marker?

Reject chat-only completion, status-only promotion, duplicate mutable owners,
silent supersession, fabricated product facts, or a Governor acting as builder.
