import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch

class ModelLoader:
    def __init__(self, models_dir: str = "/app/models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
    def download_embedding_model(self, model_name: str, cache_dir: str = None):
        """임베딩 모델 다운로드"""
        if cache_dir is None:
            cache_dir = str(self.models_dir / "embeddings")
        
        print(f"임베딩 모델 다운로드 중: {model_name}")
        model = SentenceTransformer(model_name, cache_folder=cache_dir)
        return model
    
    def download_language_model(self, model_name: str, cache_dir: str = None):
        """언어 모델 다운로드"""
        if cache_dir is None:
            cache_dir = str(self.models_dir / "language_models")
        
        print(f"언어 모델 다운로드 중: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
        return tokenizer, model
    
    def get_model_path(self, model_type: str, model_name: str) -> Path:
        """모델 경로 반환"""
        return self.models_dir / model_type / model_name
    
    def list_downloaded_models(self):
        """다운로드된 모델 목록 반환"""
        models = {}
        for model_type in ["embeddings", "language_models"]:
            type_dir = self.models_dir / model_type
            if type_dir.exists():
                models[model_type] = [d.name for d in type_dir.iterdir() if d.is_dir()]
        return models

# 사용 예시
if __name__ == "__main__":
    loader = ModelLoader()
    
    # 임베딩 모델 다운로드 예시
    # embedding_model = loader.download_embedding_model("sentence-transformers/all-MiniLM-L6-v2")
    
    # 언어 모델 다운로드 예시
    # tokenizer, model = loader.download_language_model("microsoft/DialoGPT-medium") 