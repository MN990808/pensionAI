# main.py: Creates the FastAPI application and registers public API routes.

import logging

from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.evaluate import router as evaluate_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Build the application from validated settings."""
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    application = FastAPI(title=settings.app_name, version=settings.app_version)
    application.include_router(health_router)
    application.include_router(chat_router)
    application.include_router(evaluate_router)
    return application


app = create_app()
