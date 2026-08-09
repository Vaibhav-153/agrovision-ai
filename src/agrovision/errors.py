"""Application-specific exceptions with user-safe messages."""


class AgroVisionError(Exception):
    """Base exception for expected application failures."""


class ConfigurationError(AgroVisionError):
    """Raised when required deployment configuration is missing or invalid."""


class InputValidationError(AgroVisionError):
    """Raised when an uploaded image or inference setting is invalid."""


class InferenceServiceError(AgroVisionError):
    """Raised when the hosted inference provider cannot complete a request."""


class RateLimitError(AgroVisionError):
    """Raised when the local demo request budget is temporarily exhausted."""
