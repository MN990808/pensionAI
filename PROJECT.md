<!-- PROJECT.md: Provides the master context that humans and AI agents must read before changing the project. -->
# Pension Advisor Project Context

Pension Advisor는 DB·DC·IRP·연금저축 및 연금상품 관련 자연어 질문을 분석해 작업 명세를 만들고, 조회·상담·상품 비교 에이전트를 조정한 뒤 독립 검증을 통과한 결과만 전달하는 시스템입니다. 공모전 MVP에서는 실제 금융거래가 아니라 근거 기반 조회와 의사결정 지원에 집중합니다.

## Tech Stack

| Layer | Technology | Version policy | Reason |
|---|---|---|---|
| API | Python + FastAPI | Python 3.11+, FastAPI 0.x | 타입 기반 REST API와 자동 문서 |
| Contracts | Pydantic | 2.x | TaskSpec·DST·응답 JSON 검증 |
| LLM | HyperCLOVA X | Chat Completions v3 | 한국어 NLU/NLG와 Function Calling |
| HTTP | HTTPX | 0.x | 비동기 외부 API 호출 |
| Retrieval | FAISS/Vector DB 예정 | 미확정 | 문서 RAG 확장 지점 |
| Test | Pytest | 8.x+ | 단위·API 계약 검증 |
| Deploy | Docker + Naver Cloud Server | MVP 단일 서버 | 평가용 공개 Endpoint 제공 |

## Directory Map

```text
pensionAI/
├── app/
│   ├── api/                 # HTTP routes and request boundary
│   ├── core/                # Configuration and error hierarchy
│   ├── dialogue/            # Rule router and next-action policy
│   ├── domain/              # Shared contracts: DST, TaskSpec, results
│   ├── providers/           # Stub and HyperCLOVA X providers
│   ├── retrieval/           # Retrieval interface and sample adapter
│   ├── services/            # Orchestration use cases
│   └── verification/        # Evidence and postcondition checks
├── data/
│   ├── samples/             # Public synthetic sample records only
│   └── README.md            # Local raw-data rules
├── docs/
│   ├── specifications/      # Versioned system contracts
│   └── ROADMAP.md           # Delivery gates
├── tests/                   # Unit and API contract tests
├── AGENTS.md                # AI collaboration rules
├── ARCHITECTURE.md          # System design and data flow
├── Dockerfile               # API container image
├── docker-compose.yml       # Local container runner
└── pyproject.toml           # Python dependencies and test config
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pytest
uvicorn app.main:app --reload
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `LLM_MODE` | No | `stub` or `hyperclova`; defaults to `stub` |
| `CLOVASTUDIO_API_KEY` | HyperCLOVA only | CLOVA Studio API key; never commit |
| `CLOVASTUDIO_MODEL` | No | Defaults to `HCX-005` |
| `CLOVASTUDIO_BASE_URL` | No | CLOVA Studio API host |
| `SAMPLE_DATA_PATH` | No | Public sample knowledge YAML path |
| `LOG_LEVEL` | No | Application log level |

## Conventions

- Every Python function stays below 30 executable lines.
- Each file has one primary responsibility and starts with a one-line purpose comment.
- External I/O failures must be converted to a typed `AppError` with context.
- Contracts are Pydantic models and include `schema_version` where interoperability matters.
- Only the orchestrator may commit DST changes; agents return proposed results.
- Changes to a contract require corresponding specification and test updates.
- Raw PDFs, DOCX, XLSX, credentials, account data, and generated indexes are never committed.

## First Vertical Slice

```text
Question → Rule Router → DST/DP → Retrieval → Provider → Verifier → Response
```

The slice is complete when a supported question returns `PASS` with evidence and an unsupported question returns `INSUFFICIENT_EVIDENCE` without hallucinating.
