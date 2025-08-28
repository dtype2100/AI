"""
Main application package for the embedding and rerank server.
"""

from .core.config import settings
from .core.models import ModelConfig

__all__ = ["settings", "ModelConfig"]
