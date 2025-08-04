from pydantic import BaseModel, Field

class DeleteRequest(BaseModel):
    document_id: str = Field(..., description="삭제할 문서 ID")

class DeleteResponse(BaseModel):
    success: bool
    message: str 