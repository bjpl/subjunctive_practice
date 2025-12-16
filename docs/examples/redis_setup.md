# Redis Caching Setup Guide

## Overview

The application now uses Redis for distributed caching with automatic fallback to in-memory caching if Redis is unavailable. This improves performance and reduces AI API costs.

## Features

- **Redis Primary Cache**: Fast, distributed caching with TTL support
- **In-Memory Fallback**: Automatic fallback if Redis is unavailable
- **Statistics Tracking**: Monitor cache hits, misses, and performance
- **Connection Pooling**: Efficient Redis connection management
- **JSON Serialization**: Automatic handling of complex objects
- **Key Namespacing**: Prevent key collisions with prefixes

## Installation

### Local Development (Docker)

1. **Start Redis with Docker:**
   ```bash
   docker run -d \
     --name redis-cache \
     -p 6379:6379 \
     redis:7-alpine
   ```

2. **Verify Redis is running:**
   ```bash
   docker exec -it redis-cache redis-cli ping
   # Should return: PONG
   ```

3. **Configure environment:**
   ```bash
   echo "REDIS_URL=redis://localhost:6379/0" >> .env
   ```

### Local Development (Native)

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

**Windows:**
```bash
# Use WSL2 or Docker (recommended)
# Or download from: https://github.com/microsoftarchive/redis/releases
```

### Production (Redis Cloud)

1. **Sign up for Redis Cloud:**
   - Visit: https://redis.com/try-free/
   - Create a free database (30MB free tier)

2. **Get connection URL:**
   - Navigate to database details
   - Copy the connection string

3. **Configure environment:**
   ```bash
   REDIS_URL=redis://default:password@host:port/db
   ```

### Production (AWS ElastiCache)

1. **Create ElastiCache cluster:**
   ```bash
   aws elasticache create-cache-cluster \
     --cache-cluster-id subjunctive-cache \
     --engine redis \
     --cache-node-type cache.t3.micro \
     --num-cache-nodes 1
   ```

2. **Get endpoint:**
   ```bash
   aws elasticache describe-cache-clusters \
     --cache-cluster-id subjunctive-cache \
     --show-cache-node-info
   ```

3. **Configure environment:**
   ```bash
   REDIS_URL=redis://endpoint:6379/0
   ```

## Configuration

### Environment Variables

Add to your `.env` file:

```env
# Required: Redis connection URL
REDIS_URL=redis://localhost:6379/0

# Optional: Cache TTL in seconds (default: 3600)
REDIS_CACHE_TTL=3600

# Optional: Key prefix for namespacing (default: "subjunctive")
REDIS_CACHE_PREFIX=subjunctive

# Optional: Connection pool size (default: 10)
REDIS_POOL_SIZE=10
```

### Different TTLs for Different Cache Types

The AI service uses different TTLs for different types of responses:

- **Feedback**: 1 hour (3600s) - Changes with user answers
- **Hints**: 30 minutes (1800s) - Exercise-specific
- **Insights**: 2 hours (7200s) - Based on user stats

## Testing

### Test Redis Connection

```python
# backend/test_redis.py
import asyncio
from services.cache_service import get_cache_service

async def test_redis():
    cache = get_cache_service()

    # Set a value
    await cache.set("test_key", "Hello Redis!")

    # Get the value
    value = await cache.get("test_key")
    print(f"Retrieved: {value}")

    # Check health
    health = await cache.health_check()
    print(f"Cache health: {health}")

    # Get statistics
    stats = cache.get_statistics()
    print(f"Cache stats: {stats}")

if __name__ == "__main__":
    asyncio.run(test_redis())
```

Run the test:
```bash
cd backend
python test_redis.py
```

### Run Unit Tests

```bash
cd backend
pytest tests/services/test_cache_service.py -v
```

### Check Cache Statistics

The AI service includes cache statistics in health checks:

```bash
curl http://localhost:8000/api/health/ai
```

Response includes:
```json
{
  "status": "healthy",
  "cache": {
    "redis": {
      "available": true,
      "healthy": true
    },
    "fallback": {
      "available": true,
      "size": 0
    }
  },
  "cache_statistics": {
    "hits": 150,
    "misses": 50,
    "hit_rate_percent": 75.0,
    "total_requests": 200
  }
}
```

