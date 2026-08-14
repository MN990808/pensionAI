# build_orchestrator.py: Builds and caches the configured orchestration graph for API dependencies.

from functools import lru_cache

from app.core.config import get_settings
from app.providers.hyperclova import HyperClovaProvider
from app.providers.stub import StubProvider
from app.retrieval.sample_retriever import SampleRetriever
from app.services.orchestrator import PensionOrchestrator


@lru_cache
def build_orchestrator() -> PensionOrchestrator:
    """Construct the MVP graph from validated runtime settings."""
    settings = get_settings()
    retriever = SampleRetriever(settings.sample_data_path)
    provider = HyperClovaProvider(settings) if settings.llm_mode == "hyperclova" else StubProvider()
    return PensionOrchestrator(retriever=retriever, provider=provider)
