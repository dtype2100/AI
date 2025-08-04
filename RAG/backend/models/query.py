from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., description="질문")
    limit: Optional[int] = Field(5, description="검색할 문서 수", ge=1, le=20)

class QueryResponse(BaseModel):
    success: bool
    response: str
    sources: List[Dict[str, Any]]
    query: str
    similarity_scores: Optional[List[float]] = None
    message: Optional[str] = None 