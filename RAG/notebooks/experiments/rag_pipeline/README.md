# RAG Pipeline 실험

이 디렉토리는 RAG (Retrieval-Augmented Generation) 파이프라인 실험을 위한 공간입니다.

## 🎯 목적

- 문서 수집 및 전처리 파이프라인 구축
- 벡터 검색 성능 최적화
- RAG 시스템 전체 성능 평가

## 📁 예상 파일 구조

```
rag_pipeline/
├── document_ingestion.py      # 문서 수집 및 전처리
├── vector_search_test.py      # 벡터 검색 성능 테스트
├── rag_evaluation.py          # RAG 시스템 평가
├── config/
│   ├── ingestion_config.yaml  # 수집 설정
│   └── search_config.yaml     # 검색 설정
├── results/                   # 실험 결과
└── logs/                      # 로그 파일
```

## 🔧 주요 기능

### 1. 문서 수집
- 다양한 소스에서 문서 수집
- 문서 전처리 및 청킹
- 메타데이터 추출

### 2. 벡터 검색
- 임베딩 모델 성능 비교
- 검색 알고리즘 최적화
- 검색 정확도 평가

### 3. RAG 평가
- 전체 파이프라인 성능 측정
- 응답 품질 평가
- 사용자 만족도 분석

## 📋 사용 방법

```bash
# 문서 수집 실험
python document_ingestion.py

# 벡터 검색 테스트
python vector_search_test.py

# RAG 시스템 평가
python rag_evaluation.py
```

## 📊 평가 지표

- **검색 정확도**: Precision, Recall, F1-Score
- **응답 품질**: BLEU, ROUGE, 사용자 평가
- **성능**: 응답 시간, 처리량 