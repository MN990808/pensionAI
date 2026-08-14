# test_unknown_chat.py: Verifies unsupported financial questions fail closed without fabricated evidence.

import httpx

from app.main import app


async def test_unknown_question_returns_insufficient_evidence() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/chat", json={"message": "IRP 세액공제 한도는 얼마야?"})
    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "INSUFFICIENT_EVIDENCE"
    assert payload["evidence"] == []
