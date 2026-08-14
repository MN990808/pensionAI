# errors.py: Defines typed application errors for configuration, retrieval, generation, and verification failures.


class AppError(Exception):
    """Base error carrying a stable machine code and HTTP status."""

    def __init__(self, code: str, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


class ConfigurationError(AppError):
    """Raised when required runtime configuration is invalid."""


class RetrievalError(AppError):
    """Raised when a knowledge source cannot be loaded or queried."""


class GenerationError(AppError):
    """Raised when an LLM provider cannot generate a valid response."""


class VerificationError(AppError):
    """Raised when an answer violates a verification invariant."""
