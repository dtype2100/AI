from fastapi import APIRouter, HTTPException

from ...services.rag_service import RAGService
from ...models import QueryRequest, QueryResponse

router = APIRouter()

# RAG 서비스 인스턴스 생성
rag_service = RAGService()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """질문에 대한 RAG 응답을 생성합니다."""
    try:
        result = rag_service.query(request.question, request.limit)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 