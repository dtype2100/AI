# RAG (Retrieval-Augmented Generation) API

FastAPI 기반의 RAG 시스템으로, Ollama와 벡터 데이터베이스를 활용한 문서 검색 및 생성 시스템입니다.

## 🏗️ 프로젝트 구조

```
RAG/
├── backend/                 # FastAPI 백엔드
│   ├── api/                # API 라우터
│   │   ├── routers/        # 개별 라우터
│   │   └── routes.py       # 메인 라우터
│   ├── models/             # Pydantic 모델
│   ├── services/           # 비즈니스 로직
│   └── main.py            # 애플리케이션 진입점
├── requirements.txt        # Python 의존성
├── Dockerfile             # Docker 설정
├── docker-compose.yml     # Docker Compose 설정
└── run_backend.py         # 실행 스크립트
```

## 🚀 실행 방법

### 1. 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp env.example .env
# .env 파일을 편집하여 필요한 설정을 변경

# Import 테스트 (선택사항)
python test_imports.py

# 백엔드 실행
python run_backend.py
```

### 2. 직접 실행 (backend 디렉토리에서)

```bash
cd backend
python main.py
```

### 2. Docker 실행

```bash
# Docker 이미지 빌드 및 실행
docker-compose up --build
```

## 📚 API 엔드포인트

- **문서 관리**: `/api/v1/documents`
- **검색**: `/api/v1/search`
- **쿼리**: `/api/v1/query`
- **시스템 정보**: `/api/v1/system`
- **상태 확인**: `/api/v1/health`

## 🔧 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `HOST` | 서버 호스트 | `0.0.0.0` |
| `PORT` | 서버 포트 | `8000` |
| `RELOAD` | 자동 리로드 | `true` |
| `MILVUS_HOST` | Milvus 호스트 | `localhost` |
| `MILVUS_PORT` | Milvus 포트 | `19530` |
| `OLLAMA_BASE_URL` | Ollama URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | 사용할 모델 | `llama2` |

## 📖 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 