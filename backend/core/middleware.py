"""
Custom middleware for request logging, error handling, and rate limiting.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta

from core.config import Settings


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details."""
        # Start timer
        start_time = time.time()

        # Log request
        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Request failed with error: {str(e)}")
            raise

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Time: {process_time:.3f}s"
        )

        # Add custom header with processing time
        response.headers["X-Process-Time"] = str(process_time)

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to catch and handle all errors uniformly."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with error handling."""
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(
                f"Unhandled error in {request.method} {request.url.path}: {str(exc)}",
                exc_info=True
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "path": str(request.url.path)
                }
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, settings: Settings):
        super().__init__(app)
        self.settings = settings
        self.requests = defaultdict(list)
        self.enabled = settings.RATE_LIMIT_ENABLED
        self.limit = settings.RATE_LIMIT_PER_MINUTE

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limit and process request."""
        if not self.enabled:
            return await call_next(request)

        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/api/health"]:
            return await call_next(request)

        # Get client identifier
        client_id = request.client.host if request.client else "unknown"

        # Clean old requests
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff
        ]

        # Check rate limit
        if len(self.requests[client_id]) >= self.limit:
            logger.warning(f"Rate limit exceeded for {client_id}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate Limit Exceeded",
                    "message": f"Too many requests. Limit: {self.limit} per minute.",
                    "retry_after": 60
                }
            )

        # Record this request
        self.requests[client_id].append(now)

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(
            self.limit - len(self.requests[client_id])
        )

        return response


def setup_cors_middleware(app, settings: Settings):
    """
    Configure CORS middleware for the application.

    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time", "X-RateLimit-Limit", "X-RateLimit-Remaining"]
    )


def setup_custom_middleware(app, settings: Settings):
    """
    Add all custom middleware to the application.

    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    # Add in reverse order (last added = first executed)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Rate limiting with settings
    rate_limiter = RateLimitMiddleware(app, settings)
    app.middleware("http")(rate_limiter.dispatch)
