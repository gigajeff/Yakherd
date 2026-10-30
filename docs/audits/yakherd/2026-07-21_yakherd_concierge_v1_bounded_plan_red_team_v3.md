# Independent Red Team Review - Yakherd Concierge V1 Bounded Plan V3

Date: 2026-07-21

## Review target and reproduced identity

- path: `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan_v3.md`
- schema: `yakherd-concierge-architecture-plan-v3`
- observed bytes: `142347`
- observed LF-delimited lines: `2589`
- observed SHA-256: `d687860db50cb816d899043cee9f3e7825195602a0884fead242b6a92bc28b51`
- text form: strict UTF-8; LF-only; no BOM; exactly one terminal LF; zero trailing-whitespace lines

All six bound input identities independently matched the assignment:

1. source directive: 17,487 bytes; 319 lines; SHA-256 `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`;
2. directive audit: 19,030 bytes; 164 lines; SHA-256 `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`;
3. bounded plan V1: 68,774 bytes; 1,391 lines; SHA-256 `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029`;
4. V1 plan audit: 16,166 bytes; 150 lines; SHA-256 `34b19607510fdd696904974e2cb56aced148ef2b46838dec72ce6fd5a62a6fda`;
5. bounded plan V2: 103,293 bytes; 1,956 lines; SHA-256 `68f444c46992b0dd31c8b84f328d85b86cc6851e1c3693ca22bc8b44aca2809a`;
6. V2 plan audit: 15,149 bytes; 137 lines; SHA-256 `32b1274e4350ea732b14565d9925fb8c4d9bd61728a60c6f63f039e41676b1ec`.

## Prioritized findings

### P0

No P0 finding was identified.

### P1 - The non-file resolver cannot both remain byte-bound and receive its required later values

Gate P is required to freeze one complete strict-base64 block whose decoded bytes and SHA-256 are the reviewed non-file PowerShell resolver (`candidate:323-336`). Gate Q reproduces that identity in its authorization and reviews the resolver's substitutions (`candidate:473-494`). Every launch must then submit those exact decoded source bytes as the task tool's one PowerShell command (`candidate:1719-1725`).

The same launch nevertheless requires values that do not exist when the resolver block is frozen: the later Gate Q authorization length/hash, its resolver identity, a per-invocation runner argument array, and Gate X observation/audit substitutions (`candidate:1726-1731`). No separate argv, stdin, or other authenticated data channel is defined. Writing a resolver file, changing an environment value, appending operator code, using a wrapper, or reconstructing an alternate launcher is expressly forbidden (`candidate:1724-1726`, `candidate:1760-1768`, `candidate:1770-1778`). Rendering those values into the command changes the executing source bytes, so the command is no longer the strict-base64-decoded source whose hash Gate P/Q reviewed.

The stated prelaunch checks do not cure this. They compare resolver metadata in the hash-authenticated Gate Q JSON with handed-back metadata (`candidate:1733-1740`); they never obtain and hash the actual non-file PowerShell source being executed. An altered resolver could perform those metadata comparisons while executing altered behavior. The plan therefore has neither an operational value carrier nor authentication of the active resolver bytes. `RESOLVE_AND_RUN` cannot truthfully establish the claimed Gate Q/Q-X trust boundary for Gate I-W, Gate X, Gate I-E, failure finalization, or Gate S.

This leaves V2 P1 number 4, the independently reviewed exact supervisor/launcher requirement, open.

### P1 - Outer timeout or interruption can leave the mutating Python runner alive

The resolver launches one Python runner and buffers its output, but it does not place that runner in a reviewed kill-on-close process container or bind a task-tool process-tree termination guarantee (`candidate:1754-1763`). The runner's Windows Job Object is created later around each supervised command child; active-process-limit-one and Kill-on-Close protect those children, not the runner process itself (`candidate:2193-2215`).

