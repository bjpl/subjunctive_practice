# Claude AI Service Usage Guide

## Overview

The Claude AI Service provides intelligent, personalized feedback and learning support for the Spanish Subjunctive Practice application using Anthropic's Claude API.

## Configuration

### Environment Variables

Set the following in your `.env` file:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# Optional (with defaults)
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=1000
ANTHROPIC_TEMPERATURE=0.7
```

### Initialization

The service is automatically initialized as a singleton:

```python
from services.ai_service import get_ai_service

ai_service = get_ai_service()

# Check if service is enabled
if ai_service.is_enabled:
    print("AI features available")
else:
    print("AI features disabled (missing API key)")
```

## Core Features

### 1. Generate Personalized Feedback

Provide context-aware feedback for user answers:

```python
# Prepare exercise context
exercise_context = {
    "verb": "hablar",
    "tense": "present_subjunctive",
    "person": "yo",
    "trigger": "Es importante que",
    "sentence": "Es importante que yo ___ español"
}

# Generate feedback
feedback = await ai_service.generate_feedback(
    user_answer="hable",
    correct_answer="hable",
    exercise_context=exercise_context
)

# Example output:
# "¡Excelente! You correctly used 'hable' with the present subjunctive after
#  'Es importante que'. This trigger phrase always requires the subjunctive
#  because it expresses importance. Keep up the great work!"
```

**Incorrect Answer Example:**

```python
feedback = await ai_service.generate_feedback(
    user_answer="hablo",  # Wrong - indicative instead of subjunctive
    correct_answer="hable",
    exercise_context=exercise_context
)

# Example output:
# "Not quite! The trigger phrase 'Es importante que' requires the subjunctive
#  mood, not the indicative. The correct form is 'hable', not 'hablo'.
#  Remember: phrases expressing necessity, importance, or emotion trigger
#  the subjunctive."
```

### 2. Generate Learning Insights

Analyze user performance to provide actionable insights:

```python
# Gather user statistics
user_stats = {
    "total_exercises": 150,
    "accuracy": 0.72,
    "total_study_time_minutes": 300,
    "total_sessions": 15,
    "verbs_mastered": 12,
    "verbs_learning": 8
}

# Identify weak areas
weak_areas = [
    {"area": "imperfect_subjunctive", "accuracy": 0.55},
    {"area": "irregular_verbs", "accuracy": 0.60},
    {"area": "stem_changing_verbs", "accuracy": 0.65}
]

# Generate insights
insights = await ai_service.generate_learning_insights(user_stats, weak_areas)

# Example output (list of strings):
# [
#     "Focus on the imperfect subjunctive - your 55% accuracy shows this needs attention before moving to advanced topics.",
#     "Practice irregular verbs like ser, estar, and ir more frequently; these are high-frequency verbs worth mastering.",
#     "Your 72% overall accuracy is good progress! Aim for 80% by dedicating 10 minutes daily to your weakest areas.",
#     "Stem-changing verbs (e→ie, o→ue) are close to mastery at 65% - a few focused sessions could push this over 80%.",
#     "Your consistent practice (15 sessions) is paying off! Try to maintain this rhythm for long-term retention."
# ]
```

### 3. Generate Personalized Hints

Provide context-sensitive hints without revealing answers:

```python
exercise = {
    "verb": "tener",
    "tense": "present_subjunctive",
    "person": "nosotros",
    "trigger": "Es posible que",
    "sentence": "Es posible que nosotros ___ tiempo mañana"
}

# Optional: include user's error history for personalization
user_history = [
    {"verb": "tener", "error_type": "stem_change_missed"},
    {"verb": "venir", "error_type": "stem_change_missed"},
    {"verb": "hacer", "error_type": "irregular_yo_form"}
]

hint = await ai_service.generate_personalized_hint(exercise, user_history)

# Example output:
# "The phrase 'Es posible que' expresses possibility, triggering the subjunctive.
#  For 'tener' in present subjunctive, remember it has a stem change. Think about
#  how 'tener' changes in the yo form of present indicative - the subjunctive
#  follows a similar pattern."
```

### 4. Batch Feedback Generation

Generate feedback for multiple exercises efficiently:

```python
feedback_requests = [
    {
        "user_answer": "hable",
        "correct_answer": "hable",
        "exercise_context": {"verb": "hablar", "tense": "present_subjunctive"}
    },
    {
        "user_answer": "comiera",
        "correct_answer": "coma",
        "exercise_context": {"verb": "comer", "tense": "present_subjunctive"}
    },
    {
        "user_answer": "viva",
        "correct_answer": "viva",
        "exercise_context": {"verb": "vivir", "tense": "present_subjunctive"}
    }
]

