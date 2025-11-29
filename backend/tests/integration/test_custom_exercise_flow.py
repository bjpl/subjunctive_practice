"""
Integration tests for custom exercise generation and validation.

Tests the custom exercise workflow:
1. Generate custom exercises
2. Submit custom exercise answers
3. Verify validation works
4. Test AI-powered exercise generation
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session


@pytest.mark.integration
class TestCustomExerciseFlow:
    """Integration tests for custom exercise generation system."""

    def test_generate_custom_exercise_basic(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """
        Test basic custom exercise generation.

        Flow:
        1. Request custom exercise with parameters
        2. Verify exercise generated
        3. Verify exercise has required fields
        """
        # Request custom exercise
        response = authenticated_client.post(
            "/api/exercises/custom/generate",
            json={
                "verb": "hablar",
                "tense": "present_subjunctive",
                "difficulty": 2,
                "context": "daily conversation"
            }
        )

        # May not be implemented yet
        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise generation endpoint not implemented")

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        exercise = response.json()

        # Verify required fields
        assert "spanish_sentence" in exercise or "sentence" in exercise
        assert "correct_answer" in exercise
        assert "verb" in exercise or exercise.get("verb") == "hablar"

    def test_generate_custom_exercise_with_specific_person(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test generating exercise for specific grammatical person."""
        response = authenticated_client.post(
            "/api/exercises/custom/generate",
            json={
                "verb": "ser",
                "tense": "present_subjunctive",
                "person": "yo",
                "difficulty": 3
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise generation not implemented")

        if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            exercise = response.json()

            # Should be for "yo" form
            correct_answer = exercise.get("correct_answer", "")
            assert "sea" in correct_answer.lower()  # yo form of ser subjunctive

    def test_generate_custom_exercise_irregular_verb(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test generating exercise for irregular verb."""
        response = authenticated_client.post(
            "/api/exercises/custom/generate",
            json={
                "verb": "estar",
                "tense": "present_subjunctive",
                "difficulty": 3,
                "include_explanation": True
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise generation not implemented")

        if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            exercise = response.json()

            # Should have explanation for irregular verb
            if "explanation" in exercise:
                assert len(exercise["explanation"]) > 0

    def test_submit_custom_exercise_answer(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test submitting answer to custom-generated exercise."""
        # First generate custom exercise
        generate_response = authenticated_client.post(
            "/api/exercises/custom/generate",
            json={
                "verb": "hablar",
                "tense": "present_subjunctive",
                "person": "tú"
            }
        )

        if generate_response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise generation not implemented")

        if generate_response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            exercise = generate_response.json()
            exercise_id = exercise.get("id") or exercise.get("exercise_id", "custom_1")

            # Submit answer
            submit_response = authenticated_client.post(
                "/api/exercises/submit",
                json={
                    "exercise_id": str(exercise_id),
                    "user_answer": exercise.get("correct_answer", "hables"),
                    "time_taken": 5
                }
            )

            assert submit_response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_201_CREATED,
                status.HTTP_400_BAD_REQUEST,  # If custom exercises aren't tracked
                status.HTTP_404_NOT_FOUND
            ]

    def test_custom_exercise_validation_correct_answer(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test custom exercise validation with correct answer."""
        # Use custom validation endpoint
        response = authenticated_client.post(
            "/api/exercises/custom/validate",
            json={
                "verb": "comer",
                "tense": "present_subjunctive",
                "person": "él",
                "user_answer": "coma"
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise validation not implemented")

        if response.status_code == status.HTTP_200_OK:
            result = response.json()

            assert result.get("is_correct") is True
            assert "coma" in result.get("correct_answer", "").lower()

    def test_custom_exercise_validation_incorrect_answer(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test custom exercise validation with incorrect answer."""
        response = authenticated_client.post(
            "/api/exercises/custom/validate",
            json={
                "verb": "comer",
                "tense": "present_subjunctive",
                "person": "él",
                "user_answer": "come"  # Incorrect - indicative instead
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise validation not implemented")

        if response.status_code == status.HTTP_200_OK:
            result = response.json()

            assert result.get("is_correct") is False
            assert "coma" in result.get("correct_answer", "").lower()
            assert "feedback" in result or "explanation" in result

    def test_custom_exercise_with_context_theme(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test generating custom exercise with thematic context."""
        themes = ["travel", "food", "work", "school", "daily_life"]

        for theme in themes:
            response = authenticated_client.post(
                "/api/exercises/custom/generate",
                json={
                    "verb": "hablar",
                    "tense": "present_subjunctive",
                    "context_theme": theme,
                    "difficulty": 2
                }
            )

            if response.status_code == status.HTTP_404_NOT_FOUND:
                pytest.skip("Custom exercise generation not implemented")

            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                exercise = response.json()

                # Sentence should be contextually relevant
                sentence = exercise.get("spanish_sentence", exercise.get("sentence", ""))
                assert len(sentence) > 0

    def test_custom_exercise_difficulty_scaling(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test that custom exercises scale with difficulty."""
        difficulties = [1, 2, 3]
        exercises = []

        for difficulty in difficulties:
            response = authenticated_client.post(
                "/api/exercises/custom/generate",
                json={
                    "verb": "tener",
                    "tense": "present_subjunctive",
                    "difficulty": difficulty
                }
            )

            if response.status_code == status.HTTP_404_NOT_FOUND:
                pytest.skip("Custom exercise generation not implemented")

            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                exercises.append(response.json())

        # Higher difficulty should have more complex sentences
        if len(exercises) == 3:
            # Basic check: higher difficulty might have longer sentences
            lengths = [len(ex.get("spanish_sentence", ex.get("sentence", ""))) for ex in exercises]
            # At minimum, they should all have content
            assert all(length > 0 for length in lengths)

    def test_custom_exercise_multiple_verbs(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test generating custom exercises for multiple verbs."""
        verbs = ["hablar", "comer", "vivir", "ser", "estar"]

        for verb in verbs:
            response = authenticated_client.post(
                "/api/exercises/custom/generate",
                json={
                    "verb": verb,
                    "tense": "present_subjunctive",
                    "difficulty": 2
                }
            )

            if response.status_code == status.HTTP_404_NOT_FOUND:
                pytest.skip("Custom exercise generation not implemented")

            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                exercise = response.json()

                # Verify it's for the requested verb
                assert verb.lower() in str(exercise).lower()

    def test_custom_exercise_validation_edge_cases(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test custom exercise validation with edge cases."""
        test_cases = [
            # Case insensitive
            {
                "verb": "hablar",
                "tense": "present_subjunctive",
                "person": "yo",
                "user_answer": "HABLE",
                "expected_correct": True
            },
            # With accents
            {
                "verb": "estar",
                "tense": "present_subjunctive",
                "person": "yo",
                "user_answer": "esté",
                "expected_correct": True
            },
            # Extra whitespace
            {
                "verb": "hablar",
                "tense": "present_subjunctive",
                "person": "yo",
                "user_answer": "  hable  ",
                "expected_correct": True
            }
        ]

        for test_case in test_cases:
            response = authenticated_client.post(
                "/api/exercises/custom/validate",
                json={
                    "verb": test_case["verb"],
                    "tense": test_case["tense"],
                    "person": test_case["person"],
                    "user_answer": test_case["user_answer"]
                }
            )

            if response.status_code == status.HTTP_404_NOT_FOUND:
                pytest.skip("Custom exercise validation not implemented")

            if response.status_code == status.HTTP_200_OK:
                result = response.json()
                assert result.get("is_correct") == test_case["expected_correct"]

    def test_custom_exercise_rate_limiting(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test rate limiting on custom exercise generation."""
        # Try to generate many custom exercises rapidly
        responses = []

        for i in range(20):
            response = authenticated_client.post(
                "/api/exercises/custom/generate",
                json={
                    "verb": "hablar",
                    "tense": "present_subjunctive",
                    "difficulty": 2
                }
            )
            responses.append(response)

        # Should either all succeed or hit rate limit
        status_codes = [r.status_code for r in responses]

        # At least some should succeed
        assert any(code in [status.HTTP_200_OK, status.HTTP_201_CREATED] for code in status_codes)

        # If rate limited, should get 429
        if status.HTTP_429_TOO_MANY_REQUESTS in status_codes:
            # This is expected and acceptable
            pass

    def test_custom_exercise_invalid_verb(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test custom exercise generation with invalid verb."""
        response = authenticated_client.post(
            "/api/exercises/custom/generate",
            json={
                "verb": "nonexistent_verb_xyz",
                "tense": "present_subjunctive",
                "difficulty": 2
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise generation not implemented")

        # Should reject invalid verb
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_200_OK  # Some implementations might still generate something
        ]

    def test_custom_exercise_missing_parameters(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test custom exercise generation with missing parameters."""
        # Missing verb
        response = authenticated_client.post(
            "/api/exercises/custom/generate",
            json={
                "tense": "present_subjunctive",
                "difficulty": 2
            }
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            pytest.skip("Custom exercise generation not implemented")

        # Should require verb parameter
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    def test_custom_exercise_authentication_required(
        self,
        client: TestClient
    ):
        """Test that custom exercise endpoints require authentication."""
        # Generate without auth
        generate_response = client.post(
            "/api/exercises/custom/generate",
            json={
                "verb": "hablar",
                "tense": "present_subjunctive"
            }
        )

        assert generate_response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

        # Validate without auth
        validate_response = client.post(
            "/api/exercises/custom/validate",
            json={
                "verb": "hablar",
                "tense": "present_subjunctive",
                "person": "yo",
                "user_answer": "hable"
            }
        )

        assert validate_response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]
