# Yakherd Concierge V1 - Pre-Intake Bootstrap and Candidate Implementation Architecture

Document date: 2026-07-21
Plan schema: `yakherd-concierge-architecture-plan-v3`
Status: pre-intake candidate for independent Red Team review; no product implementation authority
Architecture owner: Architecture task
Product owner: Jeffrey Martin (`gigajeff`)

## 1. Decision, authority, and exact inputs

The product owner has now made these two decisions:

1. Yakherd `v1.2.0`, rather than a moving "newest release", is the Concierge V1
   target release.
2. Architecture is authorized to convert the static-only directive into this
   bounded plan.

This record does not claim that `v1.2.0` is public yet. On 2026-07-21, the
public GitHub tags page exposed tags only through `v1.1.1`, the GitHub releases
page exposed no `v1.2.0` release, and PyPI reported `1.1.1` as latest. Gate R
below must make and authenticate the public release before any website product
implementation starts.

The exact product-direction input is:

- path: `docs/2026-07-21_yakherd_concierge_v1_build_directive_static_only.md`
- bytes: `17487`
- SHA-256: `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`
- author of record: Jeffrey Martin
- capture limitation: this path is the LF-normalized durable copy selected by
  the owner for Architecture conversion. The earlier attachment had 17,804
  bytes, CRLF line endings, and SHA-256
  `247b10e35f4dea73699807bba0150b4670cd25fe38d077f9b46ef27dd6a24308`.
  No claim is made that the durable copy preserves attachment transport bytes.
  The owner is selecting the reviewed durable copy, identified above, as the
  product-direction bytes for this plan.

The exact first review of that input is:

- path: `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_build_directive_red_team.md`
- bytes: `19030`
- SHA-256: `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`
- verdict: `FAIL`

This v3 preserves and supersedes, without editing, both earlier bounded
candidates. The first candidate and its review are:

- predecessor path:
  `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan.md`
- predecessor bytes: `68774`
- predecessor SHA-256:
  `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029`
- predecessor audit:
  `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team.md`
- predecessor-audit bytes: `16166`
- predecessor-audit SHA-256:
  `34b19607510fdd696904974e2cb56aced148ef2b46838dec72ce6fd5a62a6fda`
- predecessor verdict: `FAIL`

The immediate v2 predecessor and its review are:

- predecessor path:
  `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan_v2.md`
- predecessor bytes: `103293`
- predecessor lines: `1956`
- predecessor SHA-256:
  `68f444c46992b0dd31c8b84f328d85b86cc6851e1c3693ca22bc8b44aca2809a`
- predecessor audit:
  `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team_v2.md`
- predecessor-audit bytes: `15149`
- predecessor-audit lines: `137`
- predecessor-audit SHA-256:
  `32b1274e4350ea732b14565d9925fb8c4d9bd61728a60c6f63f039e41676b1ec`
- predecessor verdict: `FAIL`

This pre-intake plan resolves both audits by making the repository, release, byte model,
runtime policy, privacy boundary, fixtures, evidence, and later authorities
explicit. It does not retroactively call the source attachment a completed
installed-project intake. Formal unchanged `product_intake.md` intake occurs
in the separate `yakherd-web` project at Gate P, after `v1.2.0` installs that
contract. The raw prompt there will be the exact 17,487-byte durable directive
above, enclosed in the exact v1.2.0 delimiter envelope. Until Gate P passes,
this document is design evidence only and cannot authorize product code. Gate
P requires a new post-intake implementation plan and a new independent audit;
this pre-intake candidate never becomes executable merely by being copied.

## 2. Product boundary

Build one static browser application that guides a beginner through a fixed
interview, mechanically drafts a master prompt, lets the beginner edit and
approve it, and downloads a deterministic five-file ZIP handoff for Yakherd
`v1.2.0`.

Concierge V1 does not install Yakherd, authenticate to GitHub, call the GitHub
API, or create, read, or modify the visitor's GitHub repositories. It may show
the exact public, user-initiated Yakherd repository/release links in Section 6.
It does not launch Codex tasks, run product code, call a model, create an account, receive
user input at a server, or deploy anything for the visitor. Those statements
describe runtime product behavior; they do not prohibit separately authorized
maintainers from using Git, tests, or deployment tools to build and publish the
static site.

Not in V1:

- model-backed interrogation or a relay endpoint;
- PHP, Workers, functions, APIs, forms, accounts, sessions, analytics, or
  telemetry;
- the complete governed repository export, local runner, workbench, or private
  GitHub backup;
- DreamHost capability work or the retired v15 preflight;
- a service worker, web manifest, Cache API, background sync, share API, or
  browser notifications;
- any dependency, package install, vendored library, build step, minifier, or
  generated production source.

## 3. Alternatives and selected architecture

Architecture considered three data-loading designs:

1. Runtime `fetch()` of JSON and text. Rejected because it makes the no-request
   boundary timing-dependent and requires `connect-src`.
2. Inline JSON/templates in HTML. Rejected because it needs inline content and
   duplicates authoritative resources in a difficult-to-audit form.
3. Versioned source data files plus one external, committed JavaScript content
   module containing their exact base64 bytes. Selected. A dependency-free
   verifier decodes that module and requires byte equality with every source
   data file. The browser loads only HTML, CSS, JavaScript, and the local image;
   no JavaScript networking API is needed.

Architecture selects plain HTML5, one CSS file, ES2020 JavaScript modules, and
standard-library-only Python and Node verification. There is no compilation or
transformation step. The content module is committed source, not generated at
deploy time.

Every shipped JavaScript module and every Node test uses the unambiguous `.mjs`
extension. Every import specifier is a literal relative `.mjs` path. HTML entry
scripts use `type="module"`. Node therefore applies ES-module semantics without
`package.json`, a package `type`, an experimental flag, or ambient configuration.
The accepted runtime is Node `>=20.0.0`; Gate X binds the full version and
executable identity before any Implementation-authored module executes. The
Node tests do not use the `node --test` CLI. Seven test modules export
side-effect-free `runTests()` functions; `tests/test_interview.mjs` imports and
invokes them in the fixed Section 5 order and then runs its own assertions in
the same direct Node process. This avoids the CLI test runner's default child-
process isolation and its version-dependent isolation flags. No package manifest is
created. A later local/browser capability gate must separately prove that the
selected local server and host serve `.mjs` as a JavaScript MIME type before
claiming browser support.

Hosting is deliberately not selected in this plan. Cloudflare Pages and
Netlify remain candidates. Transport headers, DNS, staging, rollback, and
production are Gate H/D work after a separately reviewed hosting inventory and
owner decision. Application-flow parity under `python -m http.server` is in
scope; TLS, redirects, response headers, caching, compression, MIME overrides,
and host logs are explicitly not locally identical.

## 4. Gates and authority sequence

The gates are strictly serial. A FAIL or missing artifact parks every later
gate. PASS never grants an unnamed action.

### Gate A - plan review (current gate)

An independent Red Team reviews the exact bytes of this plan and every bound
input/predecessor record in Section 1. A PASS authorizes only Gate R-PREP
below. It does not authorize package or release-file mutation, artifact
construction, installation, Git mutation, network or browser access,
credentials, tagging, GitHub/PyPI action, publication, Gate B, product intake,
or Implementation contact.

### Gate R-PREP - documentation-only release preparation

Gate R-PREP is documentation-only. Architecture may read the current tracked
Yakherd release inputs and read-only Git metadata and may exclusively create,
with no overwrite, this one candidate:

`docs/2026-07-21_yakherd_v1.2.0_release_preparation_plan.md`

Independent Red Team may exclusively create, with no overwrite, this one
review:

`docs/audits/yakherd/2026-07-21_yakherd_v1.2.0_release_preparation_plan_red_team.md`

No other path may change. The candidate must freeze the proposed package and
release write set, source baseline, validation commands, artifact output and
retention paths, artifact inventory/schema, public-name/version expectations,
credential boundary, failure cleanup, publication transaction, rollback, and
fresh final-review boundary. It may describe later actions but cannot perform
them.

A FAIL permits only a new documentation-only candidate and fresh review. A
PASS may authorize only a separately bounded local release-candidate slice
whose exact paths and commands were reviewed. It does not authorize a tag,
push, GitHub release, PyPI upload, public mutation, or publication.

### Gate R - separately reviewed release candidate, final gate, publication, and authentication

This is a separate Yakherd engine release task, not website implementation. It
requires a fresh release candidate, all checks in `docs/RELEASE.md`, an exact
artifact inventory, independent final release review, and explicit publication
authority. Per the owner's model policy, the final release gate uses one Sol
Ultra reviewer; Ultra is not used for preparation.

Gate R cannot begin from Gate A alone. Local candidate preparation requires a
PASS at Gate R-PREP. Publication additionally requires exact completed artifact
identities, one final independent Sol Ultra release PASS, and explicit human
publication authority after those identities are known. Preparation or review
never implies publication.

The release evidence must bind all of the following before Gate B:

- tag `v1.2.0` and its full 40-hex commit;
- GitHub release URL;
- PyPI project-version URL;
- wheel and sdist direct immutable-version URLs, filenames, byte lengths, and
  lowercase SHA-256 values;
- `README.md`, package `README.md`, package `RELEASE.json`, package
  `MANIFEST.json`, installed `START_HERE.md`, and installed
  `docs/prompts/product_intake.md` paths, lengths, and SHA-256 values;
- the exact `yakherd==1.2.0` installation command and its supported Python
  range;
- evidence that a fresh install from each public artifact passes the release
  smoke test;
- public observations from GitHub and PyPI after publication.

The current intended package contract, which Gate R must either preserve or
explicitly supersede in a newly reviewed candidate, is:

- current engine baseline commit:
  `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`;
- root `README.md`: 12,252 bytes, SHA-256
  `3f520ed064dd57da8bee7260bf02502f12ab8c0198d907b849d66a3365367f02`;
- package `README.md`: 4,778 bytes, SHA-256
  `0bda15f2a8c73198ffb62647b67c880d6b33530225df9110faca09be4951354b`;
- `RELEASE.json`: 473 bytes, SHA-256
  `312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`;
- `MANIFEST.json`: 7,006 bytes, SHA-256
  `ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`;
- bootstrap SHA-256 from `RELEASE.json`:
  `c41f4f5d11e5eb3bfed9eabfdef7444e28612d124a26101df8bfb3628837a8bb`;
- installed `START_HERE.md`: 3,104 bytes, SHA-256
  `6fea5767314320f646c85a4b48de67f6ce564f5c248baa5ec8896023c421d241`;
- installed `product_intake.md`: 2,614 bytes, SHA-256
  `c1582bcc7918eeb547bcae8d4ceec14cfbe36267ed7313131012b0ba95c32604`.

Gate R writes its evidence only to an exact path named in its separately
reviewed release authorization. This plan supplies no tag, GitHub, PyPI,
credential, network, or publication authority.

### Gate B - create the separate governed project root

Target local root: `L:\dev\yakherd-web`.

This gate requires a separate authorization after Gate R. At entry:

- the literal target must not exist;
- `L:\dev` must resolve to the intended parent;
- the target and every ancestor from `L:\dev` downward must not be a symlink,
  junction, mount point, or other reparse point;
- the operator must record the resolved absolute target and parent;
- no GitHub repository, remote, credential, or network write is authorized;
- no existing path may be overwritten.

The gate creates the directory and performs a fresh `yakherd==1.2.0` install
using the exact public artifact and command bound at Gate R, with project name
`yakherd-web`. It first runs the installer's dry run. It then records the
installation receipt, exact installed path inventory, hashes, and verifier
output. Before the bootstrap prompt may write anything, Gate B freezes a
canonical `gate_b_installed_baseline` in its separately reviewed external
evidence path. It is a Section 10 canonical JSON array plus LF in ASCII
repository-path order, covers every descendant directory and regular file,
excludes the root, and has rows containing exactly `bytes`, `path`, `sha256`,
and `type`. Directories use type `DIRECTORY`, bytes 0, and SHA
`NOT_APPLICABLE`; regular files use type `REGULAR_FILE`, a nonnegative safe-
integer byte count, and 64-lowercase-hex SHA-256. Any reparse point, other type,
duplicate, case-fold collision, or escape fails Gate B. Its evidence separately
binds the exact `JEFF_STRICT_SSOT_INSTALL.json` identity; the receipt hash is
not used as a substitute for the full baseline hash. No site file is written.
The fresh bootstrap Red Team prompt then runs from the new root and must PASS.

The current Implementation task attached to `L:\dev\YAKHERD` is not an
authorized writer for the site. Before Gate Q, exactly one Implementation task
must be attached to `L:\dev\yakherd-web`, must demonstrate that the installed
`AGENTS.md` is loaded, and must be the sole product writer. No second
Implementation writer may target that checkout.

Git initialization, branch creation, GitHub repository creation, visibility,
remote creation, push, PR, and publication remain parked for their normal
post-bootstrap owner checkpoint. "Separate repository" at Gate B means a
separate future repository root; it does not smuggle Git authority into this
plan.

### Gate P - unchanged product intake in yakherd-web

After the bootstrap PASS, Architecture receives one handoff whose exact bytes
are:

```text
MASTER PROMPT START
<the exact 17,487 bytes identified in Section 1>
MASTER PROMPT END
```

If the selected prompt ends in LF, the envelope contains that LF plus the one
separate LF immediately preceding `MASTER PROMPT END`; the intake parser
removes only the boundary LF and therefore preserves the prompt's terminal LF.

Architecture follows the installed, hash-bound `product_intake.md` without
modification. In the same bounded intake transaction, it creates the raw
prompt and exact provenance, reads them back, records byte length/hash, makes
the explicit `DECISIONS.md` owner-promotion entry and corresponding `SSOT.md`
owner update while retaining that raw input is not executable authority,
updates the affected Architecture-owned paths and compact `STATUS.md` required
by the installed completion contract, and writes a new, standalone post-intake
candidate at
`docs/plans/yakherd_concierge_v1_implementation_plan.md`. That file must bind
the installed raw prompt/provenance/owner-decision identities, actual Gate R
release values, bootstrap evidence, exact Sections 5-17 of this design, all
resolved fixture identities, canonical bytes/hashes for every data file, the
complete user-facing copy inventory required by Section 7A, and its own exact
write/evidence boundaries.

The post-intake candidate also contains two canonical strict-base64 blocks.
The first decodes to the complete proposed
`scripts/concierge_gate_i_runner.py`, plus its decoded byte length, lowercase
SHA-256, literal version `yakherd-concierge-gate-i-runner/1`, exact CLI grammar,
exit-code table, import allowlist, filesystem matrix, Windows Job Object
behavior, child-environment contract, journal/event schemas, command table,
evidence serializers, and terminal-inventory rules in Sections 14-15. The
second decodes to the complete literal PowerShell prelaunch resolver source,
plus its decoded byte length, lowercase SHA-256, and literal version
`yakherd-concierge-prelaunch-resolver/1`. That source implements only the exact
identity gate and launch behavior in Section 14; it is never installed as a
file. Both blocks are design material and are not executed at Gate P. The
combined Gate P Red Team must independently strict-base64 decode, hash, and
review every byte of both blocks.

Before Gate P performs its first mutation, Architecture constructs in memory
the canonical `pre_gate_p_manifest`. It covers every descendant directory and
regular file then present below `L:\dev\yakherd-web`; the repository root is
excluded. It is a Section 10 canonical JSON array in ordinal repository-path
order. Each row contains exactly `bytes`, `origin_relation`, `path`, `sha256`,
and `type`.

`type` is exactly `DIRECTORY` or `REGULAR_FILE`. Directories use `bytes: 0` and
`sha256: "NOT_APPLICABLE"`. Regular files use a nonnegative safe-integer byte
length and a 64-lowercase-hex SHA-256. Paths are unique normalized repository-
relative strings. A symlink, junction, reparse point, other filesystem type,
escape, duplicate, or case-fold collision fails Gate P before mutation.

`origin_relation` is exactly one of:

- `GATE_B_INSTALLED_BASELINE`: the row is identical to the complete post-
  install inventory bound by Gate B, including the separately bound identity
  of `JEFF_STRICT_SSOT_INSTALL.json`; or
- `BOOTSTRAP_CREATED`: the row is one of the five
  `docs/run_records/bootstrap_cold_resume_<RUN_ID>_*.json` files or the one
  `docs/reviews/bootstrap_cold_resume_<RUN_ID>.md` file authorized by the
  installed bootstrap prompt.

All six `BOOTSTRAP_CREATED` rows use the same accepted UTC `<RUN_ID>`, are
linked by the bootstrap PASS review, and retain their observed identities. No
directory row is `BOOTSTRAP_CREATED`, because the required parent directories
are part of the installed baseline. The exact delta from the Gate B installed
baseline to `pre_gate_p_manifest` must be those six regular files: no deletion,
replacement, type change, additional path, or other byte change is permitted.

