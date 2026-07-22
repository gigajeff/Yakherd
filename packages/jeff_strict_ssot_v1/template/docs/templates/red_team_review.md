# Red Team Review: <Target>

- Date: YYYY-MM-DD
- Work ID: <stable ID>
- Review cycle: 1 | 2
- Evidence scope: <files, diff, records>
- Verdict: PASS | FAIL
- Authority effect: <none or exact bounded authorization>
- Governance budget: <=120 lines and <=16384 UTF-8 bytes unless human-approved

## Blocking Findings

For each P0/P1: ID, severity, accepted requirement/invariant reference, exact
evidence, impact on the Definition of Done, and smallest in-scope remedy.

## Advisories

P2/P3 only. Advisories do not block `PASS` and cannot become requirements.

## Checks

## Residual Risk

On cycle 2, identify each prior blocker as fixed or still open. Any new blocker
must be a fix regression or a previously missed P0/P1 with an accepted
requirement citation and explanation. A second `FAIL` stops autonomous review
and returns the decision to the human; this review cannot require cycle 3.

human action required: <exact decision, or replace with another required marker>.
