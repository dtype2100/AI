from fastapi import APIRouter, HTTPException

from ...services.rag_service import RAGService
from ...models import SystemInfoResponse

router = APIRouter()

# RAG 서비스 인스턴스 생성
rag_service = RAGService()

@router.get("/system/info", response_model=SystemInfoResponse)
async def get_system_info():
    """시스템 정보를 반환합니다."""
    try:
        result = rag_service.get_system_info()
        return SystemInfoResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 