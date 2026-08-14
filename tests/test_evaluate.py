# test_evaluate.py: Verifies the provisional GET evaluator adapter uses the canonical response contract.

import httpx

from app.main import app


async def test_evaluate_get_adapter() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/evaluate", params={"question": "프로젝트 구조"})
    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "PASS"
    assert payload["trace"]["assigned_agent"] == "knowledge_agent"
