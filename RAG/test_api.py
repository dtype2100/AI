#!/usr/bin/env python3
"""
RAG API 테스트 스크립트
"""

import requests
import json
import time
from typing import Dict, Any

class RAGAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
    
    def test_health(self) -> bool:
        """시스템 상태 확인"""
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                print("✅ 시스템 상태: 정상")
                return True
            else:
                print(f"❌ 시스템 상태: 오류 (상태 코드: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ 시스템 연결 실패: {e}")
            return False
    
    def test_add_documents(self) -> bool:
        """문서 추가 테스트"""
        documents = [
            {
                "content": "인공지능(AI)은 기계가 학습하고 추론할 수 있도록 하는 기술입니다. 머신러닝과 딥러닝을 포함합니다.",
                "title": "인공지능 소개",
                "source": "AI 가이드북",
                "metadata": {"category": "technology", "language": "ko"}
            },
            {
                "content": "머신러닝은 데이터로부터 패턴을 학습하여 예측이나 분류를 수행하는 기술입니다.",
                "title": "머신러닝 기초",
                "source": "ML 가이드",
                "metadata": {"category": "technology", "language": "ko"}
            },
            {
                "content": "딥러닝은 신경망을 사용하여 복잡한 패턴을 학습하는 머신러닝의 한 분야입니다.",
                "title": "딥러닝 소개",
                "source": "DL 가이드",
                "metadata": {"category": "technology", "language": "ko"}
            }
        ]
        
        try:
            response = requests.post(f"{self.api_url}/documents", json=documents)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 문서 추가 성공: {result['message']}")
                return True
            else:
                print(f"❌ 문서 추가 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 문서 추가 중 오류: {e}")
            return False
    
    def test_query(self, question: str) -> bool:
        """질문 답변 테스트"""
        query_data = {
            "question": question,
            "limit": 3
        }
        
        try:
            response = requests.post(f"{self.api_url}/query", json=query_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 질문 답변 성공")
                print(f"질문: {result['query']}")
                print(f"답변: {result['response']}")
                print(f"소스 수: {len(result['sources'])}")
                return True
            else:
                print(f"❌ 질문 답변 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 질문 답변 중 오류: {e}")
            return False
    
    def test_search(self, query: str) -> bool:
        """문서 검색 테스트"""
        search_data = {
            "query": query,
            "limit": 5
        }
        
        try:
            response = requests.post(f"{self.api_url}/search", json=search_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 문서 검색 성공")
                print(f"검색어: {result['query']}")
                print(f"검색 결과 수: {result['total_found']}")
                return True
            else:
                print(f"❌ 문서 검색 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 문서 검색 중 오류: {e}")
            return False
    
    def test_system_info(self) -> bool:
        """시스템 정보 조회 테스트"""
        try:
            response = requests.get(f"{self.api_url}/system/info")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 시스템 정보 조회 성공")
                print(f"시스템 상태: {result['system_status']}")
                print(f"벡터 DB 문서 수: {result['vector_db']['documents_count']}")
                print(f"AI 모델: {result['ai_model']['current_model']}")
                return True
            else:
                print(f"❌ 시스템 정보 조회 실패: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 시스템 정보 조회 중 오류: {e}")
            return False
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 RAG API 테스트 시작")
        print("=" * 50)
        
        # 1. 시스템 상태 확인
        if not self.test_health():
            print("❌ 시스템이 실행되지 않았습니다. 서버를 먼저 시작해주세요.")
            return
        
        # 2. 문서 추가
        if not self.test_add_documents():
            print("❌ 문서 추가 테스트 실패")
            return
        
        # 잠시 대기 (벡터 DB 처리 시간)
        print("⏳ 벡터 DB 처리 대기 중...")
        time.sleep(3)
        
        # 3. 질문 답변 테스트
        print("\n📝 질문 답변 테스트")
        self.test_query("인공지능이란 무엇인가요?")
        
        # 4. 문서 검색 테스트
        print("\n🔍 문서 검색 테스트")
        self.test_search("머신러닝")
        
        # 5. 시스템 정보 조회
        print("\n📊 시스템 정보 조회")
        self.test_system_info()
        
        print("\n" + "=" * 50)
        print("✅ 모든 테스트 완료!")

def main():
    """메인 함수"""
    tester = RAGAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 