For the 1,650-second Gate I-E outer call, the plan says outer interruption or timeout merely leaves the last validated journal prefix and authorizes no second invocation (`candidate:1903-1907`). That assertion is unsupported. If the outer PowerShell process or tool wait is terminated without a proven tree kill, the Python runner can remain alive, continue journal/evidence mutation, and retain the Job Object handles for its child. A supposedly stable handback can therefore change after control returns, while the no-retry rule provides no safe observation or finalization production.

The defect also applies to the repeated Gate I-W launches, Gate X confinement probe, failure-record launch, and Gate S verification because none binds the outer runner lifetime. The inner Job design closes descendant behavior only after a command child is created; it does not close the resolver-to-runner interruption boundary.

### P1 - `python -I -B` still permits ambient startup code before the reviewed entry point

Every outer resolver launch invokes the runner with exact Python flags `-I -B` (`candidate:1749-1752`). The supervised Python commands use the same pair (`candidate:1913-1917`, `candidate:1925-1927`). Gate X and the child-environment contract nevertheless claim that ambient startup/dependency resolution is closed before reviewed code runs (`candidate:1874-1879`, `candidate:2199-2205`).

Python isolated mode does not imply `-S`. `-I` implies environment isolation, safe-path behavior, and user-site suppression, but the interpreter still imports `site`; system site-packages, executable `.pth` import lines, and `sitecustomize` can run before the runner or test entry point. A read-only check with the accepted local CPython 3.13 runtime reproduced `site_loaded=True`, `no_site=0`, and one system `site-packages` path under exact `-I -B` invocation.

Those ambient sources are absent from the Gate X `executable_sources` manifest (`candidate:1823-1839`), and hashing `python.exe` does not bind separately installed site/startup files. For the outer runner this unreviewed code can execute before `sys.executable`/version validation, before the journal exists, and outside the child Job Object. For supervised children it executes inside the Job but still has unreviewed filesystem, import, native, environment, and network capability. V2 P1 number 5 therefore remains open independently of the later exact-source review.

### P1 - Mandatory platform observations contradict the closed capability matrix

Gate X must assert that the reviewed executable boundary has no unlisted network, environment/credential, registry, or process capability; the runner exception is limited to target/evidence access, one `SystemRoot` read, bounded hostname/OS/time observations, and the exact Job/pipe APIs (`candidate:1841-1859`). The executable-source manifest covers project Python/Node sources and the installed validator, but not the Python standard-library modules implementing runtime observations (`candidate:1823-1839`). Only the Python executable file's bytes/hash and version are bound (`candidate:1804-1811`).

The run-record contract nevertheless mandates Python `platform.node()` and `platform.platform(aliased=False, terse=False)` (`candidate:2305-2311`). Across the accepted CPython >=3.11 range on Windows, those APIs can transitively use `socket.gethostname`, processor environment values, WMI, registry access, and a shell/subprocess `ver` fallback. A read-only inspection of the available CPython 3.13 standard library confirmed those branches. Hashing `python.exe` does not bind the separately installed `platform.py` and its transitive modules, and the Gate X matrix neither lists nor eliminates those capabilities.

Consequently Gate X cannot truthfully emit all of `network_capability_absent`, `environment_and_credential_capability_absent`, `descendant_creation_absent`, and the stated runner capability restriction while also producing the required environment record. This is a direct continuation of V2 P1 number 5: the pre-execution capability boundary remains incomplete even though Implementation-authored sources are now reviewed before execution.

### P2 - The current-gate handoff contradicts its own no-Implementation-contact boundary

Gate A says a PASS authorizes only Gate R-PREP and explicitly does not authorize Implementation contact (`candidate:162-169`). The final handoff section nevertheless says that on PASS Red Team may tell the existing Implementation task that product work remains parked (`candidate:2570-2577`). The current authority effect again limits PASS to the documentation-only Gate R-PREP write set and says Implementation is not authorized (`candidate:2579-2589`).

A parked-status message is still contact with Implementation and is outside the exact Gate R-PREP write set. It also conflicts with this review assignment's explicit prohibition. The authority sequence must have one unambiguous owner: a current PASS can return only to Architecture for Gate R-PREP.

