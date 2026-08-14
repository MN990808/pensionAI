<!-- ROADMAP.md: Defines implementation gates and measurable completion criteria for the contest MVP. -->
# Delivery Roadmap

## Gate 0 — Account and Evaluation Contract

- Register Naver Cloud credit and verify eligible services.
- Enable CLOVA Studio and issue a server-side API key.
- Obtain the organizer's exact request/response API contract.
- Decide the public MVP scope: DB/DC/IRP/pension savings, no real trades.

**Done when:** the team can call HyperCLOVA X and has a written evaluation endpoint schema.

## Gate 1 — Local Vertical Slice

- Run FastAPI locally.
- Route a question and update DST.
- Retrieve at least one governed evidence record.
- Return `PASS`, `NEEDS_CLARIFICATION`, or `INSUFFICIENT_EVIDENCE` deterministically.

**Done when:** tests prove unsupported questions cannot produce an unsupported answer.

## Gate 2 — Naver Cloud Deployment

- Create one VPC, public subnet, Linux server, restricted ACG, and public IP.
- Deploy the Docker image behind Nginx or Caddy.
- Expose `/health` and the evaluator-compatible endpoint.
- Verify secrets are injected at runtime and absent from Git/logs.

**Done when:** an external client receives a valid health and chat response over HTTPS.

## Gate 3 — Governed Pension RAG

- Inventory and classify policy, tax, operations, FAQ, and product documents.
- Extract authority, effective date, product code, section, and source locator.
- Add OCR, section-aware chunking, lexical/vector retrieval, and reranking.
- Detect superseded and conflicting records.

**Done when:** every answer claim maps to a current source locator.

## Gate 4 — Multi-Agent Contracts

- Add Knowledge, Account Mock, Product, Advisor, and Verifier adapters.
- Run independent tasks in parallel only when dependencies permit.
- Keep canonical DST writes in the orchestrator.
- Add timeout, retry, and failure-code handling.

**Done when:** compound queries produce an auditable task graph and merged result.

## Gate 5 — Evaluation and Hardening

- Build high/medium/low and closed/open-ended evaluation cases.
- Test ambiguity, stale sources, conflicting sources, tool failure, and prompt injection.
- Measure groundedness, citation coverage, task success, latency, and token cost.
- Freeze a demo dataset and release candidate.

**Done when:** the release meets agreed thresholds without manual intervention.
