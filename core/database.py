"""
Database configuration and session management for Spanish Subjunctive Practice.
Provides SQLAlchemy engine, session factory, and base model class.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator
import os
from pathlib import Path

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./subjunctive_practice.db"
)

# For PostgreSQL in production, use:
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql://user:password@localhost:5432/subjunctive_practice"
# )

# SQLAlchemy engine configuration
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific optimizations
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    })
else:
    # PostgreSQL connection pooling
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Enable SQLite foreign keys
if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Base class for all models
Base = declarative_base()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Database session context manager.

    Usage:
        with get_db() as db:
            user = db.query(User).first()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Generator[Session, None, None]:
    """
    Get a database session (for FastAPI dependency injection).

    Usage in FastAPI:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db_session)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables."""
    try:
        from backend.models import user, exercise, progress  # noqa
    except ModuleNotFoundError:
        from models import user, exercise, progress  # noqa
    Base.metadata.create_all(bind=engine)


def reset_db():
    """Drop all tables and recreate them (development only!)"""
    try:
        from backend.models import user, exercise, progress  # noqa
    except ModuleNotFoundError:
        from models import user, exercise, progress  # noqa
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
