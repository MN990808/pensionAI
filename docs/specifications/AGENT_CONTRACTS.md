<!-- AGENT_CONTRACTS.md: Defines responsibilities, permissions, outputs, and failure behavior for each logical agent. -->
# Agent Contracts v1

## Shared Contract

Every agent receives a `TaskSpec` plus immutable DST snapshot and returns an `AgentResult`. Results include `task_id`, `status`, `claims`, `evidence_refs`, `proposed_state_patch`, and `error`.

Agents never update canonical state directly and never call tools outside `allowed_tools`.

## Roles

| Agent | Responsibility | Required input | Forbidden behavior |
|---|---|---|---|
| Orchestrator | Decompose, order, dispatch, merge | User request and DST | Invent domain facts |
| Knowledge Agent | Retrieve policy/tax/operations evidence | Query and time basis | Personalized conclusion |
| Account Agent | Read authenticated account/mock data | Auth and account ID | Advice or unauthorized write |
| Product Agent | Filter and compare current product records | Similarity basis | Suitability decision |
| Advisor Agent | Explain suitability against user profile | Goal, horizon, risk profile | Guaranteed return claim |
| Verifier | Check evidence, date, numbers, and contracts | All task results | Repair and approve its own changes |
| Response Composer | Express verified claims naturally | Approved claim set | Add new facts |

## Standard Failure Codes

- `NEEDS_CLARIFICATION`
- `INSUFFICIENT_EVIDENCE`
- `STALE_SOURCE`
- `CONFLICTING_SOURCES`
- `AUTHENTICATION_REQUIRED`
- `TOOL_FAILURE`
- `SUITABILITY_REQUIRED`
- `CONTRACT_VIOLATION`

## Timeout and Retry

- Read-only idempotent tools may retry once after transient failure.
- Non-idempotent tools require an idempotency key and explicit future approval.
- A timed-out task returns `TOOL_FAILURE`; another agent may not fabricate its result.
