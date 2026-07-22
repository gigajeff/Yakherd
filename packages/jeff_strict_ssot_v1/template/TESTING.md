# Testing

Status: protocol tests only until product intake is confirmed.

Current required checks:

```powershell
python -B scripts/ssot/validate_protocol.py --root . --strict
python -B scripts/ssot/validate_governor_delta_policy.py --root . --strict
python -B -m unittest discover -s tests/ssot -v
```

Product tests and fixtures follow the confirmed Definition of Done. Strict
Architecture plans define any additional performance, release, or deployment
gates required by their actual authorized slice.

Protocol validation proves repository-contract consistency only. It is not
evidence that future product behavior is correct.
