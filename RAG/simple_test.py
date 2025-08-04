#!/usr/bin/env python3
"""
간단한 Import 테스트
"""
import sys
import os

def test_simple_import():
    """간단한 import 테스트"""
    
    # RAG 디렉토리를 Python 경로에 추가
    rag_path = os.path.dirname(__file__)
    sys.path.insert(0, rag_path)
    
    print(f"🔍 Python 경로: {sys.path[0]}")
    print(f"📁 현재 디렉토리: {os.getcwd()}")
    print(f"📁 RAG 디렉토리: {rag_path}")
    
    try:
        print("\n1. backend 패키지 import 테스트...")
        import backend
        print("✅ backend 패키지 import 성공")
        
        print("\n2. backend.main import 테스트...")
        from backend import main
        print("✅ backend.main import 성공")
        
        print("\n3. FastAPI 앱 객체 테스트...")
        app = main.app
        print(f"✅ FastAPI 앱 객체 생성 성공: {type(app)}")
        
        print("\n🎉 모든 테스트가 성공했습니다!")
        return True
        
    except ImportError as e:
        print(f"❌ Import 오류: {e}")
        print(f"🔍 sys.path: {sys.path[:3]}")  # 처음 3개 경로만 출력
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_import()
    sys.exit(0 if success else 1) 