"""
Comprehensive AI Service Mock Fixtures

This module provides mock fixtures for all major AI APIs:
- Anthropic Claude (Claude 3.5 Sonnet, Claude 3 Opus) - ACTIVE
- OpenAI (GPT-4, GPT-3.5) - LEGACY (for testing compatibility only)
- Google Gemini (Gemini Pro, Gemini Ultra) - FUTURE

NOTE: OpenAI mocks are kept for testing purposes and multi-provider patterns.
They do NOT require the openai package to be installed as they use mocks.
The actual application uses Anthropic Claude API exclusively.

Each mock includes:
- Standard completion responses
- Streaming responses
- Error scenarios (rate limits, timeouts, authentication)
- Token usage tracking
"""

import pytest
from typing import List, Dict, Any, AsyncGenerator
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime


# ============================================================================
# Anthropic Claude Mocks
# ============================================================================

@pytest.fixture
def mock_anthropic_complete():
    """
    Mock Anthropic Claude API with comprehensive completion responses.

    Returns a fully configured mock that simulates:
    - Standard message completion
    - Realistic token usage
    - Message metadata (ID, model, role)
    """
    with patch("anthropic.Anthropic") as mock_client:
        mock_instance = Mock()

        # Create realistic response structure
        mock_response = Mock()
        mock_response.id = "msg_test123abc"
        mock_response.type = "message"
        mock_response.role = "assistant"
        mock_response.model = "claude-3-5-sonnet-20241022"
        mock_response.stop_reason = "end_turn"

        # Mock content
        mock_content_block = Mock()
        mock_content_block.type = "text"
        mock_content_block.text = "Mocked Claude response"
        mock_response.content = [mock_content_block]

        # Mock usage statistics
        mock_usage = Mock()
        mock_usage.input_tokens = 10
        mock_usage.output_tokens = 20
        mock_response.usage = mock_usage

        mock_instance.messages.create.return_value = mock_response
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_anthropic_streaming():
    """
    Mock Anthropic Claude API with streaming responses.

    Simulates event-based streaming with:
    - Message start event
    - Content block delta events
    - Message completion event
    """
    with patch("anthropic.Anthropic") as mock_client:
        mock_instance = AsyncMock()

        async def mock_stream_generator():
            """Async generator simulating streaming response"""
            events = [
                {
                    "type": "message_start",
                    "message": {
                        "id": "msg_stream_test",
                        "type": "message",
                        "role": "assistant",
                        "model": "claude-3-5-sonnet-20241022"
                    }
                },
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "text", "text": ""}
                },
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "Mocked "}
                },
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "streaming "}
                },
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "response "}
                },
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "from Claude"}
                },
                {
                    "type": "content_block_stop",
                    "index": 0
                },
                {
                    "type": "message_delta",
                    "delta": {"stop_reason": "end_turn"},
                    "usage": {"output_tokens": 4}
                },
                {
                    "type": "message_stop"
                }
            ]

            for event in events:
                yield Mock(**event)

        mock_instance.messages.stream.return_value.__aenter__.return_value = mock_stream_generator()
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_anthropic_errors():
    """
    Mock Anthropic Claude API error scenarios.

    Provides methods for testing:
    - Rate limit errors (429)
    - API errors (500, 503)
    - Authentication errors (401)
    - Invalid request errors (400)
    """
    class MockAnthropicError:
        def __init__(self):
            self.mock_client_patch = patch("anthropic.Anthropic")

        def __enter__(self):
            self.mock_client = self.mock_client_patch.__enter__()
            self.mock_instance = Mock()
            self.mock_client.return_value = self.mock_instance
            return self

        def __exit__(self, *args):
            return self.mock_client_patch.__exit__(*args)

        def rate_limit_error(self):
            """Simulate rate limit error"""
            error = Mock()
            error.status_code = 429
            error.message = "Rate limit exceeded"
            error.type = "rate_limit_error"
            self.mock_instance.messages.create.side_effect = Exception("Rate limit exceeded")
            return self.mock_instance

        def api_error(self):
            """Simulate API error"""
            error = Mock()
            error.status_code = 500
            error.message = "Internal server error"
            error.type = "api_error"
            self.mock_instance.messages.create.side_effect = Exception("API Error")
            return self.mock_instance

        def auth_error(self):
            """Simulate authentication error"""
            error = Mock()
            error.status_code = 401
            error.message = "Invalid API key"
            error.type = "authentication_error"
            self.mock_instance.messages.create.side_effect = Exception("Invalid API key")
            return self.mock_instance

        def timeout_error(self):
            """Simulate timeout error"""
            import asyncio
            self.mock_instance.messages.create.side_effect = asyncio.TimeoutError("Request timeout")
            return self.mock_instance

    yield MockAnthropicError


