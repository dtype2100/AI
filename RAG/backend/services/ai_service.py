import ollama
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.model_name = os.getenv("OLLAMA_MODEL", "llama2")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Ollama 클라이언트 설정
        ollama.set_host(self.base_url)
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """AI 모델을 사용하여 응답을 생성합니다."""
        try:
            # 컨텍스트가 있으면 프롬프트에 포함
            if context:
                full_prompt = f"""다음 컨텍스트를 참고하여 질문에 답변해주세요:

컨텍스트:
{context}

질문: {prompt}

답변:"""
            else:
                full_prompt = prompt
            
            # Ollama API 호출
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ]
            )
            
            return response['message']['content']
        except Exception as e:
            print(f"AI 응답 생성 중 오류 발생: {e}")
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    def generate_response_with_sources(self, query: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """소스 문서들을 참고하여 응답을 생성합니다."""
        try:
            # 관련 문서들을 컨텍스트로 구성
            context_parts = []
            for i, doc in enumerate(documents, 1):
                context_parts.append(f"문서 {i}:\n{doc.get('content', '')}\n")
            
            context = "\n".join(context_parts)
            
            # 프롬프트 구성
            prompt = f"""다음 문서들을 참고하여 질문에 답변해주세요. 
답변할 때는 제공된 문서의 정보를 기반으로 하되, 문서에 없는 내용은 추측하지 마세요.
답변 후에는 참고한 문서의 출처를 명시해주세요.

질문: {query}

답변:"""
            
            # AI 응답 생성
            response = self.generate_response(prompt, context)
            
            # 소스 정보 구성
            sources = []
            for doc in documents:
                sources.append({
                    'id': doc.get('id'),
                    'title': doc.get('title', ''),
                    'source': doc.get('source', ''),
                    'score': doc.get('score', 0.0)
                })
            
            return {
                'response': response,
                'sources': sources,
                'query': query
            }
        except Exception as e:
            print(f"소스 기반 응답 생성 중 오류 발생: {e}")
            return {
                'response': f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}",
                'sources': [],
                'query': query
            }
    
    def list_models(self) -> List[str]:
        """사용 가능한 모델 목록을 반환합니다."""
        try:
            models = ollama.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            print(f"모델 목록 조회 중 오류 발생: {e}")
            return []
    
    def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """모델 정보를 반환합니다."""
        try:
            model = model_name or self.model_name
            info = ollama.show(model)
            return {
                'name': info.get('name', ''),
                'size': info.get('size', 0),
                'modified_at': info.get('modified_at', ''),
                'parameters': info.get('parameters', '')
            }
        except Exception as e:
            print(f"모델 정보 조회 중 오류 발생: {e}")
            return {} 