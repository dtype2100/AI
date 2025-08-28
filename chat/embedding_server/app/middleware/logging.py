"""
Logging middleware for request tracking.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    def __init__(self, app, logger: logging.Logger = None):
        super().__init__(app)
        self.logger = logger or logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log information."""
        start_time = time.time()
        
        # Log request
        self.logger.info(
            f"Request started: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            self.logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Time: {process_time:.3f}s"
            )
            
            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log error
            self.logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"Error: {str(e)} "
                f"Time: {process_time:.3f}s"
            )
            
            raise
