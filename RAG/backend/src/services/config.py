import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Optional

load_dotenv()

class Config:
    """RAG 시스템 설정 클래스"""
    
    # 임베딩 모델 설정
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # 문서 분할 설정
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # 검색 설정
    k: int = 20
    
    # Ollama 설정
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "midm-Q8" # v"ko-llama-8B"
    
    # 벡터 저장소 설정
    vector_store_path: Optional[str] = None
    
    @classmethod
    def get_embedding_model(cls) -> HuggingFaceEmbeddings:
        """임베딩 모델을 반환합니다."""
        return HuggingFaceEmbeddings(model_name=cls.embedding_model_name)
    
    @classmethod
    def set_embedding_model_name(cls, model_name: str):
        """임베딩 모델 이름을 설정합니다."""
        cls.embedding_model_name = model_name
    
    @classmethod
    def set_chunk_settings(cls, chunk_size: int, chunk_overlap: int):
        """문서 분할 설정을 변경합니다."""
        cls.chunk_size = chunk_size
        cls.chunk_overlap = chunk_overlap
    
    @classmethod
    def set_search_settings(cls, k: int):
        """검색 설정을 변경합니다."""
        cls.k = k
    
    @classmethod
    def set_ollama_settings(cls, base_url: str, model: str):
        """Ollama 설정을 변경합니다."""
        cls.ollama_base_url = base_url
        cls.ollama_model = model
    
    @classmethod
    def set_vector_store_path(cls, path: str):
        """벡터 저장소 경로를 설정합니다."""
        cls.vector_store_path = path