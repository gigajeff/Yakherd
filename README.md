<p align="center"><img src="https://raw.githubusercontent.com/gigajeff/Yakherd/main/yakherd2.png" alt="Yakherd: stop shaving, start coding" width="100%"></p>

# Yakherd 3.0

**Stable requirements. Measured baseline. One current milestone.**

Yakherd installs a small, product-neutral SSOT harness so a coding agent can
open a repository, understand what is proven, and continue useful work without
reconstructing old conversations. One implementation task is the default.
Architecture and independent review serve concrete technical needs; there is
no mandatory team launch, bootstrap approval or product review ledger.

## Start a new project

Yakherd runs on Python 3.11+ with no runtime dependencies. Install version 3.0
from this repository:

```text
python -m pip install "git+https://github.com/gigajeff/Yakherd.git@main"
yakherd --version
yakherd setup path/to/project
yakherd doctor path/to/project
```

Confirm `yakherd --version` reports `3.0.0`. A Git install needs Git and network
access during package installation; the Yakherd installer itself never uses
the network or installs dependencies. For reproducible use, replace `main`
with the exact reviewed commit. PyPI availability is separate from a source
push; do not assume an older PyPI installation has these commands.

Open the project in your coding environment and give it your product request.
`Start Yakherd` means read the current owners and execute the authorized next
action in that task. A clear request does not need another approval after it
is recorded in NOW.md.

Setup accepts a new, empty or nonempty folder when every payload path is
absent. It preserves unrelated files and stops before writing on a collision.
Use `--dry-run` for a preview. Repeating setup on a v3 installation runs the
read-only doctor instead of reinstalling.

## What owns what

| File | Responsibility |
| --- | --- |
| `AGENTS.md` | Agent entry point and read order |
| `SSOT.md` | Stable mission, accepted requirements, invariants and operating rules |
| `BASELINE.md` | Proven facts, evidence, limitations and unknowns |
| `NOW.md` | One milestone, scope, Definition of Done, blockers and next action |
| `README.md` | Product setup, use and resume entry point |

The payload also includes a direct `START_HERE.md`, one-line `CLAUDE.md` import,
small `.gitignore`, versioned `.yakherd/profile.json` and Windows process policy.
A hash-bound `YAKHERD_INSTALL.json` records installation provenance. No product
stack, empty planning tree, permanent role roster or automation is installed.

The initial documents honestly state that product requirements are not yet
established. The agent adopts the supplied request, retains scientific and
safety constraints, and updates current owners as evidence changes. Git and
run artifacts hold history. A large specification or technical program gets
one linked owner only when useful.

## Existing projects

Follow [the migration guide](docs/SSOT_MIGRATION.md). Prepare project-specific
replacement files in a separate directory, preserving product requirements,
evidence, active work and process containment. Retire conflicting legacy
startup instructions explicitly.

```text
yakherd migrate plan YOUR_PROJECT --replacements PREPARED --output PLAN.json
yakherd migrate preview PLAN.json
```

After reviewing the exact content, set `reviewed` to `true`, compute the final
plan's SHA-256, and apply that exact plan:

```text
yakherd migrate apply PLAN.json --plan-sha256 REVIEWED_SHA256
yakherd doctor YOUR_PROJECT
```

Migration pins the package, target state and proposed content. It rejects
changed files and unsafe paths, validates the proposed structure before
writing, performs transactional replacements and retains original bytes in a
reported backup directory. Recovery limits and interrupted journals are
explained in the guide. It never guesses which product requirements to delete.
Plans/backups may contain private content; keep them out of public commits.

## What doctor establishes

Doctor reads repository data with trusted distributed code. It checks the v3
profile and owners, required NOW sections, local links, unresolved placeholders,
recognized active legacy launchers and interrupted migration state. It never
executes a repository's scripts. Customized project documents are expected.

A ready result means the structure passes those checks. It does not establish
product correctness, scientific validity, source trust or publication authority.
Independent tests and evidence remain necessary for the actual claim.

## Local execution

On Windows, use the included Y-PROC-1 broker for finite commands:

```text
yakherd exec --timeout 900 -- cmake --build build
yakherd process status
yakherd process cleanup --all-owned --dry-run --verify
```

Heavy pipelines run below normal priority and serialize while preserving
internal parallelism. Job Objects bind ownership and cleanup. Inconsistent
legacy records are warnings; unrelated processes are never cleanup targets.
The broker is Windows-specific; setup, migration and doctor are cross-platform.
The installer does not run builds, product code, network requests or Git.

## Documentation and development

- [Start or resume](START_HERE.md)
- [Canonical SSOT process](docs/SSOT_PROCESS.md)
- [Migration and recovery](docs/SSOT_MIGRATION.md)
- [Command usage](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Release verification](docs/RELEASE.md)

The v3 payload is in `packages/yakherd_v3/`. The historical V1 package remains
under `packages/jeff_strict_ssot_v1/` for provenance and regression checks; it is
not the default installer or a required product workflow.

Run `python -B -m unittest discover -s tests -v`, the v3 package tests, both
acceptance suites, `python -B scripts/verify_release.py`, and `git diff --check`.
Package changes require independent review; CI does not replace it.

Apache License 2.0. See [LICENSE](LICENSE).
