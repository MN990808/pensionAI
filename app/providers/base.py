# base.py: Defines the grounded response-provider contract used by orchestration.

from typing import Protocol

from app.domain.models import Evidence


class ResponseProvider(Protocol):
    """Provider interface for grounded answer generation."""

    async def complete(self, query: str, evidence: list[Evidence]) -> str:
        """Generate an answer from the supplied evidence only."""
        ...
