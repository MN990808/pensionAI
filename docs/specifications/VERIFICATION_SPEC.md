<!-- VERIFICATION_SPEC.md: Defines independent checks that must pass before any financial answer is delivered. -->
# Verification Specification v1

## Validation Layers

1. Contract validation: every request and result matches its Pydantic schema.
2. Tool validation: required calls succeeded and returned the requested account/time scope.
3. Evidence validation: every material claim has a source locator and authority.
4. Freshness validation: effective dates and supersession relationships are valid.
5. Numeric validation: deterministic recalculation matches the proposed claim.
6. Suitability validation: advice has the required profile and risk inputs.
7. Response validation: the composer added no claim outside the approved set.

## Outcome Codes

| Code | Meaning | Response behavior |
|---|---|---|
| `PASS` | All postconditions met | Deliver verified answer |
| `NEEDS_CLARIFICATION` | Material input missing | Ask one targeted question |
| `INSUFFICIENT_EVIDENCE` | No supported answer | State limitation and next step |
| `STALE_SOURCE` | Only expired/superseded source found | Refuse current factual claim |
| `CONFLICTING_SOURCES` | Authoritative records disagree | Expose conflict or escalate |
| `TOOL_FAILURE` | Required dependency failed | Return safe retry guidance |
| `SUITABILITY_REQUIRED` | Recommendation profile incomplete | Collect suitability inputs |

## Minimum MVP Checks

- Non-empty answer
- At least one evidence record for factual answers
- Source ID, title, effective date, and URI/locator present
- No evidence record marked `sample` may support a production financial answer
- Clarification responses contain no recommendation
- Request ID and verification status appear in the API response
