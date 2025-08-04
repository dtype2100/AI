from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class VectorDBService:
    def __init__(self):
        self.milvus_host = os.getenv("MILVUS_HOST", "localhost")
        self.milvus_port = os.getenv("MILVUS_PORT", "19530")
        self.collection_name = os.getenv("MILVUS_COLLECTION", "documents")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_size = 384  # all-MiniLM-L6-v2의 임베딩 차원
        
        # Milvus 연결
        self._connect_to_milvus()
        self._ensure_collection_exists()
    
    def _connect_to_milvus(self):
        """Milvus에 연결합니다."""
        try:
            connections.connect(
                alias="default",
                host=self.milvus_host,
                port=self.milvus_port
            )
            print(f"Milvus에 성공적으로 연결되었습니다: {self.milvus_host}:{self.milvus_port}")
        except Exception as e:
            print(f"Milvus 연결 실패: {e}")
            raise
    
    def _ensure_collection_exists(self):
        """컬렉션이 존재하지 않으면 생성합니다."""
        try:
            if utility.has_collection(self.collection_name):
                print(f"컬렉션 '{self.collection_name}'이 이미 존재합니다.")
                return
            
            # 스키마 정의
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500),
                FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=500),
                FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=2000),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.vector_size)
            ]
            
            schema = CollectionSchema(
                fields=fields,
                description="문서 벡터 저장소"
            )
            
            # 컬렉션 생성
            collection = Collection(
                name=self.collection_name,
                schema=schema,
                using="default"
            )
            
            # 인덱스 생성
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            collection.create_index(
                field_name="embedding",
                index_params=index_params
            )
            
            print(f"컬렉션 '{self.collection_name}'이 생성되었습니다.")
            
        except Exception as e:
            print(f"컬렉션 생성 중 오류 발생: {e}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """문서들을 벡터 DB에 추가합니다."""
        try:
            collection = Collection(self.collection_name)
            collection.load()
            
            # 데이터 준비
            ids = []
            contents = []
            titles = []
            sources = []
            metadatas = []
            embeddings = []
            
            for doc in documents:
                # 텍스트 임베딩 생성
                text = doc.get('content', '')
                embedding = self.embedding_model.encode(text).tolist()
                
                # 데이터 추가
                ids.append(doc.get('id', ''))
                contents.append(doc.get('content', ''))
                titles.append(doc.get('title', ''))
                sources.append(doc.get('source', ''))
                metadatas.append(str(doc.get('metadata', {})))
                embeddings.append(embedding)
            
            # 데이터 삽입
            data = [ids, contents, titles, sources, metadatas, embeddings]
            collection.insert(data)
            collection.flush()
            
            print(f"{len(documents)}개의 문서가 성공적으로 추가되었습니다.")
            return True
            
        except Exception as e:
            print(f"문서 추가 중 오류 발생: {e}")
            return False
        finally:
            if 'collection' in locals():
                collection.release()
    
    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """쿼리와 유사한 문서들을 검색합니다."""
        try:
            collection = Collection(self.collection_name)
            collection.load()
            
            # 쿼리 임베딩 생성
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # 검색 파라미터
            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 10}
            }
            
            # 유사도 검색
            results = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                output_fields=["content", "title", "source", "metadata"]
            )
            
            # 결과 포맷팅
            formatted_results = []
            for hits in results:
                for hit in hits:
                    formatted_results.append({
                        'id': hit.id,
                        'score': hit.score,
                        'content': hit.entity.get('content', ''),
                        'title': hit.entity.get('title', ''),
                        'source': hit.entity.get('source', ''),
                        'metadata': eval(hit.entity.get('metadata', '{}'))
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"검색 중 오류 발생: {e}")
            return []
        finally:
            if 'collection' in locals():
                collection.release()
    
    def delete_document(self, doc_id: str) -> bool:
        """특정 문서를 삭제합니다."""
        try:
            collection = Collection(self.collection_name)
            collection.load()
            
            # 문서 삭제
            collection.delete(f"id == '{doc_id}'")
            collection.flush()
            
            print(f"문서 {doc_id}가 성공적으로 삭제되었습니다.")
            return True
            
        except Exception as e:
            print(f"문서 삭제 중 오류 발생: {e}")
            return False
        finally:
            if 'collection' in locals():
                collection.release()
    
    def get_collection_info(self) -> Dict[str, Any]:
        """컬렉션 정보를 반환합니다."""
        try:
            collection = Collection(self.collection_name)
            stats = collection.get_statistics()
            
            return {
                'name': self.collection_name,
                'vectors_count': stats.get('row_count', 0),
                'points_count': stats.get('row_count', 0)
            }
        except Exception as e:
            print(f"컬렉션 정보 조회 중 오류 발생: {e}")
            return {
                'name': self.collection_name,
                'vectors_count': 0,
                'points_count': 0
            } 