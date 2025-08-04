from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class Document(BaseModel):
    id: Optional[str] = None
    content: str = Field(..., description="문서 내용")
    title: Optional[str] = Field(None, description="문서 제목")
    source: Optional[str] = Field(None, description="문서 출처")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="추가 메타데이터")

class DocumentResponse(BaseModel):
    success: bool
    message: str
    document_ids: Optional[List[str]] = None 