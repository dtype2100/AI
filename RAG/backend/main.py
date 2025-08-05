from fastapi import FastAPI
from src.api.rag_router import router as rag_router   
 # router 객체를 rag_router로 import

app = FastAPI()

app.include_router(rag_router)

@app.get("/")
def read_root():
    return {"message": "Connected to RAG API"}