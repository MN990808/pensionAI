# stub.py: Returns deterministic evidence content without an external LLM for safe local development.

from app.core.errors import GenerationError
from app.domain.models import Evidence


class StubProvider:
    """Deterministic provider for tests and offline onboarding."""

    async def complete(self, query: str, evidence: list[Evidence]) -> str:
        """Return the first governed sample record."""
        if not evidence:
            raise GenerationError(
                "NO_EVIDENCE_FOR_GENERATION",
                "The stub provider requires at least one evidence record.",
                500,
            )
        return evidence[0].content
