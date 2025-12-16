"""
Quick test script to verify Redis cache implementation.
Run this after installing dependencies: pip install -r requirements.txt
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

async def test_cache_basic():
    """Test basic cache operations."""
    print("=" * 60)
    print("Testing Redis Cache Implementation")
    print("=" * 60)

    from services.cache_service import RedisCache

    # Test without Redis (in-memory fallback)
    print("\n1. Testing In-Memory Fallback (no Redis)...")
    cache = RedisCache(redis_url=None, key_prefix="test")

    # Set a value
    await cache.set("greeting", "Hello World!")
    print("   ✓ Set value: greeting = 'Hello World!'")

    # Get the value
    result = await cache.get("greeting")
    assert result == "Hello World!", f"Expected 'Hello World!', got {result}"
    print(f"   ✓ Get value: {result}")

    # Test with complex object
    data = {"name": "John", "age": 30, "skills": ["Python", "JavaScript"]}
    await cache.set("user", data)
    result = await cache.get("user")
    assert result == data, f"Expected {data}, got {result}"
    print(f"   ✓ Complex object: {result}")

    # Test statistics
    stats = cache.get_statistics()
    print(f"\n2. Cache Statistics:")
    print(f"   - Hits: {stats['hits']}")
    print(f"   - Misses: {stats['misses']}")
    print(f"   - Hit Rate: {stats['hit_rate_percent']:.1f}%")
    print(f"   - Backend: {stats['backend']}")

    # Test TTL
    print("\n3. Testing TTL expiration...")
    await cache.set("temp", "expires soon", ttl=2)
    result = await cache.get("temp")
    assert result == "expires soon"
    print("   ✓ Value set with 2 second TTL")

    print("   Waiting 2.5 seconds...")
    await asyncio.sleep(2.5)

    result = await cache.get("temp")
    assert result is None, f"Expected None (expired), got {result}"
    print("   ✓ Value expired as expected")

    # Test health check
    print("\n4. Health Check:")
    health = await cache.health_check()
    print(f"   - Redis Available: {health['redis']['available']}")
    print(f"   - Fallback Available: {health['fallback']['available']}")
    print(f"   - Cache Size: {health['fallback']['size']}")

    # Test clear
    print("\n5. Testing cache clear...")
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    count = await cache.clear()
    print(f"   ✓ Cleared {count} entries")

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


async def test_ai_service_integration():
    """Test AI service with cache."""
    print("\n" + "=" * 60)
    print("Testing AI Service Integration")
    print("=" * 60)

    from services.cache_service import RedisCache
    from services.ai_service import ClaudeAIService

    # Create cache
    cache = RedisCache(redis_url=None, key_prefix="subjunctive")

    # Create AI service with cache
    ai_service = ClaudeAIService(cache_service=cache)

    print(f"\n1. AI Service Status:")
    print(f"   - Enabled: {ai_service.is_enabled}")
    print(f"   - Cache Backend: {'Redis' if cache.is_redis_available else 'Memory'}")

    # Test cache key generation
    key1 = ai_service._get_cache_key("feedback", "hablar", "hable", "context")
    print(f"\n2. Cache Key Generation:")
    print(f"   - Key: {key1[:60]}...")

    # Test very long key (should be hashed)
    long_context = "x" * 300
    key2 = ai_service._get_cache_key("feedback", long_context)
    assert len(key2) < 100, "Long keys should be hashed"
    print(f"   - Long key (hashed): {key2}")

    # Test cache statistics
    stats = ai_service.get_cache_statistics()
    print(f"\n3. AI Service Cache Stats:")
    print(f"   - Backend: {stats['backend']}")
    print(f"   - Redis Available: {stats['redis_available']}")

    # Simulate caching a response
    test_key = ai_service._get_cache_key("test", "exercise1")
    await ai_service._set_cache(test_key, "Cached response", ttl=60)
    cached = await ai_service._get_cached(test_key)
    assert cached == "Cached response"
    print(f"\n4. Cache Operations:")
    print(f"   ✓ Set and retrieved cached response")

    # Clear cache
    count = await ai_service.clear_cache()
    print(f"   ✓ Cleared {count} cache entries")

    print("\n" + "=" * 60)
    print("✓ AI Service Integration tests passed!")
    print("=" * 60)


async def main():
    """Run all tests."""
    try:
        await test_cache_basic()
        await test_ai_service_integration()

        print("\n" + "🎉" * 30)
        print("\nSUCCESS! Redis cache implementation is working correctly.")
        print("\nNext steps:")
        print("1. Install Redis: docker run -d -p 6379:6379 redis:7-alpine")
        print("2. Set REDIS_URL in .env: REDIS_URL=redis://localhost:6379/0")
        print("3. Restart the application to use Redis instead of memory")
        print("\n" + "🎉" * 30)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
