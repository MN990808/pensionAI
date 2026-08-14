# test_input_validation.py: Verifies the public API rejects empty user messages at the boundary.

import httpx

from app.main import app


async def test_empty_message_is_rejected() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/v1/chat", json={"message": ""})
    assert response.status_code == 422
