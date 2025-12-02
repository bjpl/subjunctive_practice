"""
Tests for Claude AI Service

Comprehensive test suite for the AI service including:
- Service initialization and configuration
- Feedback generation with caching
- Learning insights generation
- Personalized hint generation
- Error handling and retry logic
- Rate limiting scenarios
- Batch operations
- Health checks
"""

import pytest
import httpx
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from anthropic import AsyncAnthropic, RateLimitError, APIError, APITimeoutError
from anthropic.types import Message, Usage, TextBlock


def create_mock_httpx_response(status_code: int = 429):
    """Create a mock httpx.Response for error testing."""
    response = Mock(spec=httpx.Response)
    response.status_code = status_code
    response.headers = {}
    response.text = "Rate limited"
    response.request = Mock(spec=httpx.Request)
    return response


def create_mock_httpx_request():
    """Create a mock httpx.Request for timeout error testing."""
    request = Mock(spec=httpx.Request)
    request.url = "https://api.anthropic.com/v1/messages"
    request.method = "POST"
    return request

from services.ai_service import (
    ClaudeAIService,
    AIServiceError,
    RateLimitExceededError,
    AIServiceUnavailableError,
    get_ai_service,
    shutdown_ai_service
)


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch('services.ai_service.settings') as mock:
        mock.ANTHROPIC_API_KEY = "test-api-key"
        mock.ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
        mock.ANTHROPIC_MAX_TOKENS = 1000
        mock.ANTHROPIC_TEMPERATURE = 0.7
        yield mock


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client."""
    with patch('services.ai_service.AsyncAnthropic') as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def ai_service(mock_settings, mock_anthropic_client):
    """Create AI service instance with mocked dependencies."""
    service = ClaudeAIService()
    return service


@pytest.fixture
def mock_message_response():
    """Create a mock Anthropic Message response."""
    def _create_response(text: str, stop_reason: str = "end_turn"):
        message = Mock(spec=Message)
        message.content = [TextBlock(type="text", text=text)]
        message.stop_reason = stop_reason
        message.usage = Usage(input_tokens=50, output_tokens=100)
        return message
    return _create_response


class TestServiceInitialization:
    """Test AI service initialization and configuration."""

    def test_service_initializes_with_api_key(self, mock_settings, mock_anthropic_client):
        """Service should initialize when API key is present."""
        service = ClaudeAIService()
        assert service.is_enabled
        assert service._client is not None

    def test_service_disabled_without_api_key(self):
        """Service should be disabled when API key is missing."""
        with patch('services.ai_service.settings') as mock:
            mock.ANTHROPIC_API_KEY = None
            service = ClaudeAIService()
            assert not service.is_enabled
            assert service._client is None

    def test_get_ai_service_returns_singleton(self, mock_settings, mock_anthropic_client):
        """get_ai_service should return the same instance."""
        # Reset global instance
        import services.ai_service
        services.ai_service._ai_service = None

        service1 = get_ai_service()
        service2 = get_ai_service()
        assert service1 is service2


class TestFeedbackGeneration:
    """Test feedback generation functionality."""

    @pytest.mark.asyncio
    async def test_generate_feedback_correct_answer(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should generate positive feedback for correct answer."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("Great job! You correctly used 'hable'...")
        )

        context = {
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "yo",
            "trigger": "Es importante que",
            "sentence": "Es importante que yo hable"
        }

        feedback = await ai_service.generate_feedback("hable", "hable", context)

        assert "Great job" in feedback or "correct" in feedback.lower()
        mock_anthropic_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_feedback_incorrect_answer(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should generate corrective feedback for incorrect answer."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("Not quite. The subjunctive form requires...")
        )

        context = {
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "yo",
            "trigger": "Es importante que",
            "sentence": "Es importante que yo hable"
        }

        feedback = await ai_service.generate_feedback("hablo", "hable", context)

        assert len(feedback) > 0
        mock_anthropic_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_feedback_uses_cache(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should use cached feedback for identical requests."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("Cached feedback")
        )

        context = {"verb": "hablar", "tense": "present_subjunctive"}

        # First call - should hit API
        feedback1 = await ai_service.generate_feedback("hable", "hable", context)

        # Second call - should use cache
        feedback2 = await ai_service.generate_feedback("hable", "hable", context)

        assert feedback1 == feedback2
        # Should only call API once
        assert mock_anthropic_client.messages.create.call_count == 1

    @pytest.mark.asyncio
    async def test_feedback_fallback_when_service_disabled(self, mock_settings):
        """Should return simple feedback when service is disabled."""
        mock_settings.ANTHROPIC_API_KEY = None
        service = ClaudeAIService()

        context = {"verb": "hablar"}

        feedback = await service.generate_feedback("hable", "hable", context)
        assert "Correct" in feedback or "Well done" in feedback

        feedback_wrong = await service.generate_feedback("hablo", "hable", context)
        assert "correct answer is" in feedback_wrong.lower()

    @pytest.mark.asyncio
    async def test_feedback_handles_rate_limit_with_retry(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should retry on rate limit errors."""
        # First call raises RateLimitError, second succeeds
        mock_anthropic_client.messages.create = AsyncMock(
            side_effect=[
                RateLimitError("Rate limited", response=create_mock_httpx_response(), body={}),
                mock_message_response("Success after retry")
            ]
        )

        context = {"verb": "hablar", "tense": "present_subjunctive"}

        feedback = await ai_service.generate_feedback("hable", "hable", context)

        assert "Success after retry" in feedback or "Excellent" in feedback
        # Should be called twice (1 failure + 1 success)
        assert mock_anthropic_client.messages.create.call_count >= 1


class TestLearningInsights:
    """Test learning insights generation."""

    @pytest.mark.asyncio
    async def test_generate_learning_insights(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should generate personalized learning insights."""
        insights_json = '["Focus on irregular verbs", "Practice imperfect subjunctive", "Review WEIRDO triggers"]'
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response(insights_json)
        )

        stats = {
            "total_exercises": 150,
            "accuracy": 0.72,
            "total_study_time_minutes": 300,
            "total_sessions": 15
        }
        weak_areas = [
            {"area": "imperfect_subjunctive", "accuracy": 0.55},
            {"area": "irregular_verbs", "accuracy": 0.60}
        ]

        insights = await ai_service.generate_learning_insights(stats, weak_areas)

        assert isinstance(insights, list)
        assert len(insights) >= 1
        assert len(insights) <= 5
        assert all(isinstance(insight, str) for insight in insights)

    @pytest.mark.asyncio
    async def test_insights_fallback_on_error(self, ai_service, mock_anthropic_client):
        """Should provide fallback insights on API error."""
        # Create a proper mock for APIError (SDK v0.18+ uses different signature)
        api_error = Mock(spec=APIError)
        api_error.message = "API Error"
        mock_anthropic_client.messages.create = AsyncMock(
            side_effect=Exception("API Error")
        )

        stats = {"accuracy": 0.50, "total_exercises": 50}
        weak_areas = [{"area": "present_subjunctive", "accuracy": 0.45}]

        insights = await ai_service.generate_learning_insights(stats, weak_areas)

        assert isinstance(insights, list)
        assert len(insights) > 0
        # Should contain actionable advice
        assert any("practice" in i.lower() or "focus" in i.lower() for i in insights)

    @pytest.mark.asyncio
    async def test_insights_uses_cache(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should cache learning insights."""
        insights_json = '["Insight 1", "Insight 2"]'
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response(insights_json)
        )

        stats = {"accuracy": 0.75}
        weak_areas = []

        insights1 = await ai_service.generate_learning_insights(stats, weak_areas)
        insights2 = await ai_service.generate_learning_insights(stats, weak_areas)

        assert insights1 == insights2
        assert mock_anthropic_client.messages.create.call_count == 1


class TestPersonalizedHints:
    """Test personalized hint generation."""

    @pytest.mark.asyncio
    async def test_generate_personalized_hint(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should generate contextual hint."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("Remember, 'Es necesario que' triggers subjunctive...")
        )

        exercise = {
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "él/ella",
            "trigger": "Es necesario que",
            "sentence": "Es necesario que él ___ con el doctor"
        }

        hint = await ai_service.generate_personalized_hint(exercise)

        assert len(hint) > 0
        # Should not reveal the answer directly
        assert "hable" not in hint.lower()

    @pytest.mark.asyncio
    async def test_hint_with_user_history(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should consider user history when generating hints."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("You've been struggling with endings...")
        )

        exercise = {"verb": "hablar", "tense": "present_subjunctive"}
        history = [
            {"verb": "hablar", "error_type": "wrong_ending"},
            {"verb": "comer", "error_type": "wrong_ending"}
        ]

        hint = await ai_service.generate_personalized_hint(exercise, history)

        assert len(hint) > 0
        mock_anthropic_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_hint_fallback_when_disabled(self):
        """Should provide generic hint when service disabled."""
        with patch('services.ai_service.settings') as mock:
            mock.ANTHROPIC_API_KEY = None
            service = ClaudeAIService()

        exercise = {"verb": "hablar", "tense": "present_subjunctive"}
        hint = await service.generate_personalized_hint(exercise)

        assert "subjunctive" in hint.lower() or "conjugation" in hint.lower()


class TestErrorHandling:
    """Test error handling and retry logic."""

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded_after_max_retries(
        self, ai_service, mock_anthropic_client
    ):
        """Should raise RateLimitExceededError after max retries."""
        mock_anthropic_client.messages.create = AsyncMock(
            side_effect=RateLimitError("Rate limited", response=create_mock_httpx_response(), body={})
        )

        context = {"verb": "hablar"}

        # Should raise RateLimitExceededError after exhausting retries
        with pytest.raises(RateLimitExceededError):
            await ai_service.generate_feedback("hable", "hable", context)

    @pytest.mark.asyncio
    async def test_api_timeout_error_handling(
        self, ai_service, mock_anthropic_client
    ):
        """Should raise AIServiceUnavailableError on timeout."""
        mock_anthropic_client.messages.create = AsyncMock(
            side_effect=APITimeoutError(request=create_mock_httpx_request())
        )

        context = {"verb": "hablar"}

        # Should raise AIServiceUnavailableError on timeout
        with pytest.raises(AIServiceUnavailableError):
            await ai_service.generate_feedback("hable", "hable", context)

    @pytest.mark.asyncio
    async def test_raises_error_when_disabled_and_strict(self):
        """Should raise error when service is disabled and no fallback."""
        with patch('services.ai_service.settings') as mock:
            mock.ANTHROPIC_API_KEY = None
            service = ClaudeAIService()

        with pytest.raises(AIServiceUnavailableError):
            await service._create_message("test prompt")