### P3

The plan advertises Python `>=3.11` without an upper bound (`candidate:1712-1717`), but both frozen runtime-observation regexes accept only minor versions 11 through 99 (`candidate:458`, `candidate:550`). They reject Python 3.100 or later even though those versions satisfy the written range. This is not a current execution hazard, but the prerequisite and accepted grammar are not the same exact contract.

## V2 finding closure audit

V3 materially closes five of the seven concrete V2 defect shapes and preserves those corrections:

- Gate B now freezes a complete installed baseline before bootstrap, and Gate P truthfully represents the exact six `BOOTSTRAP_CREATED` artifacts in its pre-manifest before deriving the after-manifest (`candidate:264-280`, `candidate:338-405`).
- `RUN_COMPLETED` and `RUN_FAILED` now directly embed the complete 74-row pre-terminal inventory; `OTHER` and `UNOBSERVABLE` are representable and included in `retained_or_unresolved_paths`, with the journal-prefix self-reference excluded (`candidate:2091-2095`, `candidate:2156-2186`).
- The exact Node path is now one direct `node tests\\test_interview.mjs` process with a fixed same-process harness rather than `node --test` descendants (`candidate:139-148`, `candidate:1889-1918`).
- Overlapping command conditions now have a total precedence, explicit drain override, exit/timeout race rule, and deterministic record-failure precedence (`candidate:2112-2138`, `candidate:2217-2236`).
- Gate S is offline only; Gate C exclusively owns later local serving, browser execution, and request interception (`candidate:911-927`, `candidate:627-646`).

The frozen runner, Gate Q review, Gate I-W write-only split, Gate X source review, and Gate I-E child confinement are substantial improvements. They do not close the two remaining predecessor P1s because the authenticated outer launch is not realizable, the runner lifetime is not fail-closed, ambient Python startup remains executable, and the runtime-observation dependency violates the claimed capability matrix.

The exact Gate A PASS boundary otherwise correctly narrows intended authority to one no-overwrite Architecture candidate and its later independent review at Gate R-PREP (`candidate:164-194`). Gate P manifest self-reference, Gate X tree self-reference, candidate-evidence prefix binding, and terminal-journal prefix binding are internally separated as claimed.

## Fixture reproduction

All nine Section 11 fixtures reproduced independently:

