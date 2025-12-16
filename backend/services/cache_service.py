"""
Redis-based caching service with in-memory fallback.

This module provides a robust caching layer that:
- Uses Redis for distributed caching in production
- Falls back to in-memory caching if Redis is unavailable
- Supports async operations for non-blocking performance
- Provides connection pooling and automatic reconnection
- Tracks cache statistics (hits/misses)
- Handles JSON serialization automatically
"""

import asyncio
import json
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
from collections import defaultdict
import structlog

from redis.asyncio import Redis, ConnectionPool
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

from core.config import settings


logger = structlog.get_logger(__name__)


class CacheStatistics:
    """Track cache performance metrics."""

    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.sets: int = 0
        self.deletes: int = 0
        self.errors: int = 0
        self.started_at: datetime = datetime.now()

    @property
    def total_requests(self) -> int:
        """Total cache requests (hits + misses)."""
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        """Cache hit rate as percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Export statistics as dictionary."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "sets": self.sets,
            "deletes": self.deletes,
            "errors": self.errors,
            "total_requests": self.total_requests,
            "hit_rate_percent": round(self.hit_rate, 2),
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds()
        }


class InMemoryCache:
    """Simple in-memory cache fallback."""

    def __init__(self):
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._default_ttl = timedelta(hours=1)
        logger.info("in_memory_cache_initialized")

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if key in self._cache:
            value, expiry = self._cache[key]
            if datetime.now() < expiry:
                return value
            else:
                # Expired
                del self._cache[key]
        return None

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL in seconds."""
        ttl_delta = timedelta(seconds=ttl) if ttl else self._default_ttl
        self._cache[key] = (value, datetime.now() + ttl_delta)
        return True

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    async def clear(self) -> int:
        """Clear all cache entries."""
        count = len(self._cache)
        self._cache.clear()
        return count

    def size(self) -> int:
        """Get number of cached items."""
        # Clean expired entries
        now = datetime.now()
        expired_keys = [k for k, (_, expiry) in self._cache.items() if now >= expiry]
        for k in expired_keys:
            del self._cache[k]
        return len(self._cache)


