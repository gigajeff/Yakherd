# Start Yakherd

Yakherd is installed, but its five roles are not running until you explicitly
launch them in your coding agent. The installer cannot create chats, use your
GitHub account, or ingest your product idea.

## Codex: One Message

Open this repository as the Codex project. Confirm that Codex loaded
`AGENTS.md`, then send this message in a new main task:

> Follow `docs/prompts/codex_team_launcher.md` now. This is my explicit request
> to launch the five Yakherd role agents. Keep this task as their coordinator.
> Run the bootstrap review before product implementation, guide me through the
> one GitHub publication checkpoint, and ask me for my product master prompt if
> I have not included it below.

Codex should create five inspectable agent threads: Architecture,
Implementation, Red Team, Temporary Branch, and Governor. The coordinator is
not a sixth governance role. If Codex cannot create all five, it must report
which role is missing instead of pretending that startup succeeded.

If concurrent capacity is lower than six total threads, the coordinator may
launch role agents in batches. All five stable role identities must still be
created and remain addressable for follow-up; simultaneous activity is not a
startup requirement. Changing client capacity is a user setting, not an
installer action.

## Add Your Master Prompt To The Same Message

You may append your product idea to the launch message using these delimiters:

```text
MASTER PROMPT START
Paste the complete product prompt here.
MASTER PROMPT END
```

If you do not include it, the coordinator will ask after the bootstrap review.
The prompt is preserved before Architecture extracts requirements from it; it
is never treated as executable project law merely because it was received.

## What You Should See

| Role | Initial state | Why |
| --- | --- | --- |
| Architecture | waiting for bootstrap PASS and the master prompt | It cannot invent product intent. |
| Red Team | running the cold-resume review | Product intake is blocked until this passes. |
| Implementation | parked | It needs a reviewed Architecture authorization. |
| Temporary Branch | parked | It needs one named, approved hypothesis and isolation boundary. |
| Governor | inactive | It needs a useful baseline and separate activation approval. |

Five created roles do not mean five concurrent writers. Yakherd permits only
the writer authorized for the current slice; review and planning outputs have
separate bounded paths.

## GitHub

After the bootstrap review passes, the coordinator follows
[`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md). It verifies the active account,
asks you to confirm owner, repository name, and visibility, and only then may
initialize Git, create the GitHub repository, or push. Private is the suggested
default. Never paste an access token into the master prompt or a repository
file.

## Other Coding Agents

Use the five prompts under `docs/prompts/` as five long-lived role sessions.
The automatic multi-agent launcher is a Codex adapter; the authority and role
rules remain product- and model-neutral.
