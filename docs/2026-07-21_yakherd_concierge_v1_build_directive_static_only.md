# YAKHERD CONCIERGE V1 — BUILD DIRECTIVE (STATIC-ONLY)

Document date: 21 July 2026
Author of record: Jeffrey Martin (gigajeff)
Status: Build instruction. Under Yakherd's own rules, chat and directives are direction,
not durable authority. This document becomes authoritative only after it is supplied
through product intake, converted by Architecture into a bounded plan, and independently
PASSed by Red Team. Nothing here bypasses that chain.

---

## 0. The directive

Build exactly one thing: the **Yakherd Concierge**, a website at yakherd.dev that takes a
person from a rough software idea, through a deterministic guided interview, to an edited
and explicitly approved master prompt, and produces the five-file deterministic handoff
bundle — **implemented as a fully static website with zero server-side code, zero network
calls at runtime, and zero third-party resources.**

Do not build anything else. The hosted model relay, the repository bundle export, the
local runner, accounts, the workbench, and all execution features are explicitly out of
scope for this build. They are listed in §16 as deferred extension points that this build
must not preclude but must not implement.

---

## 1. Scope statement

**In scope (all of it, nothing more):**

1. A static multi-page website: home, Concierge, next-steps guide, privacy, troubleshooting.
2. A deterministic, client-side guided interview (no model, no AI, no network).
3. A prompt draft assembled mechanically from interview answers.
4. An edit-and-approve flow where the user owns and explicitly approves the final prompt text.
5. Client-side generation of the five-file deterministic handoff bundle as a Store-only ZIP.
6. Client-side likely-secret detection before download.
7. A client-side high-stakes gate (medical / legal / financial / safety-critical flag).
8. Exact, honest, OS-specific instructions for starting Yakherd on the user's own machine.

The build is complete when §15 (Definition of Done) is satisfied. Any feature not listed
above is out of scope regardless of how small it seems.

---

## 2. The static-only constraint (S-rules)

"As static as possible" is a hard requirement, not a preference:

- **S-01** No server-side code of any kind. No PHP, no serverless/edge functions, no API
  endpoints, no form handlers. The host serves committed bytes and nothing else.
- **S-02** Zero network requests at runtime beyond the site's own first-party static
  assets. After page load, a complete Concierge run must generate **zero** additional
  requests to any origin, including the site's own.
- **S-03** No third-party resources: no CDNs, remote fonts, analytics, tag managers,
  embeds, or cross-origin iframes.
- **S-04** No build step. Files are authored, committed, and served as-is. No npm, no
  bundler, no transpiler, no build-time downloads.
- **S-05** No cookies, fingerprinting, service worker, Cache API, background sync, or beacons.
- **S-06** All computation — interview logic, prompt assembly, hashing, ZIP construction,
  secret detection — happens in the user's browser.
- **S-07** The entire site must run unmodified from a dumb local static server
  (`python -m http.server`) with behavior identical to production.
- **S-08** The only permitted host-side configuration is a static headers/redirects file
  (e.g., `_headers`) for security headers and HTTPS enforcement.

If any requirement in this document appears to force a violation of S-01…S-08, stop and
escalate to Jeff. Do not quietly add a backend.

---

## 3. Explicit exclusions (X-rules)

The site must not, and must visibly state that it does not:

- **X-01** Install Yakherd.
- **X-02** Create a GitHub repository or touch Git in any way.
- **X-03** Launch Codex, Claude Code, or any agent task.
- **X-04** Execute, build, test, preview, or deploy any product code.
- **X-05** Call any model or AI service. There is no interview AI in this build; the
  interview is a fixed, deterministic question flow.
- **X-06** Create accounts, sessions, or logins. The site is fully anonymous.
- **X-07** Transmit the user's idea, answers, or prompt anywhere. Nothing leaves the
  browser, ever, in this build.
- **X-08** Confer approval or authority. Approval is the user's own action; Architecture
  and Red Team review still happen in the repository afterward.
- **X-09** Include yakherd.mp4 or any video.
- **X-10** Collect client-side analytics or telemetry. Aggregate, cookie-less host-level
  request counts are the only permitted measurement.

---

## 4. Repository and hosting (R-rules)