The post-intake candidate embeds the complete canonical
`pre_gate_p_manifest`, its byte length, and its SHA-256. It also embeds a
canonical Gate P after-manifest for the pre-review project tree except the plan
file containing the manifests. The after-manifest uses the same ordering,
path, type, byte, and hash rules, with rows containing exactly `after_bytes`,
`after_sha256`, `after_type`, `baseline_relation`, and `path`.

`baseline_relation` is exactly one of:

- `UNCHANGED_PRE_GATE_P_BASELINE`: the path and identity equal its
  `pre_gate_p_manifest` row;
- `CHANGED_BY_GATE_P`: the path existed in `pre_gate_p_manifest`, is in the
  exact Gate P write set, and has the reviewed after-identity; or
- `CREATED_BY_GATE_P`: the path was absent from `pre_gate_p_manifest`, is in
  the exact Gate P create set, and has the reviewed after-identity.

Rows cover every descendant directory and regular file except the containing
plan and future combined audit. Every `pre_gate_p_manifest` row maps to exactly
one unchanged or changed after-row; every created after-row was absent from the
pre-manifest. An omitted path, unexplained addition, deletion, type change, or
relation mismatch fails Gate P. The plan prints both complete manifest bytes,
lengths, and SHA-256 values.

The containing plan and future audit are excluded only to avoid self-reference
and prediction. Gate I binds their independently observed identities as two
additional pre-existing records. The combined Gate P Red Team independently
reconstructs the pre-manifest from the Gate B installed baseline plus the six
accepted bootstrap artifacts, verifies the complete before/after relation,
and binds both manifest identities.

Every Gate P decision/owner/status byte says that its effect is conditional on
PASS at the one fixed combined-audit path. Therefore no unreviewed post-audit
edit is needed: FAIL leaves a non-authoritative retained candidate requiring a
reviewed recovery plan, while PASS makes the exact already-reviewed promotion
effective. `STATUS.md` points to that fixed predicate instead of predicting a
verdict. Gate Q/I-W accepts only the separately bound containing plan,
combined audit, and exact Gate Q runner as post-manifest target additions; no
other post-manifest mutation is accepted.

Architecture then sends the raw prompt hash, provenance, exact owner changes,
SSOT/status/affected-owner diff, extraction path, plan and after-manifest
identities, unresolved questions, and complete diff together to independent
Red Team. That one review covers the full
unchanged-intake transaction and the implementation candidate at
`docs/reviews/yakherd_concierge_v1_implementation_plan_red_team.md`. Neither
review path nor plan path may pre-exist. PASS must confirm that the installed
raw prompt is exactly 17,487 bytes with the Section 1 SHA-256 and that every
intake/owner/plan step conforms to the installed contract. There is no earlier
partial "intake PASS." The current pre-intake plan is a design input to that
work, not the executable authorization. Any substitution is a new Architecture
revision and fresh review.

### Gate Q - exact governance-runner transcription and activation review

Only the combined Gate P PASS may authorize this non-product activation slice.
The sole Terra-high Implementation writer creates exactly one previously
absent file, `scripts/concierge_gate_i_runner.py`, by strict-base64 decoding the
complete block in the reviewed post-intake plan. It uses fail-if-exists create,
flush, read-back, byte-length comparison, and SHA-256 comparison. It does not
import, compile, or execute the new file and creates no other target path.

One independent Sol-xhigh reviewer then reads the exact runner, independently
strict-base64 decodes the complete prelaunch-resolver block without executing
it, and may
exclusively create these two previously absent external records:

- `L:\dev\YAKHERD\docs\audits\yakherd\2026-07-21_yakherd_web_gate_q_runner_activation_red_team.md`;
- `L:\dev\YAKHERD\docs\audits\yakherd\2026-07-21_yakherd_web_gate_q_runner_activation.json`.

Before either write, that reviewer makes exactly one read-only Python-runtime
observation with the Python-only subset of the Gate X PowerShell script: it
requires one uniquely resolved non-reparse regular `python` application,
captures/checks the integer exit from `python --version`, enforces the same
Python >=3.11 ASCII grammar, and outputs only
`PYTHON_BINARY_BYTES`, `PYTHON_BINARY_SHA256`, and `PYTHON_VERSION`. It emits no
path or environment value and performs no other command, mutation, or network
action. The complete literal command is repeated in the post-intake plan and
independently reviewed with the runner.

```powershell
$ErrorActionPreference = 'Stop'
try {
$pythonCommands = @(Get-Command python -CommandType Application -All -ErrorAction Stop)
if ($pythonCommands.Count -ne 1) { throw 'PYTHON_RUNTIME_RESOLUTION_AMBIGUOUS' }
$pythonItem = Get-Item -LiteralPath $pythonCommands[0].Source -Force -ErrorAction Stop
if ($pythonItem.PSIsContainer -or ($pythonItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'PYTHON_RUNTIME_PATH_INVALID' }
$pythonVersionOutput = & $pythonItem.FullName --version 2>&1
$pythonExit = $LASTEXITCODE
$pythonVersion = ($pythonVersionOutput | Out-String).Trim()
if ($pythonExit -ne 0) { throw 'PYTHON_RUNTIME_VERSION_COMMAND_FAILED' }
if ($pythonVersion -notmatch '^Python 3\.(1[1-9]|[2-9][0-9])\.[0-9]+$') { throw 'PYTHON_RUNTIME_VERSION_INVALID' }
$pythonHash = (Get-FileHash -LiteralPath $pythonItem.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
'PYTHON_BINARY_BYTES=' + $pythonItem.Length
'PYTHON_BINARY_SHA256=' + $pythonHash
'PYTHON_VERSION=' + $pythonVersion
} catch {
  [Console]::Error.WriteLine('PYTHON_RUNTIME_OBSERVATION_FAILED')
  exit 1
}
```

All success values are computed before the first stdout line. Any failure emits
only `PYTHON_RUNTIME_OBSERVATION_FAILED\n` on stderr, exits nonzero, and emits
no success line; the reviewer retains no caught exception text.

The JSON record is Section 10 canonical JSON plus LF with exactly `audit_bytes`,
`audit_path`, `audit_sha256`, `checks`, `prelaunch_resolver_bytes`,
`prelaunch_resolver_sha256`, `prelaunch_resolver_version`, `python_runtime`,
`runner_bytes`, `runner_path`, `runner_sha256`, `runner_version`,
`schema_version`, and `status`. `python_runtime` has exactly `binary_bytes`,
`binary_sha256`, and `version` from that observation. Resolver values reproduce
the second decoded design block and its version is exactly
`yakherd-concierge-prelaunch-resolver/1`. Schema is 1,
status is `PASS`, paths are the exact literals above/Section 5, identities are
nonnegative safe-integer bytes and lowercase SHA-256, version is
`yakherd-concierge-gate-i-runner/1`, and `checks` contains exactly, in this
order, `strict_base64_reproduced`, `source_identity_matched`, `cli_closed`,
`journal_serializer_reviewed`, `evidence_serializer_reviewed`,
`windows_job_confinement_reviewed`, `stream_boundary_reviewed`,
`child_environment_closed`, `outer_output_fixed`, `python_runtime_bound`,
`prelaunch_resolver_strict_base64_reproduced`,
`prelaunch_resolver_source_reviewed`, and
`prelaunch_resolver_substitutions_closed`, each with exactly `name` and
`status = PASS`. The audit identity is calculated after the Markdown
audit is finalized; the JSON is then exclusively created once. The audit does
not predict the JSON's identity. FAIL creates no PASS JSON, grants no retry or
execution authority, and requires a new reviewed post-intake candidate.

### Gate I-W - write-only candidate construction

Only a Gate Q PASS and the fresh combined Gate P PASS may send this exact slice
to the same sole Implementation writer. Gate I-W permits the Section 5 paths,
the behavior in Sections 6-13, and the source/journal portion of Section 15.
The reviewed runner is the only project executable it may invoke, and every
outer runner launch must pass through the exact Gate Q-reviewed prelaunch
resolver defined in Section 14. No symbolic `python` runner launch is
permitted. The runner creates and validates the journal, brackets every
remaining directory/file mutation, and emits only fixed status tokens. Gate
I-W must not import, evaluate, compile,
execute, or test any Implementation-authored Python or JavaScript. It stops
after every product/test/fixture/golden byte is durably read back and the
runner appends `PRE_EXECUTION_REVIEW_REQUESTED`.

Gate I-W and every later local gate forbid external network use, dependency
installation, Git/GitHub mutation, browser automation, screenshots, OS-matrix
work, accessibility scanners, screen readers, hosting, DNS, credentials,
staging, deployment, production, and publication.

### Gate X - independent pre-execution capability review

One independent Sol-xhigh reviewer performs an offline read-only exact-source
review. Gate X executes no Implementation-authored code. It verifies the
complete executable-source manifest, closed import graph, bounded top-level
module behavior, fixed filesystem-access matrix, absence of network,
environment, credential, dependency-resolution, dynamic-code, and process-
creation capabilities, the direct Node harness, the minimal child environment,
and the frozen runner's process-confinement implementation. It may exclusively
create these two previously absent external records:

- `L:\dev\YAKHERD\docs\audits\yakherd\2026-07-21_yakherd_web_gate_x_pre_execution_red_team.md`;
- `L:\dev\YAKHERD\docs\audits\yakherd\2026-07-21_yakherd_web_gate_x_pre_execution_authorization.json`.

After source review but before writing either record, Gate X may make exactly
one independent runtime observation using this read-only PowerShell script from
the target root:

```powershell
$ErrorActionPreference = 'Stop'
try {
$pythonCommands = @(Get-Command python -CommandType Application -All -ErrorAction Stop)
$nodeCommands = @(Get-Command node -CommandType Application -All -ErrorAction Stop)
if ($pythonCommands.Count -ne 1 -or $nodeCommands.Count -ne 1) { throw 'RUNTIME_RESOLUTION_AMBIGUOUS' }
$pythonItem = Get-Item -LiteralPath $pythonCommands[0].Source -Force -ErrorAction Stop
$nodeItem = Get-Item -LiteralPath $nodeCommands[0].Source -Force -ErrorAction Stop
if (-not $pythonItem.PSIsContainer -and -not $nodeItem.PSIsContainer -and -not ($pythonItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -and -not ($nodeItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
  $pythonVersionOutput = & $pythonItem.FullName --version 2>&1
  $pythonExit = $LASTEXITCODE
  $nodeVersionOutput = & $nodeItem.FullName --version 2>&1
  $nodeExit = $LASTEXITCODE
  $pythonVersion = ($pythonVersionOutput | Out-String).Trim()
  $nodeVersion = ($nodeVersionOutput | Out-String).Trim()
  if ($pythonExit -ne 0 -or $nodeExit -ne 0) { throw 'RUNTIME_VERSION_COMMAND_FAILED' }
  if ($pythonVersion -notmatch '^Python 3\.(1[1-9]|[2-9][0-9])\.[0-9]+$' -or $nodeVersion -notmatch '^v(2[0-9]|[3-9][0-9]|[1-9][0-9]{2,})\.[0-9]+\.[0-9]+$') { throw 'RUNTIME_VERSION_INVALID' }
  $pythonHash = (Get-FileHash -LiteralPath $pythonItem.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  $nodeHash = (Get-FileHash -LiteralPath $nodeItem.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  'PYTHON_BINARY_BYTES=' + $pythonItem.Length
  'PYTHON_BINARY_SHA256=' + $pythonHash
  'PYTHON_VERSION=' + $pythonVersion
  'NODE_BINARY_BYTES=' + $nodeItem.Length
  'NODE_BINARY_SHA256=' + $nodeHash
  'NODE_VERSION=' + $nodeVersion
} else { throw 'RUNTIME_PATH_INVALID' }
} catch {
  [Console]::Error.WriteLine('RUNTIME_OBSERVATION_FAILED')
  exit 1
}
```

On success, the six output lines are the complete allowed observation channel. They contain
no executable path, username, environment value, or credential. Gate X records
them in its audit/JSON and rejects extra output, non-ASCII, duplicate/missing
keys, invalid lengths/hashes/versions, nonzero exit, or a runtime path that is
not one non-reparse regular file. The command writes no file and uses no
network. Because all values are computed before output, failure emits only
`RUNTIME_OBSERVATION_FAILED\n` on stderr with nonzero exit and no success line;
caught exception text is not retained. No other independent runtime/path
observation is authorized.

Gate X may then execute only this Gate Q-reviewed, fixed-output capability
probe through `RESOLVE_AND_RUN`, the literal Section 14 prelaunch-resolver
operation (the notation is not a shell command or an alternate wrapper):

```powershell
RESOLVE_AND_RUN(["self-test-confinement","--gate-q-authorization","L:\\dev\\YAKHERD\\docs\\audits\\yakherd\\2026-07-21_yakherd_web_gate_q_runner_activation.json","--python-bytes","<PYTHON_BINARY_BYTES>","--python-sha256","<PYTHON_BINARY_SHA256>","--python-version-base64","<STRICT_BASE64_OF_PYTHON_VERSION>","--node-bytes","<NODE_BINARY_BYTES>","--node-sha256","<NODE_BINARY_SHA256>","--node-version-base64","<STRICT_BASE64_OF_NODE_VERSION>"])
```

The frozen subcommand executes no Implementation-authored module. It resolves
and hashes the Python/Node runtimes and requires the exact six independently
observed values supplied through its frozen validated arguments. Version
arguments are canonical padded RFC 4648 base64 of the observed ASCII version
strings, with no whitespace or alternate alphabet; byte/hash arguments are the
observed decimal/hex values. Any placeholder or mismatch stops. The subcommand creates
suspended fixed-code probe children;
proves assignment to active-process-limit-one/Kill-on-Close Job Objects before
resume; requires one attempted descendant creation to be denied; requires the
exact minimal child environment; captures rather than forwards their fixed
output; creates no file; and emits only the runner's fixed outer token. Any
other probe, inline code, shell wrapper, resolver body, network action, or
mutation is forbidden.

The Markdown audit is finalized first; the JSON then binds its exact identity,
is exclusively created once, and is never predicted by the audit. The exact
Gate X JSON schema and checks are in Section 14. A FAIL grants no
Implementation-authored-code execution, repair, or retry. It authorizes only
one already-reviewed runner `record-review-fail` invocation that validates the
final Gate X FAIL audit identity, appends `RUN_FAILED` with class
`PRE_EXECUTION_REVIEW_FAILED` and the complete embedded inventory, and stops.
That invocation also uses `RESOLVE_AND_RUN`; FAIL never authorizes a symbolic
Python or alternate-launch path.
Its exact CLI takes only the fixed audit path plus the reported nonnegative
byte length and lowercase SHA-256; it reads back and matches all three before
append and never parses or retains audit prose in the journal.
Any source change after the observation invalidates the record.

### Gate I-E - supervised local execution and evidence

The same sole Implementation writer may resume only after the frozen runner
validates the exact Gate X PASS JSON and rehashes the unchanged pre-execution
tree. The runner appends `EXECUTION_AUTHORIZED`, then is the sole command
supervisor, journal writer, run-record builder, candidate-evidence builder, and
terminal-event builder. Only evidence files 63-68 and journal appends may
change after Gate X. Any product, test, fixture, golden, runner, installed-
governance, plan, or review byte change invalidates Gate X and stops.

Gate I-E terminal `RUN_COMPLETED` means only that this authorized local source,
execution, and evidence slice finished consistently; it is not installed-
project completion or product completion. The Implementation task ends with
`autonomous next action: Gate S final independent review`.

### Later gates - not authorized here

- Gate S: one final independent Sol Ultra offline security/parser/evidence
  review of the unchanged Gate X-approved implementation bytes, supervised
  results, and deterministic archive. It has no browser, server, request-
  interception, or network authority.
- Gate T: separately reviewed same-writer owner/`STATUS.md` promotion of the
  exact Gate S-approved candidate; no product-source change is allowed.
- Gate C: separately authorized browser/OS acceptance. Gate C exclusively owns
  local HTTP serving and runtime request interception, along with the named
  Chromium/Firefox/WebKit, two-OS, extraction, fresh-install bridge, storage,
  clipboard, download, and qualified accessibility evidence.
- Gate G: owner checkpoint for Git initialization, GitHub owner/name/visibility,
  commit, remote, and push.
- Gate H: read-only static-host capability and privacy inventory followed by an
  owner hosting decision and exact response/header/cache/error-file plan.
- Gate D: transactional staging deployment, remote manifest comparison,
  rollback proof, live security/accessibility checks, and Red Team PASS.
- Gate O: explicit production and DNS authority, identical-byte deployment,
  rollback target, final PASS, and publication.

None of these later gates is implied by a Gate I-W or Gate I-E PASS.

## 5. Exact Gate Q and Gate I write set

