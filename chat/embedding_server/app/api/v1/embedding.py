"""
Embedding API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from ..deps import get_embedding_service, handle_embedding_error
from .schemas import (
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingBatchRequest,
    EmbeddingBatchResponse
)
from ...services.embedding_service import EmbeddingService
from ...core.exceptions import EmbeddingError, ValidationError


router = APIRouter(prefix="/embedding", tags=["embedding"])


@router.post("/", response_model=EmbeddingResponse)
async def create_embedding(
    request: EmbeddingRequest,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> EmbeddingResponse:
    """
    Generate embedding for a single text.
    
    Args:
        request: Embedding request containing text
        embedding_service: Injected embedding service
        
    Returns:
        EmbeddingResponse with embedding vector and metadata
    """
    try:
        result = embedding_service.get_embedding(request.text)
        
        return EmbeddingResponse(
            embedding=result["embedding"],
            text_length=result["text_length"],
            embedding_dimension=result["embedding_dimension"],
            processing_time=result["processing_time"],
            model_info=result["model_info"]
        )
        
    except (ValidationError, EmbeddingError) as e:
        handle_embedding_error(e)
    except Exception as e:
        handle_embedding_error(e)


@router.post("/batch", response_model=EmbeddingBatchResponse)
async def create_embeddings_batch(
    request: EmbeddingBatchRequest,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> EmbeddingBatchResponse:
    """
    Generate embeddings for multiple texts.
    
    Args:
        request: Batch embedding request containing list of texts
        embedding_service: Injected embedding service
        
    Returns:
        EmbeddingBatchResponse with list of embedding vectors and metadata
    """
    try:
        result = embedding_service.get_embeddings(request.texts)
        
        return EmbeddingBatchResponse(
            embeddings=result["embeddings"],
            text_count=result["text_count"],
            embedding_dimension=result["embedding_dimension"],
            processing_time=result["processing_time"],
            model_info=result["model_info"]
        )
        
    except (ValidationError, EmbeddingError) as e:
        handle_embedding_error(e)
    except Exception as e:
        handle_embedding_error(e)


@router.get("/status")
async def get_embedding_status(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> Dict[str, Any]:
    """
    Get embedding service status and model information.
    
    Args:
        embedding_service: Injected embedding service
        
    Returns:
        Dictionary containing service status and model info
    """
    try:
        return embedding_service.get_model_status()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for embedding service.
    
    Returns:
        Dictionary indicating service health
    """
    return {"status": "healthy", "service": "embedding"}
