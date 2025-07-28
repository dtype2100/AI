# 프로젝트 구조 검토 결과

전체 프로젝트의 구조를 검토하고 일관성을 확보한 결과를 정리합니다.

## 📁 프로젝트 전체 구조

```
chat_project/
├── .gitignore                    # 프로젝트 루트 제외 규칙
└── AI/
    ├── .gitignore                # AI 디렉토리 제외 규칙
    ├── README.md                 # AI 프로젝트 설명
    ├── RAG/                      # RAG 시스템
    │   ├── chat-dev-compose.yaml # Docker Compose 설정
    │   ├── README.md             # RAG 시스템 설명
    │   ├── api/                  # FastAPI 백엔드
    │   │   ├── Dockerfile        # ✅ 가상환경 사용으로 수정
    │   │   ├── main.py
    │   │   └── requirements.txt
    │   ├── web_ui/               # Streamlit 프론트엔드
    │   │   ├── Dockerfile        # ⚠️ python:3.10 베이스 (가상환경 없음)
    │   │   ├── app.py
    │   │   └── requirements.txt
    │   ├── notebooks/            # Jupyter 환경
    │   │   ├── Dockerfile        # ✅ 가상환경 사용으로 수정
    │   │   ├── check_venv.py     # ✅ 가상환경 확인 스크립트
    │   │   ├── VENV_TROUBLESHOOTING.md # ✅ 문제 해결 가이드
    │   │   ├── experiments/      # ✅ 실험 디렉토리 구조화
    │   │   │   ├── hf_ollama_langchain/
    │   │   │   ├── rag_pipeline/
    │   │   │   ├── model_comparison/
    │   │   │   ├── custom_models/
    │   │   │   └── .gitignore    # ✅ 실험 결과 제외
    │   │   └── requirements-*.txt
    │   ├── ollama/               # ✅ 로컬 경로로 변경
    │   └── qdrant/               # ✅ 로컬 경로로 변경
    └── template/                 # 템플릿 프로젝트
        ├── chat-dev-compose.yaml # ✅ 로컬 경로로 수정
        ├── README.md
        ├── api/                  # FastAPI 백엔드
        │   ├── Dockerfile        # ✅ 가상환경 사용으로 수정
        │   ├── main.py
        │   └── requirements.txt
        ├── web_ui/               # Streamlit 프론트엔드
        │   ├── Dockerfile        # ⚠️ python:3.10 베이스 (가상환경 없음)
        │   ├── app.py
        │   └── requirements.txt
        └── notebooks/            # Jupyter 환경
            ├── Dockerfile        # ✅ 가상환경 사용으로 수정
            └── requirements-*.txt
```

## 🔧 수정된 사항들

### 1. 가상환경 일관성 확보

#### ✅ 수정 완료된 Dockerfile들:
- `AI/RAG/notebooks/Dockerfile`
- `AI/RAG/api/Dockerfile`
- `AI/template/notebooks/Dockerfile`
- `AI/template/api/Dockerfile`

#### 주요 변경사항:
```dockerfile
# 이전 (시스템 Python 사용)
RUN pip install package
RUN python -m ipykernel install --user --name=python3
CMD ["jupyter", "lab", ...]

# 수정 후 (가상환경 Python 사용)
RUN /opt/venv/bin/pip install package
RUN /opt/venv/bin/python -m ipykernel install --user --name=venv
CMD ["/opt/venv/bin/jupyter", "lab", ...]
```

### 2. 데이터 저장 경로 통일

#### ✅ 수정 완료된 docker-compose.yaml들:
- `AI/RAG/chat-dev-compose.yaml`
- `AI/template/chat-dev-compose.yaml`

#### 주요 변경사항:
```yaml
# 이전 (Docker 볼륨 사용)
volumes:
  - ollama_data:/root/.ollama
  - qdrant_data:/qdrant/storage
volumes:
  ollama_data: {}
  qdrant_data: {}

# 수정 후 (로컬 경로 사용)
volumes:
  - ./ollama:/root/.ollama
  - ./qdrant:/qdrant/storage
# volumes 섹션 제거
```

### 3. 실험 디렉토리 구조화

#### ✅ 새로 생성된 구조:
```
experiments/
├── hf_ollama_langchain/     # Hugging Face → Ollama → LangChain
├── rag_pipeline/            # RAG 파이프라인 실험
├── model_comparison/        # 모델 성능 비교
├── custom_models/           # 커스텀 모델 개발
└── .gitignore              # 실험 결과 제외
```

## ⚠️ 주의사항

### 1. web_ui 서비스
**현재 상태**: `python:3.10` 베이스 이미지 사용 (가상환경 없음)

**권장사항**: 
- 일관성을 위해 Ubuntu + 가상환경으로 변경 고려
- 또는 현재 상태 유지 (단순한 Streamlit 앱이므로)

### 2. 베이스 이미지 차이
- **RAG/template**: `ubuntu:22.04` + 가상환경
- **web_ui**: `python:3.10` (가상환경 없음)

## 📋 적용 방법

### 1. 컨테이너 재빌드
```bash
# RAG 프로젝트
cd AI/RAG
docker-compose build

# Template 프로젝트
cd AI/template
docker-compose build
```

### 2. 컨테이너 재시작
```bash
# RAG 프로젝트
docker-compose down
docker-compose up -d

# Template 프로젝트
docker-compose down
docker-compose up -d
```

### 3. 가상환경 확인
```bash
# Jupyter 컨테이너 접속
docker exec -it jupyter bash

# 가상환경 상태 확인
python check_venv.py

# 커널 목록 확인
jupyter kernelspec list
```

## ✅ 검증 체크리스트

### 가상환경 설정
- [ ] 모든 Ubuntu 기반 Dockerfile에서 가상환경 사용
- [ ] pip 명령어가 `/opt/venv/bin/pip` 사용
- [ ] Python 명령어가 `/opt/venv/bin/python` 사용
- [ ] Jupyter 커널이 "Python (venv)"로 표시

### 데이터 저장
- [ ] Ollama 데이터가 `./ollama/` 경로에 저장
- [ ] Qdrant 데이터가 `./qdrant/` 경로에 저장
- [ ] Docker 볼륨 대신 로컬 경로 사용

### 실험 관리
- [ ] 실험 결과가 `experiments/*/results/`에 저장
- [ ] 로그 파일이 `experiments/*/logs/`에 저장
- [ ] .gitignore로 실험 결과 제외

### 일관성
- [ ] RAG와 template 프로젝트 설정 일치
- [ ] 모든 서비스가 동일한 패턴 사용
- [ ] 문서화 완료

## 🎯 향후 개선 사항

### 1. web_ui 통일
```dockerfile
# 현재
FROM python:3.10

# 제안
FROM ubuntu:22.04
# 가상환경 설정 추가
```

### 2. 공통 베이스 이미지
```dockerfile
# 공통 베이스 이미지 생성
FROM ubuntu:22.04 as base
# 가상환경 설정
# 공통 패키지 설치
```

### 3. 환경별 설정 분리
```yaml
# 개발/프로덕션 환경 분리
docker-compose.dev.yaml
docker-compose.prod.yaml
```

## 📊 프로젝트 상태 요약

| 구성 요소 | 상태 | 일관성 | 문서화 |
|-----------|------|--------|--------|
| RAG notebooks | ✅ 완료 | ✅ | ✅ |
| RAG api | ✅ 완료 | ✅ | ✅ |
| RAG web_ui | ⚠️ 주의 | ❌ | ✅ |
| Template notebooks | ✅ 완료 | ✅ | ✅ |
| Template api | ✅ 완료 | ✅ | ✅ |
| Template web_ui | ⚠️ 주의 | ❌ | ✅ |
| Docker Compose | ✅ 완료 | ✅ | ✅ |
| 실험 구조 | ✅ 완료 | ✅ | ✅ |
| .gitignore | ✅ 완료 | ✅ | ✅ |

전체적으로 프로젝트의 일관성과 관리 용이성이 크게 향상되었습니다! 🎉 