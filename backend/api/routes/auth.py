"""
Authentication routes: registration, login, token refresh.
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import json
import os
from pathlib import Path

from core.config import get_settings, Settings
from core.database import get_db_session
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user
)
from models.user import User, UserRole, UserProfile, UserPreference
from schemas.user import UserCreate, UserResponse
from pydantic import BaseModel

# Token schemas - should be moved to schemas/auth.py
class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str

class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

class TokenRefresh(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str


router = APIRouter(prefix="/auth", tags=["Authentication"])


# DEPRECATED: File-based user storage (kept as fallback)
# Use database storage for all new operations
USER_DATA_FILE = Path("user_data/users.json")


def load_users() -> Dict[str, Any]:
    """
    DEPRECATED: Load users from JSON file.
    Use database queries instead.
    Kept for backward compatibility only.
    """
    USER_DATA_FILE.parent.mkdir(exist_ok=True)
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users: Dict[str, Any]) -> None:
    """
    DEPRECATED: Save users to JSON file.
    Use database operations instead.
    Kept for backward compatibility only.
    """
    USER_DATA_FILE.parent.mkdir(exist_ok=True)
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2, default=str)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
):
    """
    Register a new user.

    - **username**: Unique username (3-50 characters, alphanumeric)
    - **email**: Valid email address
    - **password**: Strong password (min 8 characters, must contain letters and numbers)
    - **full_name**: Optional full name

    Returns user information and authentication tokens.
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=UserRole.STUDENT,
        is_active=True,
        is_verified=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create default user profile
    profile = UserProfile(
        user_id=user.id,
        full_name=user_data.full_name
    )
    db.add(profile)

    # Create default user preferences
    preferences = UserPreference(
        user_id=user.id
    )
    db.add(preferences)

    db.commit()
    db.refresh(user)

    # Return user response (without password)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        last_login=user.last_login
    )


@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
):
    """
    Authenticate user and return access/refresh tokens.

    - **username**: User's username
    - **password**: User's password

    Returns JWT access token and refresh token.
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create tokens
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email
    }

    access_token = create_access_token(token_data, settings)
    refresh_token = create_refresh_token(token_data, settings)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    token_refresh: TokenRefresh,
    settings: Settings = Depends(get_settings)
):
    """
    Refresh access token using refresh token.

    - **refresh_token**: Valid refresh token

    Returns new access token and refresh token.
    """
    try:
        # Decode refresh token
        payload = decode_token(token_refresh.refresh_token, settings)

        # Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        # Create new tokens
        token_data = {
            "sub": payload["sub"],
            "username": payload.get("username"),
            "email": payload.get("email")
        }

        access_token = create_access_token(token_data, settings)
        refresh_token = create_refresh_token(token_data, settings)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    db: Session = Depends(get_db_session),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get current authenticated user information.

    Requires valid access token.
    """
    # Get user ID from token
    user_id = int(current_user.get("sub"))

    # Query user from database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        last_login=user.last_login
    )
