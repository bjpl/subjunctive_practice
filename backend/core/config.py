"""
Configuration management for FastAPI application.
Loads settings from environment variables with validation.
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Spanish Subjunctive Practice API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    TESTING: bool = Field(default=False, env="TESTING")

    # API Configuration
    API_V1_PREFIX: str = "/api"

    # Security
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:80"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return []

    # Database
    DATABASE_URL: Optional[str] = Field(default=None, env="DATABASE_URL")

    # Redis
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")  # 1 hour default
    REDIS_CACHE_PREFIX: str = Field(default="subjunctive", env="REDIS_CACHE_PREFIX")
    REDIS_POOL_SIZE: int = Field(default=10, env="REDIS_POOL_SIZE")

    # Anthropic Claude
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    ANTHROPIC_MAX_TOKENS: int = Field(default=1000, env="ANTHROPIC_MAX_TOKENS")
    ANTHROPIC_TEMPERATURE: float = Field(default=0.7, env="ANTHROPIC_TEMPERATURE")

    # Email Configuration
    EMAIL_PROVIDER: str = Field(default="smtp", env="EMAIL_PROVIDER")  # "smtp" or "sendgrid"
    EMAIL_FROM_ADDRESS: str = Field(default="noreply@example.com", env="EMAIL_FROM_ADDRESS")
    EMAIL_FROM_NAME: str = Field(default="Spanish Subjunctive Practice", env="EMAIL_FROM_NAME")

    # SendGrid Configuration (if EMAIL_PROVIDER = "sendgrid")
    SENDGRID_API_KEY: Optional[str] = Field(default=None, env="SENDGRID_API_KEY")

    # SMTP Configuration (if EMAIL_PROVIDER = "smtp")
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")

    # Frontend URL (for email links)
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
        env_parse_enums=False
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Dependency for accessing settings in FastAPI routes."""
    return settings
