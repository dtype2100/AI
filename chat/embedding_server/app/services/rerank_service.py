"""
Rerank service for business logic.
"""

import time
from typing import List, Dict, Any, Optional
from ..core.rerank_model import rerank_model
from ..core.exceptions import RerankError, ValidationError


class RerankService:
    """Service class for reranking operations."""
    
    def __init__(self):
        self.model = rerank_model
    
    def validate_query(self, query: str) -> bool:
        """Validate input query."""
        if not query or not isinstance(query, str):
            return False
        
        if len(query.strip()) == 0:
            return False
        
        if len(query) > 5000:  # Max query length limit
            return False
        
        return True
    
    def validate_documents(self, documents: List[str]) -> bool:
        """Validate list of documents."""
        if not documents or not isinstance(documents, list):
            return False
        
        if len(documents) > 100:  # Max documents limit
            return False
        
        for doc in documents:
            if not doc or not isinstance(doc, str):
                return False
            
            if len(doc.strip()) == 0:
                return False
            
            if len(doc) > 10000:  # Max document length limit
                return False
        
        return True
    
    def validate_top_k(self, top_k: Optional[int], documents_count: int) -> bool:
        """Validate top_k parameter."""
        if top_k is None:
            return True
        
        if not isinstance(top_k, int) or top_k < 1:
            return False
        
        if top_k > documents_count:
            return False
        
        return True
    
    def rerank_documents(
        self, 
        query: str, 
        documents: List[str],
        top_k: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Rerank documents based on query relevance.
        
        Args:
            query: Search query
            documents: List of documents to rerank
            top_k: Number of top results to return
            
        Returns:
            Dictionary containing reranked results and metadata
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if not self.validate_query(query):
                raise ValidationError("Invalid query")
            
            if not self.validate_documents(documents):
                raise ValidationError("Invalid documents")
            
            if not self.validate_top_k(top_k, len(documents)):
                raise ValidationError("Invalid top_k parameter")
            
            # Perform reranking
            reranked_results = self.model.rerank(query, documents, top_k)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Format results
            formatted_results = []
            for doc_idx, score in reranked_results:
                formatted_results.append({
                    "document_index": doc_idx,
                    "document": documents[doc_idx],
                    "relevance_score": float(score),
                    "rank": len(formatted_results) + 1
                })
            
            print(f"Reranked {len(documents)} documents for query (time: {processing_time:.3f}s)")
            
            return {
                "query": query,
                "total_documents": len(documents),
                "results": formatted_results,
                "top_k": top_k,
                "processing_time": processing_time,
                "model_info": self.model.get_model_info()
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Failed to rerank documents: {str(e)} (time: {processing_time:.3f}s)")
            raise RerankError(f"Reranking failed: {str(e)}")
    
    def rerank_batch(
        self, 
        queries: List[str], 
        documents: List[str],
        top_k: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Rerank documents for multiple queries.
        
        Args:
            queries: List of search queries
            documents: List of documents to rerank
            top_k: Number of top results to return for each query
            
        Returns:
            Dictionary containing batch rerank results and metadata
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if not queries or not isinstance(queries, list):
                raise ValidationError("Invalid queries")
            
            if len(queries) > 10:  # Max batch queries limit
                raise ValidationError("Too many queries in batch")
            
            for query in queries:
                if not self.validate_query(query):
                    raise ValidationError(f"Invalid query: {query}")
            
            if not self.validate_documents(documents):
                raise ValidationError("Invalid documents")
            
            if not self.validate_top_k(top_k, len(documents)):
                raise ValidationError("Invalid top_k parameter")
            
            # Perform batch reranking
            batch_results = self.model.rerank_batch(queries, documents, top_k)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Format batch results
            formatted_batch_results = []
            for query_idx, query_results in enumerate(batch_results):
                query = queries[query_idx]
                formatted_results = []
                
                for doc_idx, score in query_results:
                    formatted_results.append({
                        "document_index": doc_idx,
                        "document": documents[doc_idx],
                        "relevance_score": float(score),
                        "rank": len(formatted_results) + 1
                    })
                
                formatted_batch_results.append({
                    "query": query,
                    "results": formatted_results
                })
            
            print(f"Batch reranked {len(documents)} documents for {len(queries)} queries (time: {processing_time:.3f}s)")
            
            return {
                "total_queries": len(queries),
                "total_documents": len(documents),
                "batch_results": formatted_batch_results,
                "top_k": top_k,
                "processing_time": processing_time,
                "model_info": self.model.get_model_info()
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Failed to batch rerank: {str(e)} (time: {processing_time:.3f}s)")
            raise RerankError(f"Batch reranking failed: {str(e)}")
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current model status."""
        return {
            "is_loaded": self.model.is_loaded(),
            "model_info": self.model.get_model_info(),
            "service_status": "running"
        }
