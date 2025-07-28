# Experiments 디렉토리 구조

이 디렉토리는 다양한 AI 실험과 테스트를 위한 공간입니다.

## 📁 디렉토리 구조

```
experiments/
├── hf_ollama_langchain/          # Hugging Face → Ollama → LangChain 실험
│   ├── hf_to_ollama_test.py      # 메인 테스트 스크립트
│   ├── hf_ollama_langchain_demo.ipynb  # Jupyter 노트북
│   ├── requirements.txt          # 필요한 패키지
│   └── README.md                 # 사용 가이드
├── rag_pipeline/                 # RAG 파이프라인 실험
│   ├── document_ingestion.py
│   ├── vector_search_test.py
│   └── README.md
├── model_comparison/             # 모델 성능 비교 실험
│   ├── benchmark_models.py
│   ├── performance_analysis.py
│   └── README.md
└── custom_models/                # 커스텀 모델 실험
    ├── fine_tuning/
    ├── prompt_engineering/
    └── README.md
```

## 🎯 각 디렉토리의 목적

### hf_ollama_langchain/
- Hugging Face 모델을 Ollama로 변환
- LangChain을 통한 추론 테스트
- 다양한 모델 성능 비교

### rag_pipeline/
- 문서 수집 및 전처리
- 벡터 검색 성능 테스트
- RAG 시스템 전체 파이프라인 검증

### model_comparison/
- 다양한 모델 간 성능 비교
- 벤치마크 테스트
- 성능 분석 및 시각화

### custom_models/
- 모델 파인튜닝 실험
- 프롬프트 엔지니어링
- 커스텀 모델 개발

## 📋 사용 방법

```bash
# 특정 실험 디렉토리로 이동
cd experiments/hf_ollama_langchain

# 실험 실행
python hf_to_ollama_test.py

# Jupyter 노트북 실행
jupyter notebook hf_ollama_langchain_demo.ipynb
```

## 🔄 실험 결과 관리

- 각 실험의 결과는 해당 디렉토리의 `results/` 폴더에 저장
- 실험 설정은 `config/` 폴더에 JSON/YAML 형태로 관리
- 로그는 `logs/` 폴더에 저장 