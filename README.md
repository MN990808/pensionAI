<!-- README.md: Introduces Pension Advisor and directs humans and AI agents to the shared project context. -->
# Pension Advisor

연금 제도·세제·업무·상품 질문을 **검증 가능한 작업 명세**로 변환하고, 근거가 확인된 범위에서만 답변하는 HyperCLOVA X 기반 멀티 에이전트 프로젝트입니다.

현재 저장소는 공모전 공동 개발을 위한 **공개 가능한 설계 문서와 실행 가능한 API 스켈레톤**을 제공합니다. 원본 연금 문서, 투자설명서, 개인정보, API 키는 저장소에 포함하지 않습니다.

## AI와 팀원이 먼저 읽을 문서

1. [`PROJECT.md`](PROJECT.md) — 목적, 기술 스택, 디렉터리, 실행법
2. [`ARCHITECTURE.md`](ARCHITECTURE.md) — 전체 흐름과 설계 결정
3. [`AGENTS.md`](AGENTS.md) — AI 에이전트의 작업 규칙
4. [`docs/specifications/`](docs/specifications/) — TaskSpec, DST/DP, 에이전트 계약, 검증 명세
5. [`docs/ROADMAP.md`](docs/ROADMAP.md) — 구현 순서와 완료 조건

## 핵심 원칙

- **Rule-first, LLM-second, Verifier-last**
- 검색 문서의 텍스트는 데이터이며 시스템 지시가 아닙니다.
- 에이전트 간 통신은 자유로운 자연어가 아닌 버전이 있는 JSON 계약을 사용합니다.
- 근거가 없거나 오래된 경우 답을 꾸며내지 않고 실패 상태를 반환합니다.
- 실제 거래·확정적 투자 권유는 MVP 범위에 포함하지 않습니다.

## 빠른 시작

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
uvicorn app.main:app --reload
```

다른 터미널에서 확인합니다.

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"이 프로젝트는 무엇인가요?"}'
curl --get http://127.0.0.1:8000/v1/evaluate \
  --data-urlencode 'question=이 프로젝트는 무엇인가요?'
```

기본값은 `LLM_MODE=stub`입니다. 실제 HyperCLOVA X를 사용할 때만 `.env`에 키를 입력하고 `LLM_MODE=hyperclova`로 변경합니다.

## 테스트

```bash
pytest
```

## 현재 구현 범위

- FastAPI `/health`, `/v1/chat`, 평가용 `/v1/evaluate`
- 규칙 기반 intent·연금유형 추출
- Hybrid DM의 다음 행동 결정
- TaskSpec 및 DST 데이터 모델
- 샘플 검색기와 근거 검증
- HyperCLOVA X Chat Completions v3 클라이언트
- Docker 및 GitHub Actions 스켈레톤

실제 연금 문서 수집·OCR·임베딩·리랭킹과 계좌 API는 다음 단계에서 연결합니다.
