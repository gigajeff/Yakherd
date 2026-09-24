# Start with Yakherd 3

For a new repository, install Yakherd 3.0 and run:

```text
yakherd setup YOUR_PROJECT
yakherd doctor YOUR_PROJECT
```

Open that folder in your coding environment and provide the actual product
request. `Start Yakherd` tells the agent to read AGENTS, SSOT, BASELINE and NOW,
inspect the checkout and continue the authorized next action in one task.
It does not create a team or require a bootstrap review.

The initial files state honestly that no product requirements or implementation
are established. The agent replaces that scaffold from your request and keeps
the repository's current owners up to date as work proceeds.

For an existing repository, read [the migration guide](docs/SSOT_MIGRATION.md).
Prepare and inspect replacement content, then use the reviewed, hash-pinned
`yakherd migrate` workflow. Setup never overwrites existing paths.

The [canonical process](docs/SSOT_PROCESS.md) explains autonomy, evidence,
independent verification and milestone transitions. The
[actual installed templates](packages/yakherd_v3/template/) are the single
source for the starter files. No other project's checkout is required for a
generated repository to resume.
