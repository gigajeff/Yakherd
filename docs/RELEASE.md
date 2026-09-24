# Release Process

## Candidate Gate

1. Confirm the package source contains no bytecode/cache files.
2. Run `python -B scripts/regenerate_release.py` to regenerate v3 template and
   engine bindings. The historical V1 package remains unchanged unless an
   explicit legacy repair is in scope.
3. Verify every changed package's `MANIFEST.json` and `RELEASE.json` bindings.
4. Run root tests, both package test suites and both clean acceptance suites.
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

## Version 3 distribution

The default bundled package is `packages/yakherd_v3/`; the source distribution
also preserves V1 provenance. Build with `python -m build`, inspect exact bytes
with `python scripts/verify_distribution.py dist`, then run
`python -B scripts/smoke_distribution.py dist --output .tmp/distribution-smoke`.
The smoke command creates separate clean environments and installs the exact
wheel and sdist. Source building may fetch pinned build dependencies; the
installed harness itself remains standard-library-only.

V3 adoption is a reviewed instruction migration. Existing V1 receipts, custom
product owners and process state are not overwritten by setup. Follow
[SSOT_MIGRATION.md](SSOT_MIGRATION.md) and keep plans/backups private until
reviewed for publication. GitHub source publication alone does not publish to
PyPI. Pushing a `v*.*.*` tag triggers the separate Trusted Publisher workflow
and therefore needs package-publication authorization.

## V1 Provenance

The first release imports the exact package that passed Mosaic-origin
acceptance V6 and independent V3 review. Historical review records are retained
under `docs/audits/mosaic-origin/`.
