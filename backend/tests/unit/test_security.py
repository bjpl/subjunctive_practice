"""
Unit tests for Security utilities.

Tests cover:
- Password hashing and verification
- JWT token creation and validation
- Token expiration
- Token decoding
"""

import pytest
from datetime import timedelta
from jose import jwt, JWTError
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from core.config import Settings
from fastapi import HTTPException


@pytest.mark.unit
@pytest.mark.auth
class TestPasswordSecurity:
    """Test suite for password hashing and verification."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123"
        hashed = hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # Bcrypt prefix

    def test_hash_password_different_hashes(self):
        """Test same password produces different hashes (salt)."""
        password = "TestPassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2  # Different due to salt

    def test_verify_correct_password(self):
        """Test verifying correct password."""
        password = "TestPassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Test verifying incorrect password."""
        password = "TestPassword123"
        wrong_password = "WrongPassword456"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_case_sensitive(self):
        """Test password verification is case sensitive."""
        password = "TestPassword123"
        hashed = hash_password(password)

        assert verify_password("testpassword123", hashed) is False

    def test_hash_empty_password(self):
        """Test hashing empty password."""
        hashed = hash_password("")
        assert hashed is not None
        assert verify_password("", hashed) is True

    def test_hash_special_characters(self):
        """Test hashing password with special characters."""
        password = "Test!@#$%^&*()_+{}[]|:;<>?,./"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_unicode_password(self):
        """Test hashing password with unicode characters."""
        password = "Test密码123ñ"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True


