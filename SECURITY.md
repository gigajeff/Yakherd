# Security Policy

## Supported Version

Security fixes are applied to the latest release. Older releases may be
superseded rather than patched in place.

## Reporting a Vulnerability

Do not open a public issue for a vulnerability that could enable arbitrary
file writes, path escape, overwrite, transaction corruption, hash bypass,
command execution, or unsafe retrofit behavior.

Use GitHub's private vulnerability reporting for this repository. Include:

- affected version and platform;
- minimal reproduction;
- expected and actual containment behavior;
- whether fresh install, retrofit, validation, or migration is affected; and
- any evidence of target-repository mutation.

Do not include real secrets, private repositories, or proprietary project data
in a report.
