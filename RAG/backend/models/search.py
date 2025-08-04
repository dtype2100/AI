from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="검색 쿼리")
    limit: Optional[int] = Field(10, description="검색 결과 수", ge=1, le=50)

class SearchResponse(BaseModel):
    success: bool
    documents: List[Dict[str, Any]]
    query: str
    total_found: int
    message: Optional[str] = None 