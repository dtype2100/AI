# Custom Models 실험

이 디렉토리는 커스텀 모델 개발과 실험을 위한 공간입니다.

## 🎯 목적

- 모델 파인튜닝 실험
- 프롬프트 엔지니어링
- 커스텀 모델 개발 및 평가

## 📁 예상 파일 구조

```
custom_models/
├── fine_tuning/                # 모델 파인튜닝
│   ├── data_preparation.py     # 데이터 전처리
│   ├── training_script.py      # 학습 스크립트
│   ├── evaluation.py           # 파인튜닝 모델 평가
│   └── README.md
├── prompt_engineering/         # 프롬프트 엔지니어링
│   ├── prompt_templates.py     # 프롬프트 템플릿
│   ├── prompt_testing.py       # 프롬프트 테스트
│   ├── prompt_optimization.py  # 프롬프트 최적화
│   └── README.md
├── model_adaptation/           # 모델 적응
│   ├── domain_adaptation.py    # 도메인 적응
│   ├── task_adaptation.py      # 태스크 적응
│   └── README.md
├── config/                     # 설정 파일
├── data/                       # 데이터셋
├── models/                     # 훈련된 모델
├── results/                    # 실험 결과
└── logs/                       # 로그 파일
```

## 🔧 주요 기능

### 1. Fine-tuning
- **데이터 준비**: 도메인별 데이터 수집 및 전처리
- **모델 훈련**: LoRA, QLoRA 등 효율적 파인튜닝
- **모델 평가**: 성능 측정 및 비교

### 2. Prompt Engineering
- **템플릿 설계**: 다양한 프롬프트 템플릿
- **A/B 테스트**: 프롬프트 효과 비교
- **최적화**: 자동 프롬프트 최적화

### 3. Model Adaptation
- **도메인 적응**: 특정 도메인에 맞춘 모델 조정
- **태스크 적응**: 특정 태스크에 최적화
- **성능 튜닝**: 하이퍼파라미터 최적화

## 📋 사용 방법

### Fine-tuning
```bash
cd fine_tuning

# 데이터 준비
python data_preparation.py

# 모델 훈련
python training_script.py

# 모델 평가
python evaluation.py
```

### Prompt Engineering
```bash
cd prompt_engineering

# 프롬프트 템플릿 생성
python prompt_templates.py

# 프롬프트 테스트
python prompt_testing.py

# 프롬프트 최적화
python prompt_optimization.py
```

## 📊 평가 지표

### Fine-tuning 평가
- **정확도**: 태스크별 정확도
- **손실**: 훈련/검증 손실
- **일반화**: 새로운 데이터에 대한 성능

### Prompt Engineering 평가
- **응답 품질**: 주관적 품질 평가
- **일관성**: 동일 입력에 대한 응답 일관성
- **효율성**: 토큰 사용량 대비 품질

## 🛠️ 기술 스택

### Fine-tuning
- **PEFT**: Parameter-Efficient Fine-Tuning
- **LoRA**: Low-Rank Adaptation
- **QLoRA**: Quantized LoRA
- **Transformers**: Hugging Face Transformers

### Prompt Engineering
- **LangChain**: 프롬프트 체인 관리
- **OpenAI**: GPT 모델 활용
- **Ollama**: 로컬 모델 활용

## 📈 실험 예시

### 1. 한국어 챗봇 파인튜닝
```python
# 한국어 대화 데이터로 Llama2 파인튜닝
python fine_tuning/training_script.py \
  --model_name "llama2" \
  --dataset "korean_chat" \
  --method "lora"
```

### 2. 프롬프트 최적화
```python
# 자동 프롬프트 최적화
python prompt_engineering/prompt_optimization.py \
  --task "summarization" \
  --model "gpt-3.5-turbo" \
  --iterations 100
```

## 🔍 모니터링

- **TensorBoard**: 훈련 과정 시각화
- **Weights & Biases**: 실험 추적
- **MLflow**: 모델 버전 관리 