from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"message": "RAG API is working"}

