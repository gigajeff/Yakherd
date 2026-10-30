MASTER PROMPT START

# Yakherd Concierge V1 — bounded build directive

You own the end-to-end construction of the first useful Yakherd Concierge website at yakherd.dev.

Do not merely propose another architecture plan. Build the working local website.

## 1. Product outcome

Create a charming, beginner-friendly website that turns a rough software idea into a clear, editable master prompt and then guides the user into Yakherd 1.3.0.

The visual theme is:

A friendly yak eats the user’s rough idea and poops out a polished master prompt.

Make it playful, memorable, and tasteful. The joke must not obscure usability or imply that Yakherd has already built, validated, or approved the resulting software.

The principal landing-page message is:

“Turn your rough software idea into a build-ready master prompt.”

Primary CTA:

“Feed the yak your idea”

The target user has never used GitHub, Yakherd, or an agentic development workflow.

## 2. Anti-doom-loop operating instructions

This local website build is BOUNDED work under the Yakherd 1.3.0 task protocol.

Therefore:

- Do not create an Architecture mega-plan.
- Do not ask Red Team to review this prompt or a plan.
- Do not generate V2/V3/V4 plan candidates.
- Do not create evidence schemas, evidence skeletons, candidate hashes, deterministic ZIP protocols, or release-preparation machinery.
- Do not reuse the abandoned Yakherd concierge plans or their audits.
- Do not allow Red Team to invent new product requirements.
- Only P0/P1 findings may block.
- P2/P3 findings are advisory.
- Review the implemented site—not successive descriptions of the future site.
- Use one Implementation writer only.
- Never run two implementation writers against the same checkout.
- Use at most one initial final review and one recheck.
- If both fail, stop and ask the human to rescope or accept the remaining risk.
- Spend effort producing and testing the working artifact, not proving that plans describing it are perfect.

## 3. Model and effort routing

Choose the model and reasoning effort separately for every delegated turn.

Use:

- Luna medium for mechanical work.
- Terra medium/high for routine research and implementation.
- Sol high/xhigh for architecture, difficult design decisions, or difficult debugging.
- Sol ultra only for the final independent security, deployment, parser, or release gate.
- Do not use Ultra merely because it is available.
- Do not spawn more than one Ultra agent without asking the user.

Implementation and Red Team must also choose their own model and effort using these rules.

## 4. Repository and write boundary

Create and work only in a separate website repository:

L:\dev\yakherd-web

Expected future GitHub repository:

gigajeff/yakherd-web

Do not add the website to the Yakherd package repository.

The Yakherd repository may be read only to confirm the public Yakherd 1.3.0 user contract, commands, delimiter format, branding, and START_HERE behavior.

Do not read or incorporate the abandoned untracked concierge plan/audit files or yakherd.mp4.

Local repository creation and local implementation are authorized now.

Do not create the remote GitHub repository, deploy, publish, alter DNS, or mutate DreamHost during the local-build phase. Stop at one concise human checkpoint after presenting the completed local site.

## 5. Technical boundary

V1 must be genuinely static:

- Semantic HTML
- Hand-authored CSS
- Vanilla JavaScript
- Original local SVG/CSS artwork
- No framework
- No npm dependency tree
- No build step
- No server-side code
- No Cloudflare Worker or Pages Function
- No model/API calls
- No database
- No user accounts
- No GitHub OAuth
- No analytics
- No advertising
- No cookies
- No third-party fonts, scripts, images, CDNs, or trackers
- No service worker
- No localStorage, sessionStorage, or IndexedDB
- No transmission of user-entered content

Hold answers only in ordinary page memory.

Use `textContent`, form `value`, and safe DOM construction for user-controlled content. Do not insert user content through `innerHTML`.

The website may accurately say:

“This version does not save your answers or send them to a Yakherd server. Your browser may retain page state according to its own settings.”

Do not claim that closing the tab cryptographically erases or proves deletion of browser state.

## 6. Hosting direction

The eventual host is Cloudflare Pages, not DreamHost web hosting.

The intended production arrangement is:

- Public GitHub repository: `gigajeff/yakherd-web`
- Cloudflare Pages connected to the repository
- Production branch: `main`
- Static output directory containing the committed site
- No build step; use Cloudflare’s supported no-build configuration
- Custom domains: `yakherd.dev` and `www.yakherd.dev`
- HTTPS enabled
- DreamHost may remain the domain registrar
- DNS may later move to Cloudflare as a separately reviewed deployment action

