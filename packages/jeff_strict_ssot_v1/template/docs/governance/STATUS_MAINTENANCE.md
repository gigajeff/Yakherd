# STATUS.md Maintenance Contract

Status: current product-neutral governance contract.

`STATUS.md` is a compact current-state index, not a diary and never the sole
owner of a durable result.

## Limits

- Target: 80 lines or fewer.
- Hard maximum: 120 lines and 32,768 UTF-8 bytes.
- Exactly one bold dated current-state entry.
- Stable fields are updated in place.

Crossing a limit is an error. Move detail to its real owner and link it; do not
delete evidence merely to satisfy the cap.

## Update Order

1. Promote the durable result to its real owner and mode-appropriate evidence.
2. Replace the affected `STATUS.md` field/section in place.
3. Remove stale summary prose only after its owner/evidence path resolves.
4. Preserve blockers, next authorization, forbidden actions, release state,
   Git visibility, and archive state explicitly.
5. Run the pure protocol validator.

## Mature Overflow

When a mature status exceeds either hard limit:

1. preserve its exact bytes under `docs/status_history/`;
2. record SHA-256, byte/line counts, and dated-entry ranges in an index JSON;
3. migrate live citations to owner paths or immutable archive ranges;
4. replace status with compact current state;
5. validate twice; and
6. allow rollback only when both archive and expected-current hashes match.

The migration command requires the reviewed current hash explicitly:

```powershell
python -B scripts\ssot\migrate_status_archive.py prepare `
  --root . --compact-candidate tmp\compact_STATUS.md `
  --date YYYY-MM-DD --expected-current-sha256 <64-lowercase-hex> `
  --record docs\run_records\status_prepare.json
```

Migration uses a cooperative lock and recoverable transaction journal. A
failed transaction intentionally blocks another migration until its journal
is inspected. Do not delete a journal merely to make the next command run.

Fresh bootstrap state uses
`Archive: none_bootstrap_has_no_history_archive`; it does not fabricate an
archive.
