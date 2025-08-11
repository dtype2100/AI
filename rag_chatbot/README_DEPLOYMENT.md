# 🚀 RAG Chatbot 배포 가이드

## 📋 **사전 요구사항**

- Docker & Docker Compose 설치
- 로컬 GGUF 모델 파일 준비 (SmolLM3-3B-GGUF)

## 🔧 **배포 단계**

### **1단계: 모델 파일 준비**

로컬 GGUF 모델이 다음 경로에 있는지 확인:
```
rag_chatbot/ollama_models/SmolLM3-3B-GGUF/SmolLM3-Q4_K_M.gguf
```

### **2단계: 서비스 시작**

```bash
# 프로젝트 루트 디렉토리에서
cd rag_chatbot

# 서비스 시작
docker-compose up -d
```

### **3단계: 모델 빌드 확인**

```bash
# 모델 빌드 상태 확인
docker-compose logs ollama-init

# Ollama에서 모델 목록 확인
docker exec ollama ollama list
```

### **4단계: 서비스 상태 확인**

```bash
# 모든 서비스 상태 확인
docker-compose ps

# 백엔드 헬스체크
curl http://localhost:8000/healthz
```

## 📊 **서비스 구성**

- **Ollama**: LLM 서비스 (포트 11434)
- **Qdrant**: 벡터 데이터베이스 (포트 6333)
- **Backend**: RAG API 서비스 (포트 8000)

## 🔍 **문제 해결**

### **모델 빌드 실패 시**

```bash
# 모델 빌드 재시도
docker-compose restart ollama-init

# 로그 확인
docker-compose logs ollama-init
```

### **서비스 의존성 문제**

```bash
# 모든 서비스 재시작
docker-compose down
docker-compose up -d
```

## 📝 **환경변수 설정**

주요 환경변수:
- `OLLAMA_MODEL=smollm3-3b`
- `QDRANT_URL=http://qdrant:6333`
- `EMBEDDING_MODEL_NAME=/app/rag_chatbot/embedding_models/BGE-m3-ko`

## 🎯 **사용법**

1. 서비스가 모두 시작될 때까지 대기
2. `http://localhost:8000/docs`에서 API 문서 확인
3. RAG API를 통해 문서 질의 시작
