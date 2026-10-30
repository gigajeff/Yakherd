# Independent Red Team Review — Yakherd Concierge V1 Bounded Plan V2

Date: 2026-07-21

Review target:

- path: `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan_v2.md`
- observed bytes: `103293`
- observed lines: `1956`
- observed SHA-256: `68f444c46992b0dd31c8b84f328d85b86cc6851e1c3693ca22bc8b44aca2809a`

Bound predecessors independently matched:

- source directive: 17,487 bytes; 319 lines; SHA-256 `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`;
- directive audit: 19,030 bytes; 164 lines; SHA-256 `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`;
- predecessor plan: 68,774 bytes; 1,391 lines; SHA-256 `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029`;
- predecessor-plan audit: 16,166 bytes; 150 lines; SHA-256 `34b19607510fdd696904974e2cb56aced148ef2b46838dec72ce6fd5a62a6fda`.

## Prioritized findings

### P0

No P0 finding was identified.

### P1 — Gate P cannot classify the required post-install bootstrap artifacts

Gate B records the installation receipt, installed inventory, hashes, and verifier output, and only afterward runs the mandatory bootstrap Red Team review (`candidate:208-213`). The installed bootstrap contract requires five new run records and one review file (`packages/jeff_strict_ssot_v1/template/docs/prompts/bootstrap_cold_resume_review.md:32-50`). Those six files therefore exist before Gate P but were not part of the earlier installation receipt.

Gate P's exhaustive after-manifest permits only these `baseline_relation` values: `UNCHANGED_GATE_B_RECEIPT`, `CHANGED_BY_GATE_P`, and `CREATED_BY_GATE_P` (`candidate:257-275`). A bootstrap-created run record or review is none of those. It was not in the installation receipt, and Gate P neither created nor changed it. The claimed manifest cannot truthfully cover every descendant path, and the later Gate I baseline comparison cannot succeed as specified (`candidate:1425-1449`).

This is an authority and provenance defect, not a naming issue. Gate P needs a separately identity-bound post-bootstrap/pre-intake baseline or an exact relation capable of representing every bootstrap-created artifact without relabeling its actor or time.

### P1 — The terminal failure record contains an inventory hash, not the claimed durable inventory

The journal's terminal event schemas contain `pre_terminal_inventory_sha256`; `RUN_FAILED` additionally contains `retained_paths` (`candidate:1560-1562`). No event key contains the 74 inventory rows. Later prose nevertheless calls an inventory “embedded in `RUN_COMPLETED` or `RUN_FAILED`,” defines its row schema, and says the hash covers its bytes (`candidate:1612-1629`). The body being hashed is not durably embedded or written to another authorized file.

A later recovery can remove or replace retained paths. After that, Red Team cannot reconstruct the historical failure inventory from its hash and path-name list. The gap is especially material after a create/read-back failure where no `PATH_CREATED` identity exists. `retained_paths` also excludes `OTHER`, so an abnormal authorized path can be omitted from the only stored path list (`candidate:1624-1629`).

The append-only prefix usefully names the pending operation, but it does not preserve the full historical byte/type state. V2 therefore does not fully close the predecessor P1 requiring durable structured evidence for partial and retained failures.

### P1 — The exact Node test command contradicts the no-descendant process premise

V2 correctly moves shipped and test modules to `.mjs`, closing the predecessor module-mode defect (`candidate:113-126`, `candidate:381-415`). Its exact command is nevertheless `node --test` over eight test files (`candidate:1385-1396`). Node's test runner uses process isolation by default; without an explicit, supported isolation choice it creates child test processes.

The candidate simultaneously says the reviewed test sources do not create descendants and treats any child retaining output pipes as a contract failure rather than an expected background process (`candidate:1459-1463`, `candidate:1643-1645`). The accepted range begins at Node 20, but the plan binds neither a single runtime version nor one isolation capability/flag that is supported and behaviorally identical throughout that range.

This contradiction breaks the timeout/termination/EOF-drain model for the exact command. Source-level absence of `child_process` or `worker_threads` imports does not stop the Node test harness itself from creating descendants.

### P1 — No reviewed command supervisor implements the journal's execution claims

The journal requires direct argv launch, concurrent complete-stream byte counting and hashing, a 1,048,576-byte per-stream limit, termination at 300 seconds or the first limit crossing, a 10-second EOF/exit drain deadline, strict UTF-8 and secret/machine-token scanning, deterministic suffix capture, and truthful invocation/drain failure productions (`candidate:1576-1604`, `candidate:1631-1648`, `candidate:1716-1729`).