# Returns list of feedback in same order
feedback_list = await ai_service.batch_generate_feedback(feedback_requests)

# Process results
for feedback in feedback_list:
    print(feedback)
```

## Integration with FastAPI Routes

### Example: Feedback Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from services.ai_service import get_ai_service, ClaudeAIService, AIServiceUnavailableError
from schemas.exercise import AnswerSubmit, AnswerValidation

router = APIRouter()

@router.post("/exercises/submit", response_model=AnswerValidation)
async def submit_answer(
    submission: AnswerSubmit,
    ai_service: ClaudeAIService = Depends(get_ai_service)
):
    """Submit exercise answer with AI-powered feedback."""

    # Validate answer (your existing logic)
    is_correct = check_answer(submission.user_answer, exercise.correct_answer)

    # Generate AI feedback
    try:
        feedback = await ai_service.generate_feedback(
            user_answer=submission.user_answer,
            correct_answer=exercise.correct_answer,
            exercise_context={
                "verb": exercise.verb.infinitive,
                "tense": exercise.tense,
                "person": exercise.person,
                "trigger": exercise.trigger_phrase,
                "sentence": exercise.prompt
            }
        )
    except AIServiceUnavailableError:
        # Fallback to simple feedback
        feedback = "Correct!" if is_correct else f"The correct answer is {exercise.correct_answer}"

    return AnswerValidation(
        is_correct=is_correct,
        correct_answer=exercise.correct_answer,
        user_answer=submission.user_answer,
        feedback=feedback,
        score=100 if is_correct else 0
    )
```

### Example: Progress Insights Endpoint

```python
@router.get("/progress/insights")
async def get_learning_insights(
    user_id: int,
    ai_service: ClaudeAIService = Depends(get_ai_service),
    db: Session = Depends(get_db)
):
    """Get AI-generated learning insights for user."""

    # Fetch user statistics
    stats = get_user_statistics(db, user_id)
    weak_areas = identify_weak_areas(db, user_id)

    if not ai_service.is_enabled:
        return {"insights": ["AI insights not available"], "ai_enabled": False}

    try:
        insights = await ai_service.generate_learning_insights(
            user_stats={
                "total_exercises": stats.total_exercises_completed,
                "accuracy": stats.overall_accuracy,
                "total_study_time_minutes": stats.total_study_time_minutes,
                "total_sessions": stats.total_sessions
            },
            weak_areas=[
                {"area": area.name, "accuracy": area.accuracy}
                for area in weak_areas
            ]
        )

        return {
            "insights": insights,
            "ai_enabled": True,
            "generated_at": datetime.utcnow()
        }

    except Exception as e:
        logger.error(f"Failed to generate insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")
```

## Error Handling

### Automatic Retry with Exponential Backoff

The service automatically retries on rate limit errors:

```python
# This is handled automatically by the @retry_on_rate_limit decorator
feedback = await ai_service.generate_feedback(...)
# Will retry up to 3 times with exponential backoff (1s, 2s, 4s)
```

### Graceful Degradation

Always provide fallbacks when AI service is unavailable:

```python
try:
    feedback = await ai_service.generate_feedback(
        user_answer, correct_answer, context
    )
except AIServiceUnavailableError:
    # Fallback to rule-based feedback
    feedback = generate_rule_based_feedback(user_answer, correct_answer)
except RateLimitExceededError:
    # Rate limit exceeded - use cached or simple feedback
    feedback = "Please try again in a moment."
```

## Caching

### Automatic Response Caching

Responses are automatically cached for 1 hour:

```python
# First call - hits API
feedback1 = await ai_service.generate_feedback("hable", "hable", context)

# Second identical call - uses cache (no API call)
feedback2 = await ai_service.generate_feedback("hable", "hable", context)

# feedback1 == feedback2, but only one API call made
```

### Manual Cache Management

```python
# Check cache size
cache_size = len(ai_service._cache)

# Clear cache manually
cleared_count = ai_service.clear_cache()
print(f"Cleared {cleared_count} cached entries")
```

## Health Monitoring

### Health Check

