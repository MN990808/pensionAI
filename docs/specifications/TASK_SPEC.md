<!-- TASK_SPEC.md: Specifies the versioned plan contract produced before any agent executes work. -->
# Task Specification v1

`TaskSpec` is the executable agreement between query analysis and agents. No agent runs from the raw user message alone.

## Required Fields

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | string | Contract version |
| `task_id` | string | Unique request-local task ID |
| `objective` | string | User outcome expressed without solution details |
| `intent` | enum | Lookup, account task, advice, or product lookup |
| `assigned_agent` | string | Logical agent allowed to perform the task |
| `required_inputs` | list | Slots that must exist before execution |
| `allowed_tools` | list | Explicit tool allow-list |
| `depends_on` | list | Predecessor task IDs |
| `risk_level` | enum | Low, medium, or high |
| `success_criteria` | list | Machine-checkable postconditions |
| `assumptions` | list | Low-risk exposed assumptions |

## Planning Rules

- Missing inputs that change tax, eligibility, recommendation, or account action require clarification.
- Low-risk reversible defaults may use Assume+Expose.
- Account reads require authentication state; writes are out of MVP scope.
- Product comparison depends on a declared similarity criterion.
- Calculation tasks must use deterministic tools and preserve inputs.
- Parallel tasks may not share mutable state.

## Example

```yaml
schema_version: "1.0"
task_id: T3
objective: Compare products similar to the current IRP holding
intent: product_lookup
assigned_agent: product_agent
required_inputs: [current_product, similarity_basis]
allowed_tools: [product_search, product_document_fetch]
depends_on: [T1, T2]
risk_level: high
success_criteria:
  - Every candidate has an effective date
  - Every numeric comparison has an evidence reference
assumptions: []
```
