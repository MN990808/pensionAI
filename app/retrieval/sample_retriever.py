# sample_retriever.py: Loads public synthetic evidence and provides deterministic keyword retrieval for the scaffold.

from pathlib import Path

import yaml
from pydantic import ValidationError

from app.core.errors import RetrievalError
from app.domain.models import Evidence


class SampleRetriever:
    """Small local retriever that is replaced by governed RAG later."""

    def __init__(self, path: Path) -> None:
        self._documents = self._load_documents(path)

    async def search(self, query: str, top_k: int = 5) -> list[Evidence]:
        """Match explicit sample keywords without semantic guessing."""
        normalized = query.casefold()
        matches = [
            document
            for document in self._documents
            if any(keyword.casefold() in normalized for keyword in document.keywords)
        ]
        return matches[:top_k]

    def _load_documents(self, path: Path) -> list[Evidence]:
        try:
            with path.open("r", encoding="utf-8") as stream:
                payload = yaml.safe_load(stream) or {}
        except OSError as exc:
            raise RetrievalError(
                "SAMPLE_DATA_UNAVAILABLE",
                f"Could not read sample data at {path}.",
                500,
            ) from exc
        except yaml.YAMLError as exc:
            raise RetrievalError("SAMPLE_DATA_INVALID", "Sample YAML is invalid.", 500) from exc
        return self._validate_documents(payload)

    def _validate_documents(self, payload: object) -> list[Evidence]:
        try:
            records = payload.get("documents", []) if isinstance(payload, dict) else []
            return [Evidence.model_validate(record) for record in records]
        except (ValidationError, TypeError) as exc:
            raise RetrievalError(
                "SAMPLE_CONTRACT_INVALID",
                "Sample documents do not match the Evidence contract.",
                500,
            ) from exc
