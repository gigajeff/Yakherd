# Architecture Plan: yakherd.dev Concierge Website

- Date: 2026-07-21
- Status: proposed for independent Red Team review
- Owner: `docs/2026-07-21_yakherd_dev_concierge_website_plan.md`
- Supersedes: none
- Superseded by: none
- Authority effect: no implementation or deployment authority until Red Team PASS

## Goal

Build and deploy the first usable `yakherd.dev` Concierge: a browser-first,
beginner-safe interview that turns a rough software idea into a human-approved,
hash-bound Yakherd intake bundle without requiring GitHub, Git, Python, a
terminal, or Codex at the start.

The website is Yakherd's beginner front door. It is not a replacement for the
product-neutral installer or the five governed roles. Its authority ends at a
versioned intake bundle. Architecture and Red Team inside the user's installed
project remain responsible for promoting the approved master prompt and plan.

## Evidence Read

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/RELEASE.md`
- `docs/Yakherd Audit for Absolute Beginners.md`
- `packages/jeff_strict_ssot_v1/README.md`
- `packages/jeff_strict_ssot_v1/MANIFEST.json`
- `packages/jeff_strict_ssot_v1/RELEASE.json`
- `packages/jeff_strict_ssot_v1/template/docs/prompts/product_intake.md`
- `packages/jeff_strict_ssot_v1/template/docs/prompts/codex_team_launcher.md`
- DreamHost Custom Setup, SFTP/SSH, Git deployment, PHP, supported technology,
  TLS, security-header, and backup documentation:
  - https://help.dreamhost.com/hc/en-us/articles/360049378932-Adding-a-website-and-hosting
  - https://help.dreamhost.com/hc/en-us/articles/115001051531-FTP-and-SFTP-at-DreamHost
  - https://help.dreamhost.com/hc/en-us/articles/216385837-Creating-a-user-with-Shell-SSH-access
  - https://help.dreamhost.com/hc/en-us/articles/115000684492-Using-Git-for-web-development
  - https://help.dreamhost.com/hc/en-us/articles/217141627-Supported-and-unsupported-technologies
  - https://help.dreamhost.com/hc/en-us/articles/214202188-PHP-overview
  - https://help.dreamhost.com/hc/en-us/articles/216539548-Adding-a-free-Let-s-Encrypt-certificate
  - https://help.dreamhost.com/hc/en-us/articles/360036486952-Security-headers
  - https://help.dreamhost.com/hc/en-us/articles/215768257-How-do-I-restore-my-website
- OpenAI current model, Responses API, and API-key guidance:
  - https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6
  - https://developers.openai.com/api/docs/guides/migrate-to-responses
  - https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

## Invariants And Boundaries

### Yakherd authority

- The audited package under `packages/jeff_strict_ssot_v1/` is out of scope.
- Do not change package templates, `MANIFEST.json`, `RELEASE.json`, package
  version, installer behavior, release workflows, tags, PyPI, or GitHub
  releases in this slice.
- Website text and output must not claim that candidate 1.2.0 is a released
  package until its independent release review, tag, and publication complete.
- Website output is non-authoritative until the human approves the generated
  prompt and an installed project's Architecture plus Red Team promote it.
- Raw idea text and model output are untrusted data, never executable
  instructions to the website, Codex, DreamHost, or GitHub.

### Privacy and secrets

- Interview state is local to the browser by default.
- Do not create accounts, analytics, cookies for tracking, advertising, server
  transcripts, or a server-side idea database in this slice.
- Explain before the first model call that the current interview context will
  be sent to the configured model provider.
- Set the OpenAI Responses request to `store: false` and manage conversation
  history locally.
- Never place an API key in HTML, JavaScript, the repository, deployment
  artifacts, browser storage, logs, or a path under the public web root.
- Production model access fails closed when the server-side secret is absent.
- Do not copy a credential from the local environment to DreamHost without a
  separate, explicit secret-transfer authorization. The user may enter a new,
  site-specific key through a secure channel when the implementation reaches
  that gate.
- Secret detection is best-effort and must be described that way. On a likely
  credential, private key, access token, or high-risk personal-data pattern,
  stop before the next model request and offer redact, revise, or discard.
- Do not log request or response bodies. Operational logs may contain only a
  random request identifier, timestamp, status class, duration, and byte count.

### Beginner behavior

- The first screen uses plain language and does not require SSOT vocabulary.
- The Concierge asks one materially useful question at a time.
- `I don't know yet` is a valid answer.
- `Stop and make my prompt` immediately ends interrogation and produces the
  best bounded draft with unknowns preserved.