@pytest.fixture
def mock_anthropic_custom_response():
    """
    Mock Anthropic Claude API with customizable responses.

    Allows tests to define specific response content.
    """
    with patch("anthropic.Anthropic") as mock_client:
        mock_instance = Mock()

        def create_response(text: str, tokens_in: int = 10, tokens_out: int = None):
            """Create custom mock response"""
            if tokens_out is None:
                tokens_out = len(text.split())

            mock_response = Mock()
            mock_response.id = f"msg_custom_{datetime.now().timestamp()}"
            mock_response.type = "message"
            mock_response.role = "assistant"
            mock_response.model = "claude-3-5-sonnet-20241022"
            mock_response.stop_reason = "end_turn"

            mock_content_block = Mock()
            mock_content_block.type = "text"
            mock_content_block.text = text
            mock_response.content = [mock_content_block]

            mock_usage = Mock()
            mock_usage.input_tokens = tokens_in
            mock_usage.output_tokens = tokens_out
            mock_response.usage = mock_usage

            return mock_response

        mock_instance.create_response = create_response
        mock_instance.messages.create.side_effect = lambda **kwargs: create_response(
            "Mocked response"
        )
        mock_client.return_value = mock_instance
        yield mock_instance


# ============================================================================
# OpenAI Mocks
# ============================================================================

@pytest.fixture
def mock_openai_complete():
    """
    Mock OpenAI API with comprehensive completion responses.

    Simulates GPT-4, GPT-3.5-turbo responses with:
    - Standard chat completion
    - Token usage
    - Model and finish reason
    """
    with patch("openai.OpenAI") as mock_client:
        mock_instance = Mock()

        # Create realistic completion response
        mock_choice = Mock()
        mock_choice.index = 0
        mock_choice.message = Mock(
            role="assistant",
            content="Mocked OpenAI response"
        )
        mock_choice.finish_reason = "stop"

        mock_completion = Mock()
        mock_completion.id = "chatcmpl-test123"
        mock_completion.object = "chat.completion"
        mock_completion.created = int(datetime.now().timestamp())
        mock_completion.model = "gpt-4"
        mock_completion.choices = [mock_choice]

        # Token usage
        mock_completion.usage = Mock(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30
        )

        mock_instance.chat.completions.create.return_value = mock_completion
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_openai_streaming():
    """
    Mock OpenAI API with streaming responses.

    Simulates Server-Sent Events (SSE) streaming.
    """
    with patch("openai.OpenAI") as mock_client:
        mock_instance = Mock()

        def mock_stream_generator():
            """Generator simulating streaming chunks"""
            chunks = [
                Mock(
                    id="chatcmpl-stream",
                    object="chat.completion.chunk",
                    created=int(datetime.now().timestamp()),
                    model="gpt-4",
                    choices=[Mock(
                        index=0,
                        delta=Mock(content="Mocked "),
                        finish_reason=None
                    )]
                ),
                Mock(
                    id="chatcmpl-stream",
                    object="chat.completion.chunk",
                    created=int(datetime.now().timestamp()),
                    model="gpt-4",
                    choices=[Mock(
                        index=0,
                        delta=Mock(content="streaming "),
                        finish_reason=None
                    )]
                ),
                Mock(
                    id="chatcmpl-stream",
                    object="chat.completion.chunk",
                    created=int(datetime.now().timestamp()),
                    model="gpt-4",
                    choices=[Mock(
                        index=0,
                        delta=Mock(content="response"),
                        finish_reason=None
                    )]
                ),
                Mock(
                    id="chatcmpl-stream",
                    object="chat.completion.chunk",
                    created=int(datetime.now().timestamp()),
                    model="gpt-4",
                    choices=[Mock(
                        index=0,
                        delta=Mock(content=None),
                        finish_reason="stop"
                    )]
                )
            ]
            return iter(chunks)

        mock_instance.chat.completions.create.return_value = mock_stream_generator()
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_openai_errors():
    """
    Mock OpenAI API error scenarios.
    """
    class MockOpenAIError:
        def __init__(self):
            self.mock_client_patch = patch("openai.OpenAI")

        def __enter__(self):
            self.mock_client = self.mock_client_patch.__enter__()
            self.mock_instance = Mock()
            self.mock_client.return_value = self.mock_instance
            return self

        def __exit__(self, *args):
            return self.mock_client_patch.__exit__(*args)

        def rate_limit_error(self):
            """Simulate rate limit error"""
            from openai import RateLimitError
            self.mock_instance.chat.completions.create.side_effect = RateLimitError(
                "Rate limit exceeded",
                response=Mock(status_code=429),
                body={"error": {"message": "Rate limit exceeded"}}
            )
            return self.mock_instance

        def api_error(self):
            """Simulate API error"""
            from openai import APIError
            self.mock_instance.chat.completions.create.side_effect = APIError(
                "API Error",
                request=Mock(),
                body={"error": {"message": "Internal server error"}}
            )
            return self.mock_instance

        def auth_error(self):
            """Simulate authentication error"""
            from openai import AuthenticationError
            self.mock_instance.chat.completions.create.side_effect = AuthenticationError(
                "Invalid API key",
                response=Mock(status_code=401),
                body={"error": {"message": "Invalid API key"}}
            )
            return self.mock_instance

    yield MockOpenAIError