```python
health_status = await ai_service.health_check()

# Example responses:

# When healthy:
# {
#     "status": "healthy",
#     "configured": True,
#     "model": "claude-3-5-sonnet-20241022",
#     "cache_size": 15,
#     "test_response": "OK"
# }

# When disabled:
# {
#     "status": "disabled",
#     "configured": False,
#     "message": "AI service not configured (missing API key)"
# }

# When unhealthy:
# {
#     "status": "unhealthy",
#     "configured": True,
#     "error": "API connection failed",
#     "model": "claude-3-5-sonnet-20241022"
# }
```

### Health Check Endpoint

```python
@router.get("/health/ai")
async def ai_service_health(
    ai_service: ClaudeAIService = Depends(get_ai_service)
):
    """Check AI service health."""
    return await ai_service.health_check()
```

## Best Practices

### 1. Always Handle Service Availability

```python
if ai_service.is_enabled:
    # Use AI features
    feedback = await ai_service.generate_feedback(...)
else:
    # Use fallback logic
    feedback = simple_feedback(...)
```

### 2. Use Batch Operations for Multiple Requests

```python
# ✅ Good - single batch call
results = await ai_service.batch_generate_feedback(requests)

# ❌ Bad - sequential calls
results = [await ai_service.generate_feedback(**req) for req in requests]
```

### 3. Provide Rich Context

```python
# ✅ Good - detailed context
context = {
    "verb": "hablar",
    "tense": "present_subjunctive",
    "person": "yo",
    "trigger": "Es importante que",
    "sentence": "Es importante que yo hable",
    "difficulty": "beginner",
    "theme": "daily_routines"
}

# ❌ Bad - minimal context
context = {"verb": "hablar"}
```

### 4. Monitor and Log

```python
import structlog

logger = structlog.get_logger(__name__)

try:
    feedback = await ai_service.generate_feedback(...)
    logger.info("ai_feedback_generated", user_id=user.id, exercise_id=exercise.id)
except Exception as e:
    logger.error("ai_feedback_failed", error=str(e), user_id=user.id)
    raise
```

### 5. Use Appropriate Token Limits

```python
# Short feedback - low tokens
feedback = await ai_service.generate_feedback(...)  # Uses default: 200 tokens

# Detailed insights - more tokens
insights = await ai_service.generate_learning_insights(...)  # Uses 500 tokens

# Concise hints - minimal tokens
hint = await ai_service.generate_personalized_hint(...)  # Uses 150 tokens
```

## Performance Considerations

### API Call Costs

- Feedback generation: ~150-200 tokens per call
- Learning insights: ~400-500 tokens per call
- Hints: ~100-150 tokens per call

### Optimization Strategies

1. **Cache aggressively** - Identical requests use cached responses
2. **Batch when possible** - Use `batch_generate_feedback()` for multiple requests
3. **Fallback gracefully** - Always have rule-based alternatives
4. **Monitor usage** - Track API calls and costs via health checks
5. **Rate limit users** - Prevent abuse with request throttling

## Application Shutdown

Register the cleanup function in your FastAPI app:

```python
from fastapi import FastAPI
from services.ai_service import shutdown_ai_service

app = FastAPI()

@app.on_event("shutdown")
async def shutdown():
    await shutdown_ai_service()
```

## Testing

The service includes comprehensive mocking support:

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_my_feature():
    with patch('services.ai_service.settings') as mock_settings:
        mock_settings.ANTHROPIC_API_KEY = "test-key"

        service = ClaudeAIService()
        service._client.messages.create = AsyncMock(
            return_value=mock_message_response("Test feedback")
        )

        feedback = await service.generate_feedback(...)
        assert "Test feedback" in feedback
```

## Troubleshooting

### Issue: "AI service not configured"

**Solution:** Set `ANTHROPIC_API_KEY` in your `.env` file

### Issue: Rate limit errors

**Solution:** Service auto-retries, but if persistent:
- Reduce request frequency
- Increase cache TTL
- Use batch operations

### Issue: Slow response times

**Solution:**
- Check network latency to Anthropic API
- Use caching more aggressively
- Consider reducing `max_tokens` setting
- Use batch operations for multiple requests

### Issue: Generic/unhelpful feedback

**Solution:**
- Provide more detailed exercise context
- Adjust `ANTHROPIC_TEMPERATURE` (0.6-0.8 range)
- Review and refine system prompts in service code

## Support

For issues or questions:
- Check logs with `structlog` for detailed error information
- Use health check endpoint to verify service status
- Review Anthropic API documentation: https://docs.anthropic.com/
- Contact development team with log details
