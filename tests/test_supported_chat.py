# test_supported_chat.py: Verifies a sample-supported project question passes evidence validation.

import httpx

from app.main import app


async def test_supported_question_returns_grounded_answer() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/chat", json={"message": "이 프로젝트 구조를 알려줘"})
    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "PASS"
    assert payload["evidence"][0]["document_id"] == "SAMPLE-PROJECT-001"
    assert payload["verification"]["passed"] is True
