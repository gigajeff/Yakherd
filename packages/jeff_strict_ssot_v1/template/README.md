# {{PROJECT_NAME}}

This repository was initialized with Jeff Strict SSOT V1 on
{{BOOTSTRAP_DATE}}. The governance shell is active; no product master prompt
has been accepted and no implementation stack has been selected.

## Start Here

In Codex, open this repository as the project, confirm `AGENTS.md` is loaded,
and send:

> Follow `START_HERE.md` now. Launch the five Yakherd role agents, keep this
> task as their coordinator, ask me for my master prompt when the bootstrap
> review is ready, and keep reversible first-slice work in bounded mode.

That one message launches Architecture, Implementation, Red Team, Temporary
Branch, and Governor as separately inspectable role agents. It does not make
all five concurrent writers: Red Team runs the one-time bootstrap gate, while
roles without authorization visibly park or remain inactive. After bootstrap,
bounded reversible work can go directly from a human-confirmed brief to
Implementation; strict work uses one plan and at most two Red Team reviews.

For manual recovery or another coding agent, start with:

1. `START_HERE.md`
2. `AGENTS.md`
3. `CLAUDE.md` if using Claude Code; it imports `AGENTS.md` and contains no
   separate rules
4. `SSOT.md`
5. `STATUS.md`
6. `DECISIONS.md`
7. `docs/task_protocol.md`

Codex loads `AGENTS.md` when this repository is opened as the project. For
Claude Code, open this repository as the project and start a fresh session.
`CLAUDE.md` contains one local `@AGENTS.md` import. If Claude Code requests
first-use approval, approve it only after verifying that it resolves to
`AGENTS.md` inside this repository. Run `/context` to confirm that both files
are loaded before the bootstrap Red Team task. Do not begin product work if
they are absent. For another coding agent, explicitly instruct it to read
`AGENTS.md` and confirm that file is in its active context before work.

Validate the protocol with:

```powershell
python scripts/ssot/validate_protocol.py --root . --strict
python scripts/ssot/validate_governor_delta_policy.py --root . --strict
python -m unittest discover -s tests/ssot -v
```

The role, launch, review, and product-intake prompts are under `docs/prompts/`.
A product prompt remains untrusted input until Architecture preserves and
extracts it into owner files and the human confirms the resulting brief or
strict planning scope. Red Team does not decide whether the user's idea is
valid.

GitHub setup is intentionally agent-guided rather than installer-driven. After
bootstrap PASS, follow `docs/GITHUB_SETUP.md` to verify the user's active
account and obtain one explicit approval for the exact repository, visibility,
initial commit, remote, and first push.