# ============================================================================
# Google Gemini Mocks
# ============================================================================

@pytest.fixture
def mock_gemini_complete():
    """
    Mock Google Gemini API with completion responses.

    Simulates Gemini Pro, Gemini Ultra responses.
    """
    with patch("google.generativeai.GenerativeModel") as mock_model_class:
        mock_instance = Mock()

        # Create realistic response
        mock_candidate = Mock()
        mock_part = Mock()
        mock_part.text = "Mocked Gemini response"
        mock_candidate.content = Mock(parts=[mock_part])
        mock_candidate.finish_reason = "STOP"
        mock_candidate.safety_ratings = []

        mock_response = Mock()
        mock_response.text = "Mocked Gemini response"
        mock_response.candidates = [mock_candidate]

        # Token usage
        mock_response.usage_metadata = Mock(
            prompt_token_count=10,
            candidates_token_count=20,
            total_token_count=30
        )

        mock_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_gemini_streaming():
    """
    Mock Google Gemini API with streaming responses.
    """
    with patch("google.generativeai.GenerativeModel") as mock_model_class:
        mock_instance = Mock()

        def mock_stream_generator():
            """Generator simulating streaming chunks"""
            chunks = [
                Mock(
                    text="Mocked ",
                    candidates=[Mock(
                        content=Mock(parts=[Mock(text="Mocked ")]),
                        finish_reason=None
                    )]
                ),
                Mock(
                    text="streaming ",
                    candidates=[Mock(
                        content=Mock(parts=[Mock(text="streaming ")]),
                        finish_reason=None
                    )]
                ),
                Mock(
                    text="response",
                    candidates=[Mock(
                        content=Mock(parts=[Mock(text="response")]),
                        finish_reason="STOP"
                    )]
                )
            ]
            return iter(chunks)

        mock_instance.generate_content.return_value = mock_stream_generator()
        mock_model_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_gemini_errors():
    """
    Mock Google Gemini API error scenarios.
    """
    class MockGeminiError:
        def __init__(self):
            self.mock_model_patch = patch("google.generativeai.GenerativeModel")

        def __enter__(self):
            self.mock_model = self.mock_model_patch.__enter__()
            self.mock_instance = Mock()
            self.mock_model.return_value = self.mock_instance
            return self

        def __exit__(self, *args):
            return self.mock_model_patch.__exit__(*args)

        def rate_limit_error(self):
            """Simulate rate limit error"""
            self.mock_instance.generate_content.side_effect = Exception(
                "429 Quota exceeded"
            )
            return self.mock_instance

        def api_error(self):
            """Simulate API error"""
            self.mock_instance.generate_content.side_effect = Exception(
                "500 Internal server error"
            )
            return self.mock_instance

        def safety_error(self):
            """Simulate content safety blocking"""
            mock_response = Mock()
            mock_response.text = None
            mock_candidate = Mock()
            mock_candidate.finish_reason = "SAFETY"
            mock_candidate.safety_ratings = [
                Mock(category="HARM_CATEGORY_DANGEROUS", probability="HIGH")
            ]
            mock_response.candidates = [mock_candidate]

            self.mock_instance.generate_content.return_value = mock_response
            return self.mock_instance

    yield MockGeminiError


