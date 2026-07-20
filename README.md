<p align="center">
  <img src="yakherd.png" alt="Yakherd banner" width="100%">
</p>

# Yakherd

**Yakherd - herds the yaks so your agent stops shaving them.**

Yakherd installs a strict, repository-centered single source of truth (SSOT)
harness for agentic software projects. It gives Architecture, Implementation,
Red Team, Temporary Branch, and Governor tasks durable ownership rules before
the first product prompt arrives.

[![CI](https://github.com/gigajeff/Yakherd/actions/workflows/ci.yml/badge.svg)](https://github.com/gigajeff/Yakherd/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)

## Absolute Beginner? Start Here

You do not need to understand "SSOT," Git, Python, or software architecture to
start. Yakherd is the **project-management and reliability half of vibe
coding**. It gives a coding agent a disciplined way to plan, build, check, and
remember a software project without letting important decisions disappear into
old chats.

You provide the other half: **your idea**, usually written as a master prompt.
The master prompt describes what you want the software to do. Yakherd does not
invent that idea for you; it gives the agent a safer, more organized working
environment in which to build it.

In short:

1. **Yakherd** provides the operating system for the work: roles, plans,
   decisions, evidence, review, and a durable source of truth.
2. **Your master prompt** provides the product: the problem, users, desired
   behavior, constraints, and definition of success.
3. **An agentic coding environment** such as Codex or Claude Code uses both to
   build the software.

If all you know how to do is talk to your coding agent, that is enough. Start a
new task in your agentic coding environment and tell it:

> Install Yakherd from https://github.com/gigajeff/Yakherd into a new project
> repository for me. Follow Yakherd's README and safety instructions. Do not
> overwrite an existing project. After installation and the required review,
> ask me for my idea or master prompt.

The agent can clone this repository, run the installer, and guide you through
the next step. Once Yakherd is installed and its initial review passes, give
the agent your master prompt. Together, Yakherd plus a clear master prompt can
turn an idea into usable software in Codex, Claude Code, or another capable
agentic coding environment.

Yakherd improves how the work is organized and reviewed; it does not guarantee
that every generated program is correct or safe. You should still review and
test consequential software before relying on it.

## Why Yakherd

Long-running agent projects often drift because decisions live in chat,
multiple files claim authority, failed experiments remain active, and the
human becomes a courier between tasks. Yakherd installs a small governance
shell that makes authority, current state, decisions, evidence, and review
boundaries explicit.

It is deliberately product-neutral. It does not choose your language,
framework, cloud provider, database, architecture, or deployment system.

## Quick Start

Clone Yakherd and preview a fresh installation without writing anything:

```powershell
git clone https://github.com/gigajeff/Yakherd.git
cd Yakherd
python yakherd.py init `
  --target L:\dev\MY_PROJECT `
  --project-name MY_PROJECT `
  --dry-run
```

Install into a nonexistent or empty folder:

```powershell
python yakherd.py init `
  --target L:\dev\MY_PROJECT `
  --project-name MY_PROJECT
```

Then open the generated
`docs/prompts/bootstrap_cold_resume_review.md` in a fresh Red Team task. Only
after that review passes should the repository receive its product master
prompt.

Linux and macOS use the same commands with POSIX paths and line continuations.

## What Gets Installed

- `SSOT.md`: authority map and conflict order.
- `DECISIONS.md`: durable decision owner.
- `STATUS.md`: bounded current-state index.
- `AGENTS.md`: repository operating rules.
- Architecture, Implementation, Red Team, Temporary Branch, and Governor task
  prompts.
- Governance, review, plan, run-record, and status-history directories.
- Standard-library validators and focused tests.
- A hash-bound installation receipt.

See [Usage](docs/USAGE.md) and [Architecture](docs/ARCHITECTURE.md).

## Existing Repositories

Retrofit mode is intentionally fail-closed. It requires a separately reviewed
JSON plan with an exact allowlist and expected hashes. Do not point fresh mode
at an established repository, and do not improvise a retrofit from the command
line. See [Retrofit Safety](docs/RETROFIT.md).

## Trust Boundary

Yakherd V1 distributes the exact package that passed the Mosaic-origin V3
independent review. `RELEASE.json` binds `bootstrap.py` and `MANIFEST.json`;
the manifest binds every installed template. The Git tag and GitHub release
authenticate those reviewed bytes externally.

The audited engine remains under `packages/jeff_strict_ssot_v1/` in V1 to
preserve its reviewed byte identity. A future release may rename internal
identifiers only after a new acceptance and independent review cycle.

## Non-Goals

Yakherd does not:

- run product code or experiments;
- install product dependencies;
- access project secrets;
- create automations;
- choose technical architecture;
- make Git mutations inside the target repository; or
- replace human approval for consequential decisions.

## Development

```powershell
python -B -m unittest discover `
  -s packages\jeff_strict_ssot_v1\tests -v

python packages\jeff_strict_ssot_v1\tests\run_acceptance.py `
  --package-root packages\jeff_strict_ssot_v1 `
  --output-root .tmp\acceptance `
  --date 2026-07-20
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing the audited package.

## License

Apache License 2.0. See [LICENSE](LICENSE).
