# test_health.py: Verifies the deployment health contract and safe stub mode.

import httpx

from app.main import app


async def test_health_contract() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Pension Advisor",
        "version": "0.1.0",
        "llm_mode": "stub",
    }
