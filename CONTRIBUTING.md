# Contributing to Yakherd

## Start With an Issue

For behavioral changes, open an issue describing the problem, affected
invariant, proposed evidence, and migration impact. Documentation corrections
may use a focused pull request directly.

## Development Rules

1. Keep Yakherd product-neutral.
2. Preserve no-network/no-install/no-product/no-Git behavior in the target
   repository.
3. Add or update tests for every behavior change.
4. Regenerate `MANIFEST.json` and `RELEASE.json` bindings when their governed
   inputs change.
5. Run the package tests, clean acceptance suite, release verifier, and
   `git diff --check`.
6. Record compatibility and migration implications in `CHANGELOG.md`.

## Pull Requests

Pull requests should explain:

- the user problem;
- the authority or safety invariant affected;
- tests and acceptance evidence;
- any hash-chain changes;
- rollback or migration behavior; and
- whether independent Red Team review is required before release.

Changes to the audited package are not release-ready until an independent
review confirms the exact candidate bytes.
