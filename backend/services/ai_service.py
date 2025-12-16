"""
Claude AI Service for Spanish Subjunctive Practice

This module provides AI-powered features using Anthropic's Claude API:
- Personalized feedback generation for learner answers
- Learning insights based on performance data
- Contextual hints tailored to user history

Production-ready features:
- Async/await support for non-blocking operations
- Comprehensive error handling with retry logic
- Rate limiting and API quota management
- Structured logging with context
- Type hints for maintainability
- Caching for cost optimization
"""

import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from functools import wraps
import structlog
from anthropic import AsyncAnthropic, APIError, RateLimitError, APITimeoutError
from anthropic.types import Message

from core.config import settings
from services.cache_service import get_cache_service, RedisCache


logger = structlog.get_logger(__name__)


class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass


class RateLimitExceededError(AIServiceError):
    """Raised when API rate limit is exceeded."""
    pass


class AIServiceUnavailableError(AIServiceError):
    """Raised when AI service is temporarily unavailable."""
    pass


def retry_on_rate_limit(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for retrying operations on rate limit errors with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (will be exponentially increased)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except RateLimitError as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(
                            "max_retries_exceeded",
                            function=func.__name__,
                            attempts=attempt + 1,
                            error=str(e)
                        )
                        raise RateLimitExceededError(
                            f"Rate limit exceeded after {max_retries} retries"
                        ) from e

                    # Exponential backoff
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        "rate_limit_retry",
                        function=func.__name__,
                        attempt=attempt + 1,
                        delay_seconds=delay,
                        error=str(e)
                    )
                    await asyncio.sleep(delay)
                except (APITimeoutError, APIError) as e:
                    logger.error(
                        "api_error",
                        function=func.__name__,
                        error_type=type(e).__name__,
                        error=str(e)
                    )
                    raise AIServiceUnavailableError(
                        f"AI service unavailable: {str(e)}"
                    ) from e

            # Should never reach here, but just in case
            raise last_exception

        return wrapper
    return decorator


