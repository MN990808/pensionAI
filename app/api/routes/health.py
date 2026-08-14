# health.py: Reports service readiness and active generation mode without exposing secrets.

from fastapi import APIRouter

from app.core.config import get_settings
from app.domain.models import HealthResponse


router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Return a stable health contract for deploy and evaluator checks."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        llm_mode=settings.llm_mode,
    )
