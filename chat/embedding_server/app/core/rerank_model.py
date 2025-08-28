"""
BGE rerank model management with singleton pattern.
"""

import os
from typing import List, Tuple, Optional
from sentence_transformers import CrossEncoder
from .config import settings
from .exceptions import ModelLoadError, ModelNotLoadedError


class RerankModel:
    """Singleton class for managing BGE rerank model."""
    
    _instance = None
    _model = None
    _is_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RerankModel, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._is_loaded:
            self._load_model()
    
    def _load_model(self):
        """Load the BGE rerank model."""
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                settings.rerank_model_path
            )
            
            if not os.path.exists(model_path):
                raise ModelLoadError(f"Model path does not exist: {model_path}")
            
            print(f"Loading BGE rerank model from: {model_path}")
            
            self._model = CrossEncoder(
                model_path,
                device=settings.device,
                max_length=settings.max_length
            )
            
            self._is_loaded = True
            print("BGE rerank model loaded successfully")
            
        except Exception as e:
            print(f"Failed to load BGE rerank model: {str(e)}")
            raise ModelLoadError(f"Model loading failed: {str(e)}")
    
    def rerank(
        self, 
        query: str, 
        documents: List[str],
        top_k: Optional[int] = None
    ) -> List[Tuple[int, float]]:
        """
        Rerank documents based on query relevance.
        
        Args:
            query: The search query
            documents: List of documents to rerank
            top_k: Number of top results to return (None for all)
            
        Returns:
            List of tuples (document_index, score) sorted by relevance
        """
        if not self._is_loaded:
            raise ModelNotLoadedError("Rerank model is not loaded")
        
        try:
            # Prepare pairs for cross-encoder
            pairs = [[query, doc] for doc in documents]
            
            # Get scores
            scores = self._model.predict(pairs)
            
            # Create (index, score) pairs and sort by score
            indexed_scores = list(enumerate(scores))
            indexed_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Return top_k results if specified
            if top_k is not None:
                return indexed_scores[:top_k]
            
            return indexed_scores
            
        except Exception as e:
            print(f"Failed to rerank documents: {str(e)}")
            raise ModelLoadError(f"Reranking failed: {str(e)}")
    
    def rerank_batch(
        self, 
        queries: List[str], 
        documents: List[str],
        top_k: Optional[int] = None
    ) -> List[List[Tuple[int, float]]]:
        """
        Rerank documents for multiple queries.
        
        Args:
            queries: List of search queries
            documents: List of documents to rerank
            top_k: Number of top results to return for each query
            
        Returns:
            List of rerank results for each query
        """
        if not self._is_loaded:
            raise ModelNotLoadedError("Rerank model is not loaded")
        
        try:
            results = []
            for query in queries:
                query_results = self.rerank(query, documents, top_k)
                results.append(query_results)
            
            return results
            
        except Exception as e:
            print(f"Failed to rerank batch: {str(e)}")
            raise ModelLoadError(f"Batch reranking failed: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded
    
    def get_model_info(self) -> dict:
        """Get model information."""
        return {
            "name": "bge-reranker-v2-m3-ko",
            "path": settings.rerank_model_path,
            "device": settings.device,
            "max_length": settings.max_length,
            "is_loaded": self._is_loaded
        }


# Global instance
rerank_model = RerankModel()