All paths below are relative to `L:\dev\yakherd-web`. At Gate I-W entry,
`scripts/concierge_gate_i_runner.py` is the sole listed file already present;
it must equal the exact Gate Q-reviewed identity and remain immutable. Every
other listed file and every new directory must be absent. The writer uses fail-
if-exists creation after rechecking containment and reparse-point absence. A
collision, unknown child, symlink, junction, reparse point, case-fold
collision, or failed create stops the gate without deleting or changing the
pre-existing path.

The only new directories, in creation and evidence order, are:

1. `site`
2. `site/assets`
3. `site/data`
4. `site/fallback`
5. `tests/fixtures`
6. `tests/golden`

Each is created one level at a time; recursive parent creation is forbidden.
The already-installed, receipt-bound `docs/run_records` directory is the
parent of the journal, so the journal can be the first Gate I-W mutation after
Gate Q. The reviewed runner creates the journal with `RUN_STARTED`; every
remaining new-directory and file creation is bracketed by the Section 15
events. The resulting records are
contemporaneous internal assertions plus independently checkable before/after
consistency; they do not claim to prove historical operating-system open flags
against a malicious writer.

The Yakherd install already owns `.gitignore`, `README.md`, `AGENTS.md`, the
root authority files, `scripts/ssot/*`, and `tests/ssot/*`. Gate Q/I-W must
verify unchanged pre-Gate-P paths against both reviewed manifests and Gate P
deltas against the reviewed after-manifest. They must not edit any installed
path. The runner at item 33 is created only by Gate Q; all other listed product
and project files are created only by Gate I-W:

1. `.gitattributes`
2. `LICENSE`
3. `NOTICE.md`
4. `site/index.html`
5. `site/concierge.html`
6. `site/next-steps.html`
7. `site/privacy.html`
8. `site/troubleshooting.html`
9. `site/404.html`
10. `site/assets/styles.css`
11. `site/assets/app.mjs`
12. `site/assets/concierge.mjs`
13. `site/assets/state.mjs`
14. `site/assets/bytes.mjs`
15. `site/assets/canonical-json.mjs`
16. `site/assets/crc32.mjs`
17. `site/assets/zip-store.mjs`
18. `site/assets/storage.mjs`
19. `site/assets/scanner.mjs`
20. `site/assets/content.v1.mjs`
21. `site/assets/yakherd2.png`
22. `site/data/interview.v1.json`
23. `site/data/prompt_template.v1.txt`
24. `site/data/secret_patterns.v1.json`
25. `site/data/high_stakes_terms.v1.json`
26. `site/data/yakherd_release.v1.json`
27. `site/fallback/master_prompt_template.txt`
28. `docs/CONCIERGE.md`
29. `docs/PRIVACY_BOUNDARY.md`
30. `docs/STATIC_SOURCE_POLICY.md`
31. `docs/BUNDLE_FORMAT.md`
32. `docs/CONTENT_PROVENANCE.md`
33. `scripts/concierge_gate_i_runner.py`
34. `tests/concierge_test_static_policy.py`
35. `tests/concierge_test_content_binding.py`
36. `tests/concierge_test_pages.py`
37. `tests/test_bytes.mjs`
38. `tests/test_state.mjs`
39. `tests/test_canonical_json.mjs`
40. `tests/test_crc32.mjs`
41. `tests/test_zip_store.mjs`
42. `tests/test_scanner.mjs`
43. `tests/test_storage.mjs`
44. `tests/test_interview.mjs`
45. `tests/fixtures/bundle_input.v1.json`
46. `tests/fixtures/prompt_ascii_lf.txt`
47. `tests/fixtures/prompt_unicode_lf.txt`
48. `tests/fixtures/prompt_empty.txt`
49. `tests/fixtures/prompt_rejected_lone_surrogate.json`
50. `tests/fixtures/prompt_rejected_delimiter.txt`
51. `tests/fixtures/secret_clean.txt`
52. `tests/fixtures/secret_positive.txt`
53. `tests/fixtures/high_stakes_clean.txt`
54. `tests/fixtures/high_stakes_positive.txt`
55. `tests/golden/MASTER_PROMPT.txt`
56. `tests/golden/MASTER_PROMPT_HANDOFF.txt`
57. `tests/golden/APPROVAL.json`
58. `tests/golden/BUNDLE_MANIFEST.json`
59. `tests/golden/OPEN_IN_CODEX.txt`
60. `tests/golden/yakherd_intake_6e7dd93a7067.zip`
61. `tests/golden/golden_identity.v1.json`
62. `docs/run_records/concierge_v1_local_journal.jsonl`
63. `docs/run_records/concierge_v1_pre_evidence.json`
64. `docs/run_records/concierge_v1_python_tests.json`
65. `docs/run_records/concierge_v1_node_tests.json`
66. `docs/run_records/concierge_v1_protocol_evidence.json`
67. `docs/run_records/concierge_v1_local_candidate.json`
68. `docs/run_records/concierge_v1_final_precommit.json`

No wildcard or other directory is authorized. In particular, no `_headers`, `_redirects`,
hosting configuration, workflow, dependency lockfile, package manifest,
source map, hidden IDE file, screenshot, coverage file, cache, temporary file,
generated test output, archive other than the named golden archive, or public
deployment file may be created in Gate Q or Gate I.

`.gitattributes` has exactly these UTF-8 LF bytes and one terminal LF:

```text
* text=auto eol=lf
*.png binary
*.zip binary
```

`site/assets/yakherd2.png` is an exact byte copy of
`L:\dev\YAKHERD\yakherd2.png`: 3,028,501 bytes, SHA-256
`e45c1c5449fff67c0ea4f2b4ed3af9e4886793939f89a449c9e996e1367a4383`.
The source identity must be checked before reading it into the copy operation;
the destination must be absent and exclusively created; the destination is
then read back and checked. `yakherd.mp4` is never read, copied, hashed, or
touched. The site license is Apache-2.0. `LICENSE` is an exact copy of the
engine Apache-2.0 license: 11,358 bytes, SHA-256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
`NOTICE.md` and `docs/CONTENT_PROVENANCE.md` record
Jeffrey Martin as the supplied image's author/rights owner for this repository
and identify both source and destination hashes. If that assertion cannot be
confirmed by the owner at Gate P, the image is omitted through a new reviewed
plan; it is not substituted.

The exact `NOTICE.md` body is:

```text
# Notice

Yakherd Concierge
Copyright 2026 Jeffrey Martin

Licensed under the Apache License, Version 2.0. See LICENSE.

The yakherd2.png artwork was supplied by Jeffrey Martin for Yakherd and is distributed with this repository under the same Apache-2.0 license.
```

It uses LF and one terminal LF. `docs/CONTENT_PROVENANCE.md` repeats that
statement and the literal source/destination paths, byte length, SHA-256, source
Git blob `79fecd4306c7065c72846eaf0507293c191fff19`, source engine commit bound by
Gate R, copy operator/task ID, and copy/read-back result; it contains no other
asset.

## 6. Exact runtime resource and egress policy

The site has no runtime networking JavaScript. `content.v1.mjs` is ASCII LF,
has one terminal LF, and exports one frozen object named `CONTENT_V1` with
exactly these keys in this source order: `highStakesTermsBase64`,
`interviewBase64`, `promptTemplateBase64`, `releaseBase64`, and
`secretPatternsBase64`. Each value is one literal canonical RFC 4648 base64
string: padding is present exactly when RFC 4648 requires it, and no whitespace
or alternate alphabet is allowed. The values bind the exact bytes of the five
`site/data/*` source files. The reviewed runner's `verify` subcommand and
`concierge_test_content_binding.py` decode each export with
strict base64 validation and require byte-for-byte equality with the source
file. Application code imports the module and decodes it in memory. It never
calls `fetch`.

In the defined clean, extension-free page-load trace, before the tester
activates any navigation link, the site-controlled request graph is the initial
navigation and the following same-origin static subresources referenced by
literal relative paths:

- `assets/styles.css`;
- the listed JavaScript modules reachable from `assets/app.mjs` or
  `assets/concierge.mjs` by literal relative import;
- `assets/yakherd2.png` on pages that display it.

Activation of a literal same-origin navigation link or one of the three static
external links is an intentional user navigation outside that load trace; it
may request that fixed destination and never incorporates user text. The
acceptance record must not relabel such a navigation, browser/platform traffic,
or an extension request as a site-code background request.

The interactive run begins only after all modules and embedded content bytes
are synchronously available and validated. From that ready state through ZIP
download, site application code intentionally initiates no request. User-agent,
extension, security-product, captive-portal, DNS, operating-system, and other
platform traffic is outside site control and is not described as absent.
Download uses a same-document
Blob URL created from locally computed bytes, immediately removes the anchor,
and revokes the Blob URL in a queued cleanup after the click. The user is told
that the downloaded file leaves browser-managed page memory and is controlled
by the browser and operating system.

The exact meta CSP on every HTML page is:

```text
default-src 'none'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; img-src 'self' blob:; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

`blob:` is restricted to `img-src` only if a locally generated image preview is
actually required. This plan does not require one, so implementation must omit
`blob:` and use `img-src 'self'`; Blob downloads are navigation/download
objects and do not require `img-src`. The resulting required literal is:

```text
default-src 'none'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; img-src 'self'; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

The later host response adds `frame-ancestors 'none'`; the meta policy must not
claim to enforce it. Later response headers also add `X-Content-Type-Options:
nosniff`, `Referrer-Policy: no-referrer`, and the selected HTTPS policy.

No HTML form element is used. All controls are buttons, inputs, textareas,
selects, fieldsets, and ordinary links. Exact external navigation allowlist:

- `https://github.com/gigajeff/Yakherd`
- the Gate R GitHub `v1.2.0` release URL;
- the Gate R PyPI `1.2.0` URL.

External links are static literals, are never constructed from user data, use
`target="_blank"`, and use `rel="noopener noreferrer external"`. The Concierge
run screen contains no external link between the first answer and the download
result; help opens as same-origin page navigation only after an explicit user
action and warns that navigation may lose memory-only state.

Because informational pages must work without JavaScript,
`site/next-steps.html` contains the literal Gate R tag, commit, artifact names,
lengths, hashes, URLs, and commands. The runner's `verify` subcommand extracts those fixed
text/anchor values and requires equality with `yakherd_release.v1.json`; it
also requires the home GitHub anchor to equal the allowlist. No runtime code
sets or changes an external `href`.

All JavaScript source must be UTF-8 LF, ASCII except literal UI content imported
from the bound data module, and must use only literal relative imports. Dynamic
`import()`, import maps, inline scripts, inline event handlers, source maps,
`eval`, `Function`, string timers, HTML parser sinks, prototype mutation, and
computed access to browser-global capabilities are forbidden.

The verifier fails on any source occurrence or encoded equivalent of:

- `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`,
  `RTCPeerConnection`, `WebTransport`, `importScripts`, `Worker`,
  `SharedWorker`, `serviceWorker`, `navigator.share`, `window.open`,
  `location.assign`, `location.replace`, `document.write`, `innerHTML`,
  `outerHTML`, or `insertAdjacentHTML`;
- `http:`, `https:`, protocol-relative URLs, `data:`, or remote schemes outside
  the three exact static anchor literals and the identical Gate R GitHub/PyPI
  values in `yakherd_release.v1.json`; the verifier strictly decodes every
  `content.v1.mjs` base64 export and applies the same rule to those bound bytes;
- HTML `form`, `iframe`, `object`, `embed`, `audio`, `video`, `source`, `track`,
  `portal`, `base`, `meta http-equiv="refresh"`, preload, prefetch, prerender,
  modulepreload, or service-worker registration;
- CSS backslash, `url(`, `image-set`, `src:`, `expression`, or `behavior`.
  The only permitted at-rules are the literal media queries
  `@media (prefers-reduced-motion: reduce)` and
  `@media (forced-colors: active)`; `@import`, `@font-face`, `@supports`,
  `@keyframes`, and every other at-rule fail.

The verifier is a conservative source tripwire, not proof of arbitrary
JavaScript or browser behavior. Gate S is an offline, read-only, exact-byte
source/security/parser/evidence review. Gate S does not launch a browser,
start an HTTP server, create a browser profile, intercept traffic, inspect a
network log, or receive browser, loopback-network, OS-matrix, or accessibility
authority.

Gate C, and only Gate C, owns runtime browser request interception. Gate C
remains parked until separately authorized after Gate S and Gate T. Its future
reviewed execution plan must bind the exact browser names and versions,
temporary clean profile locations and lifecycle, extension-disabled state,
cache/storage initial state, local-server argv and document URL, permitted
loopback boundary, interception mechanism, evidence paths, initiator
classification, cleanup, and failure behavior before any browser or server is
started. The public copy says the design and CSP prevent the site code from
intentionally transmitting entered text; it does not claim that a test or
browser can mathematically prove all platform behavior.

Safe user-text sinks are exactly textarea/input `.value` and ordinary node
`.textContent`. User text never enters HTML, an attribute, a URL, CSS, a log,
an exception message, a filename, a test artifact, or evidence. Console calls
are forbidden in production source. Error UI uses fixed error codes and fixed
copy only.

The one runtime attribute exception is the ephemeral download anchor: `href`
receives an opaque browser-created Blob URL and `download` receives the fixed
prefix plus prompt-hash prefix from Section 11. Neither attribute contains
prompt text. The Blob itself intentionally contains the locally computed ZIP,
as disclosed to the user.

## 7. Exact interview and prompt assembly

`interview.v1.json` is canonical UTF-8 JSON with LF and one terminal LF. It has
schema `yakherd-interview-v1`, question count 11, and this fixed order:

1. `product_summary`: "What are you hoping to make?"
2. `audience`: "Who is it for?"
3. `core_actions`: "What are the three to seven most important things a user should be able to do?"
4. `data_stored`: "What information will it store, read, or change?"
5. `platforms`: "Where should it run?"
6. `hard_constraints`: "What rules, tools, budget, deadline, or technical limits are non-negotiable?"
7. `non_goals`: "What should this first version deliberately not do?"
8. `success_criteria`: "How will you know the first version works?"
9. `assumptions`: "What assumptions are you making? Leave blank if none."
10. `risks_open_questions`: "What worries you, and what is still undecided?"
11. `high_stakes`: "Could failure affect health, legal rights, money, physical safety, or essential services?"

The top-level object has exactly `questions`, `schema_version`, and `tree_id`;
their values are the question array, integer `1`, and string
`yakherd-interview-v1`. Each of questions 1-10 has exactly `answer_kind` =
`multiline`, `id`, `label`, `max_utf8_bytes` = `8000`, and `unknown_value` =
`UNKNOWN`. Question 11 has exactly `answer_kind` = `choice`, `choices` =
`["YES","NO","UNKNOWN"]`, `id`, and `label`. Object keys follow the Section
10 canonical ordering. No help URL, branch, default answer, HTML, or additional
field is permitted.

Questions 1-10 are multiline text. Question 11 is a required choice among
`YES`, `NO`, and `UNKNOWN`; it may be skipped only by selecting `UNKNOWN`.
Internally, question 11 stores `YES` or `NO` as state `ANSWERED` with the same
value; `UNKNOWN`, skip, and `Make my prompt now` store state `UNKNOWN` with an
empty value. Prompt assembly renders that state as literal `UNKNOWN`.
Every text question has `Skip / I don't know`, stored as the literal state
`UNKNOWN`. Every one of the 11 question screens, including question 11, has a
visible `Make my prompt now` action that records each unanswered item as
`UNKNOWN` before review. Each answer is limited to 8,000 UTF-8 bytes and the
assembled editor is limited to 65,536 UTF-8 bytes.
Limits are checked after the Section 8 scalar validation and before mutation.

The review page presents ordered KNOWNS, UNKNOWNS, ASSUMPTIONS, and
CONTRADICTIONS. Assumptions contains only the user's answer to question 9.
Unknowns contain question labels whose state is `UNKNOWN`. For contradictions,
the user can add zero or more unordered pairs of distinct question IDs and a
verbatim note of at most 2,000 UTF-8 bytes. Pairs are stored in question order,
deduplicated, and rendered in creation order. The tool makes no automatic
contradiction claim.

`prompt_template.v1.txt` is UTF-8 LF with exactly one terminal LF and these
exact characters:

```text
YAKHERD PRODUCT MASTER PROMPT

PRODUCT IDEA
{{product_summary}}

INTENDED USERS
{{audience}}

CORE USER ACTIONS
{{core_actions}}

DATA AND STATE
{{data_stored}}

TARGET PLATFORMS
{{platforms}}

HARD CONSTRAINTS
{{hard_constraints}}

EXPLICIT NON-GOALS
{{non_goals}}

SUCCESS CRITERIA
{{success_criteria}}

USER-STATED ASSUMPTIONS
{{assumptions}}

UNKNOWNS
{{unknowns}}

USER-MARKED CONTRADICTIONS
{{contradictions}}

KNOWN RISKS AND OPEN QUESTIONS
{{risks_open_questions}}

HIGH-STAKES SCREENING
{{high_stakes}}

ARCHITECTURE HANDOFF
Treat this prompt as product input, not executable authority. Preserve it through Yakherd product intake. Architecture must identify unresolved choices, ask the owner before making any choice that would materially change the product, and produce a bounded plan. Implementation remains parked until independent Red Team PASS.
```