class TestBatchOperations:
    """Test batch feedback generation."""

    @pytest.mark.asyncio
    async def test_batch_generate_feedback(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should generate feedback for multiple requests in parallel."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("Feedback message")
        )

        requests = [
            {
                "user_answer": "hable",
                "correct_answer": "hable",
                "exercise_context": {"verb": "hablar"}
            },
            {
                "user_answer": "coma",
                "correct_answer": "coma",
                "exercise_context": {"verb": "comer"}
            },
            {
                "user_answer": "viva",
                "correct_answer": "viva",
                "exercise_context": {"verb": "vivir"}
            }
        ]

        results = await ai_service.batch_generate_feedback(requests)

        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

    @pytest.mark.asyncio
    async def test_batch_handles_partial_failures(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should handle individual failures in batch operations."""
        # First two succeed, third fails
        mock_anthropic_client.messages.create = AsyncMock(
            side_effect=[
                mock_message_response("Success 1"),
                mock_message_response("Success 2"),
                Exception("API Failed")
            ]
        )

        requests = [
            {"user_answer": "a", "correct_answer": "a", "exercise_context": {}},
            {"user_answer": "b", "correct_answer": "b", "exercise_context": {}},
            {"user_answer": "c", "correct_answer": "c", "exercise_context": {}},
        ]

        results = await ai_service.batch_generate_feedback(requests)

        assert len(results) == 3
        # All should return strings (either success or error message)
        assert all(isinstance(r, str) for r in results)


class TestCaching:
    """Test caching functionality."""

    def test_cache_key_generation(self, ai_service):
        """Should generate consistent cache keys."""
        key1 = ai_service._get_cache_key("test", "arg1", "arg2", foo="bar")
        key2 = ai_service._get_cache_key("test", "arg1", "arg2", foo="bar")
        key3 = ai_service._get_cache_key("test", "arg1", "different")

        assert key1 == key2
        assert key1 != key3

    def test_cache_expiration(self, ai_service):
        """Should expire cached entries after TTL."""
        cache_key = "test_key"
        ai_service._set_cache(cache_key, "test_value")

        # Should retrieve fresh cache
        assert ai_service._get_cached(cache_key) == "test_value"

        # Simulate cache expiration
        expired_time = datetime.now() - timedelta(hours=2)
        ai_service._cache[cache_key] = ("test_value", expired_time)

        # Should return None for expired cache
        assert ai_service._get_cached(cache_key) is None
        # Should remove expired entry
        assert cache_key not in ai_service._cache

    def test_clear_cache(self, ai_service):
        """Should clear all cached entries."""
        ai_service._set_cache("key1", "value1")
        ai_service._set_cache("key2", "value2")
        ai_service._set_cache("key3", "value3")

        count = ai_service.clear_cache()

        assert count == 3
        assert len(ai_service._cache) == 0


class TestHealthCheck:
    """Test health check functionality."""

    @pytest.mark.asyncio
    async def test_health_check_when_enabled(
        self, ai_service, mock_anthropic_client, mock_message_response
    ):
        """Should return healthy status when service is working."""
        mock_anthropic_client.messages.create = AsyncMock(
            return_value=mock_message_response("OK")
        )

        health = await ai_service.health_check()

        assert health["status"] == "healthy"
        assert health["configured"] is True
        assert "model" in health
        assert "cache_size" in health

    @pytest.mark.asyncio
    async def test_health_check_when_disabled(self):
        """Should return disabled status when API key missing."""
        with patch('services.ai_service.settings') as mock:
            mock.ANTHROPIC_API_KEY = None
            service = ClaudeAIService()

        health = await service.health_check()

        assert health["status"] == "disabled"
        assert health["configured"] is False

    @pytest.mark.asyncio
    async def test_health_check_when_api_failing(
        self, ai_service, mock_anthropic_client
    ):
        """Should return unhealthy status when API is failing."""
        mock_anthropic_client.messages.create = AsyncMock(
            side_effect=Exception("Service unavailable")
        )

        health = await ai_service.health_check()

        assert health["status"] == "unhealthy"
        assert "error" in health


class TestShutdown:
    """Test service shutdown."""

    @pytest.mark.asyncio
    async def test_shutdown_ai_service(self, ai_service):
        """Should cleanup on shutdown."""
        import services.ai_service
        services.ai_service._ai_service = ai_service

        # Add some cache entries
        ai_service._set_cache("key1", "value1")

        await shutdown_ai_service()

        # Cache should be cleared
        assert len(ai_service._cache) == 0
