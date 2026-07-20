# Release Process

## Candidate Gate

1. Confirm the package source contains no bytecode/cache files.
2. Regenerate `MANIFEST.json` after any governed template change.
3. Regenerate `RELEASE.json` after installer or manifest changes.
4. Run package tests and clean acceptance.
5. Run `python scripts/verify_release.py`.
6. Run CI on Windows and Linux.
7. Obtain independent Red Team review of the exact candidate bytes.
8. Build the wheel and source distribution, then smoke-install both in clean
   environments.
9. Review staged paths and create an intentional release commit.
10. Tag the exact reviewed commit as `vMAJOR.MINOR.PATCH`. The tag-triggered
    workflow must bind that tag to the project version and executing commit,
    inspect and smoke-install the exact wheel and source distribution, and hand
    those files to a separate publishing job through immutable-pinned artifact
    actions. The build job must not have `id-token: write`; only the minimal job
    that retrieves the verified files and publishes them may have that
    permission, through the dedicated `pypi` Trusted Publisher environment.

## Compatibility

Behavioral or schema changes require a changelog entry and explicit migration
analysis. Security-sensitive changes to containment, overwrite, retrofit,
validation, decision history, status migration, or evidence handling require
new adversarial tests.

## V1 Provenance

The first release imports the exact package that passed Mosaic-origin
acceptance V6 and independent V3 review. Historical review records are retained
under `docs/audits/mosaic-origin/`.
