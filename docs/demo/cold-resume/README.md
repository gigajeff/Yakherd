# Cold-Resume Proof

This is the inspectable evidence behind the animated demo in Yakherd's public
README. A newly installed repository was committed locally, then handed to a
fresh coding agent with no implementation chat and no product context. The
agent had to recover the state and next action from repository files alone.

The third isolated run passed:

- strict protocol validation: 0 errors, 0 warnings;
- Governor-policy validation: 0 errors;
- protocol tests: 30/30 passed;
- installation receipt: 43/43 byte counts and 43/43 hashes matched;
- structured evidence: all five run records valid; and
- generated Python cache paths: 0 before and 0 after.

The [independent review](review.md), [exact launch prompt](agent-prompt.txt),
[agent result](agent-result.txt), and [structured run records](run_records/)
are included here. [evidence.json](evidence.json) binds every committed proof
file with SHA-256.

## Why There Are Failed Reviews Here

This was not staged to produce a pass. The first fresh review found an ambient
wall-clock dependency in a supposedly deterministic validator and a conflict
between the review's write boundary and its JSON evidence contract. The second
found that the installed test commands generated ignored Python bytecode.
Yakherd blocked both candidates. The findings are preserved under [failed/](failed/),
the package was repaired and re-hashed, and a third newly installed repository
was reviewed from scratch.

## Provenance

- Yakherd version: `1.1.0`
- Demo-input wheel SHA-256:
  `678eded1d6f50d2348af9452671aab26e81c06bd21989454a61218b0942140b6`
- Reviewed package manifest SHA-256:
  `b997d8285da2a462716913822e883354b3a9044f49a016c274a9ff9fa1e7c1a9`
- Installation receipt SHA-256:
  `0d2811f38be3413b8919b95b2af1e18498bfafdb7e0bfd6789b1f561dd2548d5`
- Fresh repository baseline commit:
  `4088e7e8721cc6c488c2409d5635a15bdce826a8`
- Review run ID: `20260720T212954Z`

The demo-input wheel predates only the addition of these public documentation
artifacts. The governed package bytes are bound by the package-manifest hash
above. The final PyPI release is rebuilt, inspected, and smoke-installed from
the version tag by the Trusted Publishing workflow.

## About the Recording

`cold-resume.gif` is a paced terminal rendering of the exact recorded results,
not a claim that a screen recorder captured every internal tool call. Its
source scenes are in [session.json](session.json), and the renderer is
[`scripts/render_cold_resume_demo.py`](../../../scripts/render_cold_resume_demo.py).
The renderer is documentation-only and uses Pillow; Yakherd itself has no
runtime dependencies.
