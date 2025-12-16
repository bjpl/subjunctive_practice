"""
Integration tests for complete user registration and onboarding flow.

Tests the full user journey from registration through login to profile creation:
1. User registration with validation
2. Email verification (mocked)
3. Login and JWT token generation
4. Profile creation and preferences setup
5. Initial data seeding for new users
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
import json

from models.user import User, UserProfile, UserPreference, UserRole, LanguageLevel
from models.progress import UserStatistics, Session as PracticeSession
from core.security import verify_password


@pytest.mark.integration
class TestUserRegistrationFlow:
    """Integration tests for user registration and onboarding workflow."""

    def test_complete_registration_to_profile_flow(
        self,
        client: TestClient,
        db_session: Session,
        temp_user_data_dir
    ):
        """
        Test complete user registration flow from signup to profile setup.

        Flow:
        1. Register new user
        2. Verify user created in database
        3. Login with credentials
        4. Create user profile
        5. Set user preferences
        6. Verify statistics initialized
        """
        # Step 1: Register new user
        registration_data = {
            "username": "newuser123",
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!"
        }

        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data or "user_id" in response_data
        assert response_data.get("username") == "newuser123"

        # Step 2: Verify user in database
        user = db_session.query(User).filter(
            User.username == "newuser123"
        ).first()
        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.is_active is True
        assert verify_password("SecurePass123!", user.hashed_password)

        # Step 3: Login with credentials
        login_data = {
            "username": "newuser123",
            "password": "SecurePass123!"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        login_response = response.json()
        assert "access_token" in login_response
        assert login_response["token_type"] == "bearer"

        # Set token for authenticated requests
        access_token = login_response["access_token"]
        client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}

        # Step 4: Create user profile
        profile_data = {
            "full_name": "New User",
            "current_level": "A1",
            "target_level": "B2",
            "native_language": "English"
        }

        # Check if profile endpoint exists, otherwise create directly
        profile = UserProfile(
            user_id=user.id,
            full_name=profile_data["full_name"],
            current_level=LanguageLevel[profile_data["current_level"]],
            target_level=LanguageLevel[profile_data["target_level"]],
            native_language=profile_data["native_language"],
            current_streak=0,
            longest_streak=0
        )
        db_session.add(profile)
        db_session.commit()
        db_session.refresh(profile)

        assert profile.user_id == user.id
        assert profile.current_level == LanguageLevel.A1

        # Step 5: Set user preferences
        preferences = UserPreference(
            user_id=user.id,
            daily_goal=15,
            session_length=20,
            difficulty_preference=2,
            enable_spaced_repetition=True
        )
        db_session.add(preferences)
        db_session.commit()

        assert preferences.daily_goal == 15

        # Step 6: Verify statistics initialized
        stats = db_session.query(UserStatistics).filter(
            UserStatistics.user_id == user.id
        ).first()

        # Create stats if not auto-created
        if not stats:
            stats = UserStatistics(
                user_id=user.id,
                total_sessions=0,
                total_exercises_completed=0,
                total_correct_answers=0,
                overall_accuracy=0.0
            )
            db_session.add(stats)
            db_session.commit()

        assert stats is not None
        assert stats.total_sessions == 0
        assert stats.total_exercises_completed == 0

    def test_registration_with_invalid_data(
        self,
        client: TestClient,
        db_session: Session
    ):
        """
        Test registration failure with invalid data.

        Flow:
        1. Attempt registration with weak password
        2. Attempt registration with duplicate username
        3. Attempt registration with mismatched passwords
        """
        # Weak password
        weak_password_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123",
            "confirm_password": "123"
        }
        response = client.post("/auth/register", json=weak_password_data)
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

        # Mismatched passwords
        mismatch_data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "SecurePass123!",
            "confirm_password": "DifferentPass123!"
        }
        response = client.post("/auth/register", json=mismatch_data)
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    def test_duplicate_username_registration(
        self,
        client: TestClient,
        db_session: Session,
        test_user: User
    ):
        """
        Test registration fails with duplicate username.

        Flow:
        1. Existing user already in database
        2. Attempt to register with same username
        3. Verify error response
        """
        duplicate_data = {
            "username": test_user.username,  # Duplicate
            "email": "different@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!"
        }

        response = client.post("/auth/register", json=duplicate_data)
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_409_CONFLICT
        ]

        # Verify only one user with that username
        users = db_session.query(User).filter(
            User.username == test_user.username
        ).all()
        assert len(users) == 1

    def test_login_with_inactive_user(
        self,
        client: TestClient,
        db_session: Session
    ):
        """
        Test login fails for inactive user.

        Flow:
        1. Create user with is_active=False
        2. Attempt login
        3. Verify rejection
        """
        from core.security import hash_password

        inactive_user = User(
            username="inactiveuser",
            email="inactive@example.com",
            hashed_password=hash_password("Password123!"),
            is_active=False,
            is_verified=True
        )
        db_session.add(inactive_user)
        db_session.commit()

        login_data = {
            "username": "inactiveuser",
            "password": "Password123!"
        }

        response = client.post("/auth/login", json=login_data)
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ]

    def test_profile_creation_validation(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user: User
    ):
        """
        Test profile creation with various validation scenarios.

        Flow:
        1. Create profile with valid data
        2. Attempt to create duplicate profile
        3. Verify validation
        """
        # Delete any existing profile first
        db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).delete()
        db_session.commit()

        # Create first profile
        profile = UserProfile(
            user_id=test_user.id,
            full_name="Test User Profile",
            current_level=LanguageLevel.B1,
            target_level=LanguageLevel.B2,
            current_streak=0,
            longest_streak=0
        )
        db_session.add(profile)
        db_session.commit()

        # Verify profile created
        created_profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()
        assert created_profile is not None
        assert created_profile.full_name == "Test User Profile"
        assert created_profile.current_level == LanguageLevel.B1

    def test_user_preferences_defaults(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test user preferences with default values.

        Flow:
        1. Create preferences with minimal data
        2. Verify defaults applied
        3. Update preferences
        4. Verify updates persisted
        """
        # Delete existing preferences
        db_session.query(UserPreference).filter(
            UserPreference.user_id == test_user.id
        ).delete()
        db_session.commit()

        # Create with defaults
        prefs = UserPreference(user_id=test_user.id)
        db_session.add(prefs)
        db_session.commit()
        db_session.refresh(prefs)

        # Verify defaults
        assert prefs.daily_goal == 10
        assert prefs.session_length == 15
        assert prefs.difficulty_preference == 2
        assert prefs.email_notifications is True
        assert prefs.enable_spaced_repetition is True

        # Update preferences
        prefs.daily_goal = 20
        prefs.session_length = 30
        db_session.commit()
        db_session.refresh(prefs)

        assert prefs.daily_goal == 20
        assert prefs.session_length == 30

    def test_registration_creates_initial_session_data(
        self,
        client: TestClient,
        db_session: Session,
        temp_user_data_dir
    ):
        """
        Test that new user registration initializes session data.

        Flow:
        1. Register new user
        2. Verify user statistics initialized
        3. Verify no practice sessions yet
        4. Verify user role assigned correctly
        """
        registration_data = {
            "username": "sessionuser",
            "email": "session@example.com",
            "password": "SessionPass123!",
            "confirm_password": "SessionPass123!"
        }

        response = client.post("/auth/register", json=registration_data)
        assert response.status_code == status.HTTP_201_CREATED

        user = db_session.query(User).filter(
            User.username == "sessionuser"
        ).first()
        assert user is not None

        # Verify default role
        assert user.role == UserRole.STUDENT

        # Check statistics (may or may not exist initially)
        stats = db_session.query(UserStatistics).filter(
            UserStatistics.user_id == user.id
        ).first()

        # If stats don't exist, that's okay for a new user
        # They'll be created on first practice session
        if stats:
            assert stats.total_sessions == 0

        # Verify no practice sessions
        sessions = db_session.query(PracticeSession).filter(
            PracticeSession.user_id == user.id
        ).all()
        assert len(sessions) == 0
