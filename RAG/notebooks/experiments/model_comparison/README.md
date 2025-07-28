# Model Comparison 실험

이 디렉토리는 다양한 AI 모델의 성능을 비교하고 분석하는 실험을 위한 공간입니다.

## 🎯 목적

- 다양한 모델 간 성능 비교
- 벤치마크 테스트 수행
- 성능 분석 및 시각화

## 📁 예상 파일 구조

```
model_comparison/
├── benchmark_models.py         # 모델 벤치마크 테스트
├── performance_analysis.py     # 성능 분석 및 시각화
├── model_evaluation.py         # 모델 평가 지표 계산
├── config/
│   ├── benchmark_config.yaml   # 벤치마크 설정
│   └── models_config.yaml      # 모델 설정
├── results/                    # 실험 결과
│   ├── benchmarks/             # 벤치마크 결과
│   ├── analysis/               # 분석 결과
│   └── plots/                  # 시각화 차트
└── logs/                       # 로그 파일
```

## 🔧 주요 기능

### 1. 모델 벤치마크
- 다양한 모델의 추론 속도 측정
- 메모리 사용량 분석
- 정확도 및 품질 평가

### 2. 성능 분석
- 모델 간 성능 비교
- 통계적 분석
- 성능 트렌드 분석

### 3. 시각화
- 성능 차트 생성
- 비교 그래프
- 대시보드 생성

## 📋 사용 방법

```bash
# 모델 벤치마크 실행
python benchmark_models.py

# 성능 분석
python performance_analysis.py

# 모델 평가
python model_evaluation.py
```

## 📊 평가 지표

### 속도 지표
- **추론 시간**: 토큰당 처리 시간
- **처리량**: 초당 처리 토큰 수
- **지연 시간**: 응답 시작까지의 시간

### 품질 지표
- **정확도**: 정답률
- **BLEU Score**: 기계번역 품질
- **ROUGE Score**: 요약 품질
- **사용자 평가**: 주관적 품질 평가

### 리소스 지표
- **메모리 사용량**: GPU/CPU 메모리
- **전력 소비**: 에너지 효율성
- **모델 크기**: 파라미터 수

## 📈 비교 대상 모델

### 언어 모델
- Llama2 (7B, 13B, 70B)
- GPT 모델들
- Mistral 모델들
- 한국어 특화 모델들

### 임베딩 모델
- sentence-transformers
- OpenAI Embeddings
- Cohere Embeddings

## 🎨 시각화 예시

- 성능 비교 차트
- 속도 vs 품질 트레이드오프
- 리소스 사용량 분석
- 시간별 성능 변화 