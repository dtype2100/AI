import os
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings, OllamaChatModel


class RAGService:
    def __init__(
        self,
        pdf_path: str = "example.pdf",
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "rag-example",
        embedding_model: Optional[str] = None,
        llm_model: Optional[str] = None,
    ):
        """RAGService 초기화

        Args:
            pdf_path: 로드할 PDF 문서 경로.
            qdrant_url: Qdrant 서버 URL.
            collection_name: 사용할 컬렉션 이름.
            embedding_model: 임베딩 모델 이름. 지정하지 않으면 ``EMBEDDING_MODEL``
                환경 변수를 사용합니다.
            llm_model: LLM 모델 이름. 지정하지 않으면 ``LLM_MODEL`` 환경 변수를 사용합니다.

        Raises:
            ValueError: 임베딩 또는 LLM 모델을 찾을 수 없는 경우.
        """

        embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL")
        if not embedding_model:
            raise ValueError(
                "embedding_model is required. Set EMBEDDING_MODEL or pass as argument."
            )

        llm_model = llm_model or os.getenv("LLM_MODEL")
        if not llm_model:
            raise ValueError(
                "llm_model is required. Set LLM_MODEL or pass as argument."
            )

        # 1. PDF 문서 로드
        self.loader = PyPDFLoader(pdf_path)
        self.documents = self.loader.load()

        # 2. 문서 분할
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.docs = self.text_splitter.split_documents(self.documents)

        # 3. 임베딩 생성 (환경 변수 또는 인자로 지정된 모델 사용)
        self.embeddings = OllamaEmbeddings(model=embedding_model)

        # 4. Qdrant 벡터스토어에 저장
        self.qdrant = Qdrant.from_documents(
            self.docs,
            self.embeddings,
            url=qdrant_url,
            collection_name=collection_name,
        )

        # 6. LLM 모델 초기화 (환경 변수 또는 인자로 지정된 모델 사용)
        self.llm = OllamaChatModel(model=llm_model)

    def search_similar_docs(self, query: str, k: int = 3):
        # 5. 쿼리와 유사한 문서 검색
        similar_docs = self.qdrant.similarity_search(query, k=k)
        return similar_docs

    def generate_answer(self, query: str, k: int = 3):
        similar_docs = self.search_similar_docs(query, k)
        context = "\n".join([doc.page_content for doc in similar_docs])
        prompt = f"다음 내용을 참고하여 질문에 답변해 주세요:\n\n{context}\n\n질문: {query}"
        response = self.llm.invoke(prompt)
        return response


# 사용 예시 (예시이므로 실제 서비스에서는 별도 함수나 API에서 호출)
# 환경 변수 EMBEDDING_MODEL, LLM_MODEL 설정 후 인스턴스화 가능
# rag_service = RAGService()
# query = "이 문서의 주요 내용은 무엇인가요?"
# answer = rag_service.generate_answer(query)
# print(answer)