Include a `_headers` file suitable for a static Pages site, with an effective restrictive CSP and ordinary security headers. Do not add security machinery that requires a backend.

Use the applicable Cloudflare skills and current official documentation during the later deployment phase.

## 7. Beginner journey

Build this complete journey.

### A. Welcome

Explain, in ordinary language:

- What Yakherd Concierge does
- That it is free
- That no account is required
- That V1 does not use AI while the user is filling out the form
- That answers are not sent to a Yakherd server
- Approximately how long the process takes
- That the result is a starting prompt, not a guarantee that the idea is safe or feasible

### B. Rough idea

Start with one generous textarea:

“What would you like to build?”

Provide a friendly example, but do not prepopulate the answer.

Warn users not to paste passwords, API keys, private keys, medical records, financial account data, or other secrets.

### C. Progressive interview

Ask no more than twelve short, plain-language questions, one manageable step at a time.

Cover:

1. What is the idea?
2. Who is it for?
3. What problem does it solve?
4. What are the most important things the user should be able to do?
5. Where should it run: web, desktop, phone, command line, or unsure?
6. What information does it need to handle?
7. Are there important constraints?
8. What should the first version deliberately not do?
9. What would make the first version successful?
10. Are there safety, privacy, financial, medical, legal, or other high-stakes concerns?
11. What remains unknown?
12. Is there anything else the builder should know?

Every question must permit:

- A normal answer
- “I’m not sure”
- Skip

Map skipped or uncertain information honestly to `UNKNOWN`. Never invent an answer.

Allow the user to go backward and edit prior answers.

Provide an optional repeatable “Add another detail” field before generation. The user decides when to stop.

Always provide a clear “Make my prompt now” action.

### D. Prompt generation

Generate the master prompt locally and deterministically from the answers.

The prompt should contain clear sections for:

- Role
- Product objective
- Intended users
- Problem
- Core user journey
- Functional requirements
- Platform
- Data and privacy
- Constraints
- Non-goals
- Success criteria
- Unknowns and assumptions
- Risks and high-stakes considerations
- First bounded implementation slice
- Definition of Done

Do not pretend unknown information is known.

Do not generate architecture-specific requirements that the user did not request.

### E. Review and approval

Display the complete generated prompt in an editable textarea.

The user must be able to edit it freely.

Include a checkbox such as:

“I have reviewed this prompt and it represents what I currently want to build.”

Editing the prompt after approval must clear the approval checkbox.

Unchecking approval must disable the approved-copy state.

Approval means only that the text reflects the user’s intent. It does not mean Yakherd certifies the product.

### F. Copy and download

After approval, provide:

- “Copy master prompt”
- “Download MASTER_PROMPT.txt”
- “Copy for Yakherd”

The copied and downloaded master-prompt content must match the reviewed textarea exactly.

“Copy for Yakherd” must use this exact envelope:

MASTER PROMPT START
<the reviewed master prompt>
MASTER PROMPT END

Do not add extra content inside that envelope.

Do not create ZIP files, JSON manifests, hashes, receipts, or evidence packages in V1.

### G. Start building with Yakherd

After prompt creation, present an absolute-beginner next-steps page.

It must explain:

1. Install the pinned public release:

   python -m pip install yakherd==1.3.0

2. Preview a fresh project installation with `yakherd init --dry-run`.

3. Install into a new or empty project folder with `yakherd init`.

4. Open that generated folder as the Codex project.

5. Send Codex the following explicit request:

   Follow START_HERE.md now. Launch the five Yakherd role agents, keep this task as their coordinator, ask me for my master prompt when the bootstrap review is ready, and keep reversible first-slice work in bounded mode.

6. When Architecture asks for the master prompt, paste the exact “Copy for Yakherd” output.

Explain the five roles simply:

- Architecture clarifies the product and bounds the work.
- Implementation writes the product.
- Red Team checks bootstrap and genuinely strict changes.
- Temporary Branch performs isolated experiments when requested.
- Governor checks for drift when separately activated.

Explain that task creation is not the same as all five agents doing work simultaneously.

Provide separate copyable command examples for Windows PowerShell and macOS/Linux. Confirm exact commands against the public Yakherd 1.3.0 documentation before shipping them.

