# config.py: Loads and validates runtime settings from environment variables and an optional local .env file.

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.errors import ConfigurationError


class Settings(BaseSettings):
    """Validated runtime configuration."""

    app_name: str = "Pension Advisor"
    app_version: str = "0.1.0"
    llm_mode: Literal["stub", "hyperclova"] = "stub"
    clovastudio_api_key: SecretStr | None = None
    clovastudio_model: str = "HCX-005"
    clovastudio_base_url: str = "https://clovastudio.stream.ntruss.com"
    clovastudio_timeout_seconds: float = 30.0
    sample_data_path: Path = Path("data/samples/documents.yaml")
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return one validated settings instance per process."""
    try:
        return Settings()
    except ValidationError as exc:
        raise ConfigurationError(
            "INVALID_CONFIGURATION",
            "Runtime configuration is invalid.",
            500,
        ) from exc
