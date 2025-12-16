"""
Tests for Redis cache service with in-memory fallback.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from services.cache_service import (
    RedisCache,
    InMemoryCache,
    CacheStatistics,
    get_cache_service,
    shutdown_cache_service
)


class TestCacheStatistics:
    """Test cache statistics tracking."""

    def test_statistics_initialization(self):
        """Test statistics are initialized correctly."""
        stats = CacheStatistics()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.sets == 0
        assert stats.deletes == 0
        assert stats.errors == 0
        assert stats.total_requests == 0
        assert stats.hit_rate == 0.0

    def test_hit_rate_calculation(self):
        """Test hit rate is calculated correctly."""
        stats = CacheStatistics()
        stats.hits = 75
        stats.misses = 25
        assert stats.total_requests == 100
        assert stats.hit_rate == 75.0

    def test_hit_rate_with_no_requests(self):
        """Test hit rate when no requests made."""
        stats = CacheStatistics()
        assert stats.hit_rate == 0.0

    def test_to_dict(self):
        """Test statistics export to dictionary."""
        stats = CacheStatistics()
        stats.hits = 10
        stats.misses = 5
        stats.sets = 8
        stats.deletes = 2
        stats.errors = 1

        result = stats.to_dict()
        assert result["hits"] == 10
        assert result["misses"] == 5
        assert result["sets"] == 8
        assert result["deletes"] == 2
        assert result["errors"] == 1
        assert result["total_requests"] == 15
        assert result["hit_rate_percent"] == 66.67
        assert "uptime_seconds" in result


class TestInMemoryCache:
    """Test in-memory cache fallback."""

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        """Test basic set and get operations."""
        cache = InMemoryCache()
        await cache.set("test_key", "test_value")
        result = await cache.get("test_key")
        assert result == "test_value"

    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        cache = InMemoryCache()
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_with_ttl(self):
        """Test setting value with TTL."""
        cache = InMemoryCache()
        await cache.set("key", "value", ttl=1)

        # Should exist immediately
        result = await cache.get("key")
        assert result == "value"

        # Wait for expiry
        await asyncio.sleep(1.1)
        result = await cache.get("key")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test deleting a key."""
        cache = InMemoryCache()
        await cache.set("key", "value")
        assert await cache.get("key") == "value"

        deleted = await cache.delete("key")
        assert deleted is True
        assert await cache.get("key") is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist."""
        cache = InMemoryCache()
        deleted = await cache.delete("nonexistent")
        assert deleted is False

    @pytest.mark.asyncio
    async def test_clear(self):
        """Test clearing all cache entries."""
        cache = InMemoryCache()
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.set("key3", "value3")

        count = await cache.clear()
        assert count == 3

        assert await cache.get("key1") is None
        assert await cache.get("key2") is None
        assert await cache.get("key3") is None

    def test_size(self):
        """Test getting cache size."""
        cache = InMemoryCache()
        assert cache.size() == 0

        # Note: Can't use asyncio.run in sync test, so we'll test manually
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cache.set("key1", "value1"))
        loop.run_until_complete(cache.set("key2", "value2"))

        assert cache.size() == 2


class TestRedisCache:
    """Test Redis cache with fallback."""

    @pytest.mark.asyncio
    async def test_initialization_without_redis(self):
        """Test cache initializes with in-memory fallback when Redis not configured."""
        cache = RedisCache(redis_url=None, key_prefix="test")
        assert not cache.is_redis_available
        assert cache._fallback_cache is not None

    @pytest.mark.asyncio
    async def test_set_and_get_with_fallback(self):
        """Test set/get operations fall back to in-memory cache."""
        cache = RedisCache(redis_url=None, key_prefix="test")

        await cache.set("key", "value")
        result = await cache.get("key")
        assert result == "value"

    @pytest.mark.asyncio
    async def test_key_prefixing(self):
        """Test cache keys are prefixed correctly."""
        cache = RedisCache(redis_url=None, key_prefix="myapp")
        assert cache._make_key("test") == "myapp:test"

    @pytest.mark.asyncio
    async def test_json_serialization(self):
        """Test JSON serialization for complex objects."""
        cache = RedisCache(redis_url=None)

        # Test dictionary
        data = {"name": "John", "age": 30, "active": True}
        await cache.set("user", data)
        result = await cache.get("user")
        assert result == data

        # Test list
        items = [1, 2, 3, 4, 5]
        await cache.set("items", items)
        result = await cache.get("items")
        assert result == items

    @pytest.mark.asyncio
    async def test_ttl_expiration(self):
        """Test TTL expiration works correctly."""
        cache = RedisCache(redis_url=None)

        await cache.set("key", "value", ttl=1)
        assert await cache.get("key") == "value"

        # Wait for expiry
        await asyncio.sleep(1.1)
        assert await cache.get("key") is None

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test deleting keys."""
        cache = RedisCache(redis_url=None)

        await cache.set("key1", "value1")
        await cache.set("key2", "value2")

        deleted = await cache.delete("key1")
        assert deleted is True
        assert await cache.get("key1") is None
        assert await cache.get("key2") == "value2"

    @pytest.mark.asyncio
    async def test_clear(self):
        """Test clearing all cache entries."""
        cache = RedisCache(redis_url=None, key_prefix="test")

        await cache.set("key1", "value1")
        await cache.set("key2", "value2")

        count = await cache.clear()
        assert count >= 2

    @pytest.mark.asyncio
    async def test_statistics_tracking(self):
        """Test cache statistics are tracked correctly."""
        cache = RedisCache(redis_url=None)

        # Initial stats
        stats = cache.get_statistics()
        assert stats["hits"] == 0
        assert stats["misses"] == 0

        # Set a value
        await cache.set("key", "value")

        # Hit
        await cache.get("key")
        stats = cache.get_statistics()
        assert stats["hits"] == 1
        assert stats["misses"] == 0

        # Miss
        await cache.get("nonexistent")
        stats = cache.get_statistics()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate_percent"] == 50.0

    @pytest.mark.asyncio
    async def test_reset_statistics(self):
        """Test resetting cache statistics."""
        cache = RedisCache(redis_url=None)

        await cache.set("key", "value")
        await cache.get("key")

        cache.reset_statistics()
        stats = cache.get_statistics()
        assert stats["hits"] == 0
        assert stats["misses"] == 0

    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check returns correct information."""
        cache = RedisCache(redis_url=None)

        health = await cache.health_check()
        assert "redis" in health
        assert "fallback" in health
        assert "statistics" in health
        assert health["redis"]["available"] is False
        assert health["fallback"]["available"] is True

    @pytest.mark.asyncio
    @patch('services.cache_service.Redis')
    @patch('services.cache_service.ConnectionPool')
    async def test_redis_initialization_success(self, mock_pool_class, mock_redis_class):
        """Test successful Redis initialization."""
        # Mock Redis connection
        mock_pool = MagicMock()
        mock_pool_class.from_url.return_value = mock_pool

        mock_redis = AsyncMock()
        mock_redis_class.return_value = mock_redis

        cache = RedisCache(redis_url="redis://localhost:6379")

        assert cache.is_redis_available is True
        assert cache._redis is not None

    @pytest.mark.asyncio
    @patch('services.cache_service.ConnectionPool')
    async def test_redis_initialization_failure(self, mock_pool_class):
        """Test Redis initialization failure falls back to memory."""
        # Simulate connection failure
        mock_pool_class.from_url.side_effect = Exception("Connection failed")

        cache = RedisCache(redis_url="redis://localhost:6379")

        assert cache.is_redis_available is False
        assert cache._fallback_cache is not None

    @pytest.mark.asyncio
    async def test_url_masking(self):
        """Test sensitive URL parts are masked in logs."""
        cache = RedisCache(redis_url=None)

        # Test with password
        url = "redis://user:secretpassword@localhost:6379/0"
        masked = cache._mask_url(url)
        assert "secretpassword" not in masked
        assert "****" in masked

        # Test without password
        url = "redis://localhost:6379/0"
        masked = cache._mask_url(url)
        assert masked == url

    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent cache operations."""
        cache = RedisCache(redis_url=None)

        # Set multiple values concurrently
        tasks = [
            cache.set(f"key{i}", f"value{i}")
            for i in range(10)
        ]
        await asyncio.gather(*tasks)

        # Get multiple values concurrently
        tasks = [
            cache.get(f"key{i}")
            for i in range(10)
        ]
        results = await asyncio.gather(*tasks)

        assert len(results) == 10
        for i, result in enumerate(results):
            assert result == f"value{i}"

    @pytest.mark.asyncio
    async def test_string_values_not_double_serialized(self):
        """Test string values are not double-serialized."""
        cache = RedisCache(redis_url=None)

        # String should be stored as-is
        await cache.set("key", "simple string")
        result = await cache.get("key")
        assert result == "simple string"
        assert isinstance(result, str)


