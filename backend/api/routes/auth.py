"""
Authentication routes: registration, login, token refresh.
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends
import json
import os
from pathlib import Path

from core.config import get_settings, Settings
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from models.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenRefresh
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Simple file-based user storage for development
# In production, replace with database
USER_DATA_FILE = Path("user_data/users.json")


def load_users() -> Dict[str, Any]:
    """Load users from JSON file."""
    USER_DATA_FILE.parent.mkdir(exist_ok=True)
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users: Dict[str, Any]) -> None:
    """Save users to JSON file."""
    USER_DATA_FILE.parent.mkdir(exist_ok=True)
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2, default=str)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
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
    users = load_users()

    # Check if username already exists
    if user_data.username in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists
    if any(u.get("email") == user_data.email for u in users.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user_id = f"user_{len(users) + 1}_{user_data.username}"
    hashed_password = hash_password(user_data.password)

    user = {
        "user_id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "password_hash": hashed_password,
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None,
        "is_active": True
    }

    users[user_data.username] = user
    save_users(users)

    # Return user response (without password)
    return UserResponse(
        user_id=user["user_id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        created_at=datetime.fromisoformat(user["created_at"]),
        last_login=None
    )


@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    settings: Settings = Depends(get_settings)
):
    """
    Authenticate user and return access/refresh tokens.

    - **username**: User's username
    - **password**: User's password

    Returns JWT access token and refresh token.
    """
    users = load_users()

    # Find user
    user = users.get(credentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    # Update last login
    user["last_login"] = datetime.utcnow().isoformat()
    users[credentials.username] = user
    save_users(users)

    # Create tokens
    token_data = {
        "sub": user["user_id"],
        "username": user["username"],
        "email": user["email"]
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
    current_user: Dict[str, Any] = Depends(get_settings)
):
    """
    Get current authenticated user information.

    Requires valid access token.
    """
    users = load_users()

    username = current_user.get("username")
    user = users.get(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        user_id=user["user_id"],
        username=user["username"],
        email=user["email"],
        full_name=user.get("full_name"),
        created_at=datetime.fromisoformat(user["created_at"]),
        last_login=datetime.fromisoformat(user["last_login"]) if user.get("last_login") else None
    )