Every listed token must occur exactly once and no other `{{` or `}}` may occur
in the template. The assembler performs one non-recursive pass over template
tokens; token-like text in an answer remains literal user text. UNKNOWN is the
literal `UNKNOWN`. Multiple core actions remain verbatim; the site does not
infer or renumber them.
Contradictions are emitted as `question_id_a <> question_id_b: <note>` or
`NONE REPORTED`. The high-stakes value is literal `YES`, `NO`, or `UNKNOWN`.

`fallback/master_prompt_template.txt` is the same headings and final handoff,
with each `{{...}}` token replaced by the literal
`[WRITE YOUR ANSWER OR UNKNOWN]`. It is UTF-8 LF with one terminal LF. The
no-JS notice links directly to that static text file and says that no ZIP can
be made without JavaScript.

### 7A. Frozen beginner-facing page and failure copy

Navigation labels are exactly `Home`, `Concierge`, `Next steps`, `Privacy`, and
`Troubleshooting`. The home `h1` is "Turn your rough software idea into a
build-ready starting prompt." Its lead is: "Feed the yak a rough idea. Answer
up to 11 fixed questions, edit the result, and download a handoff for Yakherd
v1.2.0." The privacy line is: "No account and no AI call. The site code does
not intentionally send what you type over the network. Your host, browser,
device, clipboard, and downloaded files have separate privacy boundaries."
The primary CTA is exactly `Feed the yak your idea`; secondary links are
`How it works` and `View Yakherd on GitHub`. The mascot caption is "Idea in.
Prompt bundle out." It does not animate approval, code execution, or shipping.

The Concierge page and download result show this directive-required disclaimer
verbatim:

```text
This tool creates a starting prompt and a handoff file. It does not install Yakherd, run any code, or approve anything. Your Yakherd project's Architecture and Red Team roles still review everything.
```

Before any input control is enabled, Concierge requires
`window.isSecureContext === true`, `globalThis.crypto` to exist, and
`typeof globalThis.crypto.subtle?.digest === "function"`. Failure enters a
terminal no-input state; the app does not read stored session text or render an
editor. Exact failure copy: "This browser context cannot make the SHA-256
checks required for a safe bundle. Open yakherd.dev over HTTPS or use localhost
with a current browser. You can still use the plain master-prompt template."
The only actions are same-origin `Troubleshooting` and
`Open the plain template`. `file:` is unsupported even if a particular browser
exposes WebCrypto there. Any digest rejection later revokes approval and stops
copy/download with fixed error code `HASH_UNAVAILABLE`; no fallback hash is
implemented.

The Next steps page begins: "Your ZIP is a handoff, not an installer. Keep it
private if your idea is private." It shows the complete Gate R artifact names,
lengths, hashes, GitHub release URL, and PyPI version URL, then these literal
command templates:

```text
Windows PowerShell
py --version
git --version
py -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
Get-FileHash -Algorithm SHA256 ".\<WHEEL_FILENAME>"
py -m pip install --no-index --no-deps ".\<WHEEL_FILENAME>"
yakherd init --target "C:\dev\my-project" --project-name "my-project" --dry-run
yakherd init --target "C:\dev\my-project" --project-name "my-project"

macOS shell
python3 --version
git --version
python3 -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
shasum -a 256 "./<WHEEL_FILENAME>"
python3 -m pip install --no-index --no-deps "./<WHEEL_FILENAME>"
yakherd init --target "$HOME/dev/my-project" --project-name "my-project" --dry-run
yakherd init --target "$HOME/dev/my-project" --project-name "my-project"

Linux shell
python3 --version
git --version
python3 -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
sha256sum "./<WHEEL_FILENAME>"
python3 -m pip install --no-index --no-deps "./<WHEEL_FILENAME>"
yakherd init --target "$HOME/dev/my-project" --project-name "my-project" --dry-run
yakherd init --target "$HOME/dev/my-project" --project-name "my-project"
```

At Gate R, `<WHEEL_FILENAME>` is replaced by the one literal reviewed wheel
filename; no angle-bracket placeholder ships. Adjacent copy says: "Compare the
printed SHA-256 with the wheel SHA-256 shown above. Stop if any character
differs. Then replace the example project path and name with your own.
Use a folder that does not exist or is empty. Read the dry-run result before
running the final command. Do not point fresh install at an existing project."
It then gives the exact seven numbered `OPEN_IN_CODEX.txt` steps from Section
9. It never says the site ran a command or created a repository.

The Privacy page uses the exact six boundary bullets in Section 13 and this
heading: "The site code does not intentionally send your idea. Copy, save,
download, browser, and device behavior have separate boundaries." It avoids
the absolute words "anonymous", "never retained", and
"nothing leaves the browser". The optional-save panel uses the exact storage
success/failure language in Section 13.

The Troubleshooting page contains these fixed problem headings and actions:

- `JavaScript is off`: use the plain template; ZIP creation is unavailable.
- `Secure hashing is unavailable`: use HTTPS or localhost in a current browser;
  do not proceed from `file:` or an insecure remote origin.
- `The download was blocked`: keep the approved page open, allow this one
  download in browser controls, and retry; the site cannot inspect the browser's
  download folder.
- `Copy did not work`: select the visible text and use the operating system's
  copy command; clipboard history or sync is outside the site's control.
- `Saved data could not be verified or deleted`: manage storage for this site
  in browser settings; the page cannot claim the data is gone.
- `Yakherd did not create all five roles`: return to the installed
  `START_HERE.md`, report the missing role, and do not pretend startup passed.
- `The pinned release is unavailable`: stop; do not install another release or
  use a branch in its place.

The 404 page says: "That page is not in this static release." and provides only
same-origin Home and Concierge links. The post-intake plan must include an
exact copy inventory for every other label, error, help paragraph, button,
link, command, `aria-label`, and live-region announcement before Gate I. No
user-facing prose is left to Implementation discretion.

## 8. Editor, Unicode, approval, and copy contract

The browser textarea value is the approval domain. Browsers expose a Unicode
string, not user-authored bytes. The UI states that textarea line breaks are LF
before approval. The site rejects any carriage return code point and any
unpaired UTF-16 surrogate. It performs no Unicode normalization. It encodes the
accepted scalar string with `TextEncoder` UTF-8, without BOM. Those exact bytes
are the approved prompt bytes. Empty prompt and prompt over 65,536 UTF-8 bytes
are rejected.

The site also rejects a prompt containing either exact delimiter as a complete
LF-delimited line:

- `MASTER PROMPT START`
- `MASTER PROMPT END`

This closes the v1.2.0 intake collision. Substrings that are not complete lines
are allowed.

Approval is one reducer transition. It requires the native checkbox to be
currently checked and the exact fixed statement visible:

```text
I wrote or reviewed this prompt and I approve this exact text.
```

The transition validates the string, captures the string, UTF-8 bytes, byte
length, SHA-256, a complete bundle-input fingerprint, and the checkbox state;
then makes the textarea read-only. The approval record is valid only while all
captured values still compare equal. The Download button re-encodes and
re-hashes immediately before bundle construction and fails closed on mismatch.

Approval first performs the Section 12 secret scan. A clean result continues.
A positive result enters `AWAITING_SECRET_ACK`, remains unapproved, leaves the
editor unlocked, shows the exact spans, and offers Edit (default) or the fixed
acknowledgment. Checking that acknowledgment records it only for the current
prompt SHA-256; the user must press Approve again. Approval then reads the
injected/current clock exactly once, after text, secret, and high-stakes
validation and before committing the transition. It converts that
value to the Section 10 `generated_at`; an invalid clock or conversion failure
leaves the state unapproved. Time passing after approval does not alter the
captured timestamp. The snapshot retains the exact editor JavaScript string,
an immutable copy of its UTF-8 bytes, and this canonical fingerprint object:

```text
approval_statement
checkbox_checked
editor_bytes
editor_sha256
generated_at
high_stakes_acknowledged
high_stakes_flagged
initial_draft_sha256
prompt_edited_by_user
release_pin_sha256
secret_acknowledged
secret_flagged
secret_scan_sha256
tool_version
yakherd_target_release
```

`checkbox_checked` is literal true. `editor_bytes` is the integer UTF-8 byte
count from 1 through 65,536. `initial_draft_sha256` is SHA-256 over the initial
draft encoded under the same Section 8 scalar/no-normalization/UTF-8 rules.
`secret_flagged` is the scan boolean;
`secret_acknowledged` is true exactly when flagged and the fixed acknowledgment
was checked for the same prompt hash, otherwise false. `secret_scan_sha256`
binds a Section 10 canonical JSON object with exactly `matches`,
`prompt_sha256`, and `schema_version` = 1. `matches` is an array in merged-range
order; each row has exactly `detector_ids`, `end_utf16`, and `start_utf16`.
Offsets are nonnegative integers, end is greater than start, and detector IDs
are unique in the Section 12 detector order. A clean result has `matches: []`.
Matched text and display labels are not retained in this object. The canonical
bytes have one terminal LF. All hashes are 64 lowercase hex.
`release_pin_sha256` binds the exact canonical
`yakherd_release.v1.json` bytes. At download, the reducer reconstructs this
object from current state while retaining only the captured `generated_at`,
serializes it under Section 10, reruns both scans, and requires exact byte
equality with the captured fingerprint plus exact editor-string/UTF-8-byte
equality. There is no object-identity shortcut.

Every transition that can alter editor text, answers, contradictions,
high-stakes state, acknowledgment, release pin, restored
state, or tool version revokes approval first, clears the checkbox, clears the
snapshot, and disables download. The only route back to editing is an explicit
`Edit prompt` action that revokes approval before removing read-only state.
Checkbox deselection also revokes approval. Program code cannot assign the
editor value outside the reducer/render module. Tests invoke the shipped event
handlers and reducer, not replicas.

Once approval commits, the approval, secret, and high-stakes checkboxes are
disabled. `Edit prompt` is the only route that re-enables them, and it revokes
the snapshot before doing so.

Copy actions are native user actions with this exact disclosure adjacent:
"Copying places this text on your device clipboard. Yakherd Concierge cannot
erase clipboard history or synced clipboard copies." A failed Clipboard API
write is reported without claiming success; the visible textarea remains
selectable for manual copy. Copy never creates approval. Download requires a
valid approval snapshot.

## 9. Exact v1.2.0 handoff and bundle file bytes

`site/data/yakherd_release.v1.json` is incomplete and Gate I must not begin
until Gate R has supplied every exact public value listed in Section 4. It is a
canonical object with keys:

```text
engine_commit
github_release_url
manifest_bytes
manifest_sha256
package_readme_bytes
package_readme_sha256
product_intake_bytes
product_intake_sha256
pypi_version_url
release_json_bytes
release_json_sha256
root_readme_bytes
root_readme_sha256
sdist_bytes
sdist_filename
sdist_sha256
sdist_url
start_here_bytes
start_here_sha256
tag
version
wheel_bytes
wheel_filename
wheel_sha256
wheel_url
```

The fixed `tag` is `v1.2.0` and fixed `version` is `1.2.0`. No blank,
placeholder, `latest`, redirect-only, branch, abbreviated hash, or unverified
value is permitted. The data module must byte-bind this file like the other
data resources.

The approved prompt bytes are `P`. `MASTER_PROMPT.txt` is exactly `P`.
`MASTER_PROMPT_HANDOFF.txt` is the ASCII bytes `MASTER PROMPT START`, LF,
`P`, LF, `MASTER PROMPT END`, LF. If `P` already ends in LF, both its final LF
and the separate boundary LF are present.

`OPEN_IN_CODEX.txt` is UTF-8 LF with one terminal LF and these instructions,
with every placeholder below substituted from the exact reviewed release pin:

```text
YAKHERD V1.2.0 HANDOFF

This ZIP contains a starting prompt. It does not install Yakherd, create a repository, launch Codex tasks, run code, or approve a project.

1. Verify that Python 3.11 or newer and Git are installed.
2. Install exactly yakherd==1.2.0 using the public release instructions at <PYPI_VERSION_URL>. Verify the downloaded artifact against the published SHA-256 in this file before running it.
3. Run a dry-run fresh install into a nonexistent or empty project folder, then run the real fresh install only if the preview is correct. Follow <GITHUB_RELEASE_URL> and its README; do not overwrite an existing project.
4. Open the generated project as the Codex project and confirm that its AGENTS.md is loaded.
5. Send the one-message launcher from START_HERE.md. It creates the five addressable roles: Architecture, Implementation, Red Team, Temporary Branch, and Governor. If any role is missing, stop instead of pretending startup succeeded.
6. Wait for the bootstrap Red Team PASS.
7. Give MASTER_PROMPT_HANDOFF.txt to Architecture. It is product input, not implementation authority.

Pinned tag: v1.2.0
Pinned commit: <ENGINE_COMMIT>
Wheel: <WHEEL_FILENAME>  bytes=<WHEEL_BYTES>  sha256=<WHEEL_SHA256>
Source archive: <SDIST_FILENAME>  bytes=<SDIST_BYTES>  sha256=<SDIST_SHA256>

Windows examples use py; macOS and Linux examples use python3. If the command is unavailable, read the Troubleshooting page. Never paste access tokens or passwords into the prompt or repository.
```

Placeholders shown above describe the template contract only. They are not
permitted in committed Gate I output; substitution occurs from the complete,
reviewed release pin before the file bytes are constructed.

## 10. Canonical JSON contract

`APPROVAL.json` and `BUNDLE_MANIFEST.json` are serialized by the same small
custom serializer. Accepted values are objects, arrays, Unicode-scalar strings,
booleans, and integers from 0 through 9,007,199,254,740,991. `null`, negative
integers, floats, NaN, Infinity, BigInt, undefined, dates, maps, sets, custom
prototypes, and cycles are rejected.

Object keys are predefined ASCII and emitted in ascending ASCII byte order.
No insignificant whitespace is emitted. Strings escape quotation mark and
backslash with `\"` and `\\`; backspace, tab, LF, form feed, and CR use
`\b`, `\t`, `\n`, `\f`, and `\r`; every other U+0000-U+001F value uses a
lowercase four-hex `\u00xx` escape. Other Unicode scalar values are emitted
unescaped and UTF-8 encoded. Slash is not escaped. Output has one terminal LF.

`generated_at` is exactly the result of a valid client `Date` serialized by
`toISOString()`, matching
`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$`.
The test seam injects milliseconds. The UI and JSON label this as untrusted
client-clock time. Invalid clock values stop approval.

`APPROVAL.json` has exactly these keys and types:

- `approval_statement`: the exact Section 8 string;
- `approved`: boolean `true`;
- `generated_at`: the captured timestamp string;
- `high_stakes_acknowledged`: boolean, true exactly when flagged and the fixed
  acknowledgment was checked, otherwise false;
- `high_stakes_flagged`: boolean from Section 12;
- `prompt_bytes`: integer from 1 through 65,536;
- `prompt_edited_by_user`: boolean, true only if the approved editor string
  differs from the initial mechanically assembled draft by exact JavaScript
  string comparison;
- `prompt_sha256`: 64 lowercase hex characters over `MASTER_PROMPT.txt`;
- `schema_version`: integer `1`;
- `timestamp_source`: string `client`;
- `tool`: string `yakherd-concierge`;
- `tool_version`: string `1.0.0`;
- `yakherd_target_release`: string `v1.2.0`.

No other field is permitted. The serializer sorts them; the order above is
descriptive, not a second serialization order.

`BUNDLE_MANIFEST.json` has exactly `bundle_schema_version`, `files`, and
`yakherd_target_release`. Schema version is `1`. `files` lists the other four
files, not the manifest itself, in this fixed order:

1. `MASTER_PROMPT.txt`
2. `MASTER_PROMPT_HANDOFF.txt`
3. `APPROVAL.json`
4. `OPEN_IN_CODEX.txt`

`bundle_schema_version` is integer 1 and `yakherd_target_release` is string
`v1.2.0`. Each entry has exactly `bytes` (integer 0 through 262,144), `path`
(one of the four literal ASCII names), and `sha256` (64 lowercase hex). The
manifest serializer still sorts each object's keys; array order remains fixed.

## 11. Exact ZIP32 Store-only contract

The archive contains exactly the five directive filenames in fixed order, with
`BUNDLE_MANIFEST.json` fourth and `OPEN_IN_CODEX.txt` fifth. Names are literal
ASCII but the UTF-8 flag is set. Each entry is Store-only and its bytes are the
bytes defined above.

All integers are little-endian. Local header values:

