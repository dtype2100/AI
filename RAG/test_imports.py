#!/usr/bin/env python3
"""
Import 테스트 스크립트
"""
import sys
import os

def test_imports():
    """모든 모듈의 import를 테스트합니다."""
    
    # RAG 디렉토리를 Python 경로에 추가
    rag_path = os.path.dirname(__file__)
    sys.path.insert(0, rag_path)
    
    print("🔍 Import 테스트를 시작합니다...")
    
    try:
        # 1. 메인 앱 import 테스트
        print("1. main.py import 테스트...")
        from backend.main import app
        print("✅ main.py import 성공")
        
        # 2. API 라우터 import 테스트
        print("2. API 라우터 import 테스트...")
        from backend.api.routes import router
        print("✅ API 라우터 import 성공")
        
        # 3. 모델 import 테스트
        print("3. 모델 import 테스트...")
        from backend.models import HealthResponse, Document
        print("✅ 모델 import 성공")
        
        # 4. 서비스 import 테스트
        print("4. 서비스 import 테스트...")
        from backend.services.rag_service import RAGService
        print("✅ 서비스 import 성공")
        
        print("\n🎉 모든 import 테스트가 성공했습니다!")
        return True
        
    except ImportError as e:
        print(f"❌ Import 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 