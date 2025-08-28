"""
Health check and status utilities.
"""

import time
from typing import Dict, Any
from ..core.embedding_model import embedding_model
from ..core.rerank_model import rerank_model
from .monitoring import performance_monitor


def check_model_health() -> Dict[str, Any]:
    """Check health status of all models."""
    models_health = {}
    
    # Check embedding model
    try:
        embedding_info = embedding_model.get_model_info()
        models_health["embedding"] = {
            "status": "healthy" if embedding_info["is_loaded"] else "unhealthy",
            "model_info": embedding_info
        }
    except Exception as e:
        models_health["embedding"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Check rerank model
    try:
        rerank_info = rerank_model.get_model_info()
        models_health["rerank"] = {
            "status": "healthy" if rerank_info["is_loaded"] else "unhealthy",
            "model_info": rerank_info
        }
    except Exception as e:
        models_health["rerank"] = {
            "status": "error",
            "error": str(e)
        }
    
    return models_health


def get_system_health() -> Dict[str, Any]:
    """Get comprehensive system health status."""
    try:
        # Get performance metrics
        health_status = performance_monitor.get_health_status()
        
        # Get model health
        models_health = check_model_health()
        
        # Overall health determination
        overall_status = "healthy"
        
        # Check if any models are unhealthy
        for model_name, model_health in models_health.items():
            if model_health["status"] != "healthy":
                overall_status = "degraded"
                break
        
        # Check system metrics
        if health_status["status"] != "healthy":
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": time.time(),
            "models": models_health,
            "system": health_status["system"],
            "application": health_status["application"]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "timestamp": time.time(),
            "error": f"Failed to get health status: {str(e)}"
        }


def get_service_status() -> Dict[str, Any]:
    """Get service status information."""
    return {
        "service_name": "Embedding & Rerank Server",
        "version": "1.0.0",
        "status": "running",
        "timestamp": time.time(),
        "endpoints": {
            "embedding": "/api/v1/embedding",
            "rerank": "/api/v1/rerank",
            "health": "/health",
            "status": "/status"
        }
    }