- **R-01** The website lives in a **separate repository** (`yakherd-web`), never inside the
  audited `gigajeff/Yakherd` engine repo. Website changes must never invalidate the
  engine's reviewed snapshot.
- **R-02** License: Apache-2.0 by default (Jeff may override; record the decision).
- **R-03** Hosting: any competent static host. Recommended: Cloudflare Pages (or Netlify).
  DreamHost Shared Apache is retired for this application; DNS stays wherever Jeff prefers.
- **R-04** Staging is a second static preview URL of the same committed bytes. Deployment
  is an upload of committed bytes — nothing is generated at deploy time.
- **R-05** The DreamHost capability procedure is not restarted, referenced, or depended on.

---

## 5. Technology rules (T-rules)

- **T-01** Semantic HTML5, one hand-authored CSS file, vanilla JavaScript (ES2020 or
  earlier). No frameworks, no fetched libraries.
- **T-02** Any algorithm beyond the browser platform (CRC-32 for ZIP entries) is written
  in-repo, small, commented, and reviewed. No vendored third-party bundles.
- **T-03** SHA-256 uses WebCrypto (`crypto.subtle.digest`). The site requires a secure
  context (HTTPS or localhost); on an insecure context it detects this and shows a
  plain-language message. `file://` is not a supported target.
- **T-04** System font stack only. The only raster image permitted is the tracked
  `yakherd2.png` (SHA-256 `e45c1c54…7a4383`) plus hand-authored SVG/CSS.
- **T-05** All user-entered text goes through text-only DOM sinks (`textContent`), never
  `innerHTML`; no Markdown/HTML interpretation of anything the user typed.
- **T-06** Soft budget: total JS under ~150 KB unminified. Growth past that signals scope creep.
- **T-07** Informational pages must be fully readable with JavaScript disabled. The
  Concierge page, with JS disabled, shows a notice plus a plain, copyable static
  master-prompt template so a no-JS visitor still leaves with something useful.

---

## 6. Pages and journey

1. **Home** — headline: "Turn your rough software idea into a build-ready plan." Sub-line:
   free, private, nothing leaves your browser, no account, no AI call in this version.
   Primary CTA: "Feed the yak your idea." Secondary: "How it works" / GitHub.
2. **Concierge** — interview → draft → edit → approve → download (§7–§10).
3. **Next steps** — OS-specific instructions (Windows, macOS, Linux) for installing the
   pinned public Yakherd release and handing over the bundle.
4. **Privacy** — one screen, plain language (§11).
5. **Troubleshooting** — honest failure modes: JS disabled, insecure context, download
   blocked, partial role launch on the local side.

---

## 7. Interview specification (I-rules — deterministic, no model)

- **I-01** The interview is a fixed, versioned question tree in one committed JSON file
  (`interview.v1.json`). No question is generated at runtime.
- **I-02** One question per screen. Topics, in order: what the product is; who it is for;
  the 3–7 core user actions; data it stores; platforms/targets; hard constraints; explicit
  non-goals; success criteria; known risks and open questions; high-stakes screening (§10).
- **I-03** Every question is skippable. A skipped or "I don't know" answer is recorded
  mechanically as **UNKNOWN** — never invented, never filled in.
- **I-04** "Make my prompt now" is visible on every screen and jumps straight to the draft
  with everything unanswered listed as UNKNOWN.
- **I-05** Contradiction handling is honest about having no AI: at the review step the tool
  shows all answers side by side and asks the user to mark any pair that conflicts.
  User-marked conflicts become **CONTRADICTION** entries carried verbatim into the prompt.
  The site never claims automatic contradiction detection.
- **I-06** The review step presents four labeled sections before drafting: KNOWNS,
  UNKNOWNS, ASSUMPTIONS (only ones the user explicitly typed), CONTRADICTIONS.
- **I-07** The v1 tree contains at most 15 questions. Stopping is always the user's choice.

---

## 8. Draft, edit, approval (D-rules)

- **D-01** The draft master prompt is assembled by fixed string templates from the answers —
  mechanical substitution only, from a versioned in-repo template (`prompt_template.v1.txt`).
- **D-02** The draft opens in a plain editable textarea. The final prompt is whatever bytes
  are in that editor — the user's words, not the tool's.