No command-supervisor implementation, immutable tool identity, or exact capability is present in the 68-file write set (`candidate:340-445`). The four displayed commands and final verifier are child argv, not a supervisor. Added wrappers and flags are expressly nonequivalent (`candidate:1598-1604`). The plan also requires unlisted `node --version`, Python version, platform, hostname, username, and temporary-root observations (`candidate:118-126`, `candidate:1700-1729`).

An ordinary agent shell call does not establish complete raw-stream hashes after UI/tool truncation, pre-transcript redaction, process-tree termination, or the specified drain semantics. An improvised in-memory PowerShell/Python supervisor would itself be unreviewed executable logic outside the exact write and evidence set. Gate I therefore cannot reproducibly produce the evidence it requires from the authorized mechanisms.

### P1 — Gate I executes writer-authored code before any closed no-network or filesystem-capability gate

Gate I forbids network use and dependency installation (`candidate:297-308`), but its first command executes `scripts/verify_static.py`, which is authored by the same Implementation writer, followed by writer-authored Python and Node tests. Gate S performs independent exact-source review only afterward (`candidate:321-338`).

The pre-evidence checks deny selected process-spawning tokens but do not close Python `socket`, `urllib`, `http.client`, DNS, arbitrary filesystem reads/writes, environment/credential access, dynamic imports, or equivalent standard-library capabilities (`candidate:1439-1463`). The browser-JavaScript denylist and CSP do not constrain Python test/verifier execution. The same implementation-authored verifier cannot establish its own pre-execution containment.

No independently reviewed pre-execution source allowlist, network-disabled sandbox, filesystem boundary, or trusted installed runner is named. Thus unreviewed Gate I code can exercise exactly the external capabilities the authority boundary says remain unavailable before Gate S can detect it.

### P2 — Overlapping command failures have no canonical precedence

The journal distinguishes `EXIT_NONZERO`, `FORBIDDEN_CONTENT`, `OUTPUT_LIMIT`, and `TIMEOUT`, with different productions and classes (`candidate:1576-1596`, `candidate:1631-1646`). It does not state which event wins when conditions overlap, including:

- nonzero exit plus forbidden output;
- output-limit crossing at the timeout boundary;
- stdout and stderr crossing different limits in competing order; or
- process exit racing termination/drain observation.

Those paths can produce different canonical journal and run-record bytes from the same underlying command behavior. The FSM needs one total condition/event precedence and exact process-tree termination observation rule.

### P2 — Gate S and Gate C browser authority is inconsistent

Section 6 says Gate S performs runtime request interception (`candidate:596-600`). The authority sequence defines Gate S as the exact-source security/parser gate and separately assigns the browser/OS/request capabilities to Gate C (`candidate:321-338`, `candidate:1865-1890`). Gate I also expressly forbids browser automation (`candidate:305-308`).

No current gate receives browser authority, so this does not leak live action now. It does leave the later authority owner ambiguous: request interception must be assigned to one separately authorized gate with its exact browser/profile/network evidence, rather than being implied by Gate S prose.

### P3 — Predecessor findings that V2 materially closes

V2 does close the predecessor's substantive product-design defects, and those corrections should be preserved:

- distinct `pre-evidence`, `final-precommit`, and read-only `final-complete` verifier modes allow final-tree verification (`candidate:1385-1492`);
- the journal is the first mutation, brackets planned operations, has an explicit hash chain and terminal PASS rule, and preserves a useful pending-operation prefix (`candidate:1509-1677`);
- privacy copy now describes seven days as an application read/use policy, narrows deletion to current-key read-back, and discloses retained platform copies (`candidate:1264-1383`);
- secret detectors run before every persistence write and before restoration renders text (`candidate:1305-1319`);
- `UNKNOWN`, skipped, unanswered, and invalid restored high-stakes values fail closed, while the explicit `NO` clean case remains testable (`candidate:640-650`, `candidate:1137-1143`, `candidate:1250-1262`, `candidate:1279-1287`);
- `.mjs` removes ambiguous `.js` module classification, subject to the distinct test-runner process finding above (`candidate:113-126`);
- Architecture and Red Team freeze and independently reproduce the complete golden entry/ZIP bytes before Gate I, and the identity schema is exact (`candidate:1106-1176`);
- GitHub and browser-request language is narrowed to site-controlled behavior and explicit user navigation (`candidate:70-84`, `candidate:489-529`);
- canonical JSON, ZIP32 headers/limits, approval snapshots, delimiter framing, write set, no-overwrite behavior, separate root, and single-writer boundary remain strong;
- the A/R/B/P/I/S/T/C/G/H/D/O sequence keeps release publication, product intake, Implementation, browser/OS work, Git, hosting, staging, deployment, DNS, production, and publication separately gated (`candidate:135-338`, `candidate:1902-1956`).

