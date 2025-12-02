# AI Service Mock Usage Guide

## Overview

This document provides comprehensive guidelines for using AI service mocks in tests. All AI mocks are located in `tests/fixtures/ai_mocks.py`.

## Available Mocks

### Anthropic Claude Mocks

#### 1. `mock_anthropic_complete`
Standard completion responses with realistic structure.

```python
def test_claude_completion(mock_anthropic_complete):
    """Test Claude completion API"""
    response = mock_anthropic_complete.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.content[0].text == "Mocked Claude response"
    assert response.usage.input_tokens == 10
    assert response.usage.output_tokens == 20
```

#### 2. `mock_anthropic_streaming`
Streaming responses with event-based updates.

```python
@pytest.mark.asyncio
async def test_claude_streaming(mock_anthropic_streaming):
    """Test Claude streaming API"""
    stream = mock_anthropic_streaming.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello"}]
    )

    async with stream as response:
        async for event in response:
            if event.type == "content_block_delta":
                print(event.delta.text)
```

#### 3. `mock_anthropic_errors`
Error scenarios for testing error handling.

```python
def test_claude_rate_limit(mock_anthropic_errors):
    """Test rate limit handling"""
    with mock_anthropic_errors() as mock:
        mock.rate_limit_error()

        with pytest.raises(Exception, match="Rate limit exceeded"):
            mock.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": "Hello"}]
            )
```

#### 4. `mock_anthropic_custom_response`
Customizable responses for specific test scenarios.

```python
def test_claude_custom(mock_anthropic_custom_response):
    """Test with custom response"""
    custom_text = "This is a custom response for testing"
    mock_anthropic_custom_response.messages.create.side_effect = \
        lambda **kwargs: mock_anthropic_custom_response.create_response(custom_text)

    response = mock_anthropic_custom_response.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.content[0].text == custom_text
```

### OpenAI Mocks

#### 1. `mock_openai_complete`
Standard GPT-4/GPT-3.5-turbo completion responses.

```python
def test_openai_completion(mock_openai_complete):
    """Test OpenAI completion API"""
    response = mock_openai_complete.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.choices[0].message.content == "Mocked OpenAI response"
    assert response.usage.total_tokens == 30
```

#### 2. `mock_openai_streaming`
Server-Sent Events (SSE) streaming responses.

```python
def test_openai_streaming(mock_openai_streaming):
    """Test OpenAI streaming API"""
    stream = mock_openai_streaming.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content

    assert "streaming" in full_response
```

#### 3. `mock_openai_errors`
Error scenarios including rate limits, API errors, and auth failures.

```python
def test_openai_auth_error(mock_openai_errors):
    """Test authentication error handling"""
    with mock_openai_errors() as mock:
        mock.auth_error()

        with pytest.raises(Exception, match="Invalid API key"):
            mock.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hello"}]
            )
```

### Google Gemini Mocks

#### 1. `mock_gemini_complete`
Gemini Pro/Ultra completion responses.

```python
def test_gemini_completion(mock_gemini_complete):
    """Test Gemini completion API"""
    response = mock_gemini_complete.generate_content("Hello")

    assert response.text == "Mocked Gemini response"
    assert response.usage_metadata.total_token_count == 30
```

#### 2. `mock_gemini_streaming`
Streaming responses with chunks.

```python
def test_gemini_streaming(mock_gemini_streaming):
    """Test Gemini streaming API"""
    stream = mock_gemini_streaming.generate_content("Hello", stream=True)

    full_text = ""
    for chunk in stream:
        full_text += chunk.text

    assert "streaming" in full_text
```

#### 3. `mock_gemini_errors`
Error scenarios including safety blocking.

```python
def test_gemini_safety_block(mock_gemini_errors):
    """Test content safety blocking"""
    with mock_gemini_errors() as mock:
        mock.safety_error()

        response = mock.generate_content("Potentially harmful content")

        assert response.candidates[0].finish_reason == "SAFETY"
```

### Universal AI Mock

#### `mock_ai_service`
Multi-provider mock supporting dynamic provider switching.

```python
def test_universal_mock_anthropic(mock_ai_service):
    """Test universal mock with Anthropic"""
    mock = mock_ai_service.set_provider("anthropic").set_response("Custom response")
    ai_mock = mock.get_mock()

    response = ai_mock.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.content[0].text == "Custom response"


def test_universal_mock_openai(mock_ai_service):
    """Test universal mock with OpenAI"""
    mock = mock_ai_service.set_provider("openai").set_response("OpenAI response")
    ai_mock = mock.get_mock()

    response = ai_mock.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.choices[0].message.content == "OpenAI response"
```

## Helper Functions

### `create_mock_ai_response()`
Create custom mock responses for any provider.

```python
from tests.fixtures.ai_mocks import create_mock_ai_response

def test_custom_response():
    """Test with custom helper"""
    # Anthropic response
    anthropic_resp = create_mock_ai_response(
        provider="anthropic",
        text="Test response",
        input_tokens=15,
        output_tokens=25
    )
    assert anthropic_resp.content[0].text == "Test response"

    # OpenAI response
    openai_resp = create_mock_ai_response(
        provider="openai",
        text="Test response",
        input_tokens=15,
        output_tokens=25
    )
    assert openai_resp.choices[0].message.content == "Test response"
```

## Best Practices

### 1. Choose the Right Mock

- **Standard tests**: Use `mock_*_complete` fixtures
- **Streaming tests**: Use `mock_*_streaming` fixtures
- **Error handling**: Use `mock_*_errors` fixtures
- **Custom scenarios**: Use `mock_*_custom_response` or helper functions
- **Multi-provider**: Use `mock_ai_service`

