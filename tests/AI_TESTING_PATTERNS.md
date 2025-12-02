# AI Testing Patterns for Anthropic Claude Integration

## Overview

This document provides comprehensive guidelines for testing AI-powered features in the Spanish Subjunctive Practice application. The application uses **Anthropic's Claude API** (not OpenAI) for AI-powered functionality.

## Table of Contents

1. [AI Service Configuration](#ai-service-configuration)
2. [Mock Fixtures](#mock-fixtures)
3. [Testing Patterns](#testing-patterns)
4. [Best Practices](#best-practices)
5. [Common Pitfalls](#common-pitfalls)
6. [Example Test Cases](#example-test-cases)

## AI Service Configuration

### Environment Variables

The application uses the following Anthropic-specific configuration (see `core/config.py`):

```python
# Anthropic Claude
ANTHROPIC_API_KEY: Optional[str]           # API key for authentication
ANTHROPIC_MODEL: str                       # Default: "claude-3-5-sonnet-20241022"
ANTHROPIC_MAX_TOKENS: int                  # Default: 1000
ANTHROPIC_TEMPERATURE: float               # Default: 0.7
```

### Configuration in Tests

Override AI configuration in tests using the `test_settings` fixture:

```python
@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings with overrides."""
    return Settings(
        DATABASE_URL="sqlite:///:memory:",
        ANTHROPIC_API_KEY="test-api-key",  # Mock API key
        ANTHROPIC_MODEL="claude-3-5-sonnet-20241022",
        # ... other settings
    )
```

## Mock Fixtures

### mock_anthropic Fixture

The `mock_anthropic` fixture in `conftest.py` provides a complete mock of the Anthropic Claude API client.

#### Fixture Implementation

```python
@pytest.fixture
def mock_anthropic():
    """Mock Anthropic Claude API calls."""
    with patch("anthropic.Anthropic") as mock_client:
        # Mock the messages.create method
        mock_instance = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text="Mocked Claude response")]
        mock_instance.messages.create.return_value = mock_response
        mock_client.return_value = mock_instance
        yield mock_instance
```

#### What Gets Mocked

- **API Client Initialization**: `anthropic.Anthropic()`
- **Message Creation**: `client.messages.create()`
- **Response Structure**: Returns mock response with `.content[0].text`

#### Default Mock Behavior

- All API calls return: `"Mocked Claude response"`
- No actual network requests are made
- No API key validation occurs
- No rate limiting applies

### Customizing Mock Responses

You can customize the mock response for specific test scenarios:

```python
def test_custom_ai_response(mock_anthropic):
    """Test with custom Claude response."""
    # Customize the response
    custom_response = Mock()
    custom_response.content = [Mock(text="Custom AI generated feedback")]
    mock_anthropic.messages.create.return_value = custom_response

    # Your test code
    result = ai_powered_function()
    assert "feedback" in result.lower()
```

### Multiple Mock Responses

For tests that make multiple AI calls:

```python
def test_multiple_ai_calls(mock_anthropic):
    """Test function that calls Claude multiple times."""
    responses = [
        Mock(content=[Mock(text="First response")]),
        Mock(content=[Mock(text="Second response")]),
        Mock(content=[Mock(text="Third response")])
    ]
    mock_anthropic.messages.create.side_effect = responses

    # Test code that makes 3 AI calls
    results = function_with_multiple_calls()
    assert len(results) == 3
```

## Testing Patterns

### Pattern 1: Testing AI-Powered Features

When testing features that use Claude API:

```python
@pytest.mark.unit
def test_ai_feedback_generation(mock_anthropic, exercise_generator):
    """Test AI-generated exercise feedback."""
    # Setup custom response
    ai_feedback = "Great job! You correctly used the subjunctive mood."
    mock_response = Mock()
    mock_response.content = [Mock(text=ai_feedback)]
    mock_anthropic.messages.create.return_value = mock_response

    # Generate feedback using AI
    feedback = exercise_generator.get_ai_feedback("hable", "hablar")

    # Verify AI was called
    assert mock_anthropic.messages.create.called

    # Verify response processing
    assert ai_feedback in feedback
```

### Pattern 2: Verifying AI Call Parameters

Ensure correct parameters are passed to Claude:

```python
def test_ai_call_parameters(mock_anthropic):
    """Verify correct parameters sent to Claude API."""
    # Make AI call
    service.generate_explanation(verb="hablar", context="wishes")

    # Verify the call
    mock_anthropic.messages.create.assert_called_once()

    # Get the actual call arguments
    call_args = mock_anthropic.messages.create.call_args

    # Verify parameters
    assert call_args.kwargs['model'] == "claude-3-5-sonnet-20241022"
    assert call_args.kwargs['max_tokens'] >= 100
    assert 'messages' in call_args.kwargs
    assert len(call_args.kwargs['messages']) > 0
```

### Pattern 3: Testing AI Error Handling

Test how your code handles Claude API errors:

```python
def test_ai_api_error_handling(mock_anthropic):
    """Test handling of Claude API errors."""
    # Simulate API error
    mock_anthropic.messages.create.side_effect = Exception("API Error: Rate limit exceeded")

    # Call function that uses AI
    result = function_that_uses_claude()

    # Verify graceful degradation
    assert result is not None  # Should not crash
    assert "error" in result or result.uses_fallback
```

### Pattern 4: Testing Without AI

For features that can work without AI:

```python
def test_fallback_without_ai():
    """Test that feature works without AI."""
    # Don't use mock_anthropic fixture
    # This tests the non-AI code path

    result = exercise_generator.generate_exercise()

    # Verify it works with rule-based generation
    assert result is not None
    assert result.correct_answer is not None
```

### Pattern 5: Integration Testing with AI

For integration tests that need realistic AI responses:

```python
@pytest.mark.integration
def test_complete_exercise_flow_with_ai(mock_anthropic, authenticated_client):
    """Integration test with mocked AI responses."""
    # Setup realistic AI responses
    hint_response = Mock(content=[Mock(text="Remember: 'querer que' triggers subjunctive")])
    explanation_response = Mock(content=[Mock(text="The subjunctive expresses wishes and desires")])

    mock_anthropic.messages.create.side_effect = [hint_response, explanation_response]

    # Test complete flow
    response = authenticated_client.post("/api/exercises/generate", json={
        "difficulty": "intermediate",
        "use_ai_hints": True
    })

    assert response.status_code == 200
    assert "hint" in response.json()
```

## Best Practices

### 1. Always Mock in Unit Tests

**DO**: Use `mock_anthropic` fixture in unit tests

```python
def test_feature(mock_anthropic):  # Correct
    result = ai_feature()
    assert result is not None
```

**DON'T**: Make real API calls in unit tests

```python
def test_feature():  # Wrong - no mock!
    result = ai_feature()  # This will fail without API key
```

### 2. Test Both AI and Non-AI Paths

Many features should work without AI:

```python
def test_with_ai(mock_anthropic):
    """Test with AI enhancement."""
    result = generate_feedback(use_ai=True)
    assert result.enhanced is True

def test_without_ai():
    """Test fallback without AI."""
    result = generate_feedback(use_ai=False)
    assert result.basic_feedback is not None
```

### 3. Verify API Call Count

Prevent unnecessary API calls:

```python
def test_ai_caching(mock_anthropic):
    """Test that AI responses are cached."""
    # Call twice with same input
    result1 = get_explanation("hablar")
    result2 = get_explanation("hablar")

    # Should only call API once (second is cached)
    assert mock_anthropic.messages.create.call_count == 1
    assert result1 == result2
```

### 4. Test Error Messages

Ensure error messages don't expose Anthropic-specific details:

```python
def test_user_facing_error_messages(mock_anthropic):
    """Test that errors are user-friendly."""
    mock_anthropic.messages.create.side_effect = Exception("Anthropic API error")

    result = service.get_ai_hint()

    # User should see generic message, not API details
    assert "Anthropic" not in result.error_message
    assert "temporarily unavailable" in result.error_message.lower()
```

### 5. Test Rate Limiting

If you implement rate limiting for AI calls:

```python
def test_ai_rate_limiting(mock_anthropic):
    """Test rate limiting on AI calls."""
    # Make many rapid calls
    for i in range(100):
        service.get_ai_suggestion()

    # Should be throttled (not 100 calls)
    assert mock_anthropic.messages.create.call_count < 100
```

## Common Pitfalls

### Pitfall 1: Forgetting to Mock

**Problem**: Test fails because it tries to make real API call

```python
# Wrong - no mock
def test_ai_feature():
    result = ai_function()  # Fails: no API key
```

**Solution**: Always use the fixture

```python
# Correct
def test_ai_feature(mock_anthropic):
    result = ai_function()
```

### Pitfall 2: Wrong Import Path

**Problem**: Mock doesn't intercept calls because path is wrong

```python
# If your code does: from anthropic import Anthropic
# Mock this way:
with patch("your_module.Anthropic"):  # Wrong path!

# Should be:
with patch("anthropic.Anthropic"):  # Correct!
```

### Pitfall 3: Not Resetting Mock Between Tests

**Problem**: State leaks between tests

```python
def test_first(mock_anthropic):
    mock_anthropic.messages.create.return_value = Mock(content=[Mock(text="First")])
    # test code

def test_second(mock_anthropic):
    # This still has the "First" response!
    # Need to reset or set new return value
```

**Solution**: Fixtures are reset automatically, but if reusing, reset explicitly:

```python
def test_second(mock_anthropic):
    mock_anthropic.reset_mock()  # Clear call history
    mock_anthropic.messages.create.return_value = Mock(content=[Mock(text="Second")])
```

### Pitfall 4: Testing Implementation Details

**Problem**: Tests break when switching AI providers

```python
# Bad - too coupled to Anthropic
def test_ai_feature(mock_anthropic):
    result = service.get_hint()
    assert "claude" in result.model_name  # Too specific!
```

**Solution**: Test behavior, not implementation

```python
# Good - tests functionality
def test_ai_feature(mock_anthropic):
    result = service.get_hint()
    assert result.hint is not None
    assert len(result.hint) > 0
```

### Pitfall 5: Not Testing AI Failure

**Problem**: App crashes when AI is unavailable

```python
# Only testing success path
def test_ai_success(mock_anthropic):
    result = get_feedback()
    assert result.enhanced is True
```

**Solution**: Always test failure scenarios

```python
def test_ai_failure_fallback(mock_anthropic):
    mock_anthropic.messages.create.side_effect = Exception("API down")
    result = get_feedback()
    assert result.basic_feedback is not None  # Falls back gracefully
```

## Example Test Cases

### Complete Example: Testing AI-Enhanced Feedback

```python
import pytest
from unittest.mock import Mock
from services.feedback import FeedbackGenerator

@pytest.mark.unit
@pytest.mark.feedback
class TestAIEnhancedFeedback:
    """Test suite for AI-enhanced feedback generation."""

    def test_generate_basic_feedback_without_ai(self, feedback_generator):
        """Test basic feedback generation without AI."""
        # No mock_anthropic fixture - tests non-AI path
        result = feedback_generator.generate_feedback(
            verb="hablar",
            user_answer="hable",
            correct_answer="hable",
            use_ai=False
        )

        assert result.is_correct is True
        assert result.message is not None
        assert result.ai_enhanced is False

    def test_generate_ai_enhanced_feedback(self, mock_anthropic, feedback_generator):
        """Test AI-enhanced feedback generation."""
        # Setup mock AI response
        ai_response = """
        Excellent! You correctly conjugated 'hablar' to 'hable'.
        This shows good understanding of regular -ar verb patterns in the subjunctive.
        """
        mock_anthropic.messages.create.return_value = Mock(
            content=[Mock(text=ai_response.strip())]
        )

        # Generate feedback with AI
        result = feedback_generator.generate_feedback(
            verb="hablar",
            user_answer="hable",
            correct_answer="hable",
            use_ai=True
        )

        # Verify AI was called
        assert mock_anthropic.messages.create.called

        # Verify enhanced feedback
        assert result.is_correct is True
        assert result.ai_enhanced is True
        assert "understanding" in result.message.lower()

    def test_ai_feedback_handles_errors(self, mock_anthropic, feedback_generator):
        """Test that AI errors don't break feedback generation."""
        # Simulate API error
        mock_anthropic.messages.create.side_effect = Exception("API timeout")

        # Should still return feedback (fallback to non-AI)
        result = feedback_generator.generate_feedback(
            verb="ser",
            user_answer="soy",
            correct_answer="sea",
            use_ai=True
        )

        # Verify graceful degradation
        assert result is not None
        assert result.is_correct is False
        assert result.correct_answer == "sea"
        # May or may not be AI enhanced, but should not crash

    def test_ai_call_parameters_correct(self, mock_anthropic, feedback_generator):
        """Verify correct parameters are sent to Claude."""
        feedback_generator.generate_feedback(
            verb="querer",
            user_answer="quiera",
            correct_answer="quiera",
            use_ai=True
        )

        # Verify the call
        assert mock_anthropic.messages.create.called
        call_kwargs = mock_anthropic.messages.create.call_args.kwargs

        # Check model
        assert 'model' in call_kwargs
        assert 'claude' in call_kwargs['model'].lower()

        # Check messages structure
        assert 'messages' in call_kwargs
        assert isinstance(call_kwargs['messages'], list)
        assert len(call_kwargs['messages']) > 0

        # Check message contains relevant context
        message_text = str(call_kwargs['messages'])
        assert 'querer' in message_text or 'quiera' in message_text
```

### Example: Testing AI Service Directly

```python
@pytest.mark.unit
class TestAnthropicService:
    """Test the Anthropic service wrapper."""

    def test_initialize_client(self, test_settings, mock_anthropic):
        """Test client initialization with settings."""
        from services.ai_service import AnthropicService

        service = AnthropicService(test_settings)

        # Verify settings are used
        assert service.api_key == test_settings.ANTHROPIC_API_KEY
        assert service.model == test_settings.ANTHROPIC_MODEL

    def test_generate_text(self, mock_anthropic):
        """Test basic text generation."""
        from services.ai_service import AnthropicService

        # Setup mock response
        mock_anthropic.messages.create.return_value = Mock(
            content=[Mock(text="Generated text")]
        )

        service = AnthropicService()
        result = service.generate_text("Test prompt")

        # Verify result
        assert result == "Generated text"

        # Verify call parameters
        call_kwargs = mock_anthropic.messages.create.call_args.kwargs
        assert call_kwargs['messages'][0]['content'] == "Test prompt"

    def test_retry_on_rate_limit(self, mock_anthropic):
        """Test retry logic on rate limit errors."""
        from services.ai_service import AnthropicService

        # First call fails, second succeeds
        mock_anthropic.messages.create.side_effect = [
            Exception("Rate limit exceeded"),
            Mock(content=[Mock(text="Success after retry")])
        ]

        service = AnthropicService()
        result = service.generate_text("Test", max_retries=2)

        # Should succeed after retry
        assert result == "Success after retry"
        assert mock_anthropic.messages.create.call_count == 2
```

## Summary

### Key Points to Remember

1. **Use Anthropic, not OpenAI**: This app uses Claude API
2. **Always mock in tests**: Use `mock_anthropic` fixture
3. **Test both paths**: AI-enhanced and fallback
4. **Handle errors gracefully**: Don't let AI failures break app
5. **Verify call parameters**: Ensure correct data sent to API
6. **Test rate limiting**: Prevent excessive API usage
7. **User-friendly errors**: Don't expose API details to users

### Quick Reference

| Scenario | Fixture Needed | Example |
|----------|----------------|---------|
| Unit test with AI | `mock_anthropic` | `def test_ai(mock_anthropic):` |
| Test without AI | None | `def test_basic():` |
| Custom AI response | `mock_anthropic` | `mock_anthropic.messages.create.return_value = Mock(...)` |
| Multiple AI calls | `mock_anthropic` | `mock_anthropic.messages.create.side_effect = [...]` |
| Test AI errors | `mock_anthropic` | `mock_anthropic.messages.create.side_effect = Exception(...)` |

### Testing Checklist

When writing tests for AI-powered features:

- [ ] Mock the Anthropic API using `mock_anthropic` fixture
- [ ] Test success path with valid AI responses
- [ ] Test error path with API failures
- [ ] Test fallback behavior when AI unavailable
- [ ] Verify correct parameters sent to API
- [ ] Check that API isn't called unnecessarily
- [ ] Ensure user-facing errors are friendly
- [ ] Test rate limiting if implemented
- [ ] Verify response parsing handles edge cases
- [ ] Test caching if implemented

## Additional Resources

- Anthropic Claude API Documentation: https://docs.anthropic.com/
- Python `unittest.mock` Documentation: https://docs.python.org/3/library/unittest.mock.html
- Pytest Fixtures Guide: https://docs.pytest.org/en/stable/fixture.html

---

**Last Updated**: October 2025
**Maintainer**: Test Infrastructure Team
