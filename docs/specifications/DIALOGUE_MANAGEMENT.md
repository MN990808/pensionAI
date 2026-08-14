<!-- DIALOGUE_MANAGEMENT.md: Defines the hybrid DST and dialogue-policy behavior for multi-turn pension conversations. -->
# Dialogue Management v1

## Hybrid Ownership

- Rules own safety, authentication, required slots, permissions, and state transitions.
- The LLM proposes intent, entities, ambiguity, and natural-language phrasing.
- The policy graph selects the next action from validated state.

## Dialogue State

The canonical DST includes `state_version`, `user_goal`, `intent`, `pension_type`, `authorization`, `risk_level`, `slots`, `assumptions`, `ambiguities`, `pending_question`, `evidence_refs`, and `completed_tasks`.

Only the orchestrator increments `state_version` and applies proposed patches.

## Policy Priority

```text
Safety block
→ Authentication
→ Domain and task classification
→ Required-slot check
→ Clarify or Assume+Expose
→ TaskSpec generation
→ Agent execution
→ Verification
→ Response
```

## Clarify vs Assume+Expose

Clarify when another interpretation changes tax, eligibility, recommendation, account selection, money, or an irreversible action. Ask one high-information question per turn.

Assume+Expose when the choice is low-risk, reversible, and still useful. Record the assumption in DST and surface it in the response.

### Examples

- “비슷한 상품 추천”: clarify whether similarity means risk, asset exposure, or fee.
- “한 달 수익률”: assume the latest 30 days and expose that assumption unless the evaluator requires calendar-month precision.
- “연금 갈아타도 돼?”: clarify pension type and whether the user means institution transfer or product replacement.
