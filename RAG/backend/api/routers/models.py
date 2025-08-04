from fastapi import APIRouter, HTTPException
import sys
import os

# 상위 디렉토리의 services 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.rag_service import RAGService

router = APIRouter()

# RAG 서비스 인스턴스 생성
rag_service = RAGService()

@router.get("/models")
async def list_models():
    """사용 가능한 AI 모델 목록을 반환합니다."""
    try:
        models = rag_service.ai_service.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_name}")
async def get_model_info(model_name: str):
    """특정 모델의 정보를 반환합니다."""
    try:
        info = rag_service.ai_service.get_model_info(model_name)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 