# {{PROJECT_NAME}}

This repository was initialized with Jeff Strict SSOT V1 on
{{BOOTSTRAP_DATE}}. The governance shell is active; no product master prompt
has been accepted and no implementation stack has been selected.

Start with:

1. `AGENTS.md`
2. `SSOT.md`
3. `STATUS.md`
4. `DECISIONS.md`
5. `docs/task_protocol.md`

Validate the protocol with:

```powershell
python scripts/ssot/validate_protocol.py --root . --strict
python scripts/ssot/validate_governor_delta_policy.py --root . --strict
python -m unittest discover -s tests/ssot -v
```

The five task prompts are under `docs/prompts/`. A product prompt remains
untrusted input until Architecture extracts it into owner files and Red Team
reviews that extraction.
