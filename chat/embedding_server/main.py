"""
Main FastAPI application entry point.
Manages routers and middleware only.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.logger import setup_logger
from app.api import embedding_router, rerank_router
from app.utils.health import get_system_health, get_service_status


# Setup logger
logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Starting Embedding & Rerank Server...")
    logger.info(f"Server running on {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Embedding & Rerank Server...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="High-performance embedding and reranking API server",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(embedding_router, prefix="/api/v1")
app.include_router(rerank_router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Embedding & Rerank Server",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "/status"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return get_system_health()


# Status endpoint
@app.get("/status")
async def status_check():
    """Service status endpoint."""
    return get_service_status()


# API info endpoint
@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": "Embedding & Rerank API",
        "version": "1.0.0",
        "endpoints": {
            "embedding": {
                "base": "/api/v1/embedding",
                "endpoints": [
                    "POST / - Single text embedding",
                    "POST /batch - Batch text embedding",
                    "GET /status - Model status",
                    "GET /health - Service health"
                ]
            },
            "rerank": {
                "base": "/api/v1/rerank",
                "endpoints": [
                    "POST / - Document reranking",
                    "POST /batch - Batch document reranking",
                    "GET /status - Model status",
                    "GET /health - Service health"
                ]
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

