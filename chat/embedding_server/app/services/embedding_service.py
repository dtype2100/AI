"""
Embedding service for business logic.
"""

import time
from typing import List, Dict, Any
from ..core.embedding_model import embedding_model
from ..core.exceptions import EmbeddingError, ValidationError


class EmbeddingService:
    """Service class for embedding operations."""
    
    def __init__(self):
        self.model = embedding_model
    
    def validate_text(self, text: str) -> bool:
        """Validate input text."""
        if not text or not isinstance(text, str):
            return False
        
        if len(text.strip()) == 0:
            return False
        
        if len(text) > 10000:  # Max length limit
            return False
        
        return True
    
    def validate_texts(self, texts: List[str]) -> bool:
        """Validate list of texts."""
        if not texts or not isinstance(texts, list):
            return False
        
        if len(texts) > 100:  # Max batch size limit
            return False
        
        for text in texts:
            if not self.validate_text(text):
                return False
        
        return True
    
    def get_embedding(self, text: str) -> Dict[str, Any]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Dictionary containing embedding and metadata
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_text(text):
                raise ValidationError("Invalid input text")
            
            # Generate embedding
            embedding = self.model.get_embedding(text)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            print(f"Generated embedding for text (length: {len(text)}, time: {processing_time:.3f}s)")
            
            return {
                "embedding": embedding,
                "text_length": len(text),
                "embedding_dimension": len(embedding),
                "processing_time": processing_time,
                "model_info": self.model.get_model_info()
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Failed to generate embedding: {str(e)} (time: {processing_time:.3f}s)")
            raise EmbeddingError(f"Embedding generation failed: {str(e)}")
    
    def get_embeddings(self, texts: List[str]) -> Dict[str, Any]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            Dictionary containing embeddings and metadata
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_texts(texts):
                raise ValidationError("Invalid input texts")
            
            # Generate embeddings
            embeddings = self.model.get_embeddings(texts)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            print(f"Generated embeddings for {len(texts)} texts (time: {processing_time:.3f}s)")
            
            return {
                "embeddings": embeddings,
                "text_count": len(texts),
                "embedding_dimension": len(embeddings[0]) if embeddings else 0,
                "processing_time": processing_time,
                "model_info": self.model.get_model_info()
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Failed to generate embeddings: {str(e)} (time: {processing_time:.3f}s)")
            raise EmbeddingError(f"Embeddings generation failed: {str(e)}")
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current model status."""
        return {
            "is_loaded": self.model.is_loaded(),
            "model_info": self.model.get_model_info(),
            "service_status": "running"
        }
