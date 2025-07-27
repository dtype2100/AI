# RAG Notebooks

이 디렉토리는 RAG (Retrieval-Augmented Generation) 시스템 개발을 위한 Jupyter 노트북과 실험 환경입니다.

## 📁 디렉토리 구조

```
notebooks/
├── experiments/                    # 실험 디렉토리
│   ├── hf_ollama_langchain/       # Hugging Face → Ollama → LangChain 실험
│   │   ├── hf_to_ollama_test.py   # 메인 테스트 스크립트
│   │   ├── hf_ollama_langchain_demo.ipynb  # Jupyter 노트북
│   │   ├── requirements.txt       # 필요한 패키지
│   │   └── README.md              # 사용 가이드
│   ├── rag_pipeline/              # RAG 파이프라인 실험
│   │   └── README.md
│   ├── model_comparison/          # 모델 성능 비교 실험
│   │   └── README.md
│   ├── custom_models/             # 커스텀 모델 실험
│   │   └── README.md
│   └── README.md                  # 실험 디렉토리 가이드
├── requirements-base.txt          # 기본 패키지
├── requirements-ml.txt            # ML 관련 패키지
└── Dockerfile                     # Jupyter 환경 Docker 설정
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# RAG 환경 시작
cd AI/RAG
docker-compose up -d ollama qdrant jupyter

# Jupyter 컨테이너에 접속
docker exec -it jupyter bash
```

### 2. 패키지 설치
```bash
# 기본 패키지 설치
pip install -r requirements-base.txt
pip install -r requirements-ml.txt

# 특정 실험 패키지 설치
cd experiments/hf_ollama_langchain
pip install -r requirements.txt
```

### 3. 실험 실행
```bash
# Hugging Face → Ollama → LangChain 실험
cd experiments/hf_ollama_langchain
python hf_to_ollama_test.py

# Jupyter 노트북 실행
jupyter notebook hf_ollama_langchain_demo.ipynb
```

## 🎯 실험 카테고리

### 1. HF Ollama LangChain (`experiments/hf_ollama_langchain/`)
- Hugging Face 모델을 Ollama로 변환
- LangChain을 통한 추론 테스트
- 다양한 모델 성능 비교

### 2. RAG Pipeline (`experiments/rag_pipeline/`)
- 문서 수집 및 전처리 파이프라인
- 벡터 검색 성능 최적화
- RAG 시스템 전체 성능 평가

### 3. Model Comparison (`experiments/model_comparison/`)
- 다양한 모델 간 성능 비교
- 벤치마크 테스트 수행
- 성능 분석 및 시각화

### 4. Custom Models (`experiments/custom_models/`)
- 모델 파인튜닝 실험
- 프롬프트 엔지니어링
- 커스텀 모델 개발

## 📊 실험 결과 관리

각 실험 디렉토리에는 다음 구조가 권장됩니다:

```
experiment_name/
├── config/           # 설정 파일 (JSON/YAML)
├── data/             # 데이터셋
├── models/           # 훈련된 모델
├── results/          # 실험 결과
├── logs/             # 로그 파일
└── README.md         # 실험 설명
```

## 🔧 개발 환경

### Jupyter 환경
- **포트**: 8888
- **토큰**: devtoken
- **URL**: http://localhost:8888

### 지원하는 서비스
- **Ollama**: 로컬 LLM 서버 (포트: 11434)
- **Qdrant**: 벡터 데이터베이스 (포트: 6333)
- **FastAPI**: 백엔드 API (포트: 8000)

## 📋 실험 가이드라인

### 1. 실험 설계
- 명확한 목표와 가설 설정
- 적절한 평가 지표 선택
- 재현 가능한 실험 환경 구성

### 2. 코드 관리
- 모듈화된 코드 작성
- 설정 파일 분리
- 로깅 및 에러 처리

### 3. 결과 문서화
- 실험 과정 상세 기록
- 결과 분석 및 해석
- 향후 개선 방향 제시

## 🐛 문제 해결

### Jupyter 접속 문제
```bash
# 컨테이너 상태 확인
docker ps | grep jupyter

# 컨테이너 재시작
docker-compose restart jupyter
```

### 패키지 설치 문제
```bash
# 패키지 캐시 정리
pip cache purge

# 특정 버전 설치
pip install package==version
```

### 메모리 부족
```bash
# 사용 중인 메모리 확인
docker stats

# 불필요한 컨테이너 정리
docker system prune
```

## 📚 참고 자료

- [Jupyter 공식 문서](https://jupyter.org/documentation)
- [Docker Compose 가이드](https://docs.docker.com/compose/)
- [LangChain 문서](https://python.langchain.com/)
- [Ollama 문서](https://ollama.ai/docs)

## 🤝 기여하기

새로운 실험을 추가하거나 기존 실험을 개선하고 싶다면:

1. 해당 실험 디렉토리에 코드 추가
2. README.md 파일 업데이트
3. requirements.txt 파일 관리
4. 실험 결과 문서화 