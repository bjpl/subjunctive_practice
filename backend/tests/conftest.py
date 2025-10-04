"""
Pytest configuration and shared fixtures.

This module provides:
- Database fixtures (in-memory SQLite for testing)
- FastAPI TestClient fixtures
- Mock fixtures for external dependencies
- Factory fixtures for creating test data
- Authentication fixtures
"""

import os
import pytest
from typing import Generator, Dict, Any
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import shutil
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.core.database import Base, get_db
from backend.core.config import Settings, get_settings
from backend.core.security import create_access_token, hash_password
from backend.models.user import User, UserProfile, UserPreference
from backend.services.conjugation import ConjugationEngine
from backend.services.exercise_generator import ExerciseGenerator
from backend.services.learning_algorithm import LearningAlgorithm, SM2Card
from backend.services.feedback import FeedbackGenerator, ErrorAnalyzer


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings with overrides."""
    return Settings(
        DATABASE_URL="sqlite:///:memory:",
        JWT_SECRET_KEY="test-secret-key-for-testing-only",
        JWT_ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=30,
        REFRESH_TOKEN_EXPIRE_DAYS=7,
        ENVIRONMENT="test",
        DEBUG=True,
        TESTING=True
    )


@pytest.fixture(scope="session")
def override_settings(test_settings: Settings):
    """Override app settings with test settings."""
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield test_settings
    app.dependency_overrides.clear()


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def db_engine():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create database session for testing."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def override_get_db(db_session: Session):
    """Override get_db dependency with test database."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


