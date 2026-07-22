# Code And Protocol Review Checklist

Lead with correctness findings ordered by severity.

- Is the slice correctly classified under `docs/task_protocol.md`, based on
  actual authorized scope rather than hypothetical future work?
- Is this bounded work, or strict work with review cycle 1 or 2? A missing
  enhancement outside accepted scope is not a finding.
- Does the change stay inside its authorized slice?
- Does each durable fact have exactly one owner?
- Are owner changes and supersession explicit in `DECISIONS.md`?
- Was the real owner updated before `STATUS.md`?
- Is `STATUS.md` one dated current entry, updated in place, within both caps?
- Where strict mode or a consequential promoted claim requires structured
  evidence, does it name exact commands, exit codes, environment, supported
  claims, paths, hashes, limitations, and authority effect?
- Does protocol validation remain bounded, deterministic, standard-library
  only, read-only, and free of subprocess, product imports, network, Git, and
  writes?
- Are transcript records treated as authority-neutral retrieval aids?
- Is Governor output limited to findings/risks and the active delta policy?
- Are product choices absent until human-confirmed product intake?
- Are network, dependencies, automation, release, deployment, destructive
  actions, and Git publication separately authorized?
- Do tests include negative cases for the changed invariant?
- Does the final report state Git and remote visibility accurately?
- Does the result end with one required repository action marker?

Reject chat-only completion where durable promotion is required, status-only
promotion, duplicate mutable owners, silent supersession, fabricated product
facts, scope-expanding review findings, review-cycle evasion, or a Governor
acting as builder.