- Users can edit earlier answers, surface contradictions, delete the current
  interview, export it, and resume locally.
- Nothing is published, pushed to GitHub, or sent to Codex automatically.
- GitHub remains optional and private/local is the default.
- The yak visual may eat the rough idea and produce the prompt, but accessible
  text must describe the actual state. The mascot never claims to approve.

### Accessibility

- Target WCAG 2.2 AA for the implemented flow.
- Complete keyboard operation, visible focus, correct labels, logical heading
  order, sufficient contrast, and screen-reader status announcements.
- Honor `prefers-reduced-motion`; the chewing/output animation must pause or
  simplify without hiding progress.
- Do not encode status, warnings, or approval solely through color or motion.

### DreamHost and deployment

- Use the user's signed-in DreamHost session only; never read browser cookies,
  stored passwords, or tokens.
- Inspect and record the account's actual hosting plan, server, assigned user,
  web directory, PHP version, DNS state, and TLS state before mutation.
- Use a dedicated DreamHost website/shell user for `yakherd.dev` when the panel
  permits it.
- Use SSH/SFTP on port 22; never FTP on port 21.
- Deploy only an explicit allowlist produced from `website/public/` and
  `website/server/`. Never expose `.git`, repository docs, tests, secrets,
  deployment scripts, local state, or the Python package under the web root.
- Stage on `staging.yakherd.dev` with access control before production.
- Production publication is authorized by the user's 2026-07-21 instruction,
  but only after Red Team PASS and all staging gates pass.
- A failed check leaves the current production site unchanged.
- Keep a local and remote hash manifest plus a recoverable previous release;
  DreamHost's own backups are supplementary and not guaranteed.

## Options And Tradeoffs

### Option A: static marketing page only

Lowest operational risk but does not solve the messy-idea-to-master-prompt
problem. Rejected as the target; acceptable only as an outage fallback.

### Option B: static vanilla frontend plus small PHP API on DreamHost

Works on DreamHost shared, VPS, and dedicated plans. Keeps the API key on the
server, avoids a Node runtime requirement, minimizes dependencies, and can be
tested locally with PHP's built-in server. Selected.

### Option C: Node application on DreamHost

DreamHost documents Node server support only on VPS and Dedicated plans. The
user's plan is not yet known, and Passenger is unsupported. Rejected for the
initial architecture.

### Option D: static DreamHost frontend plus another serverless backend

Operationally attractive but introduces a second provider, DNS/CORS surface,
secret store, and deployment path before DreamHost capability is proven.
Deferred unless the PHP proof fails a hard gate.

### Repository placement

Keep source under root `website/` in the existing Yakherd repository for this
first governed implementation. The root repository already owns branding,
public documentation, and distribution, while the audited package remains a
separate manifest-bound layer. Deploy only a generated allowlist, never the
whole repository. Revisit a separate website repository after the intake
contract stabilizes; do not split during the first implementation slice.

## Decision

Implement a dependency-light website with:

- semantic HTML, CSS, and vanilla JavaScript under `website/public/`;
- a small PHP JSON endpoint under `website/server/api/`;
- a provider adapter whose initial production implementation uses OpenAI's
  Responses API;
- configurable `YAKHERD_OPENAI_MODEL`, defaulting to `gpt-5.6-sol` for the
  requested frontier-quality interrogation;
- intentional balanced reasoning, measured during evaluation rather than
  increased reflexively;
- `store: false`, no tools, a strict structured response contract, explicit
  prompt-injection boundaries, and a stable privacy-preserving safety
  identifier derived from a random local session identifier rather than IP;