- **D-03** Approval is an explicit, separate action: a checkbox with the fixed statement
  "I wrote or reviewed this prompt and I approve this exact text," plus an Approve button.
  Approval locks the text; editing again revokes approval and requires re-approval.
- **D-04** Raw answers, generated draft, and user-approved prompt stay visibly distinct at
  all times. Only the approved prompt enters the bundle.

---

## 9. The deterministic five-file bundle (B-rules)

The download is one ZIP containing exactly five files, in this fixed order:
`MASTER_PROMPT.txt`, `MASTER_PROMPT_HANDOFF.txt`, `APPROVAL.json`,
`BUNDLE_MANIFEST.json`, `OPEN_IN_CODEX.txt`.

- **B-01** `MASTER_PROMPT.txt` is the approved prompt bytes exactly as approved: UTF-8, no
  BOM, no normalization, line endings preserved. Byte length and SHA-256 are computed over
  these exact bytes.
- **B-02** `MASTER_PROMPT_HANDOFF.txt` wraps those same bytes in the exact delimiters and
  metadata required by the installed `product_intake.md` contract of the **pinned public
  Yakherd release** (B-08). Delimiters are copied from that committed file — never
  invented, paraphrased, or "improved." The bridge test (A-04) verifies this.
- **B-03** `APPROVAL.json` is canonical JSON: UTF-8, LF, lexicographically sorted keys, no
  insignificant whitespace, single trailing LF. Fields: `schema_version`, `tool`
  ("yakherd-concierge"), `tool_version`, `generated_at` (ISO-8601 UTC, client clock) with
  `timestamp_source: "client"` (never presented as trusted time), `prompt_sha256`,
  `prompt_bytes`, `approved: true`, `approval_statement` (the fixed D-03 string),
  `prompt_edited_by_user`, `high_stakes_flagged`, `high_stakes_acknowledged`,
  `yakherd_target_release`.
- **B-04** `BUNDLE_MANIFEST.json` (same canonical-JSON rules) lists, for each of the other
  four files in fixed order: `path`, `bytes`, `sha256`; plus `bundle_schema_version` and
  `yakherd_target_release`.
- **B-05** `OPEN_IN_CODEX.txt` gives the exact next steps: install the pinned Yakherd
  release per its README; start the five roles per START_HERE.md; wait for the bootstrap
  Red Team PASS; then hand `MASTER_PROMPT_HANDOFF.txt` to Architecture. It states plainly
  what will **not** happen automatically.
- **B-06** ZIP construction: Store-only (method 0), fixed entry order, fixed DOS timestamp
  (1980-01-01 00:00:00) on every entry, fixed version-made-by and external attributes,
  UTF-8 filename flag, no extra fields, no data descriptors, CRC-32 per entry via the
  reviewed in-repo implementation.
- **B-07** Determinism contract: given identical inputs — prompt bytes, answers, the
  `generated_at` string, and `tool_version` — the ZIP is **byte-identical** across
  browsers and operating systems. The test harness injects a fixed `generated_at`.
- **B-08** `yakherd_target_release` pins the newest **publicly released** Yakherd tag at
  build time (currently v1.0.0 unless a newer public tag exists at ship time). Local,
  unreleased engine versions are never referenced.
- **B-09** ZIP filename: `yakherd_intake_<first 12 hex of prompt_sha256>.zip`.

---

## 10. Secret detection and high-stakes gate (G-rules)

- **G-01** Before download, a client-side scan flags likely secrets: private-key headers,
  high-entropy token shapes, well-known key prefixes (`sk-`, `ghp_`, `AKIA`, …),
  password-adjacent phrases. On a hit: show the exact flagged spans; offer **Edit**
  (default) or **Download anyway** with explicit acknowledgment. Patterns are versioned in-repo.
- **G-02** The high-stakes screening question plus a keyword check triggers a
  model-independent warning: Yakherd and its agents are not suitable for building
  regulated or safety-critical products without qualified human experts, and this bundle
  does not change that. Download is blocked until acknowledged; the acknowledgment is
  recorded in `APPROVAL.json`.
- **G-03** Neither check phones home. Both are best-effort and are described as best-effort
  in the UI.