All nine Section 11 fixture lengths and SHA-256 values independently reproduced exactly.

## Verdict

**FAIL.** V2 substantially improves the plan, but Gate P cannot express its actual baseline, the failure inventory is not durably preserved, and the exact Gate I execution boundary contradicts Node's test isolation and lacks a reviewed supervisor and pre-execution containment. Gate R preparation remains parked.

## Required revisions before fresh review

A new exact candidate must, without performing release, intake, or implementation work:

1. Bind the complete post-bootstrap/pre-Gate-P tree and give every bootstrap-created path a truthful, exhaustive provenance relation before Gate P mutates anything.
2. Preserve the complete canonical pre-terminal inventory, including `OTHER` and every retained/partial state, in a recovery-stable durable record without journal self-reference.
3. Make the exact Node test invocation, supported Node range, isolation/descendant behavior, termination, and EOF-drain rules mutually consistent.
4. Bind one independently reviewed command supervisor/tool and its exact version, argv, raw-stream, timeout, output-limit, termination-tree, drain, redaction, environment-observation, and transcript boundary; do not leave executable orchestration to improvisation.
5. Establish a trusted pre-execution no-network, dependency, filesystem, environment, credential, import, and process-capability boundary for writer-authored Python/Node code before it runs.
6. Define total precedence for every overlapping command failure and assign runtime request interception to one separately authorized later gate.

Red Team has not selected repair bytes or changed the plan; these are exact review predicates.

## Residual risk

After revision, the later Gate R and Gate S Ultra reviews must still independently bind the public v1.2.0 supply chain, installed intake contract, reference ZIP oracle, parser behavior, source containment, and complete evidence grammar. Gate C must verify browser MIME, requests, downloads, storage, clipboard, and accessibility in named environments. Host, Git, staging, rollback, DNS, and production remain distinct high-risk gates.

## Authority effect

This FAIL authorizes Architecture only to preserve this record and prepare a new exact pre-intake candidate for fresh review. It does not authorize Gate R preparation or publication, package/release mutation, Gate B/P/I/S/T/C/G/H/D/O, Implementation contact or work, Git mutation, network/browser/DreamHost, credentials, dependencies, image actions, evidence skeletons, repository creation, hosting, DNS, staging, deployment, production, or publication.

The existing Implementation task remains parked. No executable work may be sent to it. Only after Gates R, B, and P and a separate PASS of the new post-intake plan may one exact slice be handed to the sole Implementation task attached to `L:\dev\yakherd-web`; two Implementation writers must never target the same checkout.

## Validation and preservation

- Candidate identity and text form: PASS — 103,293 bytes; 1,956 lines; strict UTF-8; LF-only; no BOM; one terminal LF; no trailing whitespace; SHA-256 `68f444c46992b0dd31c8b84f328d85b86cc6851e1c3693ca22bc8b44aca2809a`.
- All four predecessor identities: PASS, as listed above.
- Section 11 fixture reproduction: PASS for all nine advertised byte-length/SHA-256 pairs, including U+00E9 encoded as UTF-8 `c3 a9`.
- `python -B scripts\verify_release.py`: PASS (`release_verification status=passed manifest_files=47 cache_paths=0`).
- `git diff --check`: PASS.
- Non-index candidate/audit UTF-8/LF/BOM/terminal-LF/trailing-whitespace check: PASS for both files (`git diff --no-index --check` returned the expected difference status `1` with no whitespace error; strict UTF-8, LF-only, no BOM, one terminal LF, and zero trailing-whitespace lines).
- Baseline Git state: branch `main`; HEAD `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`; upstream `origin/main`; ahead/behind `0/0`; staged paths `0`; tracked-diff paths `0`.
- Only this authorized audit path was created. The candidate, predecessors, package/release bytes, prior untracked records, Git state, product paths, release state, network/browser/DreamHost, credentials, dependencies, images, evidence skeletons, GitHub/PyPI, repository creation, hosting/DNS/staging/deployment/production/publication were not changed. `yakherd.mp4` was not read, hashed, inspected, moved, or touched.

autonomous next action: Architecture may preserve this FAIL and draft one new exact pre-intake candidate; Gate R and all product work remain parked.
