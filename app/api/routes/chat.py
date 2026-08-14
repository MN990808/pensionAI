# chat.py: Validates chat requests and delegates one dialogue turn to the orchestrator.

import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.errors import AppError
from app.domain.models import ChatRequest, ChatResponse
from app.services.build_orchestrator import build_orchestrator
from app.services.orchestrator import PensionOrchestrator


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    orchestrator: PensionOrchestrator = Depends(build_orchestrator),
) -> ChatResponse:
    """Process one guarded Pension Advisor request."""
    try:
        return await orchestrator.handle(request)
    except AppError as exc:
        logger.error("chat_failed code=%s message=%s", exc.code, exc.message)
        raise HTTPException(
            status_code=exc.status_code,
            detail={"code": exc.code, "message": exc.message},
        ) from exc