- signature `0x04034b50`;
- version needed `20`;
- general-purpose flags `0x0800` only;
- compression method `0`;
- DOS time `0x0000` and DOS date `0x0021` (1980-01-01 00:00:00);
- IEEE CRC-32, compressed size, and uncompressed size in the header;
- filename byte length and filename bytes;
- extra-field length `0`; no data descriptor.

Central header values:

- signature `0x02014b50`;
- version made by `0x0314` (Unix, ZIP 2.0);
- version needed, flags, method, time, date, CRC, sizes, name length, and name
  bytes identical to the local values;
- extra length `0`, comment length `0`, disk start `0`, internal attributes
  `0`, external attributes `0x81a40000` (regular file mode 0644), and the exact
  local-header offset.

EOCD values:

- signature `0x06054b50`;
- disk number and central-directory disk `0`;
- entry counts `5` and `5`;
- exact central-directory size and offset;
- comment length `0` and no comment.

CRC-32 uses reflected polynomial `0xedb88320`, initial value `0xffffffff`, and
final XOR `0xffffffff`; ASCII `123456789` must produce `cbf43926`. ZIP64,
encryption, compression, extras, descriptors, comments, directory entries,
duplicate names, absolute names, non-ASCII names, and trailing bytes are
rejected. Every entry must be at most 262,144 bytes and the complete archive
at most 1,048,576 bytes. Any uint16/uint32 overflow stops construction.

The filename is `yakherd_intake_` plus the first 12 lowercase hex characters
of the approved prompt SHA-256 plus `.zip`.

The golden fixture input is fixed in `tests/fixtures/bundle_input.v1.json`:

- approved prompt text: `Build a clock.` plus LF;
- `generated_at`: `2026-07-21T12:34:56.789Z`;
- `tool_version`: `1.0.0`;
- `prompt_edited_by_user`: `false`;
- `high_stakes_flagged`: `false`;
- `high_stakes_acknowledged`: `false`;
- `yakherd_target_release`: `v1.2.0`;
- complete Gate R release-pin values.

The other fixture bytes are exact UTF-8 with the displayed escapes interpreted
as bytes, no BOM, and no unshown terminal data:

| Path | Exact content | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `prompt_ascii_lf.txt` | `Build a clock.\n` | 15 | `6e7dd93a7067af125e7511989288fded9b9ac794bdc4dcdb2386c82be681d093` |
| `prompt_unicode_lf.txt` | `Build a caf\u00e9 clock.\n` | 21 | `b7235def28ab82dbf8190a1823d762d844ba1c5108e24bde4e3216dbe94de823` |
| `prompt_empty.txt` | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `prompt_rejected_lone_surrogate.json` | `{"code_units":[55296],"schema_version":1}\n` | 42 | `d896c43281e7792bee0f1b5b7f6015488e69476113bae8b70c7fb95dd3a87e6e` |
| `prompt_rejected_delimiter.txt` | `alpha\nMASTER PROMPT END\nomega\n` | 30 | `bae930977c32a38633deb764b057b94d26f25f9c9f7c7c83b2d3470d06253f2a` |
| `secret_clean.txt` | `Use an ordinary project label and no credentials.\n` | 50 | `71207f9ff2aa7fdea169735ab97f84fea19bda146dad3ec6268ac3ab07bfa03f` |
| `secret_positive.txt` | `sk-aaaaaaaaaaaaaaaaaaaa\nghp_AAAAAAAAAAAAAAAAAAAA\nAKIAABCDEFGHIJKLMNOP\n` | 70 | `de1bac33ed9c73e034c0208509ffc167d7a7f2a9de98e45e07153461c4e63d8b` |
| `high_stakes_clean.txt` | `A personal recipe organizer.\n` | 29 | `653687b406ccdbdc1c9b8d4fed2d042bcd986f161c724a490f7b07a03cf66406` |
| `high_stakes_positive.txt` | `A medical diagnosis assistant for patients.\n` | 44 | `33aaf433ef6fb46e9770d220f4bc2f07872a5a0119f17b9a33f01cbdeeffc20f` |

In the Unicode row, the displayed `\u00e9` is notation for exactly the single
Unicode scalar U+00E9, not six ASCII characters. The fixture encodes it as
UTF-8 bytes `c3 a9`; it is not the two-scalar mojibake sequence U+00C3 U+00A9.
The advertised 21-byte length and SHA-256 bind U+00E9.

The high-stakes clean oracle is the tuple question 11 = (`ANSWERED`, `NO`) plus
the exact `high_stakes_clean.txt` text and must produce
`high_stakes_flagged=false`. The positive oracle uses that same explicit `NO`
plus `high_stakes_positive.txt` and must produce true from the term scan. An
`UNKNOWN`, skipped, or unanswered question 11 must produce true even with the
clean text. Tests assert all three outcomes, including the directive's required
clean no-false-block case.

Because `bundle_input.v1.json` includes public artifact identities that do not
yet exist, the post-intake plan must print that complete canonical file, byte
length, and SHA-256 before Gate I. A placeholder fixture is forbidden.

Before the product writer starts, Architecture must use a spec-only reference
construction that shares no source with the browser modules to calculate every
expected entry and ZIP byte. The post-intake plan embeds RFC 4648 base64 of the
complete exact bytes of `bundle_input.v1.json`, all five golden entry files,
the golden ZIP, and `golden_identity.v1.json`, plus each decoded byte length and
SHA-256. Red Team independently decodes and reconstructs the values directly
from Sections 9-11, checks the complete ZIP headers/offsets/CRC/manifest, and
must reproduce every identity in the same review that may authorize Gate I.
The reference construction is temporary review work; no generator or package
is placed in the product checkout. The Implementation writer may transcribe
only those reviewed bytes and may not choose or refresh an expected value.

The prompt SHA-256 prefix is fixed as `6e7dd93a7067`; that fixes the golden ZIP
path named in Section 5. `golden_identity.v1.json` is Section 10 canonical JSON
with exactly `bundle_input_bytes`, `bundle_input_sha256`, `entries`,
`schema_version`, `zip_bytes`, `zip_path`, and `zip_sha256`. Schema version is
integer 1. Byte values are nonnegative safe integers. Hashes are 64 lowercase
hex. `zip_path` is the exact Section 5 golden ZIP path. `entries` has five rows
in ZIP order, each with exactly `bytes`, `path`, and `sha256`. It does not hash
itself. The post-intake plan binds the complete identity-file bytes and hash.

The Python standard-library verifier independently parses every frozen header,
rejects any unspecified structure, and recomputes every CRC/SHA and manifest.
The Node browser implementation must reproduce the exact reviewed archive.
Neither implementation may import, invoke, or derive expected values from the
other. Tests fail on any difference and never update golden bytes. Gate S
independently checks the frozen oracle and finalized tree before accepting the
parser boundary.

## 12. Secret and high-stakes gates

`secret_patterns.v1.json` freezes these ASCII detectors and their display
labels:

- `private_key`, label `Private-key header`:
  `-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----`;
- `openai_like`, label `API-key-shaped text`: `sk-[A-Za-z0-9_-]{20,}`;
- `github_token`, label `GitHub-token-shaped text`:
  `gh[pousr]_[A-Za-z0-9]{20,}`;
- `aws_access_key`, label `AWS-access-key-shaped text`:
  `AKIA[0-9A-Z]{16}`;
- `jwt_like`, label `JWT-shaped text`:
  `eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}`;
- `password_adjacent`, label `Password- or secret-labeled value`,
  ASCII-case-insensitive:
  `(api[_ -]?key|token|password|passwd|secret)[ \t]*[:=][ \t]*[^ \t\r\n]{8,}`;
- `entropy_token`, label `High-entropy token-shaped text`:
  `[A-Za-z0-9_-]{32,}` only when the matched ASCII string contains an
  uppercase letter, lowercase letter, and digit, has at least 16 distinct
  characters, and no one character occupies more than 25 percent of the
  match. This is deliberately described as a token-shape heuristic, not an
  entropy measurement guarantee.

The file is canonical JSON with exactly `detectors` and `schema_version` = 1.
The detector array is in the order above. Regex detector objects have exactly
`flags`, `id`, `kind`, `label`, and `pattern`; `kind` is `regex`, and `flags`
is either the empty string or `i` only as stated above. The entropy detector
has exactly `alphabet`, `id`, `kind` = `entropy_ascii`, `label`,
`max_dominant_percent` = 25, `min_bytes` = 32, `min_unique` = 16, and
`required_classes` = `["upper","lower","digit"]`. The percentage check is
the exact integer inequality `dominant_count * 100 <= length * 25`. Runtime
constructs only the named fixed regular expressions and adds the global scan
flag itself.

Matching runs on the exact editor JavaScript string. Because all patterns are
ASCII, match offsets are UTF-16 code-unit half-open ranges that begin and end
on ASCII code units. Sort by start, then longer match, then detector order;
merge overlaps into one flagged range while retaining all labels. The warning
shows the exact range through `.textContent`, never HTML, and offers Edit
(default) or a separate `Download anyway` checkbox with exact text: "I
understand this may include a secret and still want to download it." Any edit
clears this acknowledgment. The check occurs before approval as specified in
Section 8; after checking, the user presses Approve again, and download later
requires the same prompt hash and scan result. Detectors are best-effort and
never described as proof that text is secret-free.

`high_stakes_terms.v1.json` contains exactly these ASCII lowercase terms:

```text
diagnosis
medical
medicine
patient
prescription
legal advice
lawsuit
contract rights
investment
financial advice
trading
credit decision
life safety
emergency
industrial control
essential service
```

The file is canonical JSON with exactly `schema_version` = 1 and `terms` = the
array above in that order. Blank, duplicate, uppercase, or additional terms
fail content validation.

Matching uses ASCII lowercase and substring search on answers and the editor;
it performs no locale or Unicode normalization. `high_stakes_flagged` is true
unless question 11 is explicitly `ANSWERED` with value `NO`, and is also true
whenever a term matches. Thus `YES`, `UNKNOWN`, skipped, and unanswered states
all fail closed into the acknowledgment gate. A short warning is visible for every
user, even when false: "Software can cause harm. If health, legal rights,
money, physical safety, or essential services are involved, use qualified
human experts." When flagged, the site also says: "Yakherd and its agents are
not suitable for regulated or safety-critical products without qualified human
experts. This bundle does not change that." Download is blocked until a
separate checkbox says: "I understand this prompt needs qualified human review
before anyone relies on the resulting software." Editing or changing answers
clears it.

## 13. Honest storage and privacy state machine

Default state is memory-only. Controls use `autocomplete="off"` and
`spellcheck="false"`, but copy states that browsers, extensions, operating
systems, input methods, crash recovery, form restoration, backups, and synced
devices are outside the site's control. The site says: "This page does not
intentionally save your text unless you turn on Save in this browser. Your
browser or device may still restore or retain data. Use Clear this session,
close the tab, and manage downloaded or clipboard copies yourself."

Optional persistence uses `localStorage` only, at the exact origin-scoped key
`yakherd.concierge.v1.session`. IndexedDB, cookies, sessionStorage, Cache API,
URL state, history state, and server state are forbidden. The stored canonical
JSON has exactly these top-level keys and types:

- `answers`: an 11-row array in question order; each row has exactly `id`,
  `state`, and `value`. ID is the fixed question ID, state is `ANSWERED` or
  `UNKNOWN`, and value is a validated scalar string up to 8,000 UTF-8 bytes for
  `ANSWERED` or the empty string for `UNKNOWN`. Zero-length text becomes
  `UNKNOWN`; nonempty whitespace is retained verbatim. For question 11 only,
  an `ANSWERED` value must be exactly `YES` or `NO`; `UNKNOWN` must have an empty
  value. Any other restored combination rejects the entire stored object,
  attempts current-key removal, restores nothing, and flags high stakes until
  the user explicitly answers `NO`.
- `contradictions`: an array of rows with exactly `id_a`, `id_b`, and `note`,
  under the ordering, uniqueness, and 2,000-byte rules in Section 7.
- `current_step`: integer 0-13, where 0-10 are questions, 11 is review, 12 is
  editor, and 13 is approval; the download result is never persisted.
- `editor_text`: validated scalar string, empty before drafting and otherwise
  at most 65,536 UTF-8 bytes.
- `expires_at_ms`: nonnegative safe integer.
- `initial_draft`: validated scalar string, empty before drafting and otherwise
  at most 65,536 UTF-8 bytes.
- `saved_at_ms`: nonnegative safe integer.
- `schema_version`: integer 1.

No additional or missing key, row, ID, or type is accepted. The object uses the
Section 10 canonical serializer and is at most 262,144 UTF-8 bytes. It never
stores a valid approval snapshot or either download-anyway acknowledgment;
restoration always requires fresh approval and acknowledgments.

The same fixed Section 12 secret detectors run before every persistence write
over every answer value, contradiction note, `editor_text`, and
`initial_draft`, with fields scanned separately so boundaries cannot create or
hide a match. A positive result prevents the write, turns Save off, attempts
verified removal of the current key, and says: `Potential secret-shaped text
was not saved by this transition. Continue in memory only. A prior browser copy
may remain unless current-key removal was verified, and other browser or device
copies are outside this page's control.` There is no Save-anyway override.

On initial storage read, schema/size/scalar validation and the same secret scan
occur before any stored user text is rendered or offered for restoration. A
positive result restores nothing, flags high stakes, attempts current-key
removal, and reports only the affected fixed field IDs and UTF-16 ranges, never
the matched text. It says whether current-key absence was observed and repeats
that other platform copies may remain.

Expiry is `saved_at_ms + 604800000`, based on the untrusted client clock.
Expiry is checked on initial read and every state transition. Invalid JSON,
wrong schema, impossible type/range, expired value, or clock rollback before
`saved_at_ms` causes a best-effort `removeItem` and no restoration. Save claims
success only when `setItem`, immediate `getItem`, and exact string comparison
all succeed. Delete claims success only when immediate `getItem` returns
`null`. Quota, security, read, write, or deletion failure uses fixed truthful
copy: data may remain in browser storage; the site cannot verify deletion.
The seven-day value is an application read/use policy, not a browser-retention
upper bound or scheduled deletion. If the page never runs again, the site does
not execute expiry cleanup. Browser restoration, sync, backups, and copies can
retain data longer.

Turning Save on performs one immediate synchronous save. While enabled, every
successful reducer transition that changes a stored field constructs a new
object, captures `saved_at_ms` from `Date.now()`, derives `expires_at_ms` with
checked safe-integer addition, serializes, bounds, writes, reads, and compares
before the UI says: `The current site-storage key was written and read back.
If this page runs after seven days, the site will treat that value as expired
and try to remove it. Your browser, restored sessions, sync, or backups may
retain copies longer.` There is no
timer, debounce, unload handler, or background write. A failed operation turns
autosave off without retry and says: `Save could not be verified. Your current
work is still on this page, and a browser copy may remain.` Turning Save
off or choosing Delete attempts verified removal and says either: `The current
site-storage key is absent on immediate read-back. Browser, restored-session,
synced, or backup copies may remain.` or `The current site-storage key could
not be verified absent; use browser site-data settings. Other browser or device
copies are outside this page's control.`

V1 stores at most one replace-in-place saved session at that sole key. The UI
therefore exposes both directive-required actions: `Delete this saved session`
and `Delete all saved sessions`. In V1 both run the same one-key removal and
immediate-null read-back contract above; neither implies browser-wide deletion.
If future versions add keys or multiple sessions, this equivalence expires and
requires a new reviewed storage schema.

The `storage` event for this exact key from another tab invalidates approval,
stops autosave, and requires an explicit Reload or Keep this tab decision; no
automatic merge occurs. Reload reparses under the same rules. Keep this tab
performs no write until the user explicitly re-enables save.

`Clear this session` revokes approval, clears in-memory state and controls,
attempts and verifies removal of the one key, and reports verified/uncertain
separately. It cannot delete clipboard contents, downloaded files, host logs,
browser history, extensions, backups, or platform restoration state.

The privacy page and adjacent disclosure say, in substance and without broader
claims:

- site application code does not intentionally send typed answers or prompts
  over the network;
- the static host necessarily receives ordinary page/asset requests and may
  retain IP address, user-agent, time, and request metadata under its own
  policy; the site has no client analytics;
- optional save is origin-local browser storage and can fail or be retained by
  the platform;
- copying and downloading are intentional transfers to OS-managed locations;
- handing the file to Codex/Yakherd is a later user action governed by those
  tools, not by this site;
- no account and no site-issued login are used; the word "anonymous" is not
  used as an absolute claim;
- secret and high-stakes checks are local best-effort warnings, not guarantees.

## 14. Gate I verification and acceptance

Permitted prerequisites are an already installed Python 3.11+ and Node 20+
runtime. No package manager or browser is invoked. The Gate P plan freezes the
complete runner implementation/interface and the complete prelaunch resolver;
Gate Q independently activates both exact identities.

