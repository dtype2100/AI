"""
Pydantic schemas for API v1 requests and responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# Base Response Schema
class BaseResponse(BaseModel):
    """Base response schema with common fields."""
    success: bool = True
    message: str = "Success"
    processing_time: Optional[float] = None


# Embedding Schemas
class EmbeddingRequest(BaseModel):
    """Request schema for single text embedding."""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to embed")


class EmbeddingResponse(BaseResponse):
    """Response schema for single text embedding."""
    embedding: List[float] = Field(..., description="Generated embedding vector")
    text_length: int = Field(..., description="Length of input text")
    embedding_dimension: int = Field(..., description="Dimension of embedding vector")
    model_info: Dict[str, Any] = Field(..., description="Model information")


class EmbeddingBatchRequest(BaseModel):
    """Request schema for batch text embedding."""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="List of texts to embed")


class EmbeddingBatchResponse(BaseResponse):
    """Response schema for batch text embedding."""
    embeddings: List[List[float]] = Field(..., description="List of generated embedding vectors")
    text_count: int = Field(..., description="Number of input texts")
    embedding_dimension: int = Field(..., description="Dimension of embedding vectors")
    model_info: Dict[str, Any] = Field(..., description="Model information")


# Rerank Schemas
class RerankRequest(BaseModel):
    """Request schema for document reranking."""
    query: str = Field(..., min_length=1, max_length=5000, description="Search query")
    documents: List[str] = Field(..., min_items=1, max_items=100, description="Documents to rerank")
    top_k: Optional[int] = Field(None, ge=1, description="Number of top results to return")


class RerankResult(BaseModel):
    """Schema for individual rerank result."""
    document_index: int = Field(..., description="Index of document in original list")
    document: str = Field(..., description="Document content")
    relevance_score: float = Field(..., description="Relevance score")
    rank: int = Field(..., description="Rank position")


class RerankResponse(BaseResponse):
    """Response schema for document reranking."""
    query: str = Field(..., description="Search query")
    total_documents: int = Field(..., description="Total number of documents")
    results: List[RerankResult] = Field(..., description="Reranked results")
    top_k: Optional[int] = Field(None, description="Number of top results returned")
    model_info: Dict[str, Any] = Field(..., description="Model information")


class RerankBatchRequest(BaseModel):
    """Request schema for batch document reranking."""
    queries: List[str] = Field(..., min_items=1, max_items=10, description="List of search queries")
    documents: List[str] = Field(..., min_items=1, max_items=100, description="Documents to rerank")
    top_k: Optional[int] = Field(None, ge=1, description="Number of top results to return for each query")


class RerankBatchResult(BaseModel):
    """Schema for batch rerank result."""
    query: str = Field(..., description="Search query")
    results: List[RerankResult] = Field(..., description="Reranked results for this query")


class RerankBatchResponse(BaseResponse):
    """Response schema for batch document reranking."""
    total_queries: int = Field(..., description="Total number of queries")
    total_documents: int = Field(..., description="Total number of documents")
    batch_results: List[RerankBatchResult] = Field(..., description="Rerank results for each query")
    top_k: Optional[int] = Field(None, description="Number of top results returned for each query")
    model_info: Dict[str, Any] = Field(..., description="Model information")


# Error Response Schema
class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Type of error")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
