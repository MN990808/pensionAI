# evaluate.py: Adapts evaluator-style GET questions to the same guarded chat orchestration flow.

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.errors import AppError
from app.domain.models import ChatRequest, ChatResponse
from app.services.build_orchestrator import build_orchestrator
from app.services.orchestrator import PensionOrchestrator


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1", tags=["evaluation"])


@router.get("/evaluate", response_model=ChatResponse)
async def evaluate(
    question: Annotated[str, Query(min_length=1, max_length=4000)],
    orchestrator: PensionOrchestrator = Depends(build_orchestrator),
) -> ChatResponse:
    """Process a GET request through the canonical chat contract."""
    try:
        return await orchestrator.handle(ChatRequest(message=question))
    except AppError as exc:
        logger.error("evaluation_failed code=%s message=%s", exc.code, exc.message)
        raise HTTPException(
            status_code=exc.status_code,
            detail={"code": exc.code, "message": exc.message},
        ) from exc
