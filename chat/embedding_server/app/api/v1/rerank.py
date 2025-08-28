"""
Rerank API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from ..deps import get_rerank_service, handle_rerank_error
from .schemas import (
    RerankRequest,
    RerankResponse,
    RerankBatchRequest,
    RerankBatchResponse
)
from ...services.rerank_service import RerankService
from ...core.exceptions import RerankError, ValidationError


router = APIRouter(prefix="/rerank", tags=["rerank"])


@router.post("/", response_model=RerankResponse)
async def rerank_documents(
    request: RerankRequest,
    rerank_service: RerankService = Depends(get_rerank_service)
) -> RerankResponse:
    """
    Rerank documents based on query relevance.
    
    Args:
        request: Rerank request containing query and documents
        rerank_service: Injected rerank service
        
    Returns:
        RerankResponse with reranked results and metadata
    """
    try:
        result = rerank_service.rerank_documents(
            query=request.query,
            documents=request.documents,
            top_k=request.top_k
        )
        
        return RerankResponse(
            query=result["query"],
            total_documents=result["total_documents"],
            results=result["results"],
            top_k=result["top_k"],
            processing_time=result["processing_time"],
            model_info=result["model_info"]
        )
        
    except (ValidationError, RerankError) as e:
        handle_rerank_error(e)
    except Exception as e:
        handle_rerank_error(e)


@router.post("/batch", response_model=RerankBatchResponse)
async def rerank_documents_batch(
    request: RerankBatchRequest,
    rerank_service: RerankService = Depends(get_rerank_service)
) -> RerankBatchResponse:
    """
    Rerank documents for multiple queries.
    
    Args:
        request: Batch rerank request containing queries and documents
        rerank_service: Injected rerank service
        
    Returns:
        RerankBatchResponse with batch rerank results and metadata
    """
    try:
        result = rerank_service.rerank_batch(
            queries=request.queries,
            documents=request.documents,
            top_k=request.top_k
        )
        
        return RerankBatchResponse(
            total_queries=result["total_queries"],
            total_documents=result["total_documents"],
            batch_results=result["batch_results"],
            top_k=result["top_k"],
            processing_time=result["processing_time"],
            model_info=result["model_info"]
        )
        
    except (ValidationError, RerankError) as e:
        handle_rerank_error(e)
    except Exception as e:
        handle_rerank_error(e)


@router.get("/status")
async def get_rerank_status(
    rerank_service: RerankService = Depends(get_rerank_service)
) -> Dict[str, Any]:
    """
    Get rerank service status and model information.
    
    Args:
        rerank_service: Injected rerank service
        
    Returns:
        Dictionary containing service status and model info
    """
    try:
        return rerank_service.get_model_status()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for rerank service.
    
    Returns:
        Dictionary indicating service health
    """
    return {"status": "healthy", "service": "rerank"}
