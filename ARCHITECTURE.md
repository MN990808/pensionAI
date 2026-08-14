<!-- ARCHITECTURE.md: Describes the Pension Advisor runtime, contracts, and deployment boundaries. -->
# Architecture

## System Overview

Pension Advisor uses a hybrid Dialogue Manager. Deterministic rules protect safety, authentication, required slots, and workflow transitions; HyperCLOVA X handles Korean intent, entities, ambiguity, planning, and natural language; an independent verifier blocks unsupported results.

## Runtime Flow

```text
Client
  → API boundary
  → Guardrails and rule router
  → Dialogue Manager (DST + DP)
  → TaskSpec builder
  → Orchestrator
      ↘ Knowledge Agent
      ↘ Account/Work Agent
      ↘ Advisor Agent
      ↘ Product Agent
  → Independent Verifier
  → Response Composer
  → Answer + Evidence + Assumptions + Next step
```

## Processing Stages

| Stage | Owner | Output |
|---|---|---|
| Rule processing | API/Guardrail | block, cache, authentication state |
| Query analysis | Dialogue Manager | intent, slots, ambiguity, DST |
| Specification | Orchestrator | versioned `TaskSpec` and dependencies |
| Execution | Logical agents/tools | typed `AgentResult` records |
| Verification | Verifier | `PASS` or explicit failure code |
| Response | Composer | grounded Korean response |

## Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Dialogue management | Hybrid rule + LLM | Safety and flexibility without opaque control |
| State ownership | Single orchestrator writer | Prevents concurrent agent state conflicts |
| Agent deployment | Logical modules in one API | Keeps the contest MVP operable and cheap |
| Model integration | Separate analyze/execute/generate calls | Avoids prompt coupling and supports verification |
| Knowledge | Governed RAG, not initial fine-tuning | Preserves dates, provenance, and document updates |
| Failure behavior | Fail closed for missing evidence | Prevents plausible but unsupported financial answers |

## MVP Deployment

```text
Internet → Public IP → Nginx/Caddy → FastAPI container
                                      ├── Local metadata/sample index
                                      └── HyperCLOVA X API over HTTPS
```

Initial Naver Cloud resources are one VPC, one public subnet, one Linux server, one restricted ACG, and one public IP. Load Balancer, managed databases, Redis, and separate agent services are deferred until a measured need exists.

## Security Boundaries

- CLOVA Studio keys stay server-side and outside Git.
- SSH is restricted to team IP addresses; only HTTP/HTTPS are public.
- Raw questions and logs must be redacted before persistent storage.
- Retrieved document text is delimited and treated as untrusted evidence.
- Tool calls are allow-listed by each Agent Contract.

## Extension Points

- Replace `SampleRetriever` with hybrid lexical/vector retrieval.
- Add Router API or HCX structured output behind the dialogue interfaces.
- Add authenticated account mock APIs without changing public chat contracts.
- Replace the stub provider with HyperCLOVA X through configuration.
- Add PostgreSQL and Redis adapters after the single-server baseline is stable.