Include direct links to:

- https://github.com/gigajeff/Yakherd/releases/tag/v1.3.0
- https://pypi.org/project/yakherd/1.3.0/

## 8. Visual direction

Create an original, cohesive visual identity.

Use:

- A warm natural palette
- A friendly yak character
- Large readable typography
- Clear progress
- Generous spacing
- Mobile-first responsive layout
- Small moments of humor
- A simple animation in which an idea card is eaten and a prompt card emerges

The animation must:

- Never block completion
- Work without sound
- Respect `prefers-reduced-motion`
- Have a useful static reduced-motion state
- Not flash
- Not interfere with screen readers or keyboard navigation

Do not fetch external assets. Prefer accessible inline SVG and CSS.

The site should feel deliberately designed, not like a generic generated dashboard.

## 9. Accessibility and resilience

Implement:

- Semantic headings and landmarks
- Proper labels and instructions
- Full keyboard navigation
- Visible focus
- Logical focus movement between interview steps
- Screen-reader announcements for step changes, errors, copy success, and prompt generation
- Sufficient color contrast
- Touch-friendly controls
- Reduced-motion support
- Useful validation errors
- A basic informational fallback when JavaScript is unavailable

Do not claim formal WCAG certification. Test the concrete implemented flow for obvious accessibility failures.

## 10. Practical verification

Test the implemented artifact, not hypothetical future implementations.

At minimum verify:

- It runs from a simple local static HTTP server.
- The complete beginner flow works.
- Back/forward editing works.
- Skip and “I’m not sure” produce `UNKNOWN`.
- Prompt generation is deterministic for identical answers.
- Generated text renders safely.
- Editing after approval revokes approval.
- Copy and downloaded TXT exactly match the reviewed prompt.
- The Yakherd envelope uses the exact delimiters.
- Text between the delimiters round-trips without alteration.
- The site does not persist form answers through web-storage APIs.
- No user-entered content is transmitted.
- Runtime observation shows no analytics, model, or third-party requests.
- All shipped assets are local or same-origin.
- Keyboard navigation works.
- A narrow mobile viewport works.
- Reduced-motion mode works.
- There are no obvious console errors.
- `git diff --check` passes.
- No secrets or machine-local files are included.

A source scan plus a focused browser request observation is sufficient for the static privacy boundary. Do not build an exhaustive theorem prover for all possible JavaScript behavior.

## 11. Deliverables

Produce a small, understandable repository containing approximately:

- Static site files
- Local artwork
- `_headers`
- README with local run instructions
- A modest automated test suite for the prompt assembler and state transitions
- Any tiny test helper required to run those tests
- No generated dependency directories

Keep the structure simple enough for a beginner to understand.

## 12. Review and publication boundary

Complete the local implementation and verification first.

Then present one concise checkpoint containing:

- What was built
- Repository path
- File inventory
- Test results
- Screenshots or local preview
- Known limitations
- Confirmation that the adaptive AI interview, GitHub OAuth, accounts, persistence, and backend remain deferred
- Proposed exact GitHub publication steps
- Proposed exact Cloudflare Pages and DNS steps

Do not create the remote repository, push, deploy, publish, or alter DNS until the user approves that checkpoint.

After approval:

- Use one independent final review of the actual implementation and deployment delta.
- Only P0/P1 findings block.
- Permit one recheck maximum.
- Then create the public repository, deploy to Cloudflare Pages, attach the domain, verify HTTPS/security headers/live behavior, and report the final URLs.

## 13. Explicitly deferred scope

Do not add any of the following to V1:

- Adaptive frontier-model interrogation
- OpenAI or other model APIs
- Accounts
- Saved projects
- Cloud synchronization
- GitHub OAuth
- Automatic GitHub project creation
- Direct Codex API integration
- Automatic creation of Codex tasks from the webpage
- Backend secret scanning
- Email
- Payments
- Analytics
- A CMS
- Blog infrastructure
- Internationalization machinery
- Service workers or offline caching
- Deterministic ZIP bundles
- Cryptographic evidence receipts
- DreamHost hosting
- A general-purpose Yakherd operating system

These can be evaluated only after the static concierge is live and observed in use.

Start now. Lead with a working result, not governance paperwork.

MASTER PROMPT END