class ClaudeAIService:
    """
    Service for interacting with Claude AI for educational purposes.

    This service provides AI-powered features for the Spanish Subjunctive
    Practice application, including personalized feedback, learning insights,
    and contextual hints.
    """

    def __init__(self, cache_service: Optional[RedisCache] = None):
        """Initialize the Claude AI service."""
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("anthropic_api_key_missing", message="AI features will be disabled")
            self._client = None
            self._enabled = False
        else:
            self._client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self._enabled = True
            logger.info(
                "ai_service_initialized",
                model=settings.ANTHROPIC_MODEL,
                max_tokens=settings.ANTHROPIC_MAX_TOKENS,
                temperature=settings.ANTHROPIC_TEMPERATURE
            )

        # Use Redis cache with in-memory fallback
        self._cache = cache_service or get_cache_service()
        logger.info(
            "cache_initialized",
            backend="redis" if self._cache.is_redis_available else "memory",
            ttl_seconds=self._cache.default_ttl
        )

    @property
    def is_enabled(self) -> bool:
        """Check if AI service is enabled and configured."""
        return self._enabled and self._client is not None

    def _get_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a cache key from function arguments."""
        import hashlib

        # Create a deterministic hash of arguments
        key_parts = [prefix]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_string = ":".join(key_parts)

        # Hash long keys to avoid Redis key length limits
        if len(key_string) > 200:
            key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
            return f"ai:{prefix}:{key_hash}"

        return f"ai:{key_string}"

    async def _get_cached(self, cache_key: str) -> Optional[str]:
        """Get cached response if still valid."""
        try:
            cached_value = await self._cache.get(cache_key)
            if cached_value:
                logger.debug("cache_hit", cache_key=cache_key[:50])
                return cached_value
            logger.debug("cache_miss", cache_key=cache_key[:50])
            return None
        except Exception as e:
            logger.warning("cache_get_error", error=str(e), cache_key=cache_key[:50])
            return None

    async def _set_cache(self, cache_key: str, content: str, ttl: Optional[int] = None) -> None:
        """Store response in cache."""
        try:
            await self._cache.set(cache_key, content, ttl=ttl)
            logger.debug("cache_set", cache_key=cache_key[:50])
        except Exception as e:
            logger.warning("cache_set_error", error=str(e), cache_key=cache_key[:50])

    async def _create_message(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Create a message using Claude API.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            max_tokens: Override default max tokens
            temperature: Override default temperature

        Returns:
            Claude's response text

        Raises:
            AIServiceUnavailableError: If service is unavailable
            RateLimitExceededError: If rate limit is exceeded
        """
        if not self.is_enabled:
            raise AIServiceUnavailableError("AI service is not configured")

        try:
            params = {
                "model": settings.ANTHROPIC_MODEL,
                "max_tokens": max_tokens or settings.ANTHROPIC_MAX_TOKENS,
                "temperature": temperature if temperature is not None else settings.ANTHROPIC_TEMPERATURE,
                "messages": [{"role": "user", "content": prompt}]
            }

            if system_prompt:
                params["system"] = system_prompt

            logger.debug(
                "api_request",
                model=params["model"],
                prompt_length=len(prompt),
                max_tokens=params["max_tokens"]
            )

            response: Message = await self._client.messages.create(**params)

            # Extract text content from response
            content = response.content[0].text if response.content else ""

            logger.info(
                "api_response_received",
                response_length=len(content),
                stop_reason=response.stop_reason,
                usage=response.usage.model_dump() if response.usage else None
            )

            return content

        except (APIError, RateLimitError, APITimeoutError):
            # Re-raise these to be handled by retry decorator
            raise
        except Exception as e:
            logger.error(
                "unexpected_error",
                error_type=type(e).__name__,
                error=str(e)
            )
            raise AIServiceUnavailableError(
                f"Unexpected error calling AI service: {str(e)}"
            ) from e

    @retry_on_rate_limit(max_retries=3, base_delay=1.0)
    async def generate_feedback(
        self,
        user_answer: str,
        correct_answer: str,
        exercise_context: Dict[str, Any]
    ) -> str:
        """
        Generate personalized feedback for a user's answer.

        Args:
            user_answer: The answer provided by the user
            correct_answer: The correct answer
            exercise_context: Context about the exercise (verb, tense, trigger, etc.)

        Returns:
            Personalized feedback message

        Example:
            >>> context = {
            ...     "verb": "hablar",
            ...     "tense": "present_subjunctive",
            ...     "person": "yo",
            ...     "trigger": "Es importante que",
            ...     "sentence": "Es importante que yo ___"
            ... }
            >>> feedback = await service.generate_feedback("hable", "hable", context)
        """
        if not self.is_enabled:
            # Fallback to simple feedback
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            if is_correct:
                return "Correct! Well done."
            return f"Not quite. The correct answer is '{correct_answer}'."

        # Check cache
        cache_key = self._get_cache_key(
            "feedback",
            user_answer,
            correct_answer,
            str(exercise_context)
        )
        cached = await self._get_cached(cache_key)
        if cached:
            return cached

        # Build contextual prompt
        verb = exercise_context.get("verb", "the verb")
        tense = exercise_context.get("tense", "subjunctive")
        person = exercise_context.get("person", "")
        trigger = exercise_context.get("trigger", "")
        sentence = exercise_context.get("sentence", "")

        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()

        system_prompt = """You are an encouraging Spanish language tutor specializing in the subjunctive mood.
Your feedback should be:
- Warm and encouraging
- Specific and educational
- Brief (2-3 sentences max)
- Focused on understanding, not just correctness
- Culturally sensitive and supportive"""

        if is_correct:
            prompt = f"""The student correctly conjugated '{verb}' in the {tense} form.

Verb: {verb}
Tense: {tense}
Person: {person}
Trigger phrase: {trigger}
Complete sentence: {sentence}
Student's answer: {user_answer}

Provide brief, encouraging feedback (2-3 sentences) that:
1. Confirms they're correct
2. Mentions one interesting point about this usage
3. Encourages continued practice"""
        else:
            prompt = f"""The student made a mistake conjugating '{verb}' in the {tense} form.

Verb: {verb}
Tense: {tense}
Person: {person}
Trigger phrase: {trigger}
Complete sentence: {sentence}
Student's answer: {user_answer}
Correct answer: {correct_answer}

Provide brief, supportive feedback (2-3 sentences) that:
1. Gently points out the error
2. Explains WHY the correct form is needed (connection to trigger/context)
3. Offers one specific tip for remembering this pattern"""

        try:
            feedback = await self._create_message(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=200,
                temperature=0.7
            )

            # Cache the response (1 hour TTL for feedback)
            await self._set_cache(cache_key, feedback, ttl=3600)

            return feedback

        except (AIServiceUnavailableError, RateLimitExceededError) as e:
            logger.warning(
                "feedback_generation_failed",
                error=str(e),
                fallback_used=True
            )
            # Fallback to simple feedback
            if is_correct:
                return f"Excellent! '{user_answer}' is correct."
            return f"The correct answer is '{correct_answer}'. Keep practicing!"

    @retry_on_rate_limit(max_retries=3, base_delay=1.0)
    async def generate_learning_insights(
        self,
        user_stats: Dict[str, Any],
        weak_areas: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate personalized learning insights based on user performance.

        Args:
            user_stats: User statistics (accuracy, sessions, time, etc.)
            weak_areas: List of areas where user is struggling

        Returns:
            List of actionable learning insights (3-5 insights)

        Example:
            >>> stats = {
            ...     "total_exercises": 150,
            ...     "accuracy": 0.72,
            ...     "weak_tenses": ["imperfect_subjunctive"],
            ...     "weak_verbs": ["ser", "estar", "ir"]
            ... }
            >>> weak_areas = [
            ...     {"area": "imperfect_subjunctive", "accuracy": 0.55},
            ...     {"area": "irregular_verbs", "accuracy": 0.60}
            ... ]
            >>> insights = await service.generate_learning_insights(stats, weak_areas)
        """
        if not self.is_enabled:
            # Fallback to generic insights
            return [
                "Keep practicing regularly to improve your skills.",
                "Focus on areas where you score below 70%.",
                "Review the subjunctive triggers and their patterns."
            ]

        # Check cache
        cache_key = self._get_cache_key(
            "insights",
            str(user_stats),
            str(weak_areas)
        )
        cached = await self._get_cached(cache_key)
        if cached:
            # Parse cached JSON-like response
            import json
            try:
                # Cache already stores deserialized objects
                if isinstance(cached, list):
                    return cached
                return json.loads(cached)
            except (json.JSONDecodeError, TypeError):
                # If cache is corrupted, regenerate
                pass

        system_prompt = """You are an expert Spanish language learning coach.
Analyze student performance data and provide actionable, specific insights.
Your insights should be:
- Data-driven and specific
- Actionable with concrete next steps
- Encouraging but honest
- Focused on learning strategies
- Limited to 3-5 key points"""

        # Build detailed performance summary
        total_exercises = user_stats.get("total_exercises", 0)
        accuracy = user_stats.get("accuracy", 0)
        total_time = user_stats.get("total_study_time_minutes", 0)
        sessions = user_stats.get("total_sessions", 0)

        weak_areas_text = "\n".join([
            f"- {area.get('area', 'unknown')}: {area.get('accuracy', 0):.0%} accuracy"
            for area in weak_areas[:5]  # Limit to top 5
        ])

        prompt = f"""Analyze this Spanish learner's performance data:

OVERALL STATISTICS:
- Total exercises completed: {total_exercises}
- Overall accuracy: {accuracy:.0%}
- Total study time: {total_time} minutes
- Number of sessions: {sessions}

WEAK AREAS:
{weak_areas_text or "- No significant weak areas identified"}

Based on this data, provide 3-5 specific, actionable learning insights.
Format as a JSON array of strings.
Each insight should be one clear sentence with a specific recommendation.

Example format:
["Insight 1 here", "Insight 2 here", "Insight 3 here"]"""

        try:
            response = await self._create_message(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=500,
                temperature=0.6
            )

            # Parse JSON response
            import json
            # Extract JSON from response (Claude might add extra text)
            start_idx = response.find("[")
            end_idx = response.rfind("]") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                insights = json.loads(json_str)

                # Validate and limit insights
                if isinstance(insights, list) and all(isinstance(i, str) for i in insights):
                    insights = insights[:5]  # Limit to 5 insights

                    # Cache the response (2 hours TTL for insights, they change less frequently)
                    await self._set_cache(cache_key, insights, ttl=7200)

                    return insights

            # If parsing fails, return fallback
            raise ValueError("Could not parse insights from response")

        except (AIServiceUnavailableError, RateLimitExceededError, ValueError) as e:
            logger.warning(
                "insights_generation_failed",
                error=str(e),
                fallback_used=True
            )
            # Fallback insights based on data
            fallback_insights = []

            if accuracy < 0.6:
                fallback_insights.append(
                    "Focus on mastering the basic subjunctive triggers before moving to advanced patterns."
                )
            elif accuracy < 0.8:
                fallback_insights.append(
                    "You're making good progress! Focus on your weak areas to reach 80% accuracy."
                )
            else:
                fallback_insights.append(
                    "Excellent progress! Challenge yourself with more difficult exercises."
                )

            if weak_areas:
                top_weak = weak_areas[0].get("area", "weak areas")
                fallback_insights.append(
                    f"Spend extra time practicing {top_weak} - this will significantly improve your overall score."
                )

            if sessions > 0 and total_exercises / sessions < 10:
                fallback_insights.append(
                    "Try to complete at least 10-15 exercises per session for better retention."
                )

            return fallback_insights[:5]

    @retry_on_rate_limit(max_retries=3, base_delay=1.0)
    async def generate_personalized_hint(
        self,
        exercise: Dict[str, Any],
        user_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate a personalized hint for an exercise based on user history.

        Args:
            exercise: Exercise details (verb, tense, trigger, sentence, etc.)
            user_history: Optional list of recent attempts/errors by user

        Returns:
            Personalized hint that guides without giving away the answer

        Example:
            >>> exercise = {
            ...     "verb": "hablar",
            ...     "tense": "present_subjunctive",
            ...     "person": "él/ella",
            ...     "trigger": "Es necesario que",
            ...     "sentence": "Es necesario que él ___ con el doctor"
            ... }
            >>> history = [
            ...     {"verb": "hablar", "error_type": "wrong_ending"},
            ...     {"verb": "comer", "error_type": "wrong_ending"}
            ... ]
            >>> hint = await service.generate_personalized_hint(exercise, history)
        """
        if not self.is_enabled:
            # Fallback to generic hint
            tense = exercise.get("tense", "subjunctive")
            return f"Think about the {tense} conjugation pattern for this verb."

        # Check cache (no user_history in cache key - hints should be fresh)
        cache_key = self._get_cache_key("hint", str(exercise))
        cached = await self._get_cached(cache_key)
        if cached:
            return cached

        system_prompt = """You are a patient Spanish tutor providing helpful hints.
Your hints should:
- Guide the learner without revealing the answer
- Connect to the subjunctive trigger in the sentence
- Be specific to this verb and tense
- Be encouraging and brief (1-2 sentences)
- Not include the actual conjugated form"""

        verb = exercise.get("verb", "the verb")
        tense = exercise.get("tense", "subjunctive")
        person = exercise.get("person", "")
        trigger = exercise.get("trigger", "")
        sentence = exercise.get("sentence", "")

        # Analyze user history for patterns
        history_text = ""
        if user_history:
            recent_errors = [h.get("error_type") for h in user_history[-3:] if h.get("error_type")]
            if recent_errors:
                history_text = f"\nRecent error patterns: {', '.join(recent_errors)}"

        prompt = f"""Create a helpful hint for this Spanish subjunctive exercise:

Verb (infinitive): {verb}
Tense needed: {tense}
Person: {person}
Trigger phrase: {trigger}
Sentence: {sentence}{history_text}

Provide a brief hint (1-2 sentences) that:
1. Reminds them WHY subjunctive is needed (connection to the trigger)
2. Guides them toward the correct conjugation pattern
3. Does NOT reveal the actual answer

Be specific to this exercise, not generic."""

        try:
            hint = await self._create_message(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=150,
                temperature=0.7
            )

            # Cache the hint (30 minutes TTL for hints)
            await self._set_cache(cache_key, hint, ttl=1800)

            return hint

        except (AIServiceUnavailableError, RateLimitExceededError) as e:
            logger.warning(
                "hint_generation_failed",
                error=str(e),
                fallback_used=True
            )
            # Fallback hint
            if trigger:
                return f"Remember: '{trigger}' triggers the subjunctive. Think about the {tense} pattern for {person}."
            return f"This exercise requires the {tense} form. Consider the verb ending for {person}."

    async def batch_generate_feedback(
        self,
        feedback_requests: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate feedback for multiple exercises in parallel.

        Args:
            feedback_requests: List of dicts with keys: user_answer, correct_answer, exercise_context

        Returns:
            List of feedback messages in the same order as requests
        """
        if not self.is_enabled:
            return [
                "Feedback unavailable - AI service not configured"
            ] * len(feedback_requests)

        tasks = [
            self.generate_feedback(
                req["user_answer"],
                req["correct_answer"],
                req["exercise_context"]
            )
            for req in feedback_requests
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to error messages
        return [
            result if isinstance(result, str) else f"Error generating feedback: {str(result)}"
            for result in results
        ]

    async def clear_cache(self) -> int:
        """
        Clear the response cache.

        Returns:
            Number of cache entries cleared
        """
        count = await self._cache.clear()
        logger.info("cache_cleared", entries_cleared=count)
        return count

    def get_cache_statistics(self) -> Dict[str, Any]:
        """
        Get cache performance statistics.

        Returns:
            Dictionary with cache stats (hits, misses, hit rate, etc.)
        """
        return self._cache.get_statistics()

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the AI service.

        Returns:
            Health status information
        """
        # Check cache health
        cache_health = await self._cache.health_check()

        if not self.is_enabled:
            return {
                "status": "disabled",
                "configured": False,
                "message": "AI service not configured (missing API key)",
                "cache": cache_health
            }

        try:
            # Make a minimal API call to verify connectivity
            test_response = await self._create_message(
                prompt="Respond with 'OK' if you can read this.",
                max_tokens=10,
                temperature=0
            )

            return {
                "status": "healthy",
                "configured": True,
                "model": settings.ANTHROPIC_MODEL,
                "cache": cache_health,
                "cache_statistics": self.get_cache_statistics(),
                "test_response": test_response[:50]  # First 50 chars
            }

        except Exception as e:
            logger.error("health_check_failed", error=str(e))
            return {
                "status": "unhealthy",
                "configured": True,
                "error": str(e),
                "model": settings.ANTHROPIC_MODEL,
                "cache": cache_health
            }


# Global service instance
_ai_service: Optional[ClaudeAIService] = None


def get_ai_service() -> ClaudeAIService:
    """
    Get or create the global AI service instance.

    This function is used as a FastAPI dependency.

    Returns:
        ClaudeAIService instance
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = ClaudeAIService()
    return _ai_service


async def shutdown_ai_service() -> None:
    """
    Cleanup function to be called on application shutdown.
    """
    global _ai_service
    if _ai_service:
        await _ai_service.clear_cache()
        await _ai_service._cache.close()
        logger.info("ai_service_shutdown")