# ============================================================================
# Universal AI Mock (Multi-Provider)
# ============================================================================

@pytest.fixture
def mock_ai_service():
    """
    Universal AI service mock supporting multiple providers.

    Allows tests to switch between providers dynamically.
    """
    class UniversalAIMock:
        def __init__(self):
            self.provider = "anthropic"  # default
            self.response_text = "Mocked AI response"

        def set_provider(self, provider: str):
            """Set AI provider (anthropic, openai, gemini)"""
            self.provider = provider
            return self

        def set_response(self, text: str):
            """Set custom response text"""
            self.response_text = text
            return self

        def get_mock(self):
            """Get appropriate mock for selected provider"""
            if self.provider == "anthropic":
                return self._mock_anthropic()
            elif self.provider == "openai":
                return self._mock_openai()
            elif self.provider == "gemini":
                return self._mock_gemini()
            else:
                raise ValueError(f"Unknown provider: {self.provider}")

        def _mock_anthropic(self):
            """Internal Anthropic mock"""
            with patch("anthropic.Anthropic") as mock_client:
                mock_instance = Mock()
                mock_response = Mock()
                mock_response.content = [Mock(text=self.response_text)]
                mock_instance.messages.create.return_value = mock_response
                mock_client.return_value = mock_instance
                return mock_instance

        def _mock_openai(self):
            """Internal OpenAI mock"""
            with patch("openai.OpenAI") as mock_client:
                mock_instance = Mock()
                mock_completion = Mock()
                mock_completion.choices = [
                    Mock(message=Mock(content=self.response_text))
                ]
                mock_instance.chat.completions.create.return_value = mock_completion
                mock_client.return_value = mock_instance
                return mock_instance

        def _mock_gemini(self):
            """Internal Gemini mock"""
            with patch("google.generativeai.GenerativeModel") as mock_model:
                mock_instance = Mock()
                mock_response = Mock(text=self.response_text)
                mock_instance.generate_content.return_value = mock_response
                mock_model.return_value = mock_instance
                return mock_instance

    yield UniversalAIMock()


# ============================================================================
# Helper Functions
# ============================================================================

def create_mock_ai_response(
    provider: str,
    text: str,
    input_tokens: int = 10,
    output_tokens: int = 20
) -> Mock:
    """
    Helper function to create mock AI response for any provider.

    Args:
        provider: AI provider name (anthropic, openai, gemini)
        text: Response text
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Mock response object
    """
    if provider == "anthropic":
        mock_response = Mock()
        mock_response.content = [Mock(text=text)]
        mock_response.usage = Mock(input_tokens=input_tokens, output_tokens=output_tokens)
        return mock_response

    elif provider == "openai":
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=text))]
        mock_response.usage = Mock(
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens
        )
        return mock_response

    elif provider == "gemini":
        mock_response = Mock()
        mock_response.text = text
        mock_response.usage_metadata = Mock(
            prompt_token_count=input_tokens,
            candidates_token_count=output_tokens,
            total_token_count=input_tokens + output_tokens
        )
        return mock_response

    else:
        raise ValueError(f"Unknown provider: {provider}")
