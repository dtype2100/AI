import os
from typing import List, Dict, Any, Generator
from langchain_ollama import OllamaChatModel

class ChatService:
    """간단한 채팅 서비스"""
    
    def __init__(self, model_name: str = "SmolLM3-Q4_K_M"):
        """
        ChatService 초기화
        
        Args:
            model_name: 사용할 모델 이름 (환경변수 OLLAMA_MODEL로도 설정 가능)
        """
        # .env 파일 로드 (한 번만 실행)
        self._load_env()
        
        # 환경변수에서 모델명 가져오기 (기본값: 전달받은 model_name)
        self.model_name = os.getenv("SmolLM3-Q4_K_M", model_name)
        
        # Ollama 모델 초기화
        self.model = OllamaChatModel(
            model=self.model_name,
            base_url="http://localhost:11434"
        )
    
    def _load_env(self):
        """환경변수 로드 (한 번만 실행)"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            # dotenv가 설치되지 않은 경우 무시
            pass
    
    def chat(self, messages: List[Dict[str, Any]]) -> str:
        """일반 채팅"""
        return self.model.invoke(messages).content
    
    def chat_stream(self, messages: List[Dict[str, Any]]) -> Generator[str, None, None]:
        """스트리밍 채팅"""
        for chunk in self.model.stream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                yield chunk.content
    
    def chat_with_tools(self, messages: List[Dict[str, Any]], tools: List[Any]) -> str:
        """툴을 사용한 채팅"""
        return self.model.invoke(messages, tools=tools).content