`RESOLVE_AND_RUN(ARGUMENTS)` everywhere in this plan means one literal
invocation of the decoded Gate Q-reviewed PowerShell source whose version is
`yakherd-concierge-prelaunch-resolver/1`; it is notation, not permission to
invent a function, wrapper, or command. The post-intake plan prints that source
in full and its deterministic rendering rule. The task tool submits those
exact decoded source bytes directly as its one PowerShell command; it does not
decode or compile a script block at runtime, write a `.ps1`, use a profile, or
append operator code. Its only per-invocation values are (a) the exact Gate Q
authorization byte length and SHA-256 from the reviewer handback, (b) the exact
resolver byte length, SHA-256, and version from that same handback, and (c) one
literal runner argument array printed by the reviewed post-intake plan, with
only the explicitly typed Gate X observation/audit identity substitutions.
Every string is passed as a PowerShell array element, never reparsed as source.

Before launching Python, the resolver performs all of these operations in this
order and short-circuits on the first failure: read the fixed Gate Q
authorization path as bytes; require its handed-back byte length and SHA-256;
strictly decode it as UTF-8 and parse only that already hash-authenticated JSON;
require the complete Gate Q schema, PASS status, checks, runner identity,
resolver identity, and Python-runtime identity; require that the authorization's
resolver identity equals the exact handed-back resolver byte length, SHA-256,
and version; require the supplied argument array to match one exact frozen
runner CLI production in the
post-intake plan; uniquely resolve one `python` application; require a
non-reparse regular executable; compare its byte length and SHA-256 with Gate
Q before executing it; require the already authenticated Gate Q version to
match the frozen Python >=3.11 grammar (the binary identity makes a second
`--version` process redundant); require the fixed runner path to be a contained
non-reparse regular file and compare its byte
length/SHA-256 with Gate Q; immediately repeat both file identity comparisons
to narrow replacement races; and only then invoke that resolved absolute
Python path with literal
`-I`, `-B`, the resolved absolute runner path, and the array elements. It never
uses the symbolic name `python` for that launch.

The resolver buffers rather than forwards runner stdout/stderr, accepts only
the one fixed runner token and corresponding frozen exit-code-table value,
then emits that token and exits with that value. Any resolver, invocation,
PowerShell, native-command, output, or pairing failure emits only
`YAKHERD_PRELAUNCH_FAIL\n` on stderr and one frozen nonzero resolver exit code;
it emits no success line, caught exception, path, source bytes, environment
value, or child output. It creates/changes no file, environment value, or
process other than the one verified Python runner; uses no network, profile,
pipeline-to-executable, command-string construction, `Invoke-Expression`, or
dynamic code; and does not supervise the runner's children. Gate P and Gate Q
review its complete imports/types/cmdlets, UTF-8 and JSON rules, exact failure
precedence, token/exit table, substitution grammar, and absence of additional
capability. Gate X independently rechecks the same source identity and
contract before its first runner invocation. A task tool unable to submit this
exact resolver source and closed array stops before Python execution.

`scripts/concierge_gate_i_runner.py` is the sole
authorized journal writer, command supervisor, run-record builder, candidate-
evidence builder, and terminal-event builder. The exact resolver above is the
sole PowerShell prelaunch exception; it is an identity gate and outer launcher,
not a journal writer, command supervisor, or evidence serializer. No other
shell wrapper, operator-supplied inline Python, PowerShell orchestration,
alternate evidence serializer, or agent reconstruction is equivalent. The
sole Python inline-code exception is the fixed probe-child byte string embedded
in the Gate P-reviewed runner and used only by Gate X
`self-test-confinement`. The runner emits to the outer tool only one of
the fixed ASCII lines `YAKHERD_RUNNER_OK\n`, `YAKHERD_RUNNER_FAIL\n`, or
`YAKHERD_RUNNER_INCOMPLETE\n`; it never forwards child output.

During Gate I-W, the only permitted runner commands are its frozen `begin`,
`prepare-directory`, `confirm-directory`, `prepare-file`, `confirm-file`,
`request-preexecution-review`, `record-review-fail`, and `fail` subcommands. The post-intake plan
prints the exact token array for every invocation after substituting only the
reviewed literal Section 5 path, expected byte length/SHA-256, and one bounded
Implementation task ID. Each array is supplied only to `RESOLVE_AND_RUN`; the
resolver authenticates Gate Q, Python, and the runner before that invocation.
The runner validates the current journal grammar and
all immutable input identities before every transition, including that its
current `sys.executable` byte length/SHA-256 and version equal the Gate Q
`python_runtime` object. It cannot import or
execute an Implementation-authored file in these subcommands.

Gate I-W ends at `PRE_EXECUTION_REVIEW_REQUESTED`. Gate X then writes its audit
and canonical authorization JSON. That JSON has exactly `audit`, `checks`,
`executable_sources`, `executable_sources_sha256`, `gate_p_after_manifest_sha256`,
`gate_q_authorization_sha256`, `pre_execution_tree`, `prelaunch_resolver`,
`pre_execution_tree_sha256`, `project_root`, `runtime`, `schema_version`, and
`status`. Schema is integer 1, status is
`PASS`, and project root is literal `L:\dev\yakherd-web`.

`audit` has exactly `bytes`, `path`, and `sha256` and binds the finalized Gate X
Markdown audit. `runtime` has exactly `node` and `python`; each has exactly
`binary_bytes`, `binary_sha256`, and `version`. Gate X resolves the actual executable without
retaining its machine-specific absolute path, records the complete version
line and binary SHA-256, and requires Python >=3.11 and Node >=20. The runner
re-resolves each as the same sole application command, rehashes both before
child launch, and invokes their resolved
absolute paths without a shell.

`prelaunch_resolver` has exactly `bytes`, `sha256`, and `version`; it reproduces
the Gate Q authorization values and version
`yakherd-concierge-prelaunch-resolver/1`. Gate X independently decodes the
post-intake strict-base64 block, matches those values, reviews its complete
source and closed substitution grammar, and requires the exact resolver for
its own `self-test-confinement` launch. The Gate X `checks` array therefore
includes the literal PASS checks `prelaunch_resolver_identity_matched`,
`prelaunch_resolver_source_reviewed`, and
`prelaunch_resolver_launch_contract_closed` in the exact order stated below.

`executable_sources` is in ASCII path order and covers the runner plus every
Python/Node source reachable from any exact child argv or import/discovery
edge: all Gate I `.py`/`.mjs` and the installed
`scripts/ssot/validate_protocol.py`. The Python discovery pattern is deliberately
`concierge_test_*.py`; it cannot select installed `tests/ssot/test_*.py` and
Gate I-E does not execute those broader installer tests. Each row has
exactly `bytes`, `imports`, `path`, `read_paths`, `sha256`,
`top_level_effects`, and `write_paths`. The four capability fields are ASCII-
sorted arrays of literal strings. The matrix must enumerate every import and
every possible filesystem read/write or top-level effect; `NONE` is represented
by an empty array, not an omitted field.

`executable_sources_sha256` is SHA-256 over the Section 10 canonical
serialization of the complete `executable_sources` array plus LF. Gate X also
reconstructs the journal's pre-review source-identity manifest, which has rows
containing exactly `bytes`, `path`, and `sha256`, and requires its hash to equal
`PRE_EXECUTION_REVIEW_REQUESTED.executable_source_manifest_sha256`.

`checks` contains exactly these rows in this order, each with exactly `name`
and `status = PASS`: `import_graph_closed`, `dynamic_code_absent`,
`network_capability_absent`, `external_filesystem_capability_absent`,
`environment_and_credential_capability_absent`,
`dependency_resolution_closed`, `descendant_creation_absent`,
`module_top_level_side_effects_bounded`,
`prelaunch_resolver_identity_matched`,
`prelaunch_resolver_source_reviewed`,
`prelaunch_resolver_launch_contract_closed`,
`runner_process_confinement_reviewed`, and `child_environment_closed`.
For the `*_absent` checks, absence applies to every Implementation-authored or
installed child source. The governance runner's non-product capabilities are
instead limited to its independently reviewed matrix: target-tree reads;
journal/evidence writes; the exact source asset/license and plan/audit/release
records frozen by Gate P; the exact Gate Q/Gate X records; the resolved runtime
executables; the one `SystemRoot` read; bounded OS hostname/version/UTC-clock
observations used only for the hashed machine and run-record fields; and the Job Object/process/pipe APIs
defined here. No other runner path, environment key, registry, credential,
network, package, process, or dynamic-code capability is permitted.
`pre_execution_tree` is a Section 10 canonical JSON array covering every
descendant directory and regular file at the Gate X observation
boundary, with rows in ASCII path order containing exactly `bytes`, `path`,
`sha256`, and `type`; directory rows use bytes 0/SHA `NOT_APPLICABLE`, regular
files use their exact identities, the root is excluded, and any other type or
reparse point fails. The journal row binds the complete prefix through
`PRE_EXECUTION_REVIEW_REQUESTED`. `pre_execution_tree_sha256` is SHA-256 over
that complete embedded array's canonical bytes plus LF; reserialization must
match. `gate_p_after_manifest_sha256`,
`gate_q_authorization_sha256`, `executable_sources_sha256`, and
`pre_execution_tree_sha256` are lowercase SHA-256 strings over the exact
reviewed values. Gate X independently constructs this record; the runner does
not generate or self-approve it.

Gate X fails unless Python children are isolated with `-I -B`, inherit no
ambient `PYTHONPATH`, user site, credential, proxy, package-manager, or startup
configuration, and import only the reviewed standard-library/local allowlist.
It fails on dynamic import, `eval`, `exec`, `compile`, native extension loading,
network APIs, environment/credential reads, package resolution, or process
creation in Implementation-authored Python. Node sources may use only literal
local `.mjs` imports plus individually listed `node:` built-ins; they may not
use dynamic import, `eval`, `Function`, WebAssembly, native add-ons, package
resolution, `process.env`, credential stores, networking, or process/worker
creation. The only `process` member uses are the harness's literal fixed-token
`process.stdout.write` calls and assignment of integer 0/1 to
`process.exitCode`; all other process access fails Gate X. Any Node filesystem built-in is limited by exact-source semantics to
the literal read-only project paths in its matrix. Tests use in-memory values
and reviewed project fixture reads; they create no OS temporary file.

The seven non-harness Node test files export one side-effect-free `runTests()`
function and do not import `node:test`. `tests/test_interview.mjs` imports those
seven functions in Section 5 order, invokes them sequentially, then runs its
own interview assertions. It catches every failure, writes only fixed ASCII
`NODE_TESTS_FAIL\n`, and exits nonzero; success writes only
`NODE_TESTS_PASS\n`. No assertion body, stack, path, fixture text, or exception
is emitted.

After Gate X PASS, the only outer Gate I-E command, from the target root, is:

```powershell
RESOLVE_AND_RUN(["execute","--journal","docs\\run_records\\concierge_v1_local_journal.jsonl","--gate-q-authorization","L:\\dev\\YAKHERD\\docs\\audits\\yakherd\\2026-07-21_yakherd_web_gate_q_runner_activation.json","--gate-x-authorization","L:\\dev\\YAKHERD\\docs\\audits\\yakherd\\2026-07-21_yakherd_web_gate_x_pre_execution_authorization.json","--candidate","docs\\run_records\\concierge_v1_local_candidate.json"])
```

The outer command tool must permit a 1,650-second timeout and at least 64 raw
output bytes. The runner's complete outer output is one fixed line of at most
28 ASCII bytes, so no truncation, secret classification, or UI-dependent suffix
rule is involved. Outer interruption or timeout grants no PASS and leaves the
last validated journal prefix; it does not authorize a second invocation.

The runner validates both external PASS records and the unchanged pre-execution
tree, appends `EXECUTION_AUTHORIZED`, and supervises these exact child argv
arrays in order:

```text
["python","-I","-B","scripts\\concierge_gate_i_runner.py","verify","--phase","pre-evidence","--journal","docs\\run_records\\concierge_v1_local_journal.jsonl"]
["python","-I","-B","-m","unittest","discover","-s","tests","-p","concierge_test_*.py","-v"]
["node","tests\\test_interview.mjs"]
["python","-I","-B","scripts\\ssot\\validate_protocol.py","--root",".","--strict","--evidence","docs\\run_records\\concierge_v1_pre_evidence.json","--evidence","docs\\run_records\\concierge_v1_python_tests.json","--evidence","docs\\run_records\\concierge_v1_node_tests.json"]
```

After each result is journaled, the runner exclusively creates and reads back
the matching Section 15 run record. The fourth child validates the first three
records. The runner then creates candidate 67, appends `FINAL_VERIFY_STARTED`,
and supervises exactly:

```text
["python","-I","-B","scripts\\concierge_gate_i_runner.py","verify","--phase","final-precommit","--journal","docs\\run_records\\concierge_v1_local_journal.jsonl","--evidence","docs\\run_records\\concierge_v1_local_candidate.json"]
```

It creates record 68 and appends `RUN_COMPLETED` only on PASS. Gate S and later
reviewers may run only this frozen read-only command against the untouched tree:

```powershell
RESOLVE_AND_RUN(["verify-complete","--journal","docs\\run_records\\concierge_v1_local_journal.jsonl","--evidence","docs\\run_records\\concierge_v1_local_candidate.json","--gate-x-authorization","L:\\dev\\YAKHERD\\docs\\audits\\yakherd\\2026-07-21_yakherd_web_gate_x_pre_execution_authorization.json"])
```

That subcommand launches no child and changes no file. No default or ignore-
evidence mode exists. Gate I-E PASS means valid
records, a valid immutable `PRE_FINAL_PASS` candidate, and a journal ending in
`RUN_COMPLETED`; none alone grants installed-project completion.

Before creating the journal, the reviewed runner performs one read-only
preflight. The current target tree must equal the reviewed Gate P after-
manifest plus the separately bound containing plan, combined audit, and exact
Gate Q runner. Separately, the runner validates the two external Gate Q audit/
PASS-JSON identities. For every `UNCHANGED_PRE_GATE_P_BASELINE` row,
the identity equals both its pre-manifest and after-manifest identity. Every
`CHANGED_BY_GATE_P` and `CREATED_BY_GATE_P` row equals its reviewed after-
identity. The runner checks the embedded pre-manifest identity and exact six-
file bootstrap delta from the Gate B installed baseline. `docs/run_records` is
the expected installed non-reparse directory; `.git` is absent; all six new
directories and every listed file except the runner are absent with no case-
fold alias; ancestors are contained/non-reparse; source image/license
identities match; and no other writer targets the root. Failure causes no Gate
I-W mutation. On success, the runner exclusively creates the journal with its
complete canonical `RUN_STARTED` line, flushes, reads back, and begins the
Section 15 state machine.

In `pre-evidence` phase, the runner's `verify` subcommand fails unless:

- the six Section 5 directories, product files 1-61, and journal file 62 are
  present; files 63-68 are absent; and no unexpected path exists beneath
  `site`, `tests/fixtures`, or `tests/golden`;
- the current baseline matches both Gate P manifests and the separately bound
  plan/audit and Gate Q runner/audit/authorization identities; every unchanged
  pre-Gate-P path retains its reviewed identity and each authorized Gate P
  delta has its exact after-identity. The only post-Gate-P child directly under
  `scripts` is `concierge_gate_i_runner.py`, and the only new product test paths
  are the exact Section 5 entries;
- every text file is valid UTF-8, follows its required LF/terminal-LF rule, and
  has no BOM or trailing whitespace; HTML/CSS/JS satisfy the Section 6 policy;
- every internal link and subresource resolves to an allowlisted regular file
  inside `site` with no symlink/reparse escape;
- content-module bytes equal all five source data files;
- release pin is complete, canonical, `v1.2.0`, and matches Gate R evidence;
- image and license identities match Section 5;
- no secret fixture value occurs in product, evidence, error text, or generated
  retained output;
- every executable source identity equals the Gate X manifest; all Gate X
  capability rows are PASS; Implementation-authored Python/Node sources contain
  no process, network, dynamic-code, environment/credential, package-resolution,
  or unlisted filesystem capability. The runner's separately reviewed process
  capability is the sole exception and is not treated as product capability;
- ZIP golden archive satisfies every Section 11 byte rule and its identity
  record;
- total unminified JavaScript is at most 153,600 bytes;
- informational pages contain meaningful main text and navigation without
  JavaScript, and Concierge has the no-JS notice/fallback;
- all pages have one `h1`, named landmarks, labels, logical heading order,
  skip link, language, viewport, meta CSP, no autoplay/motion dependency, and
  no disallowed element/attribute;
- CSS includes visible focus, 320px reflow rules, reduced-motion, forced-colors,
  and declared colors meeting the fixed tested contrast pairs at 4.5:1 or 3:1
  for large text.

