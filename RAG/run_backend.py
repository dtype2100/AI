#!/usr/bin/env python3
"""
RAG Backend 실행 스크립트
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# backend 디렉토리를 Python 경로에 추가
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, os.path.dirname(__file__))  # RAG 디렉토리를 Python 경로에 추가
os.chdir(backend_path)  # 작업 디렉토리를 backend로 변경

# 환경 변수 로드
load_dotenv()

if __name__ == "__main__":
    # 서버 설정
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 RAG API 서버를 시작합니다...")
    print(f"📍 서버 주소: http://{host}:{port}")
    print(f"📚 API 문서: http://{host}:{port}/docs")
    print(f"🔍 ReDoc 문서: http://{host}:{port}/redoc")
    
    # 서버 실행
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    ) 