"""
Server settings and configuration management.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server settings
    app_name: str = "Embedding & Rerank Server"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Model paths (relative to app root)
    embedding_model_path: str = os.getenv("EMBEDDING_MODEL_PATH", "ai_models/ai_models/bge/BGE-m3-ko")
    rerank_model_path: str = os.getenv("RERANK_MODEL_PATH", "ai_models/bge/bge-reranker-v2-m3-ko")
        
    # Model settings
    device: str = "cpu"  # "cpu" or "cuda"
    max_length: int = 512
    
    # Performance settings
    batch_size: int = 32
    max_concurrent_requests: int = 10
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