Because this verifier is the first supervised child, `pre-evidence` accepts
only the valid source-write prefix ending in `PRE_EXECUTION_REVIEW_REQUESTED`,
the exact `EXECUTION_AUTHORIZED` Gate X binding, and
`COMMAND_STARTED(name="pre_evidence_verifier")`. The subsequent
`COMMAND_FINISHED` is appended only after the confined child exits. No other
pending or terminal event is accepted in this phase.

Both final modes repeat every product check and baseline/Gate X identity check, validate all
applicable installed-protocol run records, validate the canonical pre-final
candidate and referenced identities, and validate the journal/hash chain and
reconstructed inventories. `final-precommit` requires files 1-67, file 68
absent, only files 62-67 as new `docs/run_records` children, and terminal event
`FINAL_VERIFY_STARTED`. `final-complete` requires files 1-68, only files 62-68
as new run-record children, and terminal event `RUN_COMPLETED`. Identical bytes
always produce the same result in each mode;
there is no hidden first-run state. A journal ending `RUN_FAILED`, an event not
accepted by the selected mode, or an incomplete/invalid chain returns nonzero.
There is no mutation, cleanup, evidence exception, or status override.

Unit tests cover empty/ASCII/Unicode/LF values, surrogate and CR rejection,
every approval-invalidating transition, checkbox deselection, direct shipped
handlers, storage corruption/quota/delete/multi-tab events, delimiter
collision, canonical JSON lexical bytes, CRC fixture, ZIP header/limit
failures, deterministic golden equality, clean and positive secret fixtures,
the explicit (`ANSWERED`,`NO`,clean-text) high-stakes false case, positive-term
and UNKNOWN/skip high-stakes true cases, all high-stakes terms, contradiction
ordering, editor size, and content binding. Gate I tests create no OS temporary
file; all mutation-oriented cases operate on in-memory byte arrays or injected
in-memory storage adapters.

No Gate I-E test claims cross-browser, screen-reader, host-header, TLS, real fresh
public install, extraction on other operating systems, or deployed behavior.
Those are later gates.

## 15. Exact Gate I evidence, journal, and failure behavior

Gate I-W/I-E has seven durable evidence files: append-only journal 62, installed-
protocol command records 63-66, immutable pre-final candidate 67, and final-
precommit command record 68. The Gate Q runner exists before them and is not an
evidence file. Read-only preflight occurs before any evidence exists. If
preflight fails, no Gate I-W mutation is allowed. After preflight passes, the
reviewed runner exclusively creates the journal with its complete `RUN_STARTED`
line as initial content in the installed `docs/run_records` parent; that is the
first Gate I-W mutation. Every later directory/file mutation or supervised
command is bracketed by runner-authored journal events. The
candidate 67 can truthfully remain after a later final-verifier failure because
its status is only `PRE_FINAL_PASS`; Gate I-E slice PASS exists only in a valid
terminal `RUN_COMPLETED` journal and is still not installed-project completion.

### 15.1 Canonical append-only journal

`docs/run_records/concierge_v1_local_journal.jsonl` is strict UTF-8, LF-only,
BOM-free JSON Lines. Every complete line is one Section 10 canonical JSON
object plus LF with exactly `detail`, `event`, `previous_line_sha256`,
`schema_version`, and `seq`. Schema version is integer 2. Sequence starts at 0
and increments by one. The first previous hash is 64 zeroes; each later value
is SHA-256 over the exact preceding complete line including LF. Truncation,
rewriting, deletion, reordering, a partial final line, or a chain mismatch is
failure. Each append checks the prior file length/hash, appends only at EOF,
flushes, reads back, and validates the complete chain before the next mutation.

Allowed events and exact `detail` keys are:

1. `RUN_STARTED`: `authorized_paths_sha256`, `implementation_task_id`,
   `gate_p_after_manifest_sha256`, `gate_q_authorization_sha256`,
   `journal_created_exclusively` = true, `plan_sha256`,
   `pre_gate_p_manifest_sha256`, `prelaunch_resolver_sha256`, `project_root`,
   `red_team_audit_sha256`, `sole_writer` = true.
2. `DIRECTORY_CREATE_STARTED`: `path`.
3. `DIRECTORY_CREATED`: `path`, `type` = `DIRECTORY`.
4. `PATH_CREATE_STARTED`: `path`.
5. `PATH_CREATED`: `bytes`, `path`, `sha256`, `type` = `REGULAR_FILE`.
6. `PRE_EXECUTION_REVIEW_REQUESTED`: `executable_source_manifest_sha256`,
   `gate_x_audit_path`, and `gate_x_authorization_path`. It deliberately
   contains no pre-execution-tree hash; Gate X computes that tree only after
   this complete line exists, avoiding self-reference.
7. `EXECUTION_AUTHORIZED`: `authorization_bytes`, `authorization_path`,
   `authorization_sha256`, `executable_sources_sha256`,
   `pre_execution_tree_sha256`; the authorization path is the exact Gate X JSON
   and the source/tree hashes must match.
8. `COMMAND_STARTED`: `argv`, `name`.
9. `COMMAND_FINISHED`: `exit_code`, `failure_reason`, `name`, `stderr_bytes`,
   `stderr_sha256`, `stderr_summary`, `stdout_bytes`, `stdout_sha256`,
   `stdout_summary`, `status`.
10. `RUN_RECORD_CREATE_STARTED`: `command_name`, `path`.
11. `RUN_RECORD_CREATED`: `bytes`, `command_name`, `path`, `sha256`; only after
   exclusive creation and read-back.
12. `CANDIDATE_EVIDENCE_CREATE_STARTED`: `path`; after this line is appended
   and read back, the complete-file prefix hash is calculated and placed only
   in the candidate evidence. This event contains no resulting-prefix hash and
   therefore no self-reference.
13. `CANDIDATE_EVIDENCE_CREATED`: `bytes`, `path`, `sha256`; only after
   exclusive creation and read-back.
14. `FINAL_VERIFY_STARTED`: `argv`, `name` =
    `final_precommit_verifier`.
15. `FINAL_VERIFY_FINISHED`: the same exact keys as `COMMAND_FINISHED`.
16. `RUN_COMPLETED`: `pre_terminal_inventory`,
    `pre_terminal_inventory_sha256`, `status` = `PASS`.
17. `RUN_FAILED`: `failed_check`, `failure_class`,
    `pre_terminal_inventory`, `pre_terminal_inventory_sha256`,
    `retained_or_unresolved_paths`, `status` = `FAIL`.

The only success grammar is: `RUN_STARTED`; the six directory STARTED/CREATED
pairs in Section 5 order; the 60 file STARTED/CREATED pairs for Section 5 files
1-61 except the already activated runner at 33, in Section 5 order;
`PRE_EXECUTION_REVIEW_REQUESTED`; the externally written Gate X audit and PASS
JSON; `EXECUTION_AUTHORIZED`; each of the four Section 14 command
STARTED/FINISHED pairs immediately followed
by its matching run-record STARTED/CREATED pair for files 63-66; candidate-
evidence STARTED/CREATED for file 67; final-verifier STARTED/FINISHED followed
by its run-record STARTED/CREATED for file 68; then `RUN_COMPLETED`. Every
command finish on this success path is `PASS`. A command or mutation cannot
overlap another operation. A `RUN_FAILED` may terminate after any valid
`RUN_STARTED` prefix and must match the pending or just-failed operation. A
crash may leave a valid nonterminal prefix. No event may follow either terminal
event.

The exact command-failure productions are also valid. An ordinary
`COMMAND_FINISHED(status="FAIL")` is followed by its matching run-record
STARTED/CREATED pair and then `RUN_FAILED`; failure class is `COMMAND_FAILED`
for `EXIT_NONZERO`/`FORBIDDEN_CONTENT`, `COMMAND_OUTPUT_LIMIT` for
`OUTPUT_LIMIT`, or `COMMAND_TIMEOUT` for `TIMEOUT`, with `failed_check` equal
to the command name.
`FINAL_VERIFY_FINISHED(status="FAIL")` is followed by record 68's
STARTED/CREATED pair and then `RUN_FAILED`; the corresponding classes are
`FINAL_VERIFY_FAILED`, `FINAL_VERIFY_OUTPUT_LIMIT`, or `FINAL_VERIFY_TIMEOUT`,
and `failed_check` is `final_precommit_verifier`. If either mandatory record cannot
be created or read back, `RUN_FAILED` instead uses the corresponding
run-record failure class and record path when a safe append remains possible.
If executable resolution/identity validation or process creation fails before
a resumable child exists, no run record is fabricated; the gate terminates as
`COMMAND_INVOCATION_FAILED` or `FINAL_VERIFY_INVOCATION_FAILED`. If the child
was created suspended but Job Object creation, limit configuration, assignment,
or resume fails, the runner terminates the still-suspended child and uses
`COMMAND_CONFINEMENT_FAILED` or `FINAL_VERIFY_CONFINEMENT_FAILED`; authored
code never resumes and there is no unconfined fallback. A resumed confined
child that does not yield both pipe EOFs, Job Object active-process count zero,
and a real direct-child integer exit during the ten-second drain uses
`COMMAND_DRAIN_INCOMPLETE` or `FINAL_VERIFY_DRAIN_INCOMPLETE`; this overrides
every latched condition, skips FINISHED, and creates no run record.
`COMMAND_TIMEOUT` and `FINAL_VERIFY_TIMEOUT` are reserved for a timed-out
confined child that does complete all three drain observations and therefore
has a truthful FINISHED event and run record. These are the only productions
after a command STARTED event.

The four command names are exactly `pre_evidence_verifier`, `python_tests`,
`node_tests`, and `protocol_evidence_validation`. Their `argv` values are the
four literal child arrays printed in Section 14, in that order. The final name
is `final_precommit_verifier` and its `argv` is the literal final child array.
The runner resolves `python` to its own `sys.executable` and `node` to the one
Gate X-bound executable, verifies the recorded binary hash/version, and stores
the stable symbolic token in evidence. No executable substitution, added flag,
reordered test, inherited environment prefix, shell wrapper, or omitted token
is equivalent.

`authorized_paths_sha256` is SHA-256 over the Section 10 canonical JSON array
containing the six directory strings followed by all 68 file strings, each in
Section 5 order. Every inventory has 74 rows in that same order. Ordering
called ordinal elsewhere in this section means ascending ASCII bytes; all
authorized paths and event names are ASCII.

`pre_terminal_inventory` is the complete 74-row array embedded directly in
`RUN_COMPLETED` or `RUN_FAILED`, not merely an identity. It is the filesystem
observation made immediately before the terminal append. The journal row in
that array records the byte length and SHA-256 of the complete validated
journal prefix immediately before the terminal line, so it never claims to
inventory or hash the line containing itself. Every other row is the observed
state at that same boundary.

`pre_terminal_inventory_sha256` is SHA-256 over the complete UTF-8 bytes,
including one terminal LF, of the embedded array serialized under Section 10
canonical JSON in Section 5 order. Re-serializing the embedded value must
reproduce the hash byte-for-byte. The embedded array remains the authoritative
historical observation after any separately reviewed recovery; recovery
evidence records a new before/after comparison and never rewrites the journal.

Each inventory row has exactly `bytes`, `path`, `sha256`, and `type`. Type is
`ABSENT`, `DIRECTORY`, `OTHER`, `REGULAR_FILE`, or `UNOBSERVABLE`.
`REGULAR_FILE` uses its nonnegative safe-integer byte length and 64-lowercase-
hex SHA-256. Every other type uses bytes 0 and SHA string `NOT_APPLICABLE`.
`UNOBSERVABLE` conservatively records that the runner could not determine a
truthful type/identity; it is invalid in `RUN_COMPLETED` but permitted in
`RUN_FAILED`. `retained_or_unresolved_paths` is derived, never independently
trusted, and equals in ordinal order every row whose type is `DIRECTORY`,
`REGULAR_FILE`, `OTHER`, or `UNOBSERVABLE`. Thus an abnormal or unreadable path
cannot disappear from failure evidence.

For `RUN_COMPLETED`, final verification requires every non-journal live row to
still equal the embedded inventory and forbids `OTHER`/`UNOBSERVABLE`. For
`RUN_FAILED`, later live bytes need not equal the historical array. If the
terminal append itself is absent or corrupt, the run is `INCOMPLETE` or
`CORRUPT` and no terminal-inventory claim is fabricated.

Command `status` is `PASS` or `FAIL`. `failure_reason` is `NONE` exactly for
PASS and otherwise `EXIT_NONZERO`, `FORBIDDEN_CONTENT`, `OUTPUT_LIMIT`, or
`TIMEOUT`. Each output byte count is a nonnegative safe integer and each SHA is
over the complete corresponding raw stream, with the empty SHA for zero bytes.

