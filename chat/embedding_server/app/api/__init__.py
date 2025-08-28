"""
API modules for endpoints and schemas.
"""

from .v1.embedding import router as embedding_router
from .v1.rerank import router as rerank_router

__all__ = ["embedding_router", "rerank_router"]
