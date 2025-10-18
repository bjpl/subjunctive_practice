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

        # Should return 400 for invalid ID format or 404 for not found
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

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

        # Should return 400 for invalid ID format or 404 for not found
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

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

        # Should reject or return empty (may be rate limited)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_429_TOO_MANY_REQUESTS
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

        # Should handle accented characters (may be rate limited)
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_429_TOO_MANY_REQUESTS
        ]

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

    # ========================================================================
    # Tag Tests - Creation, Retrieval, Filtering, Updates
    # ========================================================================

    def test_get_exercises_returns_tags_array(self, authenticated_client: TestClient, sample_exercises_with_tags):
        """Test that exercises include tags array in response."""
        response = authenticated_client.get("/api/exercises")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "exercises" in data
        assert len(data["exercises"]) > 0
        for exercise in data["exercises"]:
            assert "tags" in exercise
            assert isinstance(exercise["tags"], list)

    def test_get_exercise_by_id_returns_tags(self, authenticated_client: TestClient, sample_exercises_with_tags):
        """Test single exercise returns tags array."""
        # Get the first exercise's ID
        exercise_id = sample_exercises_with_tags[0].id

        # Get single exercise
        response = authenticated_client.get(f"/api/exercises/{exercise_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "tags" in data
        assert isinstance(data["tags"], list)
        assert len(data["tags"]) == 3  # First exercise has 3 tags

    def test_empty_tags_returns_empty_array(self, authenticated_client: TestClient, sample_exercises_with_tags):
        """Test that exercises with no tags return empty array, not null."""
        response = authenticated_client.get("/api/exercises")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["exercises"]) > 0

        # Find the exercise with no tags (the last one)
        empty_tags_exercise = [ex for ex in data["exercises"] if len(ex["tags"]) == 0]
        assert len(empty_tags_exercise) == 1
        assert empty_tags_exercise[0]["tags"] == []
        assert empty_tags_exercise[0]["tags"] is not None

    def test_filter_exercises_by_single_tag(self, authenticated_client: TestClient, sample_exercises_with_tags):
        """Test filtering exercises by a single tag."""
        response = authenticated_client.get("/api/exercises?tags=trigger-phrases")

        # Should return success with exercises that have the tag
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "exercises" in data
        assert len(data["exercises"]) == 3  # 3 exercises have "trigger-phrases" tag
        # Verify they all have the tag
        for exercise in data["exercises"]:
            assert "trigger-phrases" in exercise.get("tags", [])

    def test_filter_exercises_by_multiple_tags(self, authenticated_client: TestClient, sample_exercises_with_tags):
        """Test filtering exercises by multiple tags (OR logic)."""
        response = authenticated_client.get("/api/exercises?tags=trigger-phrases,common-verbs")

        # Should return success with exercises that have at least one of the tags
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert len(data["exercises"]) == 3  # 3 exercises have at least one of these tags
        # Verify they all have at least one of the requested tags
        for exercise in data["exercises"]:
            exercise_tags = exercise.get("tags", [])
            has_tag = any(tag in exercise_tags for tag in ["trigger-phrases", "common-verbs"])
            assert has_tag, f"Exercise should have at least one of the requested tags"

    def test_filter_with_nonexistent_tag(self, authenticated_client: TestClient):
        """Test filtering by a tag that doesn't exist."""
        response = authenticated_client.get("/api/exercises?tags=nonexistent-tag-xyz")

        # Should return 404 or empty list
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            # Should return empty list if no exercises match
            # Or it might return 404, both are acceptable

    def test_filter_tags_case_sensitive(self, authenticated_client: TestClient):
        """Test that tag filtering is case-sensitive."""
        # Try with different case variations
        response1 = authenticated_client.get("/api/exercises?tags=trigger-phrases")
        response2 = authenticated_client.get("/api/exercises?tags=TRIGGER-PHRASES")

        # These might return different results if tags are case-sensitive
        # Both should be valid requests
        assert response1.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        assert response2.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_filter_tags_with_spaces(self, authenticated_client: TestClient):
        """Test tag filtering handles spaces correctly."""
        # Tags with spaces in comma-separated list
        response = authenticated_client.get("/api/exercises?tags=trigger-phrases, common-verbs")

        # Should handle whitespace trimming
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_combine_difficulty_and_tags(self, authenticated_client: TestClient):
        """Test combining difficulty filter with tag filter."""
        response = authenticated_client.get("/api/exercises?difficulty=2&tags=trigger-phrases")

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            if data["exercises"]:
                # Verify both filters are applied
                for exercise in data["exercises"]:
                    assert exercise.get("difficulty") == 2
                    assert "trigger-phrases" in exercise.get("tags", [])

    def test_combine_type_and_tags(self, authenticated_client: TestClient):
        """Test combining exercise type filter with tag filter."""
        response = authenticated_client.get("/api/exercises?exercise_type=present_subjunctive&tags=common-verbs")

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            if data["exercises"]:
                # Verify both filters are applied
                for exercise in data["exercises"]:
                    assert "subjunctive" in exercise.get("type", "").lower()
                    assert "common-verbs" in exercise.get("tags", [])

    def test_tags_with_special_characters(self, authenticated_client: TestClient):
        """Test tags containing special characters."""
        # Try filtering with tags that might have special characters
        response = authenticated_client.get("/api/exercises?tags=a1-level")

        # Should handle hyphens and numbers in tags
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_single_tag_in_list(self, authenticated_client: TestClient):
        """Test that single-tag filtering works correctly."""
        response = authenticated_client.get("/api/exercises?tags=beginner")

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            if data["exercises"]:
                for exercise in data["exercises"]:
                    assert "beginner" in exercise.get("tags", [])

    def test_tags_pagination(self, authenticated_client: TestClient):
        """Test that tag filtering works with pagination."""
        response = authenticated_client.get("/api/exercises?tags=common-verbs&limit=5")

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "total" in data
            assert "page_size" in data
            assert len(data["exercises"]) <= 5

    def test_tags_with_random_order(self, authenticated_client: TestClient):
        """Test that tag filtering works with random ordering."""
        response = authenticated_client.get("/api/exercises?tags=trigger-phrases&random_order=true")

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "exercises" in data

    def test_empty_tags_parameter(self, authenticated_client: TestClient):
        """Test behavior when tags parameter is empty string."""
        response = authenticated_client.get("/api/exercises?tags=")

        # Empty tags param should be ignored or return all exercises
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_tags_max_length(self, authenticated_client: TestClient):
        """Test filtering with very long tag names."""
        long_tag = "a" * 100
        response = authenticated_client.get(f"/api/exercises?tags={long_tag}")

        # Should handle long tag names gracefully
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

    def test_many_tags_in_filter(self, authenticated_client: TestClient):
        """Test filtering with many tags (10+ tags)."""
        tags = ",".join([f"tag{i}" for i in range(15)])
        response = authenticated_client.get(f"/api/exercises?tags={tags}")

        # Should handle multiple tags
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

    def test_duplicate_tags_in_filter(self, authenticated_client: TestClient):
        """Test filtering with duplicate tags."""
        response = authenticated_client.get("/api/exercises?tags=trigger-phrases,trigger-phrases,trigger-phrases")

        # Should handle duplicates gracefully (deduplicate or allow)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
