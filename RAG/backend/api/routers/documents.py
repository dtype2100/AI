from fastapi import APIRouter, HTTPException
from typing import List

from ...services.rag_service import RAGService
from ...models import (
    Document, DocumentResponse, SearchRequest, SearchResponse,
    DeleteResponse, BatchProcessRequest, BatchProcessResponse
)

router = APIRouter()

# RAG 서비스 인스턴스 생성
rag_service = RAGService()

@router.post("/documents", response_model=DocumentResponse)
async def add_documents(documents: List[Document]):
    """문서들을 RAG 시스템에 추가합니다."""
    try:
        # Pydantic 모델을 딕셔너리로 변환
        docs = [doc.dict() for doc in documents]
        result = rag_service.add_documents(docs)
        
        return DocumentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """문서 검색을 수행합니다."""
    try:
        result = rag_service.search_documents(request.query, request.limit)
        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: str):
    """특정 문서를 삭제합니다."""
    try:
        result = rag_service.delete_document(document_id)
        return DeleteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=BatchProcessResponse)
async def batch_process_documents(request: BatchProcessRequest):
    """대량의 문서를 배치로 처리합니다."""
    try:
        # Pydantic 모델을 딕셔너리로 변환
        docs = [doc.dict() for doc in request.documents]
        result = rag_service.batch_process(docs, request.chunk_size)
        
        return BatchProcessResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 