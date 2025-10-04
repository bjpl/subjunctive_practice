"""
Logging Configuration Module
Provides structured logging with multiple output formats and handlers
"""
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional
import structlog
from structlog.types import FilteringBoundLogger
import os


def get_log_level(level_str: str = "INFO") -> int:
    """Convert string log level to logging constant."""
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return levels.get(level_str.upper(), logging.INFO)


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    log_file: Optional[str] = None,
    service_name: str = "subjunctive-backend",
) -> FilteringBoundLogger:
    """
    Configure structured logging with appropriate handlers and formatters.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Output format (json, console)
        log_file: Optional log file path
        service_name: Name of the service for log identification

    Returns:
        Configured structlog logger
    """
    # Determine processors based on format
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if log_format == "json":
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(get_log_level(log_level)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=get_log_level(log_level),
    )

    # Add file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(get_log_level(log_level))

        if log_format == "json":
            file_handler.setFormatter(
                logging.Formatter("%(message)s")
            )
        else:
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )

        logging.getLogger().addHandler(file_handler)

    # Get logger instance
    logger = structlog.get_logger(service_name)

    # Bind common context
    logger = logger.bind(
        service=service_name,
        environment=os.getenv("ENVIRONMENT", "development"),
        version=os.getenv("VERSION", "unknown"),
    )

    return logger


def configure_uvicorn_logging(log_level: str = "INFO") -> Dict[str, Any]:
    """
    Configure uvicorn logging settings.

    Args:
        log_level: Logging level for uvicorn

    Returns:
        Dictionary with uvicorn logging configuration
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": log_level.upper()},
            "uvicorn.error": {"level": log_level.upper()},
            "uvicorn.access": {"handlers": ["access"], "level": log_level.upper(), "propagate": False},
        },
    }


class LoggerMixin:
    """Mixin class to add structured logging to any class."""

    @property
    def logger(self) -> FilteringBoundLogger:
        """Get logger instance with class context."""
        if not hasattr(self, "_logger"):
            self._logger = structlog.get_logger(self.__class__.__name__)
        return self._logger

    def log_with_context(self, level: str, message: str, **kwargs) -> None:
        """
        Log a message with additional context.

        Args:
            level: Log level (debug, info, warning, error, critical)
            message: Log message
            **kwargs: Additional context to include in log
        """
        log_method = getattr(self.logger, level.lower())
        log_method(message, **kwargs)


def get_request_logger(request_id: str) -> FilteringBoundLogger:
    """
    Get a logger bound with request context.

    Args:
        request_id: Unique request identifier

    Returns:
        Logger with request context
    """
    logger = structlog.get_logger("api")
    return logger.bind(request_id=request_id)


# Convenience functions for common logging patterns
def log_api_request(
    logger: FilteringBoundLogger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    **kwargs
) -> None:
    """Log API request with standard format."""
    logger.info(
        "api_request",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=round(duration_ms, 2),
        **kwargs
    )


def log_database_query(
    logger: FilteringBoundLogger,
    query_type: str,
    table: str,
    duration_ms: float,
    success: bool = True,
    **kwargs
) -> None:
    """Log database query with standard format."""
    log_level = "info" if success else "error"
    getattr(logger, log_level)(
        "database_query",
        query_type=query_type,
        table=table,
        duration_ms=round(duration_ms, 2),
        success=success,
        **kwargs
    )


def log_external_api_call(
    logger: FilteringBoundLogger,
    service: str,
    endpoint: str,
    status_code: Optional[int],
    duration_ms: float,
    success: bool = True,
    **kwargs
) -> None:
    """Log external API call with standard format."""
    log_level = "info" if success else "error"
    getattr(logger, log_level)(
        "external_api_call",
        service=service,
        endpoint=endpoint,
        status_code=status_code,
        duration_ms=round(duration_ms, 2),
        success=success,
        **kwargs
    )


# Initialize default logger
default_logger = setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_format=os.getenv("LOG_FORMAT", "console"),
    log_file=os.getenv("LOG_FILE"),
    service_name="subjunctive-backend",
)
