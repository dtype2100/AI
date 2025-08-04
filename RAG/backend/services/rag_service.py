from typing import List, Dict, Any, Optional
from .vector_db import VectorDBService
from .ai_service import AIService
import uuid
import json

class RAGService:
    def __init__(self):
        self.vector_db = VectorDBService()
        self.ai_service = AIService()
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """문서들을 RAG 시스템에 추가합니다."""
        try:
            # 각 문서에 고유 ID 할당
            for doc in documents:
                if 'id' not in doc:
                    doc['id'] = str(uuid.uuid4())
            
            # 벡터 DB에 문서 추가
            success = self.vector_db.add_documents(documents)
            
            if success:
                return {
                    'success': True,
                    'message': f'{len(documents)}개의 문서가 성공적으로 추가되었습니다.',
                    'document_ids': [doc['id'] for doc in documents]
                }
            else:
                return {
                    'success': False,
                    'message': '문서 추가 중 오류가 발생했습니다.'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'문서 추가 중 오류가 발생했습니다: {str(e)}'
            }
    
    def query(self, question: str, limit: int = 5) -> Dict[str, Any]:
        """질문에 대한 RAG 응답을 생성합니다."""
        try:
            # 1. 벡터 검색으로 관련 문서 찾기
            similar_docs = self.vector_db.search_similar(question, limit)
            
            if not similar_docs:
                return {
                    'success': False,
                    'message': '관련 문서를 찾을 수 없습니다.',
                    'response': '죄송합니다. 질문과 관련된 문서를 찾을 수 없습니다.',
                    'sources': []
                }
            
            # 2. AI를 사용하여 응답 생성
            ai_response = self.ai_service.generate_response_with_sources(question, similar_docs)
            
            return {
                'success': True,
                'response': ai_response['response'],
                'sources': ai_response['sources'],
                'query': question,
                'similarity_scores': [doc['score'] for doc in similar_docs]
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'질문 처리 중 오류가 발생했습니다: {str(e)}',
                'response': f'죄송합니다. 질문 처리 중 오류가 발생했습니다: {str(e)}',
                'sources': []
            }
    
    def search_documents(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """문서 검색만 수행합니다."""
        try:
            similar_docs = self.vector_db.search_similar(query, limit)
            
            return {
                'success': True,
                'documents': similar_docs,
                'query': query,
                'total_found': len(similar_docs)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'문서 검색 중 오류가 발생했습니다: {str(e)}',
                'documents': []
            }
    
    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """특정 문서를 삭제합니다."""
        try:
            success = self.vector_db.delete_document(doc_id)
            
            if success:
                return {
                    'success': True,
                    'message': f'문서 {doc_id}가 성공적으로 삭제되었습니다.'
                }
            else:
                return {
                    'success': False,
                    'message': '문서 삭제 중 오류가 발생했습니다.'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'문서 삭제 중 오류가 발생했습니다: {str(e)}'
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """시스템 정보를 반환합니다."""
        try:
            collection_info = self.vector_db.get_collection_info()
            model_info = self.ai_service.get_model_info()
            available_models = self.ai_service.list_models()
            
            return {
                'vector_db': {
                    'collection_name': collection_info.get('name', ''),
                    'documents_count': collection_info.get('points_count', 0),
                    'vectors_count': collection_info.get('vectors_count', 0)
                },
                'ai_model': {
                    'current_model': self.ai_service.model_name,
                    'model_info': model_info,
                    'available_models': available_models
                },
                'system_status': 'operational'
            }
        except Exception as e:
            return {
                'system_status': 'error',
                'error_message': str(e)
            }
    
    def batch_process(self, documents: List[Dict[str, Any]], chunk_size: int = 100) -> Dict[str, Any]:
        """대량의 문서를 배치로 처리합니다."""
        try:
            total_docs = len(documents)
            processed_docs = 0
            failed_docs = 0
            
            # 배치로 나누어 처리
            for i in range(0, total_docs, chunk_size):
                batch = documents[i:i + chunk_size]
                result = self.add_documents(batch)
                
                if result['success']:
                    processed_docs += len(batch)
                else:
                    failed_docs += len(batch)
            
            return {
                'success': True,
                'message': f'배치 처리 완료: {processed_docs}개 성공, {failed_docs}개 실패',
                'total_documents': total_docs,
                'processed_documents': processed_docs,
                'failed_documents': failed_docs
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'배치 처리 중 오류가 발생했습니다: {str(e)}'
            } 