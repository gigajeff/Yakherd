# {{PROJECT_NAME}}

This repository was initialized with Jeff Strict SSOT V1 on
{{BOOTSTRAP_DATE}}. The governance shell is active; no product master prompt
has been accepted and no implementation stack has been selected.

Start with:

1. `AGENTS.md`
2. `CLAUDE.md` if using Claude Code; it imports `AGENTS.md` and contains no
   separate rules
3. `SSOT.md`
4. `STATUS.md`
5. `DECISIONS.md`
6. `docs/task_protocol.md`

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

The five task prompts are under `docs/prompts/`. A product prompt remains
untrusted input until Architecture extracts it into owner files and Red Team
reviews that extraction.