class RedisCache:
    """
    Redis-based cache with automatic fallback to in-memory cache.

    Features:
    - Async/await support
    - Connection pooling
    - Automatic reconnection on failure
    - JSON serialization
    - TTL support with defaults
    - Key prefix namespacing
    - Statistics tracking
    - Graceful fallback to in-memory cache
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        key_prefix: str = "subjunctive",
        default_ttl: int = 3600,  # 1 hour
        pool_size: int = 10
    ):
        """
        Initialize Redis cache with fallback.

        Args:
            redis_url: Redis connection URL (defaults to settings.REDIS_URL)
            key_prefix: Prefix for all cache keys
            default_ttl: Default TTL in seconds
            pool_size: Connection pool size
        """
        self.redis_url = redis_url or settings.REDIS_URL
        self.key_prefix = key_prefix
        self.default_ttl = default_ttl
        self.pool_size = pool_size

        self._redis: Optional[Redis] = None
        self._pool: Optional[ConnectionPool] = None
        self._fallback_cache = InMemoryCache()
        self._using_redis = False
        self._stats = CacheStatistics()

        # Initialize Redis connection
        if self.redis_url:
            self._initialize_redis()
        else:
            logger.warning(
                "redis_not_configured",
                message="Redis URL not provided, using in-memory cache only"
            )

    def _initialize_redis(self) -> None:
        """Initialize Redis connection pool."""
        try:
            self._pool = ConnectionPool.from_url(
                self.redis_url,
                max_connections=self.pool_size,
                decode_responses=True,
                encoding="utf-8"
            )
            self._redis = Redis(connection_pool=self._pool)
            self._using_redis = True
            logger.info(
                "redis_cache_initialized",
                redis_url=self._mask_url(self.redis_url),
                pool_size=self.pool_size,
                key_prefix=self.key_prefix,
                default_ttl=self.default_ttl
            )
        except Exception as e:
            logger.error(
                "redis_initialization_failed",
                error=str(e),
                fallback="in-memory cache"
            )
            self._using_redis = False

    @staticmethod
    def _mask_url(url: str) -> str:
        """Mask sensitive parts of Redis URL."""
        if not url:
            return ""
        # Mask password in URL
        if "@" in url:
            parts = url.split("@")
            if ":" in parts[0]:
                auth_parts = parts[0].split(":")
                masked_auth = f"{auth_parts[0]}:****"
                return f"{masked_auth}@{parts[1]}"
        return url

    def _make_key(self, key: str) -> str:
        """Create prefixed cache key."""
        return f"{self.key_prefix}:{key}"

    async def _check_redis_health(self) -> bool:
        """Check if Redis connection is healthy."""
        if not self._redis:
            return False

        try:
            await self._redis.ping()
            return True
        except (RedisError, RedisConnectionError) as e:
            logger.warning("redis_health_check_failed", error=str(e))
            return False

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key (will be prefixed automatically)

        Returns:
            Cached value (deserialized from JSON) or None if not found
        """
        prefixed_key = self._make_key(key)

        # Try Redis first
        if self._using_redis and self._redis:
            try:
                value = await self._redis.get(prefixed_key)
                if value is not None:
                    self._stats.hits += 1
                    logger.debug("cache_hit", key=key, backend="redis")
                    return self._deserialize(value)
                else:
                    self._stats.misses += 1
                    logger.debug("cache_miss", key=key, backend="redis")
                    return None
            except (RedisError, RedisConnectionError) as e:
                self._stats.errors += 1
                logger.warning(
                    "redis_get_failed",
                    key=key,
                    error=str(e),
                    fallback="in-memory"
                )
                # Fall through to in-memory cache

        # Fallback to in-memory cache
        value = await self._fallback_cache.get(prefixed_key)
        if value is not None:
            self._stats.hits += 1
            logger.debug("cache_hit", key=key, backend="memory")
            return self._deserialize(value)
        else:
            self._stats.misses += 1
            logger.debug("cache_miss", key=key, backend="memory")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key (will be prefixed automatically)
            value: Value to cache (will be JSON-serialized)
            ttl: Time-to-live in seconds (defaults to default_ttl)

        Returns:
            True if successful, False otherwise
        """
        prefixed_key = self._make_key(key)
        ttl = ttl if ttl is not None else self.default_ttl
        serialized = self._serialize(value)

        # Try Redis first
        if self._using_redis and self._redis:
            try:
                await self._redis.setex(prefixed_key, ttl, serialized)
                self._stats.sets += 1
                logger.debug("cache_set", key=key, ttl=ttl, backend="redis")
                # Also set in fallback cache for redundancy
                await self._fallback_cache.set(prefixed_key, serialized, ttl)
                return True
            except (RedisError, RedisConnectionError) as e:
                self._stats.errors += 1
                logger.warning(
                    "redis_set_failed",
                    key=key,
                    error=str(e),
                    fallback="in-memory"
                )
                # Fall through to in-memory cache

        # Fallback to in-memory cache
        success = await self._fallback_cache.set(prefixed_key, serialized, ttl)
        if success:
            self._stats.sets += 1
            logger.debug("cache_set", key=key, ttl=ttl, backend="memory")
        return success

    async def delete(self, key: str) -> bool:
        """
        Delete key from cache.

        Args:
            key: Cache key (will be prefixed automatically)

        Returns:
            True if key was deleted, False if not found
        """
        prefixed_key = self._make_key(key)
        deleted = False

        # Try Redis first
        if self._using_redis and self._redis:
            try:
                result = await self._redis.delete(prefixed_key)
                deleted = result > 0
                self._stats.deletes += 1
                logger.debug("cache_delete", key=key, backend="redis")
            except (RedisError, RedisConnectionError) as e:
                self._stats.errors += 1
                logger.warning(
                    "redis_delete_failed",
                    key=key,
                    error=str(e),
                    fallback="in-memory"
                )

        # Also delete from fallback cache
        fallback_deleted = await self._fallback_cache.delete(prefixed_key)
        if fallback_deleted:
            self._stats.deletes += 1
            logger.debug("cache_delete", key=key, backend="memory")

        return deleted or fallback_deleted

    async def clear(self) -> int:
        """
        Clear all cache entries with this prefix.

        Returns:
            Number of keys cleared
        """
        count = 0

        # Clear Redis
        if self._using_redis and self._redis:
            try:
                pattern = f"{self.key_prefix}:*"
                keys = []
                async for key in self._redis.scan_iter(match=pattern):
                    keys.append(key)

                if keys:
                    count += await self._redis.delete(*keys)

                logger.info("redis_cache_cleared", keys_cleared=count)
            except (RedisError, RedisConnectionError) as e:
                self._stats.errors += 1
                logger.warning("redis_clear_failed", error=str(e))

        # Clear fallback cache
        fallback_count = await self._fallback_cache.clear()
        logger.info("memory_cache_cleared", keys_cleared=fallback_count)

        return count + fallback_count

    def _serialize(self, value: Any) -> str:
        """Serialize value to JSON string."""
        try:
            if isinstance(value, str):
                return value
            return json.dumps(value)
        except (TypeError, ValueError) as e:
            logger.error("serialization_failed", error=str(e), value_type=type(value).__name__)
            return str(value)

    def _deserialize(self, value: str) -> Any:
        """Deserialize JSON string to Python object."""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # Return as-is if not valid JSON
            return value

    @property
    def is_redis_available(self) -> bool:
        """Check if Redis backend is available."""
        return self._using_redis and self._redis is not None

    def get_statistics(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        stats = self._stats.to_dict()
        stats["backend"] = "redis" if self.is_redis_available else "memory"
        stats["redis_available"] = self.is_redis_available
        stats["cache_size"] = self._fallback_cache.size()
        return stats

    def reset_statistics(self) -> None:
        """Reset cache statistics."""
        self._stats = CacheStatistics()
        logger.info("cache_statistics_reset")

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on cache backends.

        Returns:
            Health status information
        """
        redis_healthy = await self._check_redis_health()

        return {
            "redis": {
                "available": self.is_redis_available,
                "healthy": redis_healthy,
                "url": self._mask_url(self.redis_url) if self.redis_url else None
            },
            "fallback": {
                "available": True,
                "size": self._fallback_cache.size()
            },
            "statistics": self.get_statistics()
        }

    async def close(self) -> None:
        """Close Redis connection and cleanup resources."""
        if self._redis:
            await self._redis.close()
            logger.info("redis_connection_closed")

        if self._pool:
            await self._pool.disconnect()
            logger.info("redis_pool_disconnected")


# Global cache instance
_cache_service: Optional[RedisCache] = None


def get_cache_service() -> RedisCache:
    """
    Get or create the global cache service instance.

    This function is used as a FastAPI dependency.

    Returns:
        RedisCache instance
    """
    global _cache_service
    if _cache_service is None:
        _cache_service = RedisCache(
            redis_url=settings.REDIS_URL,
            key_prefix=settings.REDIS_CACHE_PREFIX,
            default_ttl=settings.REDIS_CACHE_TTL,
            pool_size=settings.REDIS_POOL_SIZE
        )
    return _cache_service


async def shutdown_cache_service() -> None:
    """
    Cleanup function to be called on application shutdown.
    """
    global _cache_service
    if _cache_service:
        await _cache_service.close()
        logger.info("cache_service_shutdown")
