"""
Dependency injection for API endpoints.
"""

from .v1.schemas import ErrorResponse
from ..services.embedding_service import EmbeddingService
from ..services.rerank_service import RerankService
from ..core.exceptions import EmbeddingError, RerankError, ValidationError
from fastapi import HTTPException


def get_embedding_service() -> EmbeddingService:
    """Dependency injection for embedding service."""
    return EmbeddingService()


def get_rerank_service() -> RerankService:
    """Dependency injection for rerank service."""
    return RerankService()


def handle_embedding_error(error: Exception) -> ErrorResponse:
    """Handle embedding service errors."""
    if isinstance(error, ValidationError):
        raise HTTPException(status_code=400, detail=str(error))
    elif isinstance(error, EmbeddingError):
        raise HTTPException(status_code=500, detail=str(error))
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


def handle_rerank_error(error: Exception) -> ErrorResponse:
    """Handle rerank service errors."""
    if isinstance(error, ValidationError):
        raise HTTPException(status_code=400, detail=str(error))
    elif isinstance(error, RerankError):
        raise HTTPException(status_code=500, detail=str(error))
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
