"""
Model configuration and settings.
"""

from pydantic import BaseModel
from typing import Optional


class EmbeddingModelConfig(BaseModel):
    """Configuration for embedding models."""
    
    name: str = "BGE-m3-ko"
    path: str = "ai_models/ai_models/bge/BGE-m3-ko"
    device: str = "cpu"
    max_length: int = 512
    normalize_embeddings: bool = True


class RerankModelConfig(BaseModel):
    """Configuration for rerank models."""
    
    name: str = "bge-reranker-v2-m3-ko"
    path: str = "ai_models/bge/bge-reranker-v2-m3-ko"
    device: str = "cpu"
    max_length: int = 512


class ModelConfig(BaseModel):
    """Overall model configuration."""
    
    embedding: EmbeddingModelConfig = EmbeddingModelConfig()
    rerank: RerankModelConfig = RerankModelConfig()
    
    # Common settings
    batch_size: int = 32
    use_cache: bool = True
    cache_dir: Optional[str] = None