## Monitoring

### Redis CLI Commands

```bash
# Connect to Redis
redis-cli

# Check memory usage
INFO memory

# List all keys (development only!)
KEYS subjunctive:*

# Get cache entry
GET subjunctive:ai:feedback:hash123

# Check TTL for a key
TTL subjunctive:ai:feedback:hash123

# Get number of keys
DBSIZE

# Monitor real-time commands
MONITOR
```

### Monitor Cache Performance

```python
# Get cache statistics programmatically
from services.ai_service import get_ai_service

service = get_ai_service()
stats = service.get_cache_statistics()

print(f"Hit Rate: {stats['hit_rate_percent']:.1f}%")
print(f"Total Requests: {stats['total_requests']}")
print(f"Cache Backend: {stats['backend']}")
```

## Fallback Behavior

The system automatically falls back to in-memory caching if:

1. **Redis URL not configured** - Uses in-memory from start
2. **Redis connection fails** - Falls back on first error
3. **Redis operations timeout** - Retries in-memory

Fallback is transparent - no code changes needed!

## Performance Optimization

### Recommended Settings

**Development:**
```env
REDIS_CACHE_TTL=1800        # 30 minutes
REDIS_POOL_SIZE=5           # Smaller pool
```

**Production:**
```env
REDIS_CACHE_TTL=7200        # 2 hours
REDIS_POOL_SIZE=20          # Larger pool
```

**High Traffic:**
```env
REDIS_CACHE_TTL=14400       # 4 hours
REDIS_POOL_SIZE=50          # Much larger pool
```

### Cache Warming

Pre-populate cache with common responses:

```python
async def warm_cache():
    service = get_ai_service()

    # Common exercises
    common_contexts = [
        {"verb": "hablar", "tense": "present_subjunctive"},
        {"verb": "ser", "tense": "present_subjunctive"},
        # ... add more
    ]

    for context in common_contexts:
        await service.generate_feedback(
            "answer", "correct", context
        )
```

## Troubleshooting

### Redis Connection Issues

**Error: Connection refused**
```bash
# Check if Redis is running
docker ps | grep redis
# Or
redis-cli ping
```

**Error: Authentication failed**
```bash
# Verify password in REDIS_URL
REDIS_URL=redis://:correct_password@host:port/db
```

**Error: Timeout**
```bash
# Increase pool size or check network
REDIS_POOL_SIZE=20
```

### Memory Issues

**Redis memory full**
```bash
# Check memory usage
redis-cli INFO memory

# Set max memory (in redis.conf)
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Debugging

Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

View cache operations:
```python
import structlog
logger = structlog.get_logger(__name__)

# Logs will show:
# - cache_hit / cache_miss
# - cache_set / cache_delete
# - redis_get_failed (fallback triggered)
```

## Best Practices

1. **Use appropriate TTLs** - Don't cache forever
2. **Monitor hit rates** - Aim for >70% hit rate
3. **Key prefixes** - Use different prefixes per environment
4. **Graceful degradation** - Always have fallback
5. **Regular cleanup** - Clear old entries periodically
6. **Security** - Use Redis passwords in production
7. **Backups** - Redis data is ephemeral, don't store critical data

## Cost Savings

**With Redis caching:**

- 75% cache hit rate = 75% fewer AI API calls
- Average AI call: $0.003 (Claude Sonnet)
- 10,000 requests/day: **$7.50/day savings**
- Monthly: **$225 savings**

**Redis Cloud Free Tier:**
- 30MB storage (enough for ~10,000 cached responses)
- **Cost: $0/month**

**Net monthly savings: $225** 💰

## Next Steps

1. ✅ Configure REDIS_URL in .env
2. ✅ Start Redis server
3. ✅ Run tests to verify
4. ✅ Monitor cache statistics
5. ✅ Adjust TTLs based on usage
6. ✅ Set up Redis in production

## Additional Resources

- [Redis Documentation](https://redis.io/docs/)
- [Redis Python Client](https://redis-py.readthedocs.io/)
- [Redis Cloud](https://redis.com/try-free/)
- [AWS ElastiCache](https://aws.amazon.com/elasticache/)
- [Cache Strategies](https://redis.io/docs/manual/patterns/)
