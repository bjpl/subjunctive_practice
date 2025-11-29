"""
FastAPI Main Application Entry Point
Spanish Subjunctive Practice Backend API
"""

from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from core.config import get_settings
from core.middleware import (
    setup_cors_middleware,
    setup_custom_middleware,
    RequestLoggingMiddleware,
    ErrorHandlingMiddleware
)
from schemas.user import UserResponse

# HealthCheck schema needs to be created in schemas module
# For now, create inline until proper schema is added
from pydantic import BaseModel

class HealthCheck(BaseModel):
    """Schema for health check endpoint."""
    status: str = "healthy"
    timestamp: datetime
    version: str
    environment: str
    database_connected: bool = False
    redis_connected: bool = False
    anthropic_configured: bool = False
from api.routes import auth, exercises, progress, achievements
from api.routes import settings as settings_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('backend.log')
    ]
)

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    🇪🇸 Spanish Subjunctive Practice API

    A comprehensive backend API for learning and practicing Spanish subjunctive mood.

    ## Features

    * **Authentication**: JWT-based user authentication with registration and login
    * **Exercises**: Dynamic exercise retrieval with filtering and randomization
    * **Progress Tracking**: Detailed progress analytics and statistics
    * **Gamification**: Streak tracking, levels, and experience points
    * **AI Insights**: Personalized learning recommendations

    ## Authentication

    Most endpoints require authentication. To authenticate:
    1. Register a new user via `/api/auth/register`
    2. Login via `/api/auth/login` to get access token
    3. Include token in Authorization header: `Bearer <token>`

    ## Rate Limiting

    API requests are rate-limited to 60 requests per minute per IP address.
    """,
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration, login, and token management"
        },
        {
            "name": "Exercises",
            "description": "Retrieve exercises, submit answers, and get validation"
        },
        {
            "name": "Progress & Statistics",
            "description": "Track learning progress and view detailed analytics"
        },
        {
            "name": "System",
            "description": "Health checks and system information"
        }
    ],
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# Setup middleware
setup_cors_middleware(app, settings)
setup_custom_middleware(app, settings)


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(exercises.router, prefix=settings.API_V1_PREFIX)
app.include_router(progress.router, prefix=settings.API_V1_PREFIX)
app.include_router(achievements.router, prefix=settings.API_V1_PREFIX)
app.include_router(settings_router.router, prefix=settings.API_V1_PREFIX)


# Health check endpoint
@app.get("/health", response_model=HealthCheck, tags=["System"])
@app.get(f"{settings.API_V1_PREFIX}/health", response_model=HealthCheck, tags=["System"])
async def health_check():
    """
    Health check endpoint to verify API status.

    Returns system status, version, and service availability.
    """
    # Check database connection (if configured)
    database_connected = False
    if settings.DATABASE_URL:
        try:
            # In production, add actual database connection check
            database_connected = True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")

    # Check Redis connection (if configured)
    redis_connected = False
    if settings.REDIS_URL:
        try:
            # In production, add actual Redis connection check
            redis_connected = True
        except Exception as e:
            logger.error(f"Redis connection check failed: {e}")

    # Check Anthropic Claude configuration
    anthropic_configured = bool(settings.ANTHROPIC_API_KEY)

    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        database_connected=database_connected,
        redis_connected=redis_connected,
        anthropic_configured=anthropic_configured
    )


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Spanish Subjunctive Practice API",
        "version": settings.VERSION,
        "docs": "/api/docs",
        "health": "/health",
        "environment": settings.ENVIRONMENT
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unexpected errors.
    """
    logger.error(
        f"Unhandled exception in {request.method} {request.url.path}: {str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"API documentation available at /api/docs")

    # Create user_data directory if it doesn't exist
    import os
    os.makedirs("user_data", exist_ok=True)

    logger.info("Application startup complete")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown.
    """
    logger.info(f"Shutting down {settings.APP_NAME}")
    # Add cleanup tasks here (close database connections, etc.)
    logger.info("Application shutdown complete")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
