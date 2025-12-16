"""
Redis Cache Usage Examples

This file demonstrates how to use the Redis cache service in different scenarios.
"""

import asyncio
from typing import Dict, Any, List


# Example 1: Basic Cache Operations
# ==================================

async def example_basic_operations():
    """Basic cache set/get/delete operations."""
    from services.cache_service import get_cache_service

    cache = get_cache_service()

    # Set a simple value
    await cache.set("user:123:name", "Alice")

    # Get the value
    name = await cache.get("user:123:name")
    print(f"User name: {name}")

    # Set with TTL (expires in 60 seconds)
    await cache.set("session:abc123", {"user_id": 123, "active": True}, ttl=60)

    # Delete a key
    await cache.delete("user:123:name")


# Example 2: Caching AI Responses
# ================================

async def example_ai_response_caching():
    """Cache AI-generated responses with different TTLs."""
    from services.ai_service import get_ai_service

    service = get_ai_service()

    # Generate feedback (cached for 1 hour)
    feedback = await service.generate_feedback(
        user_answer="hable",
        correct_answer="hable",
        exercise_context={
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "yo",
            "trigger": "Es importante que"
        }
    )
    print(f"Feedback: {feedback}")

    # Second call uses cache (no API call)
    feedback_cached = await service.generate_feedback(
        user_answer="hable",
        correct_answer="hable",
        exercise_context={
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "yo",
            "trigger": "Es importante que"
        }
    )
    # feedback_cached is retrieved from cache instantly!


# Example 3: Cache Statistics and Monitoring
# ===========================================

async def example_cache_monitoring():
    """Monitor cache performance."""
    from services.ai_service import get_ai_service

    service = get_ai_service()

    # Get cache statistics
    stats = service.get_cache_statistics()

    print(f"Cache Performance:")
    print(f"  Hits: {stats['hits']}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Hit Rate: {stats['hit_rate_percent']:.1f}%")
    print(f"  Backend: {stats['backend']}")

    # Health check
    health = await service.health_check()
    print(f"\nCache Health:")
    print(f"  Redis Available: {health['cache']['redis']['available']}")
    print(f"  Redis Healthy: {health['cache']['redis']['healthy']}")


# Example 4: Batch Operations with Cache
# =======================================

async def example_batch_caching():
    """Efficient batch operations with caching."""
    from services.ai_service import get_ai_service

    service = get_ai_service()

    # Prepare multiple feedback requests
    requests = [
        {
            "user_answer": "hable",
            "correct_answer": "hable",
            "exercise_context": {"verb": "hablar", "tense": "present_subjunctive"}
        },
        {
            "user_answer": "sea",
            "correct_answer": "sea",
            "exercise_context": {"verb": "ser", "tense": "present_subjunctive"}
        },
        {
            "user_answer": "vaya",
            "correct_answer": "vaya",
            "exercise_context": {"verb": "ir", "tense": "present_subjunctive"}
        }
    ]

    # Generate feedback in parallel (uses cache when available)
    feedbacks = await service.batch_generate_feedback(requests)

    for i, feedback in enumerate(feedbacks):
        print(f"Exercise {i+1}: {feedback[:50]}...")


# Example 5: Custom Cache with Different TTLs
# ============================================

async def example_custom_ttls():
    """Use different TTLs for different data types."""
    from services.cache_service import get_cache_service

    cache = get_cache_service()

    # User session: 30 minutes
    await cache.set(
        "session:user123",
        {"user_id": 123, "logged_in": True},
        ttl=1800  # 30 minutes
    )

    # Exercise data: 1 hour
    await cache.set(
        "exercise:spanish:present",
        {"verb": "hablar", "conjugation": "hable"},
        ttl=3600  # 1 hour
    )

    # Static content: 24 hours
    await cache.set(
        "content:verbs:list",
        ["hablar", "comer", "vivir"],
        ttl=86400  # 24 hours
    )

    # Temporary data: 5 minutes
    await cache.set(
        "temp:verification_code",
        "ABC123",
        ttl=300  # 5 minutes
    )


# Example 6: Cache Warming on Startup
# ====================================

async def example_cache_warming():
    """Pre-populate cache with common data."""
    from services.ai_service import get_ai_service

    service = get_ai_service()

    # Most common exercises
    common_exercises = [
        ("hablar", "present_subjunctive", "yo"),
        ("ser", "present_subjunctive", "yo"),
        ("ir", "present_subjunctive", "yo"),
        ("tener", "present_subjunctive", "él/ella"),
        ("hacer", "present_subjunctive", "nosotros/nosotras"),
    ]

    print("Warming cache with common exercises...")

    for verb, tense, person in common_exercises:
        # This will cache the response
        await service.generate_personalized_hint(
            exercise={
                "verb": verb,
                "tense": tense,
                "person": person,
                "trigger": "Es importante que"
            }
        )
        print(f"  ✓ Cached hint for {verb} ({tense})")

    print("Cache warming complete!")


