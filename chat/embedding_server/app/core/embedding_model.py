"""
BGE embedding model management with singleton pattern.
"""

import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from .config import settings
from .exceptions import ModelLoadError, ModelNotLoadedError


class EmbeddingModel:
    """Singleton class for managing BGE embedding model."""
    
    _instance = None
    _model = None
    _is_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._is_loaded:
            self._load_model()
    
    def _load_model(self):
        """Load the BGE embedding model."""
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                settings.embedding_model_path
            )
            
            if not os.path.exists(model_path):
                raise ModelLoadError(f"Model path does not exist: {model_path}")
            
            print(f"Loading BGE embedding model from: {model_path}")
            
            self._model = HuggingFaceEmbeddings(
                model_name=model_path,
                model_kwargs={'device': settings.device},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            self._is_loaded = True
            print("BGE embedding model loaded successfully")
            
        except Exception as e:
            print(f"Failed to load BGE embedding model: {str(e)}")
            raise ModelLoadError(f"Model loading failed: {str(e)}")
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        if not self._is_loaded:
            raise ModelNotLoadedError("Embedding model is not loaded")
        
        try:
            embedding = self._model.embed_query(text)
            return embedding
        except Exception as e:
            print(f"Failed to generate embedding: {str(e)}")
            raise ModelLoadError(f"Embedding generation failed: {str(e)}")
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        if not self._is_loaded:
            raise ModelNotLoadedError("Embedding model is not loaded")
        
        try:
            embeddings = self._model.embed_documents(texts)
            return embeddings
        except Exception as e:
            print(f"Failed to generate embeddings: {str(e)}")
            raise ModelLoadError(f"Embeddings generation failed: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded
    
    def get_model_info(self) -> dict:
        """Get model information."""
        return {
            "name": "BGE-m3-ko",
            "path": settings.embedding_model_path,
            "device": settings.device,
            "is_loaded": self._is_loaded
        }


# Global instance
embedding_model = EmbeddingModel()
