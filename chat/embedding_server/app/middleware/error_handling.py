"""
Global error handling middleware.
"""

import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from ..core.exceptions import EmbeddingServerError
from ..api.v1.schemas import ErrorResponse


class ErrorHandlingMiddleware:
    """Middleware for global error handling."""
    
    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)
    
    async def __call__(self, scope, receive, send):
        """Handle errors during request processing."""
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            await self.handle_error(scope, e, send)
    
    async def handle_error(self, scope, exc: Exception, send):
        """Handle different types of errors."""
        if isinstance(exc, RequestValidationError):
            # Handle validation errors
            error_response = ErrorResponse(
                error="Validation error",
                error_type="validation_error",
                details={"errors": exc.errors()}
            )
            await self.send_error_response(send, status.HTTP_422_UNPROCESSABLE_ENTITY, error_response)
            
        elif isinstance(exc, EmbeddingServerError):
            # Handle custom application errors
            error_response = ErrorResponse(
                error=str(exc),
                error_type=type(exc).__name__
            )
            await self.send_error_response(send, status.HTTP_500_INTERNAL_SERVER_ERROR, error_response)
            
        else:
            # Handle unexpected errors
            self.logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
            error_response = ErrorResponse(
                error="Internal server error",
                error_type="internal_error"
            )
            await self.send_error_response(send, status.HTTP_500_INTERNAL_SERVER_ERROR, error_response)
    
    async def send_error_response(self, send, status_code: int, error_response: ErrorResponse):
        """Send error response."""
        response = JSONResponse(
            status_code=status_code,
            content=error_response.dict()
        )
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": response.headers.raw
        })
        await send({
            "type": "http.response.body",
            "body": response.body
        })


def get_error_handling_middleware(app):
    """Get configured error handling middleware."""
    return ErrorHandlingMiddleware(app)
