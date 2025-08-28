"""
CORS middleware configuration.
"""

from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from ..core.config import settings


def get_cors_middleware():
    """Get configured CORS middleware."""
    return FastAPICORSMiddleware(
        allow_origins=["*"],  # Allow all origins in development
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )
