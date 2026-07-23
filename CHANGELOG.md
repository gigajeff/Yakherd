# Changelog

All notable changes to Yakherd are recorded here.

## 1.3.1 - Unreleased

- Corrects `Y-PROC-1` as `Y-PROC-1.1`: coherent PID/time/path/command-line,
  parent-epoch, task/execution and Job-membership snapshots are now classified
  before any cleanup. PID reuse, legacy records, and contradictory evidence are
  warnings and are never cleanup targets.
- Separates cleanup warnings from blockers. Only a still-live, Job-verified,
  task-owned process whose cleanup failed with concrete hazard evidence blocks
  unrelated work. `yakherd process resume --task TASK_ID` records one explicit
  warning acknowledgement and cannot waive a blocker.

## 1.3.0 - Unreleased

- Adds Windows policy `Y-PROC-1` and a standard-library `yakherd exec` broker
  that atomically creates commands inside kill-on-close Job Objects before
  their first instruction, serializes heavy top-level pipelines, preserves
  internal parallelism, and runs heavy work below normal priority.
- Adds PID-plus-creation-time process records, identity-verified startup
  reconciliation, status, dry-run and scoped owned cleanup, timeout/cancel
  cleanup, and a session-scoped Stop/SubagentStop-compatible hook command
  without silently installing hook automation.
- Rejects known REPL, detached, watcher, daemon, and development-server forms;
  persistent-process leases and adaptive worker budgeting remain explicitly
  deferred and fail closed.
- Installs a compact `AGENTS.md` invariant and detailed
  `.yakherd/policies/Y-PROC-1.md` owner. Existing `mosaic_colmap`, `SPLATOMATIC`,
  and `CROCHET` repositories retain their partial mitigations until a later
  narrow, reviewed retrofit proves native enforcement before removing text.
- Adds a root `docs/task_protocol.md` as Yakherd's canonical development owner,
  retains the separately scoped packaged template copy, and validates both
  files and both `AGENTS.md` ownership pointers in the release verifier.
- Includes the root task protocol in the source distribution; the installed
  template task protocol remains hash-bound in the wheel and source archive.

- Adds proportional `bounded` and `strict` work modes so reversible local
  slices can proceed directly from a human-confirmed brief without universal
  Architecture and Red Team gates.
- Constrains Red Team to accepted requirements and hazards introduced by the
  exact diff, makes P2/P3 advisory, removes `pass_with_fixes`, and caps each
  strict work ID at one initial review plus one recheck before mandatory human
  rescoping, risk acceptance, or cancellation.
- Requires one active plan/review path per work ID and forbids version-suffixed
  candidate proliferation as a way to evade the review circuit breaker.
- Adds a beginner `START_HERE.md` handoff and an explicit Codex launcher that
  creates all five governed role agents under one non-authoritative
  coordinator, with fail-closed reporting when any role cannot be created.
- Defines visible startup states so the five roles exist without violating the
  single-writer rule: Red Team reviews, Architecture waits, Implementation and
  Temporary Branch park, and Governor stays inactive.
- Adds master-prompt delimiters, raw UTF-8 preservation, SHA-256/byte-length
  provenance, Architecture extraction, and human confirmation of the first
  bounded brief or strict planning scope.
- Adds approval-gated setup for the user's own GitHub account and project while
  preserving the installer's no-network/no-Git-mutation boundary.
- Makes the launcher, GitHub checkpoint, and prompt provenance mechanically
  required by the generated protocol validator and negative tests.
- Existing installations require a separately reviewed, hash-pinned retrofit;
  Yakherd does not overwrite them automatically.

## 1.1.1 - 2026-07-20

- Pins the PyPI publishing action to the immutable `v1.14.0` source SHA that
  also names its published container image. The failed `v1.1.0` workflow had
  already passed every source, test, acceptance, archive, and smoke-install
  gate before stopping at the unavailable commit-SHA container image; it did
  not upload a distribution.
- Separates the unprivileged build, test, acceptance, archive inspection, and
  smoke-install work from the minimal Trusted Publisher job. Only that final
  job can mint the PyPI OIDC token, and it can only retrieve and publish the
  verified distribution artifact.
- Keeps the reviewed governance payload unchanged apart from the regenerated
  package-version and release-hash bindings.

## 1.1.0 - 2026-07-20

- Adds first-class Claude Code support through a generated `CLAUDE.md` adapter
  that imports the authoritative `AGENTS.md`.
- Makes the Claude adapter part of the required, hash-pinned protocol and adds
  negative validation fixtures for missing or divergent adapters.
- Documents the capabilities required of coding environments and distinguishes
  native Codex/Claude Code support from explicit compatibility with other
  agents and ordinary AI chat.
- Adds platform-specific beginner installation prompts and clarifies that the
  Mosaic-origin audits authenticate the 1.0.0 bytes only.
- Documents project-session, first-import approval, and loaded-context checks
  required before Claude Code begins governed work.
- Fresh 1.1.0 installations gain `CLAUDE.md`; existing repositories require a
  separately reviewed retrofit because Yakherd never overwrites them silently.
- Removes the pure protocol validator's ambient wall-clock dependency so the
  same repository bytes and arguments always produce the same result.
- Gives the bootstrap cold-resume review an explicit, bounded JSON run-record
  write set so a fresh Red Team can satisfy the repository evidence contract.
- Makes every installed protocol-check command bytecode-free and requires the
  cold review to fail if its own checks create Python cache paths.
- Adds the dependency-free `yakherd` Python package and console command, with
  tag-bound GitHub Trusted Publishing for wheel and source distributions.
- Leads installation documentation with bash/macOS/Linux examples, followed
  by equivalent Windows PowerShell commands.
- Adds an inspectable cold-resume recording with its exact prompt and result,
  passing review, structured run records, preserved failed attempts, and a
  SHA-256 evidence index.

## 1.0.0 - 2026-07-20

- First public Yakherd release.
- Includes the exact independently reviewed Jeff Strict SSOT V1 package.
- Provides fresh-install and reviewed retrofit modes.
- Includes five task roles: Architecture, Implementation, Red Team, Temporary
  Branch, and Governor.
- Includes compact status, decision-history, transcript-neutrality, Governor
  delta-policy, validation, and migration controls.
- Adds a root Yakherd launcher, documentation, CI, release verification, and
  Apache-2.0 licensing.