class TestGlobalCacheService:
    """Test global cache service instance."""

    def test_get_cache_service_singleton(self):
        """Test get_cache_service returns singleton instance."""
        service1 = get_cache_service()
        service2 = get_cache_service()
        assert service1 is service2

    @pytest.mark.asyncio
    async def test_shutdown_cache_service(self):
        """Test cache service shutdown."""
        service = get_cache_service()
        assert service is not None

        await shutdown_cache_service()
        # Service should still exist but connections should be closed


class TestIntegrationWithAIService:
    """Integration tests with AI service."""

    @pytest.mark.asyncio
    async def test_cache_key_generation(self):
        """Test cache key generation for AI service."""
        cache = RedisCache(redis_url=None, key_prefix="subjunctive")

        # Simulate AI service cache keys
        key1 = cache._make_key("ai:feedback:hablar:hable")
        key2 = cache._make_key("ai:insights:user123:stats")

        assert key1.startswith("subjunctive:")
        assert key2.startswith("subjunctive:")

    @pytest.mark.asyncio
    async def test_cache_different_ttls(self):
        """Test different TTLs for different types of AI responses."""
        cache = RedisCache(redis_url=None)

        # Feedback: 1 hour
        await cache.set("feedback:1", "Great work!", ttl=3600)

        # Hints: 30 minutes
        await cache.set("hint:1", "Think about the trigger", ttl=1800)

        # Insights: 2 hours
        await cache.set("insights:1", ["Insight 1", "Insight 2"], ttl=7200)

        # All should be retrievable
        assert await cache.get("feedback:1") == "Great work!"
        assert await cache.get("hint:1") == "Think about the trigger"
        assert await cache.get("insights:1") == ["Insight 1", "Insight 2"]


# Performance test (optional, can be run manually)
@pytest.mark.skipif(True, reason="Performance test - run manually")
@pytest.mark.asyncio
async def test_cache_performance():
    """Test cache performance with many operations."""
    cache = RedisCache(redis_url=None)

    import time

    # Write performance
    start = time.time()
    for i in range(1000):
        await cache.set(f"key{i}", f"value{i}")
    write_time = time.time() - start
    print(f"1000 writes: {write_time:.2f}s ({1000/write_time:.0f} ops/s)")

    # Read performance
    start = time.time()
    for i in range(1000):
        await cache.get(f"key{i}")
    read_time = time.time() - start
    print(f"1000 reads: {read_time:.2f}s ({1000/read_time:.0f} ops/s)")

    stats = cache.get_statistics()
    print(f"Hit rate: {stats['hit_rate_percent']}%")
