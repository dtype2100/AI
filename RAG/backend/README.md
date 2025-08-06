# RAG Backend

`RAGService`는 모델 이름을 인자로 받거나 환경 변수를 통해 읽어옵니다.

환경 변수:

- `EMBEDDING_MODEL`: `OllamaEmbeddings`에 사용할 임베딩 모델 이름
- `LLM_MODEL`: `OllamaChatModel`에 사용할 LLM 모델 이름

이 값들이 설정되어 있지 않으면 `RAGService` 초기화 시 예외가 발생합니다.

