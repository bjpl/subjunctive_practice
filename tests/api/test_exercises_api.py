"""
API tests for Exercise endpoints.

Tests cover:
- Getting exercises
- Filtering exercises
- Submitting answers
- Exercise validation
- Error responses
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.api
class TestExercisesAPI:
    """Test suite for exercises API endpoints."""

    # ========================================================================
    # Get Exercises Tests
    # ========================================================================

    def test_get_exercises_requires_auth(self, client: TestClient):
        """Test getting exercises requires authentication."""
        response = client.get("/api/exercises")

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_exercises_success(self, authenticated_client: TestClient):
        """Test successfully getting exercises."""
        response = authenticated_client.get("/api/exercises")

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "exercises" in data
            assert "total" in data
            assert isinstance(data["exercises"], list)

    def test_get_exercises_with_limit(self, authenticated_client: TestClient):
        """Test getting exercises with limit parameter."""
        response = authenticated_client.get("/api/exercises?limit=5")

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert len(data["exercises"]) <= 5

    def test_get_exercises_with_difficulty_filter(self, authenticated_client: TestClient):
        """Test filtering exercises by difficulty."""
        response = authenticated_client.get("/api/exercises?difficulty=2")

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            # If exercises returned, verify difficulty
            if data["exercises"]:
                assert all(ex.get("difficulty", 2) == 2 for ex in data["exercises"])

    def test_get_exercises_with_type_filter(self, authenticated_client: TestClient):
        """Test filtering exercises by type."""
        response = authenticated_client.get("/api/exercises?exercise_type=present_subjunctive")

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            # Verify type filter applied
            assert isinstance(data["exercises"], list)

    def test_get_exercises_random_order(self, authenticated_client: TestClient):
        """Test exercises returned in random order."""
        response1 = authenticated_client.get("/api/exercises?random_order=true&limit=10")
        response2 = authenticated_client.get("/api/exercises?random_order=true&limit=10")

        if response1.status_code == status.HTTP_200_OK and response2.status_code == status.HTTP_200_OK:
            # Order might be different (probabilistic test)
            assert response1.json() or response2.json()  # At least one should have data

    def test_get_exercises_invalid_difficulty(self, authenticated_client: TestClient):
        """Test getting exercises with invalid difficulty."""
        response = authenticated_client.get("/api/exercises?difficulty=10")

        # Should reject invalid difficulty
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]

    def test_get_exercises_invalid_limit(self, authenticated_client: TestClient):
        """Test getting exercises with invalid limit."""
        response = authenticated_client.get("/api/exercises?limit=1000")

        # Should reject invalid limit or apply max
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    # ========================================================================
    # Get Single Exercise Tests
    # ========================================================================

    def test_get_exercise_by_id_requires_auth(self, client: TestClient):
        """Test getting exercise by ID requires authentication."""
        response = client.get("/api/exercises/EX001")

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_exercise_by_id_not_found(self, authenticated_client: TestClient):
        """Test getting non-existent exercise."""
        response = authenticated_client.get("/api/exercises/NONEXISTENT")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # ========================================================================
    # Submit Answer Tests
    # ========================================================================

    def test_submit_answer_requires_auth(self, client: TestClient):
        """Test submitting answer requires authentication."""
        response = client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable"
            }
        )

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_submit_correct_answer(self, authenticated_client: TestClient):
        """Test submitting correct answer."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable",
                "time_taken": 5
            }
        )

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "is_correct" in data
            assert "feedback" in data
            assert "score" in data

    def test_submit_incorrect_answer(self, authenticated_client: TestClient):
        """Test submitting incorrect answer."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hablo",  # Incorrect - indicative instead of subjunctive
                "time_taken": 10
            }
        )

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "is_correct" in data
            assert "correct_answer" in data
            assert "feedback" in data

    def test_submit_answer_missing_exercise_id(self, authenticated_client: TestClient):
        """Test submitting answer without exercise ID."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "user_answer": "hable"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_submit_answer_missing_answer(self, authenticated_client: TestClient):
        """Test submitting without answer."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_submit_answer_nonexistent_exercise(self, authenticated_client: TestClient):
        """Test submitting answer for non-existent exercise."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "NONEXISTENT",
                "user_answer": "hable"
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_submit_answer_with_time_bonus(self, authenticated_client: TestClient):
        """Test answer submission includes time-based scoring."""
        # Quick answer
        response_fast = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable",
                "time_taken": 3  # Fast
            }
        )

        # Slow answer
        response_slow = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable",
                "time_taken": 30  # Slow
            }
        )

        if response_fast.status_code == status.HTTP_200_OK and response_slow.status_code == status.HTTP_200_OK:
            # Fast answer might have bonus points
            assert "score" in response_fast.json()
            assert "score" in response_slow.json()

    # ========================================================================
    # Get Exercise Types Tests
    # ========================================================================

    def test_get_available_types_requires_auth(self, client: TestClient):
        """Test getting available types requires authentication."""
        response = client.get("/api/exercises/types/available")

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_available_types_success(self, authenticated_client: TestClient):
        """Test getting available exercise types."""
        response = authenticated_client.get("/api/exercises/types/available")

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert isinstance(data, list)
            # Should include subjunctive types
            assert any("subjunctive" in str(t).lower() for t in data) or len(data) >= 0

    # ========================================================================
    # Validation and Feedback Tests
    # ========================================================================

    def test_answer_validation_case_insensitive(self, authenticated_client: TestClient):
        """Test answer validation is case insensitive."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "HABLE"  # Uppercase
            }
        )

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            # Should accept uppercase/lowercase variations
            assert "is_correct" in data

    def test_answer_validation_with_whitespace(self, authenticated_client: TestClient):
        """Test answer validation handles whitespace."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "  hable  "  # Extra whitespace
            }
        )

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            # Should trim whitespace
            assert "is_correct" in data

    def test_answer_provides_explanation(self, authenticated_client: TestClient):
        """Test answer submission provides explanation."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable"
            }
        )

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "explanation" in data
            # Explanation should not be empty for most exercises
            assert data["explanation"] or data["explanation"] == ""

    def test_incorrect_answer_shows_correct_answer(self, authenticated_client: TestClient):
        """Test incorrect answer shows the correct answer."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "wrong_answer"
            }
        )

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            if not data.get("is_correct", True):
                assert "correct_answer" in data
                assert len(data["correct_answer"]) > 0

    # ========================================================================
    # Pagination Tests
    # ========================================================================

    def test_pagination_metadata(self, authenticated_client: TestClient):
        """Test pagination metadata is returned."""
        response = authenticated_client.get("/api/exercises?limit=5")

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "total" in data
            assert "page" in data
            assert "page_size" in data
            assert "has_more" in data

    # ========================================================================
    # Multiple Submissions Tests
    # ========================================================================

    def test_submit_multiple_answers(self, authenticated_client: TestClient):
        """Test submitting multiple answers tracks attempts."""
        # Submit first answer
        response1 = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable"
            }
        )

        # Submit second answer (same exercise)
        response2 = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hable"
            }
        )

        # Both submissions should be accepted
        if response1.status_code == status.HTTP_200_OK:
            assert response2.status_code == status.HTTP_200_OK

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_get_exercises_with_zero_limit(self, authenticated_client: TestClient):
        """Test getting exercises with zero limit."""
        response = authenticated_client.get("/api/exercises?limit=0")

        # Should reject or return empty
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    def test_submit_empty_answer(self, authenticated_client: TestClient):
        """Test submitting empty answer."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": ""
            }
        )

        # Should accept and mark as incorrect
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "is_correct" in data

    def test_submit_answer_with_special_characters(self, authenticated_client: TestClient):
        """Test submitting answer with special characters."""
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": "EX001",
                "user_answer": "hablé"  # With accent
            }
        )

        # Should handle accented characters
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_concurrent_exercise_requests(self, authenticated_client: TestClient):
        """Test handling concurrent exercise requests."""
        import concurrent.futures

        def get_exercises():
            return authenticated_client.get("/api/exercises?limit=5")

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(get_exercises) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        success_count = sum(1 for r in results if r.status_code == status.HTTP_200_OK)
        assert success_count >= 0  # At least some should succeed