---

## 11. Privacy and storage (P-rules)

- **P-01** Default: memory-only. Closing the tab loses the session, and the UI says so.
- **P-02** Optional "Save in this browser": localStorage/IndexedDB with 7-day expiry,
  read-after-write verification before claiming success, per-session delete, delete-all.
- **P-03** The privacy page states, truthfully and briefly: nothing you type leaves your
  browser; no account, no cookie, no analytics, no AI call; deleting local data cannot
  recall files you already downloaded.
- **P-04** Because of the S-rules, the privacy story is verifiable by anyone with DevTools
  open — the site should invite exactly that inspection.

---

## 12. Honesty requirements (H-rules)

- **H-01** The site must nowhere claim, imply, or animate that it builds, approves, or
  ships software. Required disclaimer on the Concierge and download pages: "This tool
  creates a starting prompt and a handoff file. It does not install Yakherd, run any code,
  or approve anything. Your Yakherd project's Architecture and Red Team roles still review
  everything."
- **H-02** No mascot animation or visual that implies authority, approval, or completion.
- **H-03** All AI-related copy must reflect X-05: this version contains no AI. The future
  assisted interview may be mentioned only as clearly labeled "planned."

---

## 13. Accessibility and security

- **A11Y** WCAG 2.2 AA: full keyboard operation, visible focus, screen-reader
  announcements for step changes and errors, reflow at 320 px, contrast ≥ 4.5:1,
  forced-colors and reduced-motion support, plain-language errors.
- **SEC** Strict CSP (`default-src 'none'; script-src 'self'; style-src 'self';
  img-src 'self'`) via the static headers file, mirrored in a meta tag;
  `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`,
  `frame-ancestors 'none'`. No inline event handlers.

---

## 14. Testing and acceptance gates (A-rules)

- **A-01 Determinism:** identical inputs (B-07) produce byte-identical ZIPs on Chromium,
  Firefox, and WebKit, on at least two operating systems.
- **A-02 Zero-network:** automated check confirms zero non-first-party requests on load
  and **zero requests of any kind** during a complete Concierge run after load.
- **A-03 Extraction:** the ZIP extracts with OS defaults on Windows, macOS, Linux; hashes
  in `BUNDLE_MANIFEST.json` match extracted files.
- **A-04 Bridge:** `MASTER_PROMPT_HANDOFF.txt` is accepted by the exact committed
  `product_intake.md` contract of the pinned public release in a fresh Yakherd
  installation, with byte length and SHA-256 matching.
- **A-05 Secret/high-stakes:** planted-secret and high-stakes fixtures all trigger; clean
  fixtures produce no false block.
- **A-06 Accessibility:** keyboard-only and screen-reader walkthrough of the full journey;
  automated scan with zero AA violations.
- **A-07 No-JS:** informational pages readable; Concierge no-JS fallback (T-07) present.
- **A-08 Local parity:** S-07 verified against `python -m http.server`.
- **A-09 Honesty:** every page reviewed against §12; no claim of installation, execution,
  approval, or AI.

---

## 15. Definition of done

All A-gates pass with recorded evidence; the site is live on the chosen static host and on
staging from identical committed bytes; B-08 pins the newest public tag; and an
independent Red Team review of the **implementation** (not just the plan) has PASSed.
A plan-level PASS is not completion.

---

## 16. Deferred extension points — do not build, do not preclude

- The assisted (model-backed) interview via one narrow relay endpoint. Keep question flow,
  drafting, and bundle generation cleanly separated so a relay can later feed the same
  draft pipeline — but no relay code, endpoint stubs, or provider references ship now.
- The complete governed repository bundle (Option F), the local runner, private GitHub
  backup, accounts, and any workbench.
- Any DreamHost work.

---

## 17. Stop conditions

Stop and escalate to Jeff, rather than improvising, if: (1) any requirement seems to
demand server code, a third-party script, or a runtime network call; (2) the
`product_intake.md` contract of the pinned public release cannot be satisfied byte-exactly;
(3) determinism (A-01) cannot be achieved; (4) the honest no-AI interview proves so weak in
novice testing that the team is tempted to fake intelligence client-side — in that case
the answer is the deferred relay in §16, never a pretend AI.
