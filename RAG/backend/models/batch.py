from pydantic import BaseModel, Field
from typing import List, Optional
from .document import Document

class BatchProcessRequest(BaseModel):
    documents: List[Document] = Field(..., description="처리할 문서 목록")
    chunk_size: Optional[int] = Field(100, description="배치 크기", ge=1, le=1000)

class BatchProcessResponse(BaseModel):
    success: bool
    message: str
    total_documents: int
    processed_documents: int
    failed_documents: int 