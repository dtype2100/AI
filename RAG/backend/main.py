from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

# API 라우터 import
from api.routes import router

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="RAG API",
    description="Retrieval-Augmented Generation API with Ollama and Milvus",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(router, prefix="/api/v1", tags=["RAG"])

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "RAG API에 오신 것을 환영합니다!",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "내부 서버 오류",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )

if __name__ == "__main__":
    # 서버 설정
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 RAG API 서버를 시작합니다...")
    print(f"📍 서버 주소: http://{host}:{port}")
    print(f"📚 API 문서: http://{host}:{port}/docs")
    print(f"🔍 ReDoc 문서: http://{host}:{port}/redoc")
    
    # 서버 실행 (backend 디렉토리에서 직접 실행할 때)
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