@pytest.mark.unit
@pytest.mark.auth
class TestJWTTokens:
    """Test suite for JWT token creation and validation."""

    def test_create_access_token(self, test_settings):
        """Test creating access token."""
        data = {"sub": "user123", "username": "testuser"}
        token = create_access_token(data, test_settings)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self, test_settings):
        """Test creating refresh token."""
        data = {"sub": "user123", "username": "testuser"}
        token = create_refresh_token(data, test_settings)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_access_token_contains_data(self, test_settings):
        """Test access token contains provided data."""
        data = {"sub": "user123", "username": "testuser", "email": "test@example.com"}
        token = create_access_token(data, test_settings)

        # Decode without verification to check contents
        payload = jwt.decode(
            token,
            test_settings.JWT_SECRET_KEY,
            algorithms=[test_settings.JWT_ALGORITHM]
        )

        assert payload["sub"] == "user123"
        assert payload["username"] == "testuser"
        assert payload["email"] == "test@example.com"

    def test_access_token_has_expiration(self, test_settings):
        """Test access token has expiration claim."""
        data = {"sub": "user123"}
        token = create_access_token(data, test_settings)

        payload = jwt.decode(
            token,
            test_settings.JWT_SECRET_KEY,
            algorithms=[test_settings.JWT_ALGORITHM]
        )

        assert "exp" in payload
        assert "iat" in payload
        assert payload["type"] == "access"

    def test_refresh_token_has_longer_expiration(self, test_settings):
        """Test refresh token has longer expiration than access token."""
        data = {"sub": "user123"}

        access_token = create_access_token(data, test_settings)
        refresh_token = create_refresh_token(data, test_settings)

        access_payload = jwt.decode(
            access_token,
            test_settings.JWT_SECRET_KEY,
            algorithms=[test_settings.JWT_ALGORITHM]
        )

        refresh_payload = jwt.decode(
            refresh_token,
            test_settings.JWT_SECRET_KEY,
            algorithms=[test_settings.JWT_ALGORITHM]
        )

        assert refresh_payload["exp"] > access_payload["exp"]
        assert refresh_payload["type"] == "refresh"

    def test_custom_expiration_delta(self, test_settings):
        """Test creating token with custom expiration."""
        data = {"sub": "user123"}
        custom_delta = timedelta(minutes=5)

        token = create_access_token(data, test_settings, expires_delta=custom_delta)

        assert token is not None

    def test_decode_valid_token(self, test_settings):
        """Test decoding valid token."""
        data = {"sub": "user123", "username": "testuser"}
        token = create_access_token(data, test_settings)

        decoded = decode_token(token, test_settings)

        assert decoded["sub"] == "user123"
        assert decoded["username"] == "testuser"

    def test_decode_invalid_token_raises_exception(self, test_settings):
        """Test decoding invalid token raises exception."""
        invalid_token = "invalid.token.here"

        with pytest.raises(HTTPException) as exc_info:
            decode_token(invalid_token, test_settings)

        assert exc_info.value.status_code == 401

    def test_decode_expired_token_raises_exception(self, test_settings, expired_jwt_token):
        """Test decoding expired token raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            decode_token(expired_jwt_token, test_settings)

        assert exc_info.value.status_code == 401

    def test_decode_token_with_wrong_secret(self, test_settings):
        """Test decoding token with wrong secret raises exception."""
        data = {"sub": "user123"}
        token = create_access_token(data, test_settings)

        # Change the secret
        wrong_settings = Settings(
            JWT_SECRET_KEY="wrong-secret-key",
            JWT_ALGORITHM=test_settings.JWT_ALGORITHM
        )

        with pytest.raises(HTTPException) as exc_info:
            decode_token(token, wrong_settings)

        assert exc_info.value.status_code == 401

    def test_token_type_field(self, test_settings):
        """Test token contains type field."""
        access_data = {"sub": "user123"}
        refresh_data = {"sub": "user123"}

        access_token = create_access_token(access_data, test_settings)
        refresh_token = create_refresh_token(refresh_data, test_settings)

        access_payload = decode_token(access_token, test_settings)
        refresh_payload = decode_token(refresh_token, test_settings)

        assert access_payload["type"] == "access"
        assert refresh_payload["type"] == "refresh"

    def test_token_includes_issued_at(self, test_settings):
        """Test token includes issued at timestamp."""
        data = {"sub": "user123"}
        token = create_access_token(data, test_settings)

        payload = decode_token(token, test_settings)

        assert "iat" in payload
        assert isinstance(payload["iat"], int)

    def test_token_different_each_time(self, test_settings):
        """Test tokens are different even with same data (due to timestamps)."""
        import time
        data = {"sub": "user123"}

        token1 = create_access_token(data, test_settings)
        time.sleep(1.1)  # Wait over 1 second to ensure different timestamp
        token2 = create_access_token(data, test_settings)

        # Tokens should be different due to different iat and exp
        # Decode to verify timestamps are different
        payload1 = decode_token(token1, test_settings)
        payload2 = decode_token(token2, test_settings)
        assert payload1["iat"] != payload2["iat"] or payload1["exp"] != payload2["exp"]
        assert token1 != token2

    def test_token_with_empty_data(self, test_settings):
        """Test creating token with minimal data."""
        data = {}
        token = create_access_token(data, test_settings)

        payload = decode_token(token, test_settings)

        assert "exp" in payload
        assert "iat" in payload
        assert "type" in payload

    def test_token_with_various_data_types(self, test_settings):
        """Test token with various data types."""
        data = {
            "sub": "user123",
            "username": "testuser",
            "roles": ["user", "admin"],
            "permissions": {"read": True, "write": True},
            "count": 42,
            "active": True
        }

        token = create_access_token(data, test_settings)
        payload = decode_token(token, test_settings)

        assert payload["sub"] == "user123"
        assert payload["username"] == "testuser"
        assert payload["roles"] == ["user", "admin"]
        assert payload["permissions"] == {"read": True, "write": True}
        assert payload["count"] == 42
        assert payload["active"] is True


@pytest.mark.unit
@pytest.mark.auth
class TestSecurityEdgeCases:
    """Test edge cases and security scenarios."""

    def test_very_long_password(self):
        """Test hashing very long password."""
        password = "a" * 1000
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_password_with_null_bytes(self):
        """Test password with null bytes - bcrypt rejects null bytes."""
        from passlib.exc import PasswordValueError

        password = "test\x00password"

        # Bcrypt doesn't allow null bytes - expect error
        with pytest.raises(PasswordValueError):
            hash_password(password)

    def test_token_with_large_payload(self, test_settings):
        """Test token with large payload."""
        data = {
            "sub": "user123",
            "data": "x" * 1000  # Large string
        }

        token = create_access_token(data, test_settings)
        payload = decode_token(token, test_settings)

        assert payload["data"] == "x" * 1000

    def test_decode_malformed_token(self, test_settings):
        """Test decoding malformed token."""
        malformed_tokens = [
            "not.a.token",
            "",
            "single-part",
            "two.parts",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"
        ]

        for token in malformed_tokens:
            with pytest.raises(HTTPException):
                decode_token(token, test_settings)

    def test_password_hash_consistency(self):
        """Test same password can be verified multiple times."""
        password = "TestPassword123"
        hashed = hash_password(password)

        # Verify multiple times
        for _ in range(10):
            assert verify_password(password, hashed) is True

    def test_token_cannot_be_modified(self, test_settings):
        """Test that modifying token invalidates it."""
        data = {"sub": "user123", "role": "user"}
        token = create_access_token(data, test_settings)

        # Try to modify the token
        parts = token.split(".")
        if len(parts) == 3:
            # Modify the payload (middle part)
            modified_token = parts[0] + ".modified." + parts[2]

            with pytest.raises(HTTPException):
                decode_token(modified_token, test_settings)
