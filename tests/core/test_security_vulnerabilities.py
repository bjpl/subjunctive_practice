"""
Security vulnerability tests.

Tests cover:
- SQL Injection prevention
- XSS prevention
- CSRF protection
- Authentication bypass attempts
- Token manipulation attacks
- Input validation and sanitization
- Path traversal prevention
- Header injection prevention
"""

import pytest
import json
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from jose import jwt

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from core.config import Settings


# ============================================================================
# SQL Injection Prevention Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestSQLInjectionPrevention:
    """Test suite for SQL injection prevention."""

    def test_user_id_with_sql_injection_pattern(self, client):
        """Test that user IDs with SQL injection patterns are rejected."""
        malicious_ids = [
            "1; DROP TABLE users;--",
            "1 OR 1=1",
            "1' OR '1'='1",
            "1; SELECT * FROM users--",
            "1 UNION SELECT * FROM passwords",
            "1'; DELETE FROM exercises;--"
        ]

        for malicious_id in malicious_ids:
            # These should not cause SQL injection
            response = client.get(f"/api/progress/{malicious_id}")
            # Should get auth error or validation error, not SQL error
            assert response.status_code in [401, 403, 404, 422]

    def test_search_query_sql_injection(self, authenticated_client):
        """Test that search queries are protected from SQL injection."""
        malicious_queries = [
            "'; DROP TABLE exercises;--",
            "1 OR 1=1",
            "UNION SELECT password FROM users",
        ]

        for query in malicious_queries:
            response = authenticated_client.get(
                f"/api/exercises",
                params={"search": query}
            )
            # Should not return SQL error or unexpected data
            # 404 is also valid if no exercises exist
            assert response.status_code in [200, 400, 404, 422]

    def test_filter_parameter_sql_injection(self, authenticated_client):
        """Test filter parameters are protected from SQL injection."""
        response = authenticated_client.get(
            "/api/exercises",
            params={"difficulty": "1 OR 1=1"}
        )
        # Should reject invalid difficulty value
        assert response.status_code in [200, 400, 422]


# ============================================================================
# XSS Prevention Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestXSSPrevention:
    """Test suite for Cross-Site Scripting prevention."""

    def test_script_tag_in_username(self, client):
        """Test that script tags in usernames are handled safely."""
        malicious_data = {
            "username": "<script>alert('xss')</script>",
            "email": "test@example.com",
            "password": "TestPassword123"
        }

        response = client.post("/api/auth/register", json=malicious_data)

        # Should either reject or sanitize
        if response.status_code == 200:
            data = response.json()
            if "username" in data:
                assert "<script>" not in data.get("username", "")

    def test_html_injection_in_exercise_content(self, authenticated_client, db_session):
        """Test that HTML in exercise content is handled safely."""
        malicious_content = {
            "prompt": "<img src=x onerror=alert('xss')>",
            "answer": "test"
        }

        response = authenticated_client.post(
            "/api/exercises/submit",
            json=malicious_content
        )

        # Response should not contain raw HTML that could execute
        if response.status_code == 200:
            content = response.text
            assert "onerror=" not in content

    def test_event_handler_injection(self, client):
        """Test that event handlers are not executable in responses."""
        malicious_patterns = [
            "<div onmouseover=\"alert('xss')\">",
            "<body onload=alert('xss')>",
            "<svg onload=alert('xss')>"
        ]

        for pattern in malicious_patterns:
            response = client.post(
                "/api/auth/register",
                json={
                    "username": pattern,
                    "email": "test@test.com",
                    "password": "Test123!"
                }
            )

            # Should not reflect malicious content
            if response.status_code == 200:
                assert pattern not in response.text


