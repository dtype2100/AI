<<<<<<< HEAD
# Chat Project - 멀티 컨테이너 RAG/챗봇 개발 환경

이 프로젝트는 RAG(검색 기반 생성) 및 챗봇 개발을 위한 멀티 컨테이너 환경을 제공합니다. 
Ollama(LLM), Qdrant(Vector DB), FastAPI(RAG API), Streamlit(Web UI), JupyterLab(노트북) 등 다양한 서비스를 Docker Compose로 손쉽게 실행할 수 있습니다.

---

## 📁 디렉터리 구조

```
chat_project/
├── api/                # FastAPI 백엔드 (RAG API)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── web_ui/             # 프론트엔드 (Streamlit)
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── notebooks/          # JupyterLab 환경 및 ML/LLM 실험
│   ├── Dockerfile
│   ├── requirements-base.txt
│   └── requirements-ml.txt
├── chat-dev-compose.yaml  # docker-compose 파일
└── README.md
```

---

## 🐳 주요 서비스 및 포트

| 서비스      | 설명                        | 포트      |
|-------------|-----------------------------|-----------|
| Ollama      | LLM 서버                    | 11434     |
| Qdrant      | 벡터스토어(Vector DB)       | 6333      |
| API         | FastAPI 기반 RAG API        | 8000      |
| Web UI      | Streamlit 프론트엔드        | 3000      |
| JupyterLab  | 데이터/ML 실험 환경         | 8888      |

---

## ⚡️ 실행 방법

1. **(필수) 환경변수 파일 생성**
   - `api/.env` 파일을 아래 내용으로 생성하세요:
     ```
     QDRANT_HOST=qdrant
     QDRANT_PORT=6333
     OLLAMA_HOST=ollama
     OLLAMA_PORT=11434
     ```

2. **도커 컴포즈 실행**
   ```bash
   docker compose -f chat-dev-compose.yaml up --build
   ```

3. **접속 주소**
   - Web UI:      http://localhost:3000
   - JupyterLab:  http://localhost:8888 (토큰: devtoken)
   - FastAPI:     http://localhost:8000/docs
   - Ollama:      http://localhost:11434
   - Qdrant:      http://localhost:6333

---

## 📝 각 서비스 설명

### 1. **api/**
- FastAPI 기반 RAG API 서버
- Ubuntu 22.04 + Python venv 환경에서 동작
- 주요 파일: `main.py`, `requirements.txt`, `Dockerfile`

### 2. **web_ui/**
- Streamlit 기반 프론트엔드
- 주요 파일: `app.py`, `requirements.txt`, `Dockerfile`

### 3. **notebooks/**
- JupyterLab 환경 (ML, LLM 실험)
- 다양한 ML/LLM 패키지 requirements-base.txt, requirements-ml.txt로 관리
- Ubuntu 22.04 + Python venv + JupyterLab

### 4. **Ollama, Qdrant**
- LLM 및 벡터스토어 컨테이너, 별도 설정 없이 바로 사용 가능

---

## ⚠️ 참고 및 주의사항

- **포트 충돌**: 이미 사용 중인 포트가 있다면 docker-compose.yaml에서 포트를 변경하세요.
- **권한 문제**: Windows 환경에서는 notebooks 볼륨 마운트 시 권한 문제가 발생할 수 있습니다.
- **의존성 추가**: ML/LLM 패키지는 notebooks/requirements-*.txt에 추가 후 재빌드하세요.
- **web_ui 가상환경**: web_ui는 기본 python:3.10 이미지를 사용합니다. venv가 필요하면 notebooks, api와 동일하게 Dockerfile을 수정하세요.

---

## 💬 문의/기여

- 추가 기능, 버그 제보, 개선 요청은 이슈로 남겨주세요.
=======
# AI 프로젝트 컬렉션

이 저장소는 다양한 AI 관련 프로젝트들을 모아놓은 컬렉션입니다. 각 프로젝트는 독립적으로 실행 가능하며, AI 기술의 다양한 응용 사례를 보여줍니다.

## 📁 프로젝트 구조

```
chat_project/
├── AI/
│   └── RAG/                    # Retrieval-Augmented Generation 프로젝트
│       ├── api/               # RAG API 서버
│       ├── web_ui/            # 웹 사용자 인터페이스
│       ├── notebooks/         # Jupyter 노트북
│       └── chat-dev-compose.yaml  # Docker Compose 설정
└── README.md
```

## 🚀 현재 포함된 프로젝트

### 1. RAG (Retrieval-Augmented Generation)
- **위치**: `AI/RAG/`
- **설명**: 문서 검색과 생성 AI를 결합한 질의응답 시스템
- **구성 요소**:
  - API 서버 (`api/`): RAG 기능을 제공하는 백엔드 API
  - 웹 UI (`web_ui/`): 사용자 친화적인 웹 인터페이스
  - 노트북 (`notebooks/`): 개발 및 실험용 Jupyter 노트북
  - Docker 설정: 컨테이너화된 배포 환경

## 🔮 향후 추가 예정 프로젝트

이 저장소는 지속적으로 확장될 예정이며, 다음과 같은 AI 프로젝트들이 추가될 계획입니다:

- **컴퓨터 비전 프로젝트**: 이미지 분류, 객체 감지, 이미지 생성
- **자연어 처리 프로젝트**: 텍스트 분류, 감정 분석, 번역
- **음성 인식/합성 프로젝트**: STT, TTS, 음성 변환
- **추천 시스템**: 협업 필터링, 콘텐츠 기반 추천
- **강화학습 프로젝트**: 게임 AI, 로봇 제어
- **대화형 AI**: 챗봇, 멀티턴 대화 시스템
- **데이터 분석 AI**: 자동화된 인사이트 생성, 예측 모델링

## 🛠️ 기술 스택

각 프로젝트는 다음과 같은 기술들을 활용합니다:

- **Python**: 주요 개발 언어
- **Docker**: 컨테이너화 및 배포
- **FastAPI**: API 개발
- **Streamlit**: 웹 UI 개발
- **Jupyter**: 데이터 분석 및 실험
- **Machine Learning Libraries**: TensorFlow, PyTorch, scikit-learn 등

## 📖 사용법

각 프로젝트는 독립적인 디렉토리에 있으며, 개별 README 파일을 통해 상세한 사용법을 제공합니다.

### RAG 프로젝트 실행 예시

```bash
cd AI/RAG
docker-compose -f chat-dev-compose.yaml up
```

## 🤝 기여하기

새로운 AI 프로젝트를 추가하거나 기존 프로젝트를 개선하고 싶으시다면:

1. 새로운 프로젝트 디렉토리를 `AI/` 폴더 아래에 생성
2. 프로젝트별 README 작성
3. Docker 설정 추가 (선택사항)
4. Pull Request 생성

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해 주세요.

---

**참고**: 이 저장소는 AI 기술 학습과 실험을 위한 개인/교육용 프로젝트입니다. 상업적 사용 시에는 각 프로젝트의 라이선스를 확인해 주세요.
>>>>>>> 1de3b1b80d282141b95bf741b9c6ca102e8ea80e