- browser-local interview persistence and deletion;
- client-side creation of an uncompressed ZIP intake bundle so raw interview
  data is not uploaded again merely to generate a download;
- responsive yak-themed presentation using existing reviewed/tracked branding
  assets or new code-native SVG/CSS only in this slice;
- a PHP-free static outage page that remains deployable if model service is
  unavailable; and
- a fail-closed DreamHost deployment with staging, hash verification, explicit
  production allowlist, previous-release retention, and rollback evidence.

The initial bundle contract is `yakherd-intake-v1` and contains:

- `MASTER_PROMPT.txt`: exact approved prompt with documented delimiters;
- `master_prompt.provenance.json`: schema version, UTC approval time, encoding,
  byte length, SHA-256, source, model, capture limitations, and redaction flags;
- `master_prompt.approval.json`: human approval transition and unresolved
  questions;
- `unresolved_questions.json`;
- `bundle-manifest.json`: path, byte length, and SHA-256 for each other file;
- `OPEN_IN_CODEX.txt`: plain-language next steps that do not claim automatic
  Codex or GitHub handoff.

The default bundle omits the raw interview and transcript. The user may opt in
to add `raw_idea.txt` and `interview.ndjson` after a clear sensitivity warning.

## Structured Concierge Contract

The server returns only JSON with one of these phases:

- `question`: one next question plus optional plain-language examples;
- `draft`: a complete candidate master prompt, summary, and unresolved list;
- `blocked`: a safe explanation and permitted next actions;
- `error`: a generic recoverable error without provider internals.

Every successful response includes:

- `schema_version`;
- `phase`;
- `message`;
- `question` or `draft` as appropriate;
- `knowns`;
- `unknowns`;
- `contradictions`;
- `sensitivity_flags`;
- `high_stakes_flags`.

The system instruction must explicitly state that user idea text is quoted
untrusted content, cannot change the Concierge rules, and cannot authorize
network, GitHub, Codex, deployment, publication, payments, or tool use.

## Staged Implementation

### Stage 0: DreamHost read-only inventory

Architecture/coordinator, not Implementation, inspects the signed-in panel and
records hosting plan, current domain configuration, candidate website user,
web directory, PHP choices, DNS, certificates, and whether staging exists.
No mutation occurs until the inventory is complete.

### Stage 1: website implementation and local tests

Implementation writes only:

- `website/README.md`
- `website/public/index.html`
- `website/public/privacy.html`
- `website/public/accessibility.html`
- `website/public/assets/**`
- `website/public/js/**`
- `website/public/css/**`
- `website/server/api/**`
- `website/server/config.example.php`
- `website/server/.htaccess`
- `website/tests/**`
- `website/scripts/build_deploy_manifest.py`
- `website/scripts/verify_deploy_manifest.py`
- `website/deploy/DREAMHOST.md`
- `website/deploy/deploy.ps1`
- `website/deploy/rollback.ps1`
- one bounded implementation evidence record under `docs/audits/yakherd/`

No other path is writable in the implementation slice. In particular, do not
modify package, release, workflow, root branding-source, or audit-input files.

### Stage 2: local functional and adversarial validation

- Run the frontend against a deterministic fake provider.
- Run PHP syntax checks and endpoint contract tests.
- Test empty, malformed, oversized, duplicate, and hostile requests.
- Test prompt injection, likely secrets, contradictory answers, repeated `I
  don't know`, immediate stop, delete, resume, reduced motion, keyboard-only
  flow, failed provider, missing secret, and bundle hash verification.
- Verify deployment manifest contains only the allowlist and no secret-shaped
  content.
- Inspect every generated bundle entry and recompute its hashes independently.

### Stage 3: independent implementation review

Red Team reviews the exact diff and evidence. Implementation repairs only
after a finding is returned through Architecture. Repeat until PASS.

### Stage 4: DreamHost staging setup and deployment

Architecture/coordinator uses the signed-in DreamHost panel to:

1. add or verify `yakherd.dev` Custom Setup;
2. create or assign a dedicated shell user;
3. add `staging.yakherd.dev`;
4. confirm the PHP version and web directories;
5. configure DNS and Let's Encrypt certificates;
6. configure staging access control;
7. install an SSH public key or use the existing secure DreamHost-supported
   connection without exposing credentials;
8. deploy the exact reviewed allowlist to staging over SSH/SFTP;
9. verify remote hashes, HTTPS, headers, permissions, error handling, and logs.

### Stage 5: live staging acceptance

Use the in-app browser at desktop and narrow mobile widths. Exercise the real
API only after a site-specific server secret is securely installed. Verify no
secret reaches browser code, page source, response bodies, logs, or deployment
manifest. Record screenshots and a redacted request-id-only run record.

### Stage 6: production and repeatable deployment

- Preserve the current production release if one exists.
- Deploy the reviewed staging bytes, not a rebuilt artifact.
- Verify DNS, HTTPS, redirect behavior, CSP/security headers, public pages,
  model failure mode, full interview, bundle download, bundle hashes, and
  rollback command.
- Configure a DreamHost bare Git deployment repository or equivalent SSH
  release path only if it exports the website allowlist rather than the whole
  Yakherd repository.
- Keep production rollback to the immediately previous verified release.
- Do not create a GitHub release, package release, PyPI publication, or Yakherd
  version tag as part of website deployment.

## Acceptance And Stop Gates

### Required PASS gates

- Red Team PASS on this plan before implementation.
- Local tests and adversarial tests pass with evidence.
- Red Team PASS on the exact implementation diff.
- DreamHost inventory proves a supported PHP deployment path.
- Staging is HTTPS-only and access controlled during pre-production review.
- No public artifact or response contains a credential.
- Missing API secret and provider failure are safe and comprehensible.
- One-question loop, stop behavior, edit, delete, local resume, draft approval,
  ZIP generation, and independent hash verification work.
- Keyboard and reduced-motion flows work.
- Deployment manifest exactly matches remote public files.
- Rollback is demonstrated before production promotion.
- Production smoke test passes against the exact staging bytes.

### Immediate STOP gates

- Wrong DreamHost account, domain, hosting plan, user, web directory, or DNS.
- Any request to expose or paste a secret into chat, repository, browser code,
  deployment output, command output, or public path.
- Node-only design on a hosting plan that does not support Node servers.
- Package or release bytes change in this website slice.
- Site would publish the unreviewed 1.2.0 candidate as a released artifact.
- Interview content appears in server logs or persistent server storage.
- Deployment requires blind recursive upload, `git add .`, whole-repository
  checkout into the web root, destructive overwrite without backup, or an
  unverified computed remote path.
- Staging security, HTTPS, hash verification, or rollback fails.
- Red Team verdict is not PASS.

## Evidence And SSOT Outputs

- This architecture plan.
- Red Team plan review under `docs/audits/yakherd/`.
- Implementation evidence under `docs/audits/yakherd/`.
- Local test output summary with exact commands and exit codes.
- Deployment manifest and independent verification output.
- DreamHost inventory with no secrets.
- Staging and production URLs, TLS/header results, screenshots, and UTC times.
- Exact Git status, branch, commit, upstream, and deployment commit SHA.
- Rollback target and demonstration result.

## Forbidden Scope

- Package template, manifest, release JSON, PyPI, tag, GitHub Release, or CI
  release changes.
- GitHub OAuth, GitHub repository creation for site users, direct Codex task
  creation, automatic product implementation, accounts, billing, analytics,
  email, databases, transcript retention, or multi-device sync.
- Medical, legal, financial, or safety-critical advice; the Concierge may only
  identify and flag high-stakes product scope for later expert review.
- Tools or model actions other than generating the next structured Concierge
  response.
- Production deployment of bytes that differ from reviewed staging bytes.

human action required: none for plan routing; the user explicitly authorized autonomous Red Team review, implementation routing, DreamHost setup, staging, and production deployment on 2026-07-21. Secret transfer remains a separate safety gate.