### 2. Test Error Scenarios

Always test error handling:

```python
@pytest.mark.parametrize("error_type", ["rate_limit", "api_error", "auth_error"])
def test_error_handling(mock_anthropic_errors, error_type):
    """Test all error scenarios"""
    with mock_anthropic_errors() as mock:
        if error_type == "rate_limit":
            mock.rate_limit_error()
        elif error_type == "api_error":
            mock.api_error()
        elif error_type == "auth_error":
            mock.auth_error()

        with pytest.raises(Exception):
            mock.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": "Hello"}]
            )
```

### 3. Verify Token Usage

Always verify token usage in tests:

```python
def test_token_tracking(mock_anthropic_complete):
    """Verify token usage tracking"""
    response = mock_anthropic_complete.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}]
    )

    assert response.usage.input_tokens > 0
    assert response.usage.output_tokens > 0
```

### 4. Test Streaming Properly

Use async/await for streaming tests:

```python
@pytest.mark.asyncio
async def test_streaming_complete(mock_anthropic_streaming):
    """Test complete streaming flow"""
    stream = mock_anthropic_streaming.messages.stream(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}]
    )

    events = []
    async with stream as response:
        async for event in response:
            events.append(event.type)

    assert "message_start" in events
    assert "content_block_delta" in events
    assert "message_stop" in events
```

### 5. Isolate External Dependencies

Always patch at the module level:

```python
@pytest.fixture
def my_service_with_mock(mock_anthropic_complete):
    """Service with mocked AI"""
    # The mock is already patched globally
    from services.my_ai_service import MyAIService
    return MyAIService()
```

## Common Patterns

### Pattern 1: Test AI-Powered Feature

```python
def test_ai_feedback_generation(mock_anthropic_complete):
    """Test AI-powered feedback"""
    from services.feedback import FeedbackGenerator

    generator = FeedbackGenerator()
    feedback = generator.generate_with_ai(
        user_answer="hablo",
        correct_answer="hable"
    )

    assert feedback is not None
    assert len(feedback) > 0
```

### Pattern 2: Test Retry Logic

```python
def test_retry_on_rate_limit(mock_anthropic_errors):
    """Test retry logic on rate limit"""
    with mock_anthropic_errors() as mock:
        attempt_count = 0

        def side_effect(*args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise Exception("Rate limit exceeded")
            return create_mock_ai_response("anthropic", "Success")

        mock.messages.create.side_effect = side_effect

        # Your retry logic here
        result = retry_with_backoff(mock.messages.create)
        assert attempt_count == 3
```

### Pattern 3: Test Multiple Providers

```python
@pytest.mark.parametrize("provider,fixture", [
    ("anthropic", "mock_anthropic_complete"),
    ("openai", "mock_openai_complete"),
    ("gemini", "mock_gemini_complete")
])
def test_all_providers(provider, fixture, request):
    """Test feature with all providers"""
    mock = request.getfixturevalue(fixture)

    # Test implementation
    assert mock is not None
```

## Integration with Existing Tests

To add AI mocking to existing tests:

```python
# Before
def test_my_feature():
    result = my_function()
    assert result

# After
def test_my_feature(mock_anthropic_complete):
    # AI calls are now mocked automatically
    result = my_function()
    assert result
```

## Troubleshooting

### Issue: Mock not being used

**Solution**: Ensure the import path is correct in the patch decorator:

```python
# Wrong
@patch("anthropic.Anthropic")

# Correct
with patch("your_module.anthropic.Anthropic"):
    pass
```

### Issue: Async tests failing

**Solution**: Use `@pytest.mark.asyncio` and async fixtures:

```python
@pytest.mark.asyncio
async def test_async_feature(mock_anthropic_streaming):
    result = await async_function()
    assert result
```

### Issue: Mock not resetting between tests

**Solution**: Use function-scoped fixtures (default) or explicitly reset:

```python
@pytest.fixture
def my_mock(mock_anthropic_complete):
    yield mock_anthropic_complete
    # Cleanup/reset if needed
    mock_anthropic_complete.reset_mock()
```

## Examples by Use Case

### Use Case: Testing Exercise Generation with AI

```python
def test_ai_exercise_generation(mock_anthropic_complete):
    """Test AI-powered exercise generation"""
    from services.exercise_generator import ExerciseGenerator

    generator = ExerciseGenerator()
    exercise = generator.generate_with_ai_assistance(
        verb="hablar",
        difficulty="intermediate"
    )

    assert exercise.verb == "hablar"
    assert exercise.difficulty == "intermediate"
```

### Use Case: Testing Feedback with Streaming

```python
@pytest.mark.asyncio
async def test_streaming_feedback(mock_anthropic_streaming):
    """Test streaming feedback generation"""
    from services.feedback import StreamingFeedback

    feedback = StreamingFeedback()
    chunks = []

    async for chunk in feedback.generate_streaming(
        user_answer="hablo",
        correct_answer="hable"
    ):
        chunks.append(chunk)

    assert len(chunks) > 0
```

### Use Case: Testing Error Recovery

```python
def test_error_recovery(mock_anthropic_errors):
    """Test graceful error handling"""
    with mock_anthropic_errors() as mock:
        mock.api_error()

        from services.ai_service import AIService
        service = AIService()

        # Should handle error gracefully
        result = service.generate_with_fallback("test")

        # Should fall back to non-AI method
        assert result is not None
```

## Summary

- Use provider-specific mocks for focused tests
- Use universal mock for multi-provider scenarios
- Always test error conditions
- Verify token usage and metadata
- Test streaming with async/await
- Isolate external dependencies with proper patching

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Google Gemini Documentation](https://ai.google.dev/docs)
