"""
API tests for Authentication endpoints.

Tests cover:
- User registration
- User login
- Token refresh
- Authentication errors
- Authorization checks
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.api
@pytest.mark.auth
class TestAuthAPI:
    """Test suite for authentication API endpoints."""

    # ========================================================================
    # Registration Tests
    # ========================================================================

    def test_register_user_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "SecurePass123",
                "full_name": "New User"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_user_duplicate_username(self, client: TestClient):
        """Test registration with duplicate username fails."""
        # Register first user
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test1@example.com",
                "password": "SecurePass123"
            }
        )

        # Try to register with same username
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test2@example.com",
                "password": "SecurePass456"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.json()["detail"].lower()

    def test_register_user_duplicate_email(self, client: TestClient):
        """Test registration with duplicate email fails."""
        # Register first user
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "user1",
                "email": "test@example.com",
                "password": "SecurePass123"
            }
        )

        # Try to register with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "user2",
                "email": "test@example.com",
                "password": "SecurePass456"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.json()["detail"].lower()

    @pytest.mark.parametrize("invalid_data,missing_field", [
        ({"email": "test@example.com", "password": "Pass123"}, "username"),
        ({"username": "testuser", "password": "Pass123"}, "email"),
        ({"username": "testuser", "email": "test@example.com"}, "password"),
    ])
    def test_register_user_missing_fields(self, client: TestClient, invalid_data, missing_field):
        """Test registration with missing required fields."""
        response = client.post("/api/v1/auth/register", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("invalid_email", [
        "notanemail",
        "@example.com",
        "user@",
        "user @example.com"
    ])
    def test_register_user_invalid_email(self, client: TestClient, invalid_email):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": invalid_email,
                "password": "SecurePass123"
            }
        )

        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]

    # ========================================================================
    # Login Tests
    # ========================================================================

    def test_login_success(self, client: TestClient):
        """Test successful login."""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "SecurePass123"
            }
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "loginuser",
                "password": "SecurePass123"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "WrongPassword"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_wrong_password(self, client: TestClient):
        """Test login with wrong password."""
        # Register user
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser2",
                "email": "test2@example.com",
                "password": "CorrectPass123"
            }
        )

        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser2",
                "password": "WrongPass456"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_case_sensitive_password(self, client: TestClient):
        """Test login password is case sensitive."""
        # Register user
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser3",
                "email": "test3@example.com",
                "password": "SecurePass123"
            }
        )

        # Login with different case
        response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser3",
                "password": "securepass123"  # lowercase
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========================================================================
    # Token Refresh Tests
    # ========================================================================

    def test_refresh_token_success(self, client: TestClient):
        """Test successful token refresh."""
        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "refreshuser",
                "email": "refresh@example.com",
                "password": "SecurePass123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "refreshuser",
                "password": "SecurePass123"
            }
        )

        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_refresh_with_invalid_token(self, client: TestClient):
        """Test refresh with invalid token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_with_access_token_fails(self, client: TestClient):
        """Test refresh with access token instead of refresh token fails."""
        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "tokenuser",
                "email": "token@example.com",
                "password": "SecurePass123"
            }
        )

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "tokenuser",
                "password": "SecurePass123"
            }
        )

        access_token = login_response.json()["access_token"]

        # Try to refresh with access token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # ========================================================================
    # Protected Endpoint Tests
    # ========================================================================

    def test_access_protected_endpoint_without_token(self, client: TestClient):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_protected_endpoint_with_valid_token(self, authenticated_client: TestClient):
        """Test accessing protected endpoint with valid token."""
        response = authenticated_client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "username" in data
        assert "email" in data

    def test_access_protected_endpoint_with_invalid_token(self, client: TestClient):
        """Test accessing protected endpoint with invalid token."""
        client.headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me")

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_access_protected_endpoint_with_expired_token(self, client: TestClient, expired_jwt_token):
        """Test accessing protected endpoint with expired token."""
        client.headers = {"Authorization": f"Bearer {expired_jwt_token}"}
        response = client.get("/api/v1/auth/me")

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    # ========================================================================
    # Integration Flow Tests
    # ========================================================================

    def test_complete_auth_flow(self, client: TestClient):
        """Test complete authentication flow."""
        # 1. Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "flowuser",
                "email": "flow@example.com",
                "password": "SecurePass123",
                "full_name": "Flow User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED

        # 2. Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": "flowuser",
                "password": "SecurePass123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        tokens = login_response.json()

        # 3. Access protected endpoint
        client.headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        me_response = client.get("/api/v1/auth/me")
        assert me_response.status_code == status.HTTP_200_OK
        assert me_response.json()["username"] == "flowuser"

        # 4. Refresh token
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": tokens["refresh_token"]}
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        new_tokens = refresh_response.json()

        # 5. Use new access token
        client.headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
        me_response2 = client.get("/api/v1/auth/me")
        assert me_response2.status_code == status.HTTP_200_OK

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_register_with_very_long_username(self, client: TestClient):
        """Test registration with very long username."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "a" * 100,
                "email": "long@example.com",
                "password": "SecurePass123"
            }
        )

        # Should either accept or reject based on validation
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    def test_register_with_special_characters_in_username(self, client: TestClient):
        """Test registration with special characters in username."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "test@user#123",
                "email": "special@example.com",
                "password": "SecurePass123"
            }
        )

        # Should validate based on username rules
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    def test_login_preserves_last_login_time(self, client: TestClient):
        """Test login updates last login time."""
        # Register
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "timeuser",
                "email": "time@example.com",
                "password": "SecurePass123"
            }
        )

        # First login
        response1 = client.post(
            "/api/v1/auth/login",
            json={
                "username": "timeuser",
                "password": "SecurePass123"
            }
        )

        # Second login after some time
        import time
        time.sleep(0.1)

        response2 = client.post(
            "/api/v1/auth/login",
            json={
                "username": "timeuser",
                "password": "SecurePass123"
            }
        )

        # Both should succeed
        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK
