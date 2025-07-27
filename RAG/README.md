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