| Fixture | Bytes | SHA-256 |
| --- | ---: | --- |
| `prompt_ascii_lf.txt` | 15 | `6e7dd93a7067af125e7511989288fded9b9ac794bdc4dcdb2386c82be681d093` |
| `prompt_unicode_lf.txt` | 21 | `b7235def28ab82dbf8190a1823d762d844ba1c5108e24bde4e3216dbe94de823` |
| `prompt_empty.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `prompt_rejected_lone_surrogate.json` | 42 | `d896c43281e7792bee0f1b5b7f6015488e69476113bae8b70c7fb95dd3a87e6e` |
| `prompt_rejected_delimiter.txt` | 30 | `bae930977c32a38633deb764b057b94d26f25f9c9f7c7c83b2d3470d06253f2a` |
| `secret_clean.txt` | 50 | `71207f9ff2aa7fdea169735ab97f84fea19bda146dad3ec6268ac3ab07bfa03f` |
| `secret_positive.txt` | 70 | `de1bac33ed9c73e034c0208509ffc167d7a7f2a9de98e45e07153461c4e63d8b` |
| `high_stakes_clean.txt` | 29 | `653687b406ccdbdc1c9b8d4fed2d042bcd986f161c724a490f7b07a03cf66406` |
| `high_stakes_positive.txt` | 44 | `33aaf433ef6fb46e9770d220f4bc2f07872a5a0119f17b9a33f01cbdeeffc20f` |

The Unicode fixture uses the single scalar U+00E9 encoded as UTF-8 `c3 a9`.

## Verdict

**FAIL.** V3 is materially stronger and resolves the manifest, terminal-inventory, Node-harness, failure-precedence, and Gate S/C defects. It does not supply an authenticated executable non-file resolver invocation, cannot stop or account for an orphaned outer runner, permits unreviewed Python startup before its entry point, and cannot truthfully close the mandatory runtime-observation capability matrix. The authority handoff also contradicts the exact no-Implementation-contact boundary.

## Required revisions before fresh review

A new exact candidate must, without performing any Gate R-PREP, release, intake, or product action:

1. Bind one operational resolver invocation primitive whose actual executing bytes are authenticated and whose later Gate Q/Gate X values travel through an independently authenticated, non-source-changing argument channel. The exact tool/API carrier, quoting/encoding, byte-hash domain, parse-failure behavior, and transcript boundary must be reviewable and must not rely on an unbound wrapper or metadata-only self-claim.
2. Bind the complete outer resolver/runner process lifetime. Every timeout, task interruption, resolver failure, and runner failure must have a proven tree-wide stop/drain observation and deterministic journal/evidence outcome before control can be handed back; an unobserved live runner must never be described as a stable prefix.
3. Prevent every unreviewed Python startup source from executing before the runner and its Python children. The exact invocation and bound runtime/import-root policy must exclude or independently authenticate system site-packages, `.pth` code, `sitecustomize`, and every other startup hook before claiming a closed source graph.
4. Make the environment record compatible with the capability policy. Remove the transitive `platform.*` capability, replace it with exact reviewed primitives, or explicitly bind and review every required runtime/standard-library/OS dependency and allowed environment/registry/process/network edge. Gate X checks and the runner matrix must state the same truth.
5. Remove the Gate A permission to contact Implementation. The current PASS handoff may go only to Architecture and may authorize only the exact Gate R-PREP documentation candidate and fresh review.
6. Make the accepted Python-version grammar identical to the advertised supported range.

Red Team has not selected implementation bytes or repaired the candidate.

## Residual risk

After revision, Gate R-PREP and the later final Ultra release gate must still bind the complete public v1.2.0 supply chain. The combined Gate P review must independently decode and review the full runner/resolver/golden blocks and complete intake manifests. Gate Q/X/S must verify the resulting bytes and all adverse FSM paths. Gate C, Git, hosting, staging, rollback, DNS, deployment, and production remain separate high-risk gates with no current authority.

## Authority effect

This FAIL authorizes Architecture only to preserve this audit and draft one new exact pre-intake candidate for fresh independent review. It does not authorize Gate R-PREP, release preparation or mutation, Gate R/B/P/Q/I-W/X/I-E/S/T/C/G/H/D/O, Implementation contact or work, Git mutation, network/browser/DreamHost, credentials, dependencies, images, evidence skeletons, creation of `L:\dev\yakherd-web`, GitHub/PyPI, hosting, DNS, staging, deployment, production, or publication.

The existing Implementation task remains parked and was not contacted.

## Validation and preservation

- `python -B scripts\\verify_release.py`: PASS (`release_verification status=passed manifest_files=47 cache_paths=0`).
- `git diff --check`: PASS.
- Candidate and audit non-index UTF-8/LF/BOM/terminal-LF/trailing-whitespace validation: PASS for both files (`git diff --no-index --check` returned the expected difference status `1` with no whitespace error; strict UTF-8, LF-only, no BOM, exactly one terminal LF, and zero trailing-whitespace lines).
- Baseline Git state: branch `main`; HEAD `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`; upstream `origin/main`; ahead/behind `0/0`; staged paths `0`; tracked-diff paths `0`.
- The six current intended release-contract identities in `candidate:229-244` independently matched the repository bytes.
- Only this authorized audit path was created. The candidate, every predecessor, package/release bytes, prior records, Git state, release state, product paths, network/browser/DreamHost, credentials, dependencies, images, GitHub/PyPI, target repository, hosting/DNS/staging/deployment/production/publication were not changed. `yakherd.mp4` was not read, hashed, inspected, moved, or touched.

autonomous next action: Architecture may preserve this FAIL and draft one new exact pre-intake candidate; Gate R-PREP and all product work remain parked.
