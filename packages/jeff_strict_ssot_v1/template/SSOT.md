# SSOT Authority Map

Status: current authority map for {{PROJECT_NAME}}.

Each subject has one current owner. Indexes and summaries may link to an owner
but must not copy mutable detail.

| Subject | Current owner | State |
| --- | --- | --- |
| Authority map | `SSOT.md` | current |
| Current project state | `STATUS.md` | current index only |
| Accepted and superseded decisions | `DECISIONS.md` | current |
| Architecture boundaries | `ARCHITECTURE.md` | awaiting product intake |
| Test strategy | `TESTING.md` | protocol-only |
| Git workflow | `GIT_SYNC.md` | current |
| Domain invariants | `docs/domain_invariants.md` | empty pending intake |
| Task boundaries | `docs/task_protocol.md` | current |
| Evidence contract | `docs/validation_protocol.md` | current |
| Product master prompt | `docs/master_prompts/000_PRODUCT_PROMPT_NOT_RECEIVED.md` | not received |
| Governance findings | `docs/governance/OPEN_FINDINGS.md` | current, non-authoritative |
| Governance risks | `docs/governance/RISK_REGISTER.md` | current, non-authoritative |

Owner changes require a decision in `DECISIONS.md` with explicit predecessor,
successor, retained boundary, and date. Closing a finding does not repair stale
owner text; update the actual owner and every affected index.
