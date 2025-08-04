from fastapi import APIRouter
from ...models import HealthResponse
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """시스템 상태 확인"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now()
    ) 