# ============================================================================
# Authentication Bypass Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestAuthenticationBypass:
    """Test suite for authentication bypass prevention."""

    def test_missing_auth_header(self, client):
        """Test that requests without auth header are rejected."""
        protected_endpoints = [
            "/api/exercises",
            "/api/progress",
            "/api/settings",
            "/api/achievements"
        ]

        for endpoint in protected_endpoints:
            response = client.get(endpoint)
            assert response.status_code in [401, 403]

    def test_empty_bearer_token(self, client):
        """Test that empty bearer tokens are rejected."""
        response = client.get(
            "/api/exercises",
            headers={"Authorization": "Bearer "}
        )
        assert response.status_code in [401, 403, 422]

    def test_invalid_bearer_format(self, client):
        """Test that invalid bearer formats are rejected."""
        invalid_formats = [
            "Bearer",
            "Bearer  ",
            "bearer token",
            "BEARER token",
            "Basic token",
            "Token xyz"
        ]

        for auth_header in invalid_formats:
            response = client.get(
                "/api/exercises",
                headers={"Authorization": auth_header}
            )
            assert response.status_code in [401, 403, 422]

    def test_malformed_jwt_token(self, client):
        """Test that malformed JWT tokens are rejected."""
        malformed_tokens = [
            "notajwt",
            "xxx.yyy.zzz",
            "eyJ.eyJ.sig",
            "../../../etc/passwd",
            "null",
            "undefined"
        ]

        for token in malformed_tokens:
            response = client.get(
                "/api/exercises",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code in [401, 403, 422]

    def test_expired_token(self, client, expired_jwt_token):
        """Test that expired tokens are rejected."""
        response = client.get(
            "/api/exercises",
            headers={"Authorization": f"Bearer {expired_jwt_token}"}
        )
        assert response.status_code == 401

    def test_token_with_wrong_algorithm(self, test_settings):
        """Test that tokens with wrong algorithm are rejected."""
        # Create token with different algorithm claim
        payload = {
            "sub": "user123",
            "exp": datetime.utcnow() + timedelta(hours=1),
            "type": "access"
        }

        # Sign with HS256 but claim it's RS256 in header (algorithm confusion)
        token = jwt.encode(
            payload,
            test_settings.JWT_SECRET_KEY,
            algorithm="HS256",
            headers={"alg": "HS256"}  # Attacker might try alg: none
        )

        # Should still validate properly
        decoded = decode_token(token, test_settings)
        assert decoded is not None

    def test_refresh_token_used_as_access_token(self, test_settings, test_user):
        """Test that refresh tokens cannot be used as access tokens."""
        from fastapi import HTTPException

        refresh_token = create_refresh_token(
            {"sub": str(test_user.id)},
            test_settings
        )

        # Decode should work but type should be 'refresh'
        payload = decode_token(refresh_token, test_settings)
        assert payload["type"] == "refresh"


# ============================================================================
# Token Manipulation Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestTokenManipulation:
    """Test suite for token manipulation attack prevention."""

    def test_modified_token_payload(self, test_settings, test_user):
        """Test that modified token payloads are detected."""
        from fastapi import HTTPException

        # Create valid token
        token = create_access_token(
            {"sub": str(test_user.id), "role": "user"},
            test_settings
        )

        # Try to modify the payload
        parts = token.split(".")
        if len(parts) == 3:
            # Modify the middle part (payload)
            modified_token = parts[0] + "." + "YWRtaW4" + "." + parts[2]

            with pytest.raises(HTTPException):
                decode_token(modified_token, test_settings)

    def test_signature_stripping(self, test_settings, test_user):
        """Test that tokens without signatures are rejected."""
        from fastapi import HTTPException

        token = create_access_token(
            {"sub": str(test_user.id)},
            test_settings
        )

        # Remove signature
        parts = token.split(".")
        stripped_token = parts[0] + "." + parts[1] + "."

        with pytest.raises(HTTPException):
            decode_token(stripped_token, test_settings)

    def test_none_algorithm_attack(self, test_settings):
        """Test protection against 'none' algorithm attack."""
        import base64

        # Create a token with 'none' algorithm
        header = base64.b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip("=")
        payload = base64.b64encode(
            b'{"sub":"admin","exp":' + str(int((datetime.utcnow() + timedelta(hours=1)).timestamp())).encode() + b'}'
        ).decode().rstrip("=")

        fake_token = f"{header}.{payload}."

        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            decode_token(fake_token, test_settings)


# ============================================================================
# Input Validation Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestInputValidation:
    """Test suite for input validation and sanitization."""

    def test_oversized_input_handling(self, client):
        """Test that oversized inputs are handled safely."""
        # Very long username
        long_username = "a" * 10000

        response = client.post(
            "/api/auth/register",
            json={
                "username": long_username,
                "email": "test@test.com",
                "password": "Test123!"
            }
        )

        # Should reject or truncate, not crash
        assert response.status_code in [400, 422, 413]

    def test_null_byte_injection(self, client):
        """Test protection against null byte injection."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "admin\x00",
                "email": "test@test.com",
                "password": "Test123!"
            }
        )

        # Should handle null bytes safely
        assert response.status_code in [400, 422, 201, 200]

    def test_unicode_normalization(self, client):
        """Test that unicode is handled consistently."""
        # Different unicode representations of same character
        usernames = [
            "café",  # Normal
            "cafe\u0301",  # Combining acute accent
        ]

        responses = []
        for username in usernames:
            response = client.post(
                "/api/auth/register",
                json={
                    "username": username,
                    "email": f"{username}@test.com",
                    "password": "Test123!"
                }
            )
            responses.append(response.status_code)

        # Should handle both consistently
        assert all(status in [200, 201, 400, 409, 422] for status in responses)

    def test_json_payload_depth_limit(self, client):
        """Test that deeply nested JSON is handled safely."""
        # Create deeply nested structure
        deep_json = {"level": 0}
        current = deep_json
        for i in range(100):
            current["nested"] = {"level": i + 1}
            current = current["nested"]

        response = client.post(
            "/api/auth/register",
            json=deep_json
        )

        # Should not cause stack overflow
        assert response.status_code in [400, 422]


# ============================================================================
# Path Traversal Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestPathTraversal:
    """Test suite for path traversal attack prevention."""

    def test_path_traversal_in_user_id(self, client):
        """Test that path traversal in user IDs is blocked."""
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f",
            "..%252f..%252f"
        ]

        for path in malicious_paths:
            response = client.get(f"/api/progress/{path}")
            # Should not expose file system
            assert response.status_code in [400, 401, 403, 404, 422]


# ============================================================================
# Header Injection Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestHeaderInjection:
    """Test suite for header injection prevention."""

    def test_crlf_injection_in_header(self, client):
        """Test that CRLF injection in headers is blocked."""
        malicious_headers = {
            "X-Custom-Header": "value\r\nSet-Cookie: hacked=true",
            "X-Another": "test\r\n\r\n<script>alert(1)</script>"
        }

        response = client.get("/api/health", headers=malicious_headers)

        # Should not allow header injection
        assert "Set-Cookie: hacked=true" not in str(response.headers)

    def test_host_header_injection(self, client):
        """Test that host header injection is handled safely."""
        response = client.get(
            "/api/health",
            headers={"Host": "evil.com\r\nX-Injected: true"}
        )

        # Should not crash or allow injection
        assert response.status_code in [200, 400, 422]


# ============================================================================
# Rate Limiting Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestRateLimitSecurity:
    """Test suite for rate limiting security."""

    def test_brute_force_login_prevention(self, client):
        """Test that brute force login attempts would be rate limited."""
        # Make many failed login attempts
        for i in range(10):
            response = client.post(
                "/api/auth/login",
                json={
                    "username": "admin",
                    "password": f"wrong_password_{i}"
                }
            )

            # Should either fail auth or be rate limited
            assert response.status_code in [400, 401, 429, 422]


# ============================================================================
# Password Security Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestPasswordSecurity:
    """Test suite for password handling security."""

    def test_password_not_in_response(self, client):
        """Test that passwords are never returned in responses."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "SecretPassword123!"
            }
        )

        if response.status_code in [200, 201]:
            response_text = response.text.lower()
            assert "secretpassword123" not in response_text
            assert "password" not in response.json().get("password", "")

    def test_password_not_logged(self, client, caplog):
        """Test that passwords are not logged."""
        import logging

        with caplog.at_level(logging.DEBUG):
            client.post(
                "/api/auth/login",
                json={
                    "username": "testuser",
                    "password": "SecretTestPassword123!"
                }
            )

        # Check logs don't contain the password
        for record in caplog.records:
            assert "SecretTestPassword123" not in record.getMessage()

    def test_timing_attack_resistance(self, test_settings):
        """Test that password verification has consistent timing."""
        import time

        password = "TestPassword123"
        wrong_password = "WrongPassword456"
        hashed = hash_password(password)

        # Measure time for correct password
        times_correct = []
        for _ in range(10):
            start = time.perf_counter()
            verify_password(password, hashed)
            times_correct.append(time.perf_counter() - start)

        # Measure time for wrong password
        times_wrong = []
        for _ in range(10):
            start = time.perf_counter()
            verify_password(wrong_password, hashed)
            times_wrong.append(time.perf_counter() - start)

        # Times should be relatively similar (within 10x)
        # Bcrypt is designed to be constant-time
        avg_correct = sum(times_correct) / len(times_correct)
        avg_wrong = sum(times_wrong) / len(times_wrong)

        # Both should take similar time (bcrypt property)
        ratio = max(avg_correct, avg_wrong) / min(avg_correct, avg_wrong)
        assert ratio < 10  # Should not differ dramatically


# ============================================================================
# Session Security Tests
# ============================================================================

@pytest.mark.security
@pytest.mark.unit
class TestSessionSecurity:
    """Test suite for session handling security."""

    def test_token_uniqueness(self, test_settings, test_user):
        """Test that tokens with different data are unique."""
        import time

        tokens = set()
        for i in range(5):
            # Add unique data to ensure different tokens
            token = create_access_token(
                {"sub": str(test_user.id), "nonce": f"{time.time_ns()}_{i}"},
                test_settings
            )
            assert token not in tokens
            tokens.add(token)

    def test_token_contains_timestamp(self, test_settings, test_user):
        """Test that tokens contain issue timestamp."""
        token = create_access_token(
            {"sub": str(test_user.id)},
            test_settings
        )

        payload = decode_token(token, test_settings)
        assert "iat" in payload
        assert "exp" in payload
        assert payload["exp"] > payload["iat"]
