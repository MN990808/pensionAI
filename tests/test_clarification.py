# test_clarification.py: Verifies high-risk personalized advice requests collect pension type before execution.

import httpx

from app.main import app


async def test_personal_advice_requires_pension_type() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/chat", json={"message": "나에게 맞는 상품 추천해줘"})
    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "NEEDS_CLARIFICATION"
    assert payload["clarification"]["slot"] == "pension_type"
    assert payload["evidence"] == []
