# Start with Yakherd 3

For a new repository, install Yakherd 3.0 and run:

```text
yakherd setup YOUR_PROJECT
yakherd doctor YOUR_PROJECT
```

Open that folder as the project in your coding environment. The shortest
startup message is:

> Read START_HERE.md and follow it.

You do not need a master prompt before starting. If you have no product brief
yet, use this more explicit first message:

> Read START_HERE.md, then AGENTS.md, SSOT.md, BASELINE.md and NOW.md. Use this
> repository's SSOT process. No product brief exists yet: help me define the
> project goal, then record the agreed requirements and first milestone in
> the appropriate files. Do not invent product requirements.

The installed handoff and initial NOW.md already tell the agent to obtain a
missing product objective. A conversation or short request is enough; a
formal master prompt is optional. Record accepted requirements in SSOT.md,
proven facts in BASELINE.md, and one executable milestone in NOW.md as they
become available.

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