# Example 7: Cache Invalidation
# ==============================

async def example_cache_invalidation():
    """Clear cache when data changes."""
    from services.cache_service import get_cache_service

    cache = get_cache_service()

    # User updates their settings
    user_id = 123

    # Clear user-specific cache
    await cache.delete(f"user:{user_id}:preferences")
    await cache.delete(f"user:{user_id}:stats")
    await cache.delete(f"user:{user_id}:insights")

    print(f"Invalidated cache for user {user_id}")

    # Or clear all AI cache
    from services.ai_service import get_ai_service
    service = get_ai_service()
    count = await service.clear_cache()
    print(f"Cleared {count} AI cache entries")


# Example 8: Graceful Degradation
# ================================

async def example_graceful_degradation():
    """Handle cache failures gracefully."""
    from services.cache_service import get_cache_service

    cache = get_cache_service()

    # The cache service automatically falls back to in-memory cache
    # if Redis is unavailable. No error handling needed!

    try:
        await cache.set("key", "value")
        value = await cache.get("key")
        # Works whether Redis is available or not
    except Exception as e:
        # Cache errors are logged but don't break the application
        print(f"Cache operation failed: {e}")
        # Continue with business logic


# Example 9: Performance Testing
# ===============================

async def example_performance_test():
    """Test cache performance."""
    from services.cache_service import get_cache_service
    import time

    cache = get_cache_service()

    # Write performance
    start = time.time()
    for i in range(100):
        await cache.set(f"perf:key{i}", f"value{i}")
    write_time = time.time() - start

    # Read performance
    start = time.time()
    for i in range(100):
        await cache.get(f"perf:key{i}")
    read_time = time.time() - start

    print(f"Performance Test:")
    print(f"  100 writes: {write_time:.3f}s ({100/write_time:.0f} ops/s)")
    print(f"  100 reads: {read_time:.3f}s ({100/read_time:.0f} ops/s)")

    # Check statistics
    stats = cache.get_statistics()
    print(f"  Hit rate: {stats['hit_rate_percent']:.1f}%")


# Example 10: Production Configuration
# =====================================

def example_production_config():
    """Recommended production configuration."""

    config = """
# Production .env configuration

# Redis Cloud connection
REDIS_URL=redis://default:password@redis-12345.cloud.redislabs.com:12345/0

# Cache settings
REDIS_CACHE_TTL=7200          # 2 hours default TTL
REDIS_CACHE_PREFIX=subj_prod  # Unique prefix per environment
REDIS_POOL_SIZE=20            # Larger pool for high traffic

# Application settings
ENVIRONMENT=production
LOG_LEVEL=INFO

# Enable all production features
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
    """

    print("Production Configuration Example:")
    print(config)


# Example 11: Development vs Production
# ======================================

def example_environment_configs():
    """Different configurations for different environments."""

    configs = {
        "development": {
            "REDIS_URL": "redis://localhost:6379/0",
            "REDIS_CACHE_TTL": 1800,  # 30 minutes
            "REDIS_CACHE_PREFIX": "subj_dev",
            "REDIS_POOL_SIZE": 5,
        },
        "staging": {
            "REDIS_URL": "redis://staging-redis:6379/0",
            "REDIS_CACHE_TTL": 3600,  # 1 hour
            "REDIS_CACHE_PREFIX": "subj_staging",
            "REDIS_POOL_SIZE": 10,
        },
        "production": {
            "REDIS_URL": "redis://prod-redis-cluster:6379/0",
            "REDIS_CACHE_TTL": 7200,  # 2 hours
            "REDIS_CACHE_PREFIX": "subj_prod",
            "REDIS_POOL_SIZE": 20,
        }
    }

    for env, config in configs.items():
        print(f"\n{env.upper()} Configuration:")
        for key, value in config.items():
            print(f"  {key}={value}")


# Main execution
# ==============

async def main():
    """Run examples."""
    print("Redis Cache Usage Examples")
    print("=" * 60)

    print("\n1. Basic Operations")
    print("-" * 60)
    await example_basic_operations()

    print("\n2. Cache Statistics")
    print("-" * 60)
    await example_cache_monitoring()

    print("\n3. Custom TTLs")
    print("-" * 60)
    await example_custom_ttls()

    print("\n4. Environment Configurations")
    print("-" * 60)
    example_environment_configs()

    print("\n" + "=" * 60)
    print("Examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
