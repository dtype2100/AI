# .gitignore 파일 구조 및 관리

이 문서는 프로젝트의 .gitignore 파일 구조와 관리 방법을 설명합니다.

## 📁 .gitignore 파일 위치

```
chat_project/
├── .gitignore                    # 프로젝트 루트 (전체 프로젝트)
└── AI/
    ├── .gitignore                # AI 디렉토리 (AI 관련 특화)
    └── RAG/
        └── notebooks/
            └── experiments/
                └── .gitignore    # 실험 디렉토리 (실험 결과 특화)
```

## 🎯 각 .gitignore의 역할

### 1. 프로젝트 루트 (.gitignore)
**위치**: `/chat_project/.gitignore`
**목적**: 전체 프로젝트에 대한 포괄적인 제외 규칙

**주요 제외 항목**:
- 환경 변수 파일 (.env, *.env)
- Python 관련 파일 (__pycache__, *.pyc, venv 등)
- IDE 설정 (.vscode, .idea)
- 시스템 파일 (.DS_Store, Thumbs.db)
- 대용량 파일 (모델 파일, 데이터 파일)
- 보안 관련 파일 (키 파일, 인증서)

### 2. AI 디렉토리 (.gitignore)
**위치**: `/chat_project/AI/.gitignore`
**목적**: AI/RAG 프로젝트에 특화된 제외 규칙

**주요 제외 항목**:
- Ollama 모델 및 데이터 (`RAG/ollama/`)
- Qdrant 벡터 데이터베이스 (`RAG/qdrant/`)
- 실험 결과 및 로그
- ML/AI 특정 캐시 (Hugging Face, PyTorch)
- 실험 결과 파일 (*_test_results.json)

### 3. 실험 디렉토리 (.gitignore)
**위치**: `/chat_project/AI/RAG/notebooks/experiments/.gitignore`
**목적**: 실험 결과 및 데이터 파일 제외

**주요 제외 항목**:
- 실험 결과 폴더 (`*/results/`, `*/logs/`)
- 로컬 설정 파일 (`*/config/local_*.yaml`)
- 테스트 결과 파일
- 대용량 모델 파일
- 데이터 파일 (CSV, JSON 등)

## 🔧 .gitignore 규칙 우선순위

Git은 가장 가까운 .gitignore 파일부터 적용합니다:

1. **실험 디렉토리** (.gitignore) - 가장 구체적
2. **AI 디렉토리** (.gitignore) - 중간 수준
3. **프로젝트 루트** (.gitignore) - 가장 일반적

## 📋 주요 제외 패턴

### 대용량 파일
```
# 모델 파일
*.bin
*.safetensors
*.ckpt
*.pth
*.pt
*.onnx
*.tflite
*.pb

# 데이터베이스
RAG/ollama/
RAG/qdrant/
```

### 보안 파일
```
# 환경 변수
.env
.env.local
*.env

# 키 파일
*.key
*.pem
id_rsa
id_ed25519
*.pub
secrets/
```

### 임시 파일
```
# Python 캐시
__pycache__/
*.py[cod]

# 로그 파일
*.log
logs/

# 임시 파일
*.tmp
*.temp
*.bak
```

### ML/AI 특정
```
# Hugging Face 캐시
.cache/huggingface/
.cache/torch/
.cache/transformers/

# 실험 추적
wandb/
mlruns/
mlflow.db

# TensorBoard
runs/
tensorboard_logs/
```

## ✅ 제외 규칙 확인

### 현재 제외된 파일들 확인
```bash
cd AI
git status --ignored
```

### 특정 파일이 제외되는지 확인
```bash
git check-ignore <파일명>
```

### 제외 규칙 테스트
```bash
# 예시: test_results.json이 제외되는지 확인
git check-ignore test_results.json
```

## 🚨 주의사항

### 1. 이미 추적 중인 파일
이미 Git에 추가된 파일은 .gitignore로 제외할 수 없습니다:
```bash
# 이미 추적 중인 파일 제거
git rm --cached <파일명>

# 디렉토리 전체 제거
git rm -r --cached <디렉토리명>
```

### 2. 예외 규칙 (!)
특정 파일은 제외하지 않으려면 `!` 사용:
```gitignore
# 모든 JSON 파일 제외
*.json

# 하지만 설정 파일은 포함
!config.json
!requirements.json
```

### 3. 디렉토리 vs 파일
```gitignore
# 디렉토리 전체 제외
logs/

# 특정 파일만 제외
*.log
```

## 🔄 .gitignore 업데이트

### 새로운 파일 타입 추가
1. 적절한 .gitignore 파일 선택
2. 패턴 추가
3. 테스트: `git check-ignore <새파일>`

### 실험 결과 관리
```bash
# 실험 결과 폴더 생성
mkdir experiments/my_experiment/results
mkdir experiments/my_experiment/logs

# 자동으로 제외됨 (이미 .gitignore에 포함)
```

## 📊 효과적인 .gitignore 관리

### 1. 정기적 검토
- 월 1회 .gitignore 파일 검토
- 불필요한 규칙 제거
- 새로운 파일 타입 추가

### 2. 팀 협업
- .gitignore 변경 시 팀원과 공유
- 변경 사유 문서화
- 코드 리뷰에 포함

### 3. 백업
- 중요한 설정 파일은 별도 보관
- .gitignore 변경 전 백업
- 버전 관리 시스템 활용

## 🎯 모범 사례

### 1. 계층적 구조
- 프로젝트 수준: 일반적인 규칙
- 도메인 수준: 특정 기술 스택
- 실험 수준: 결과 및 데이터

### 2. 명확한 주석
```gitignore
# ===== AI/RAG 관련 =====
# Ollama 모델 및 데이터 (대용량 파일)
RAG/ollama/
```

### 3. 정기적 테스트
```bash
# 제외 규칙 테스트
git check-ignore RAG/ollama/models/llama2.bin
git check-ignore experiments/test/results.json
```

이렇게 구조화된 .gitignore를 통해 프로젝트를 깔끔하게 관리할 수 있습니다! 