# ============================================================================
# FastAPI TestClient Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def client(override_settings, override_get_db) -> TestClient:
    """Create FastAPI test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, test_user, test_settings: Settings) -> TestClient:
    """Create authenticated test client with JWT token."""
    token_data = {
        "sub": str(test_user.id),
        "username": test_user.username,
        "email": test_user.email
    }
    access_token = create_access_token(token_data, test_settings)

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }

    return client


# ============================================================================
# User and Authentication Fixtures
# ============================================================================

@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create test user in database."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_with_profile(db_session: Session, test_user: User) -> User:
    """Create test user with profile."""
    profile = UserProfile(
        user_id=test_user.id,
        full_name="Test User",
        current_level="B1",
        target_level="B2",
        native_language="English",
        current_streak=5,
        longest_streak=10
    )
    db_session.add(profile)

    preferences = UserPreference(
        user_id=test_user.id,
        daily_goal=10,
        session_length=15,
        difficulty_preference=2
    )
    db_session.add(preferences)

    db_session.commit()
    db_session.refresh(test_user)
    return test_user


@pytest.fixture
def admin_user(db_session: Session) -> User:
    """Create admin user."""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123"),
        role="admin",
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def valid_jwt_token(test_user: User, test_settings: Settings) -> str:
    """Create valid JWT token for test user."""
    token_data = {
        "sub": str(test_user.id),
        "username": test_user.username,
        "email": test_user.email
    }
    return create_access_token(token_data, test_settings)


@pytest.fixture
def expired_jwt_token(test_user: User, test_settings: Settings) -> str:
    """Create expired JWT token."""
    token_data = {
        "sub": str(test_user.id),
        "username": test_user.username,
        "email": test_user.email
    }
    return create_access_token(
        token_data,
        test_settings,
        expires_delta=timedelta(seconds=-1)
    )


# ============================================================================
# Service Fixtures
# ============================================================================

@pytest.fixture
def conjugation_engine() -> ConjugationEngine:
    """Create conjugation engine instance."""
    return ConjugationEngine()


@pytest.fixture
def exercise_generator(conjugation_engine: ConjugationEngine) -> ExerciseGenerator:
    """Create exercise generator instance."""
    return ExerciseGenerator(conjugation_engine)


@pytest.fixture
def learning_algorithm() -> LearningAlgorithm:
    """Create learning algorithm instance."""
    return LearningAlgorithm(initial_difficulty="intermediate")


@pytest.fixture
def error_analyzer() -> ErrorAnalyzer:
    """Create error analyzer instance."""
    return ErrorAnalyzer()


@pytest.fixture
def feedback_generator(conjugation_engine: ConjugationEngine, error_analyzer: ErrorAnalyzer) -> FeedbackGenerator:
    """Create feedback generator instance."""
    return FeedbackGenerator(conjugation_engine, error_analyzer)


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = Mock(
            choices=[
                Mock(
                    message=Mock(
                        content="Mocked OpenAI response"
                    )
                )
            ]
        )
        yield mock


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch("redis.Redis") as mock:
        redis_instance = Mock()
        redis_instance.get.return_value = None
        redis_instance.set.return_value = True
        redis_instance.delete.return_value = 1
        mock.return_value = redis_instance
        yield redis_instance


# ============================================================================
# Factory Fixtures
# ============================================================================

class UserFactory:
    """Factory for creating test users."""

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.counter = 0

    def create(self, **kwargs) -> User:
        """Create a user with optional overrides."""
        self.counter += 1
        defaults = {
            "username": f"user{self.counter}",
            "email": f"user{self.counter}@example.com",
            "hashed_password": hash_password("Password123"),
            "is_active": True,
            "is_verified": True
        }
        defaults.update(kwargs)

        user = User(**defaults)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user


@pytest.fixture
def user_factory(db_session: Session) -> UserFactory:
    """Factory fixture for creating users."""
    return UserFactory(db_session)


class SM2CardFactory:
    """Factory for creating SM2 cards."""

    def __init__(self):
        self.counter = 0

    def create(self, **kwargs) -> SM2Card:
        """Create SM2 card with optional overrides."""
        self.counter += 1
        defaults = {
            "item_id": f"card_{self.counter}",
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "yo",
            "easiness_factor": 2.5,
            "interval": 0,
            "repetitions": 0,
            "next_review": datetime.now(),
            "total_reviews": 0,
            "correct_reviews": 0
        }
        defaults.update(kwargs)
        return SM2Card(**defaults)


@pytest.fixture
def card_factory() -> SM2CardFactory:
    """Factory fixture for creating SM2 cards."""
    return SM2CardFactory()


# ============================================================================
# Temporary Directory Fixtures
# ============================================================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_user_data_dir(temp_dir: Path) -> Path:
    """Create temporary user_data directory."""
    user_data = temp_dir / "user_data"
    user_data.mkdir(exist_ok=True)

    # Patch the USER_DATA_FILE paths
    with patch("backend.api.routes.auth.USER_DATA_FILE", user_data / "users.json"):
        with patch("backend.api.routes.exercises.EXERCISE_DATA_FILE", user_data / "fallback_exercises.json"):
            yield user_data


# ============================================================================
# Data Fixtures
# ============================================================================

@pytest.fixture
def sample_verbs() -> Dict[str, list]:
    """Sample verbs for testing."""
    return {
        "regular_ar": ["hablar", "estudiar", "trabajar"],
        "regular_er": ["comer", "beber", "leer"],
        "regular_ir": ["vivir", "escribir", "abrir"],
        "irregular": ["ser", "estar", "ir", "haber", "tener"],
        "stem_changing_e_ie": ["pensar", "querer", "sentir"],
        "stem_changing_o_ue": ["poder", "dormir", "volver"],
        "stem_changing_e_i": ["pedir", "servir", "repetir"]
    }


@pytest.fixture
def sample_exercises() -> list:
    """Sample exercises for testing."""
    return [
        {
            "id": "EX001",
            "type": "present_subjunctive",
            "verb": "hablar",
            "person": "yo",
            "sentence": "Es importante que yo ____ español.",
            "correct_answer": "hable",
            "difficulty": 1,
            "category": "Impersonal_Expressions"
        },
        {
            "id": "EX002",
            "type": "present_subjunctive",
            "verb": "ser",
            "person": "tú",
            "sentence": "Quiero que tú ____ feliz.",
            "correct_answer": "seas",
            "difficulty": 3,
            "category": "Wishes"
        }
    ]


# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Cleanup test files after each test."""
    yield
    # Clean up any test files created
    test_files = [
        "user_data/users.json",
        "user_data/fallback_exercises.json"
    ]
    for file_path in test_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


# ============================================================================
# Logging Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def setup_test_logging():
    """Setup logging for tests."""
    import logging

    # Create logs directory
    log_dir = Path("tests/logs")
    log_dir.mkdir(exist_ok=True, parents=True)

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    )

    yield

    # Cleanup
    logging.shutdown()


# ============================================================================
# Performance Testing Fixtures
# ============================================================================

@pytest.fixture
def benchmark_config() -> Dict[str, Any]:
    """Configuration for performance benchmarks."""
    return {
        "max_response_time": 200,  # milliseconds
        "max_db_query_time": 50,   # milliseconds
        "concurrent_requests": 10,
        "load_test_duration": 5     # seconds
    }
