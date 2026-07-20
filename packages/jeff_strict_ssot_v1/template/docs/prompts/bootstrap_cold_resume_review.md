# Bootstrap Cold-Resume Red Team Prompt

Use a fresh task with no bootstrap implementation chat.

Read all root owner files, `docs/task_protocol.md`, validation/governance
contracts, five task prompts, package install manifest, and validator tests.

Verify that a fresh reader can recover:

- the one-owner rule and authority map;
- current state, blockers, next action, forbidden actions, and archive state;
- accepted/superseded decision mechanics;
- all five task boundaries and single-writer rule;
- evidence classes and done gate;
- pure-validator prohibitions;
- Governor inactive/delta behavior;
- transcript authority neutrality;
- Git/remote visibility boundary; and
- the block on product implementation before reviewed intake.

Run protocol/governor validators and tests. Review install-manifest hashes.
Do not edit or repair the target. Write one independent review under
`docs/reviews/`, lead with findings, and state whether product intake may begin.

End with one required repository marker.
