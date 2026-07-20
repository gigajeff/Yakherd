# Testing

Status: protocol tests only until product intake is reviewed.

Current required checks:

```powershell
python -B scripts/ssot/validate_protocol.py --root . --strict
python -B scripts/ssot/validate_governor_delta_policy.py --root . --strict
python -B -m unittest discover -s tests/ssot -v
```

Product tests, fixtures, performance gates, release checks, and deployment
checks must be defined by Architecture after requirements are accepted.

Protocol validation proves repository-contract consistency only. It is not
evidence that future product behavior is correct.
