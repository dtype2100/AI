"""
Custom exceptions for the embedding and rerank server.
"""


class EmbeddingServerError(Exception):
    """Base exception for embedding server errors."""
    pass


class ModelLoadError(EmbeddingServerError):
    """Raised when a model fails to load."""
    pass


class EmbeddingError(EmbeddingServerError):
    """Raised when embedding generation fails."""
    pass


class RerankError(EmbeddingServerError):
    """Raised when reranking fails."""
    pass


class ValidationError(EmbeddingServerError):
    """Raised when input validation fails."""
    pass


class ModelNotLoadedError(EmbeddingServerError):
    """Raised when trying to use a model that hasn't been loaded."""
    pass


class ConfigurationError(EmbeddingServerError):
    """Raised when there's a configuration error."""
    pass
