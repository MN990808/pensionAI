# base.py: Defines the async retrieval contract used by the orchestrator.

from typing import Protocol

from app.domain.models import Evidence


class Retriever(Protocol):
    """Retrieval adapter interface."""

    async def search(self, query: str, top_k: int = 5) -> list[Evidence]:
        """Return governed evidence ordered by relevance."""
        ...
