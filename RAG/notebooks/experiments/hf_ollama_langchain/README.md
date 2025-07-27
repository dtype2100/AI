# Hugging Face → Ollama → LangChain 테스트 가이드

이 가이드는 Hugging Face에서 모델을 다운로드하고 Ollama로 변환한 후 LangChain으로 추론 테스트를 수행하는 방법을 설명합니다.

## 📋 사전 요구사항

### 1. Docker Compose 환경 설정
```bash
# RAG 환경 시작
cd AI/RAG
docker-compose up -d ollama
```

### 2. Python 패키지 설치
```bash
# Jupyter 컨테이너에 접속
docker exec -it jupyter bash

# 패키지 설치
pip install -r requirements-hf-ollama.txt
```

### 3. Hugging Face 토큰 설정 (선택사항)
```bash
# 환경변수 설정
export HUGGING_FACE_HUB_TOKEN="your_token_here"
```

## 🚀 사용 방법

### 방법 1: Python 스크립트 실행
```bash
# Jupyter 컨테이너에서 실행
python hf_to_ollama_test.py
```

### 방법 2: Jupyter 노트북 실행
```bash
# Jupyter 노트북 시작
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# 브라우저에서 http://localhost:8888 접속
# hf_ollama_langchain_demo.ipynb 파일 실행
```

## 📁 생성되는 파일들

### 1. 모델 파일
- `./ollama/models/`: 다운로드된 모델들이 저장되는 폴더
- `./ollama/models.json`: 설치된 모델 목록

### 2. 결과 파일
- `ollama_test_results.json`: 테스트 결과가 저장되는 JSON 파일

## 🔧 주요 기능

### 1. 모델 다운로드
```python
# Hugging Face 모델을 Ollama로 다운로드
converter = HFToOllamaConverter()
converter.pull_model_from_hf("llama2", "meta-llama/Llama-2-7b-chat-hf")
```

### 2. 추론 테스트
```python
# LangChain으로 추론 테스트
llm = Ollama(model="llama2", temperature=0.7)
response = llm("안녕하세요!")
print(response)
```

### 3. 채팅 테스트
```python
# 채팅 모델 테스트
chat_model = ChatOllama(model="llama2", temperature=0.7)
messages = [
    SystemMessage(content="당신은 도움이 되는 AI 어시스턴트입니다."),
    HumanMessage(content="파이썬을 배우고 싶어요.")
]
response = chat_model(messages)
print(response.content)
```

## 📊 지원하는 모델들

### 기본 모델
- **Llama2**: `meta-llama/Llama-2-7b-chat-hf`
- **CodeLlama**: `codellama/CodeLlama-7b-Instruct-hf`
- **Mistral**: `mistralai/Mistral-7B-Instruct-v0.2`

### 한국어 모델
- **KoAlpaca**: `beomi/KoAlpaca-Polyglot-12.8B`
- **KoBART**: `gogamza/kobart-base-v2`

## 🛠️ 커스텀 모델 생성

### Modelfile 생성
```python
# 커스텀 Modelfile 생성
modelfile_path = converter.create_custom_modelfile(
    model_name="my-model",
    hf_model_id="your-model-id",
    template="당신은 {{ .System }}\n\n사용자: {{ .Prompt }}\n\n어시스턴트: "
)
```

### 모델 생성
```python
# Modelfile로부터 모델 생성
converter.create_model_from_modelfile("my-model", modelfile_path)
```

## 🔍 모니터링 및 관리

### 1. 모델 목록 확인
```bash
# API로 확인
curl http://localhost:11434/api/tags

# Python으로 확인
converter.list_installed_models()
```

### 2. 모델 제거
```bash
# API로 제거
curl -X DELETE http://localhost:11434/api/delete \
  -H "Content-Type: application/json" \
  -d '{"name": "model-name"}'
```

### 3. 디스크 사용량 확인
```bash
# 모델 폴더 크기 확인
du -sh ./ollama/
```

## ⚠️ 주의사항

### 1. 메모리 요구사항
- **7B 모델**: 최소 8GB RAM
- **13B 모델**: 최소 16GB RAM
- **70B 모델**: 최소 64GB RAM

### 2. 디스크 공간
- **7B 모델**: ~4GB
- **13B 모델**: ~8GB
- **70B 모델**: ~40GB

### 3. 다운로드 시간
- 인터넷 속도에 따라 10분~1시간 소요
- 모델 크기가 클수록 더 오래 걸림

## 🐛 문제 해결

### 1. Ollama 서버 연결 실패
```bash
# 서버 상태 확인
docker ps | grep ollama

# 서버 재시작
docker-compose restart ollama
```

### 2. 모델 다운로드 실패
```bash
# 로그 확인
docker logs ollama

# 토큰 설정 확인
echo $HUGGING_FACE_HUB_TOKEN
```

### 3. 메모리 부족
```bash
# 사용 중인 메모리 확인
docker stats ollama

# 다른 모델 제거
curl -X DELETE http://localhost:11434/api/delete \
  -H "Content-Type: application/json" \
  -d '{"name": "large-model"}'
```

## 📈 성능 최적화

### 1. GPU 사용 (선택사항)
```yaml
# docker-compose.yml에 GPU 설정 추가
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 2. 모델 파라미터 조정
```python
# 추론 속도 vs 품질 트레이드오프
llm = Ollama(
    model="llama2",
    temperature=0.1,  # 낮을수록 일관성 높음
    top_p=0.9,
    top_k=40
)
```

## 📚 추가 자료

- [Ollama 공식 문서](https://ollama.ai/docs)
- [LangChain Ollama 통합](https://python.langchain.com/docs/integrations/llms/ollama)
- [Hugging Face 모델 허브](https://huggingface.co/models)

## 🤝 기여하기

버그 리포트나 기능 요청은 이슈를 생성해주세요.
Pull Request도 환영합니다! 