The runner is standard-library-only and Windows-specific for Gate I-E. Before
launch it creates a dedicated Windows Job Object and sets both
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and active-process limit one. It creates
the direct child suspended, assigns it to that job, and only then resumes it.
Assignment/configuration/resume failure terminates the suspended child and
stops; there is no unconfined fallback. Active-process limit one prevents the
child from creating any descendant. The runner launches the reviewed absolute
runtime executable without a shell and supplies a minimal environment instead
of inheriting the parent: the reviewed `SystemRoot` value plus, for Python,
only `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, and `PYTHONUTF8=1`; for Node, only
`NODE_DISABLE_COLORS=1`. Proxy, credential, package-manager, startup, user-site,
and `PATH` variables are absent. Gate Q must review the actual Job Object and
environment implementation; prose is not capability evidence.

The runner concurrently consumes raw stdout/stderr, incrementally hashes and
counts all bytes, and retains at most 1,048,577 raw bytes per stream for later
classification. Crossing 1,048,576 bytes or a 300-second monotonic deadline
latches termination, closes child stdin, requests whole-Job termination once,
and starts a ten-second drain. Completion requires both EOFs, Job Object active-
process count zero, and a real direct-child integer exit; otherwise
`*_DRAIN_INCOMPLETE` overrides every other condition. Counts/hashes are never
falsely capped.

When drain completes, one reason is derived from completed observations in this
total precedence:

1. `OUTPUT_LIMIT` if either complete stream exceeds 1,048,576 bytes;
2. `TIMEOUT` if the timeout latch was set;
3. `FORBIDDEN_CONTENT` if either within-cap stream fails strict UTF-8 or
   contains a forbidden token;
4. `EXIT_NONZERO` if the integer exit is nonzero;
5. `NONE`.

Competing stdout/stderr crossings collapse to one `OUTPUT_LIMIT`; reader
scheduling cannot change the category. At each supervisor cycle, direct-child
exit is polled before comparing `monotonic_ns` with the deadline. An already
observed integer exit prevents the timeout latch; otherwise the latch becomes
permanent at `monotonic_ns >= deadline_ns`. A later complete-stream limit still
outranks timeout. Thus output limit outranks timeout/forbidden/exit, forbidden
content outranks nonzero exit, and a truthful FINISHED row is deterministic.
If a FINISHED row is followed by run-record create/read-back failure, the
terminal class is that newest record operation; the FINISHED row preserves the
earlier reason. Named productions outrank `UNEXPECTED_EXCEPTION`.

Summary is exactly `EMPTY`, `BOUNDED_NONSECRET`, or `FORBIDDEN_CONTENT`.
`exit_code` is a nonnegative 32-bit integer. Gate I-W stops at preflight if
`.git` exists; Git is never invoked and has no not-applicable command row.

All SHA fields are strings matching `^[0-9a-f]{64}$`; byte/count/sequence
fields are nonnegative safe integers; booleans are JSON booleans. Every path is
one fixed authorized relative-path string except `project_root`, which is the
literal `L:\dev\yakherd-web`. Task ID is a nonempty printable ASCII string of
1-256 characters. Event names, statuses, types, summaries, and failure classes
are only the literals defined here.

Failure class is exactly `DIRECTORY_CREATE_FAILED`,
`DIRECTORY_READBACK_FAILED`, `PATH_CREATE_FAILED`, `PATH_READBACK_FAILED`,
`COMMAND_FAILED`, `COMMAND_INVOCATION_FAILED`, `COMMAND_OUTPUT_LIMIT`,
`COMMAND_TIMEOUT`, `COMMAND_CONFINEMENT_FAILED`, `COMMAND_DRAIN_INCOMPLETE`,
`PRE_EXECUTION_REVIEW_FAILED`,
`RUN_RECORD_CREATE_FAILED`, `RUN_RECORD_READBACK_FAILED`,
`CANDIDATE_EVIDENCE_CREATE_FAILED`,
`CANDIDATE_EVIDENCE_READBACK_FAILED`, `FINAL_VERIFY_FAILED`,
`FINAL_VERIFY_INVOCATION_FAILED`, `FINAL_VERIFY_OUTPUT_LIMIT`,
`FINAL_VERIFY_TIMEOUT`, `FINAL_VERIFY_CONFINEMENT_FAILED`,
`FINAL_VERIFY_DRAIN_INCOMPLETE`, or
`UNEXPECTED_EXCEPTION`. `failed_check` is respectively the pending directory
path, pending file path, literal `gate_x_pre_execution`, exact command name or
run-record path, candidate-evidence path,
`final_precommit_verifier`, or literal `UNEXPECTED`. A failed/corrupt journal
append cannot safely append a second line claiming that it failed; the last
validated prefix or corrupt tail is itself the durable result and is classified
`INCOMPLETE` or `CORRUPT`.

Before a create or command, its STARTED line is durably validated. Thus a
crash, tool interruption, create/read-back failure, candidate-evidence failure,
or inability to record a terminal failure still leaves a prefix naming the
in-progress operation. A successfully appended terminal event additionally
preserves the complete historical inventory. An absent terminal inventory is
classified only as `INCOMPLETE`/`CORRUPT`; it is never promoted into a claim
about historical bytes. An absent terminal `RUN_COMPLETED` is never PASS.

### 15.2 Installed-protocol structured run records

Command names map to run-record paths exactly as follows:

| Command name | Record path |
| --- | --- |
| `pre_evidence_verifier` | `docs/run_records/concierge_v1_pre_evidence.json` |
| `python_tests` | `docs/run_records/concierge_v1_python_tests.json` |
| `node_tests` | `docs/run_records/concierge_v1_node_tests.json` |
| `protocol_evidence_validation` | `docs/run_records/concierge_v1_protocol_evidence.json` |
| `final_precommit_verifier` | `docs/run_records/concierge_v1_final_precommit.json` |

Each is a strict instance of installed evidence schema version 1 with exactly
the top-level keys `artifacts`, `authority_effect`, `command`, `environment`,
`evidence_class`, `exit_code`, `limitations`, `schema_version`, `stderr`,
`stdout`, `supported_claim`, `timestamp_utc`, and `working_directory`. It is
UTF-8/LF/BOM-free JSON with ASCII-ordinal object keys, no insignificant
whitespace, and one terminal LF. This evidence serializer permits JSON `null`
only where the installed stream schema requires it; it is intentionally not
the bundle serializer in Section 10.

`schema_version` is integer 1. `working_directory` is literal
`L:\dev\yakherd-web`. `command` is the exact journal `argv`; `exit_code` is the
same nonnegative integer. `evidence_class` is `protocol` for
`pre_evidence_verifier` and `protocol_evidence_validation`, and `product` for
the other three. `timestamp_utc` is captured immediately after command exit,
matches `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`, and is explicitly an operator-clock
observation rather than product input.

`environment` has exactly `machine`, `os`, and `runtime`. `machine` is
`sha256:` plus SHA-256 over UTF-8 bytes of Python `platform.node()`; empty input
stops the gate and the raw name is never retained. `os` is the nonempty,
printable-ASCII Python `platform.platform(aliased=False, terse=False)` result,
bounded to 256 characters. `runtime` is the exact recorded Python version for
Python commands or Node version for the Node command, bounded to 128 printable
ASCII characters and satisfying the Section 14 minimum.

`stdout` and `stderr` each have exactly `inline`, `path`, and `sha256`.
`path` and `sha256` are JSON null. Classification is chunk-independent: after
EOF, any stream over the raw cap is forbidden without decoding; otherwise the
complete retained raw stream is decoded once with strict UTF-8 and scanned as
one string against all Section 12 patterns plus exact nonempty tokens for raw
`platform.node()`, the resolved Python/Node executable paths and their parent
directories, and the literal project/source roots. The runner never calls
`getpass.getuser()` or `tempfile.gettempdir()` and reads no username/home/temp
environment key. Invalid UTF-8 or any match makes the journal
summary `FORBIDDEN_CONTENT`, command status FAIL, and `inline` exactly
`[OUTPUT_REDACTED]`. An empty clean stream uses summary `EMPTY` and empty
`inline`. A nonempty clean stream uses summary `BOUNDED_NONSECRET`; `inline` is
the longest complete-scalar suffix of the actual decoded stream whose UTF-8 is
at most 16,384 bytes. Thus chunk boundaries and unbounded token matches cannot
change durable bytes, and matched text is never retained. Full raw-stream byte counts, hashes, and the
`EMPTY`/`BOUNDED_NONSECRET`/`FORBIDDEN_CONTENT` classification remain in the
journal. `artifacts` is an array of objects with exactly `path` and
`sha256`. It is empty for the first three commands; the protocol-validation
record lists records 63-65 in order; the final-precommit record lists candidate
67. All referenced artifacts are immutable by that point.

For journal status `PASS`, `supported_claim` is respectively: `local static source and golden checks
passed`; `local Python product tests passed`; `local shipped-module Node tests
passed`; `records 63-65 satisfy the installed evidence schema`; or
`final-precommit validation of candidate 67 and its active journal prefix
passed`. For status `FAIL`, it is the exact concatenation of the command name,
` failed; this record preserves bounded execution evidence and grants no pass
claim.` A zero exit accompanied by forbidden output or a stream-cap failure
uses the FAIL form. `authority_effect` is exactly `none; this record does not authorize
another gate`. `limitations` is exactly this three-string array in order:

1. `Local dependency-free command only; no browser, operating-system matrix, network, host, deployment, or production claim.`
2. `Only sanitized bounded output suffixes are inline; complete raw-stream byte counts and SHA-256 values are in the append-only journal.`
3. `Timestamp and environment identity are operator observations, not product input or publication authority.`

The fourth Section 14 command validates records 63-65 with the installed pure
validator. Both final modes validate all applicable records against these
same installed rules; `final-complete` includes record 68. A failed command
still gets its truthful run record before `RUN_FAILED` when that record can be
created safely.

### 15.3 Canonical pre-final candidate evidence

`docs/run_records/concierge_v1_local_candidate.json` is Section 10 canonical
JSON with exactly these top-level keys:

```text
authorizations
checks
commands
directories
files
governance_runner
implementation
journal_prefix_sha256
prelaunch_resolver
release_pin
root
schema_version
source_asset
status
unexpected_paths
```

`schema_version` is integer 3 and `status` is `PRE_FINAL_PASS`.
`unexpected_paths` is an
empty array. `journal_prefix_sha256` is the full journal hash immediately after
`CANDIDATE_EVIDENCE_CREATE_STARTED`; it cannot include the evidence's own
identity.

`authorizations` has exactly `bootstrap_audit`, `gate_a_audit`,
`gate_p_combined_audit`, `gate_q_activation`, `gate_r_evidence`,
`gate_x_authorization`, and `plan`. Each is an object with
exactly `bytes`, `path`, `sha256`, and `status`; status is `PASS` for
audits/evidence and `REVIEWED` for the post-intake plan. `release_pin` is
exactly the parsed canonical `yakherd_release.v1.json` object, with no wrapper
or extra key.

`root` has exactly `absolute_path`, `ancestor_reparse_points_at_gate_b`,
`ancestor_reparse_points_at_gate_i`, `baseline_install_receipt_sha256`,
`gate_b_installed_baseline_sha256`, `gate_p_after_manifest_sha256`,
`gate_x_pre_execution_tree_sha256`, `git_state`,
`pre_gate_p_manifest_sha256`, and
`target_existed_before_gate_b`. The absolute path is literal
`L:\dev\yakherd-web`; both reparse arrays are empty; the receipt hash is 64
lowercase hex and refers only to `JEFF_STRICT_SSOT_INSTALL.json`, not a whole-
tree baseline; the Gate B baseline, pre-Gate-P manifest, Gate P after-manifest,
and Gate X tree hashes are the exact reviewed lowercase values;
`git_state` is literal `ABSENT`; and the final field is boolean false. It does
not claim the installed root was absent at Gate I.

`governance_runner` has exactly `bytes`, `gate_q_authorization_sha256`, `path`,
`sha256`, and `version`. Path is
`scripts/concierge_gate_i_runner.py`; version is
`yakherd-concierge-gate-i-runner/1`; the remaining values exactly match Gate Q.

`prelaunch_resolver` has exactly `bytes`, `gate_q_authorization_sha256`,
`sha256`, and `version`. Version is
`yakherd-concierge-prelaunch-resolver/1`; the remaining values exactly match
Gate Q and Gate X. It records the identity required for every outer runner
launch and does not claim that the non-file resolver is part of the target
tree.

`implementation` has exactly `effort`, `model`, `runtime_node`,
`runtime_python`, `sole_writer` = true, and `task_id`. Model is literal
`gpt-5.6-terra`, effort is literal `high`, task ID follows the journal grammar,
and runtime strings are printable ASCII of 1-128 characters whose recorded
versions satisfy Python >=3.11 and Node >=20.

`source_asset` has exactly `destination_bytes`, `destination_path`,
`destination_sha256`, `source_bytes`, `source_engine_commit`, `source_git_blob`,
`source_path`, and `source_sha256`, all bound by Section 5.

`directories` has exactly six rows in Section 5 order. Each has exactly
`after_type` = `DIRECTORY`, `before_type` = `ABSENT`, and `path`.

`files` has exactly 66 rows in Section 5 order for files 1-66, not candidate 67
or future final-precommit record 68. Each row has exactly `after_bytes`,
`after_sha256`, `after_type` = `REGULAR_FILE`, `before_type`, and `path`.
`before_type` is `REGULAR_FILE` only for file 33, the exact Gate Q runner, and
is `ABSENT` for every other row. The runner's before/after identities are equal.
The journal row hashes the journal prefix named above, not later appended lines.

`commands` has exactly four rows in Section 14 order. Each row has exactly
`argv`, `exit_code`, `failure_reason`, `name`, `stderr_sha256`, `stderr_summary`,
`stderr_bytes`, `stdout_bytes`, `stdout_sha256`, `stdout_summary`, and `status`,
using the journal types and exact command names/order. The final verifier is
not self-embedded; its later result is journaled.

`checks` is an array in this exact name order: `authorized_inventory`,
`gate_p_baseline`, `gate_q_runner`, `gate_x_pre_execution`, `git_absent`,
`content_binding`, `static_source_policy`,
`release_pin`, `asset_identity`, `golden_oracle`, `python_tests`, `node_tests`,
`protocol_evidence_validation`, `encoding_whitespace`, `no_secret_retention`,
and `unexpected_paths`. Each row has exactly `name` and `status`; every status
is `PASS`.

Every authorization object has a nonnegative safe-integer `bytes`, its exact
path frozen by the post-intake plan, a lowercase-hex `sha256`, and its stated
literal status. Project records use repository-relative paths; only
`gate_a_audit`, `gate_q_activation`, `gate_r_evidence`, and
`gate_x_authorization` may use their exact external
`L:\dev\YAKHERD` paths frozen by the reviewed Gate A/Gate R records. Every source-asset byte field is a
nonnegative safe integer; its hashes and Git blob are lowercase hex of lengths
64 and 40; its engine commit is 40 lowercase hex; and its paths are the exact
Section 5 source/destination strings. No alternate,
missing, extra, reordered-array, mixed-type, or null shape is valid. Candidate
status is derived only when all required check rows pass, `.git` is absent,
all directory/file read-backs match, and every authorization is bound. It is
not overall Gate I-E or installed-project completion.

### 15.4 Output and failure boundaries

The candidate evidence and journal contain no user test prompt other than
hashes of the public non-secret fixtures, no source body, no machine username, no secret, no
absolute temp path, no browser content, no screenshot, and no credential.
Command output is incrementally bounded, hashed, and scanned under Section
15.1; durable files store byte counts, full-stream hashes, and fixed summaries,
not raw output. Forbidden content or the stream cap makes the run FAIL.

Implementation never cleans an unknown or pre-existing path. On failure after
journal creation the reviewed runner appends `RUN_FAILED` with the embedded
inventory when possible, stops, and asks
Architecture for a recovery plan. It does not retry, delete, overwrite, commit,
reset, move, or publish. Only a separately reviewed recovery plan may remove
created files. A failure while appending still leaves the last validated
prefix; no later product mutation is permitted.

After `RUN_COMPLETED`, Implementation reports byte lengths and SHA-256 values
for the pre-final candidate, all five installed-protocol records, and the final
completed journal. It reports `.git` absent, installed-project completion not
yet claimed, and ends with `autonomous next action: Gate S final independent review`.
Gate S reproduces every identity and may run only the reviewed runner's exact
read-only `verify-complete` subcommand without mutating any file or launching a
child.

## 16. Later acceptance requirements retained from the directive

The following remain required for product completion but are intentionally not
part of Gate I:

- identical bundle bytes for the fixed fixture in current Chromium, Firefox,
  and WebKit on at least two operating systems;
- Gate C request interception in separately authorized clean, extension-
  disabled temporary profiles. The permitted site-origin graph is the initial
  loopback document navigation and the exact reviewed same-origin static
  subresources. From `interactive-ready` through download, there must be no
  site-code-initiated request. Non-site browser/platform traffic is classified
  separately and cannot be converted into a product claim. Gate S performs no
  part of this runtime check;
- ZIP extraction with default tools on Windows, macOS, and Linux, followed by
  exact hashes;
- a fresh public-artifact `v1.2.0` install and unchanged `product_intake.md`
  bridge preserving prompt length/hash, including terminal LF;
- keyboard-only, 320px reflow, zoom, forced-colors, reduced-motion, and
  qualified screen-reader walkthrough, plus a named automated scanner whose
  installation/capability is separately authorized;
- no-JS and secure-context/insecure-context behavior;
- Gate C proof that the unmodified committed site completes the full
  application flow under `python -m http.server`, serves `.mjs` with an
  executable JavaScript MIME type, and produces the reviewed deterministic
  bundle, while separately recording that TLS, redirects, response headers,
  caching, compression, and logs are not locally production-equivalent;
- Gate S exact-source security/parser/completed-evidence Red Team PASS;
- Gate T PASS and successful same-writer promotion of the reviewed result to
  its real owner paths and compact `STATUS.md`, with supersession/staleness and
  Git-absence visibility recorded;
- GitHub, staging, hosting headers, custom error, MIME, caching, compression,
  redirects, public allowlist, rollback, and production evidence;
- staging and production serving the same committed site bytes.

The final Definition of Done is all of the above, including Gate T promotion,
plus an owner-approved public release. A plan PASS, Gate I-E candidate-slice
PASS, or staging PASS is not product completion.

## 17. Stop conditions and forbidden improvisation

Stop without workaround if:

- `v1.2.0` is not public and exactly authenticated;
- its public intake or START_HERE bytes differ from the release pin;
- the target root or a destination is present, ambiguous, or reparse-backed;
- the new task cannot prove installed `AGENTS.md` is active;
- a second writer is active on the same checkout;
- the exact source directive cannot pass unchanged product intake;
- a prompt contains a delimiter line or an unsupported Unicode value;
- deterministic golden ZIP bytes diverge;
- the Gate Q runner or prelaunch-resolver bytes/activation identity differ,
  any runner launch cannot use the exact resolver, its fixed capability probe
  fails, or Gate X cannot close the executable-source/capability matrix;
- Job Object assignment, active-process limit one, minimal child environment,
  complete pipe drain, or exact Python/Node runtime identity is unavailable;
- the site would need a network API, third-party resource, dependency, build
  step, backend, inline script, unsafe sink, or unlisted file;
- local novice testing tempts the team to describe fixed logic as AI;
- a test capability is absent;
- an exact public, GitHub, hosting, DNS, credential, staging, deployment,
  rollback, or production fact is unknown.

Do not substitute another release, host, repository, asset, task, framework,
test tool, path, or privacy promise. Return to Architecture for a new exact
candidate and fresh independent review.

## 18. Model routing and handoff

- Mechanical inventories and hashing: Luna medium when available.
- Routine implementation/research: Terra medium/high.
- Architecture or difficult debugging: Sol high/xhigh.
- Final independent security, parser, deployment, or release gate: one Sol
  Ultra agent only. Do not use Ultra for drafting or routine work, and do not
  start a second Ultra agent without owner permission.
- Never run two implementation writers against the same checkout.

Every delegated message states task role, model, effort, routing reason, exact
input hashes, permitted write set, forbidden actions, evidence path, stop
conditions, and whether token usage is task-bounded or continuation-based.

For the current review, Red Team must return PASS or FAIL against this exact
plan and exclusively create only
`docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team_v3.md`.
That path must be absent at entry. On PASS,
Red Team may tell the existing Implementation task only that product work
remains parked pending Gates R-PREP/R/B/P/Q and a correctly attached separate-
repo Implementation task. It must not send Gate I-W as executable work until
those gates have exact independent PASS evidence.

## 19. Current authority effect

Before its independent PASS, this candidate authorizes only documentation
validation and fresh review. A PASS authorizes only the exact documentation-
only Gate R-PREP write set in Section 4. It does not authorize release mutation,
Git/tag/GitHub/PyPI,
network or browser action, creation of `L:\dev\yakherd-web`, product intake,
Implementation, dependency use, image copying, evidence-skeleton creation,
credentials, hosting inventory, DNS, staging, deployment, production, or
publication. All prior v15/DreamHost records remain preserved future work and
stay parked.
