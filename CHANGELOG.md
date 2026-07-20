# Changelog

All notable changes to Yakherd are recorded here.

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
