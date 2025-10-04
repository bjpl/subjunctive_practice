# Scaling Guide

Comprehensive guide to scaling the Spanish Subjunctive Practice Application to handle growth in users, traffic, and data.

## Table of Contents

1. [Scaling Overview](#scaling-overview)
2. [Horizontal vs Vertical Scaling](#horizontal-vs-vertical-scaling)
3. [Application Scaling](#application-scaling)
4. [Database Scaling](#database-scaling)
5. [Caching Strategy](#caching-strategy)
6. [Load Balancing](#load-balancing)
7. [Performance Optimization](#performance-optimization)
8. [Capacity Planning](#capacity-planning)

---

## Scaling Overview

### Current Capacity (Single Instance)

```yaml
Application Server:
  CPU: 1 core
  Memory: 512 MB
  Capacity: ~100 concurrent users
  Throughput: ~50 req/sec

Database:
  Type: PostgreSQL
  Storage: 10 GB
  Connections: 100
  Capacity: ~500 concurrent connections

Redis Cache:
  Memory: 256 MB
  Capacity: ~1M keys
```

### Growth Targets

| Metric | Current | 6 Months | 1 Year | 2 Years |
|--------|---------|----------|--------|---------|
| Users | 1,000 | 10,000 | 50,000 | 200,000 |
| Concurrent Users | 50 | 500 | 2,500 | 10,000 |
| Requests/sec | 10 | 100 | 500 | 2,000 |
| Database Size | 1 GB | 10 GB | 50 GB | 200 GB |

### Scaling Triggers

**Scale Up When:**
- CPU usage > 70% sustained for 10 minutes
- Memory usage > 80%
- Response time p95 > 200ms
- Error rate > 1%
- Database connections > 80%

**Scale Down When:**
- CPU usage < 30% for 1 hour
- Memory usage < 40%
- Cost optimization opportunity

---

## Horizontal vs Vertical Scaling

### Vertical Scaling (Scale Up)

**Advantages:**
- Simpler implementation
- No code changes required
- Better for database

**Disadvantages:**
- Limited by hardware
- Downtime required
- Single point of failure

**When to Use:**
- Database scaling
- Quick fix for immediate capacity
- Stateful services

**Implementation:**
```bash
# Railway - Upgrade plan
railway upgrade --plan pro

# AWS - Resize instance
aws ec2 modify-instance-attribute \
    --instance-id i-1234567890abcdef0 \
    --instance-type t3.large

# Requires restart
```

### Horizontal Scaling (Scale Out)

**Advantages:**
- Nearly unlimited scaling
- High availability
- No downtime deployment

**Disadvantages:**
- More complex
- Requires stateless design
- Increased operational overhead

**When to Use:**
- Application servers
- API services
- Read-heavy workloads

**Implementation:**
```bash
# Add application servers to load balancer
# See Load Balancing section below
```

---

## Application Scaling

### Stateless Application Design

**Requirements:**
- No local session storage (use Redis)
- No local file storage (use S3/object storage)
- Database connection pooling
- Idempotent operations

**Configuration:**
```python
# backend/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Use environment-based config, not local files
    environment: str = "production"

    # External session storage
    redis_url: str

    # External file storage
    s3_bucket: str
    s3_region: str

    # Connection pooling
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # No local state
    session_type: str = "redis"  # Not "filesystem"
```

### Auto-Scaling Configuration

#### Railway Auto-Scaling

```yaml
# railway.toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on-failure"
restartPolicyMaxRetries = 10

[scaling]
minInstances = 2  # Always at least 2 for HA
maxInstances = 10
cpuThreshold = 70
memoryThreshold = 80
```

#### AWS Auto Scaling

```yaml
# autoscaling.yml
AutoScalingGroup:
  MinSize: 2
  MaxSize: 10
  DesiredCapacity: 2
  HealthCheckType: ELB
  HealthCheckGracePeriod: 300

ScalingPolicies:
  ScaleUpPolicy:
    MetricName: CPUUtilization
    TargetValue: 70
    ScaleUpCooldown: 300

  ScaleDownPolicy:
    MetricName: CPUUtilization
    TargetValue: 30
    ScaleDownCooldown: 600
```

### Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Basic load test
ab -n 10000 -c 100 https://api.subjunctivepractice.com/health

# More realistic test with authorization
cat > post_data.json << EOF
{"email": "test@example.com", "password": "test123"}
EOF

ab -n 1000 -c 50 -p post_data.json \
   -T application/json \
   https://api.subjunctivepractice.com/api/v1/auth/login

# Advanced load testing with K6
npm install -g k6

cat > load-test.js << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 200 },  // Ramp to 200 users
    { duration: '5m', target: 200 },  // Stay at 200 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // < 1% errors
  },
};

export default function () {
  const res = http.get('https://api.subjunctivepractice.com/api/v1/exercises');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
EOF

k6 run load-test.js
```

---

## Database Scaling

### Read Replicas

```
┌──────────────┐
│   Primary    │  ← Write operations
│  (Master)    │
└──────┬───────┘
       │ Replication
       ├─────────────┬─────────────┐
       │             │             │
┌──────▼───────┐ ┌──▼─────────┐ ┌─▼──────────┐
│  Replica 1   │ │ Replica 2  │ │ Replica 3  │
│   (Read)     │ │  (Read)    │ │  (Read)    │
└──────────────┘ └────────────┘ └────────────┘
```

#### Setup Read Replicas

**Railway:**
```bash
# Add read replica via dashboard
railway add postgres-replica --primary subjunctive-postgres
```

**AWS RDS:**
```bash
aws rds create-db-instance-read-replica \
    --db-instance-identifier subjunctive-replica-1 \
    --source-db-instance-identifier subjunctive-primary \
    --availability-zone us-east-1b
```

#### Application Code for Read/Write Splitting

```python
# backend/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Write database (primary)
write_engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20
)

# Read database (replica)
read_engine = create_engine(
    settings.database_replica_url,
    pool_size=20,  # More connections for reads
    max_overflow=40
)

class Database:
    @staticmethod
    def get_session(readonly: bool = False):
        """Get database session - read or write"""
        engine = read_engine if readonly else write_engine
        return Session(bind=engine)

# Usage
# Read operations
with Database.get_session(readonly=True) as session:
    exercises = session.query(Exercise).all()

# Write operations
with Database.get_session(readonly=False) as session:
    session.add(new_exercise)
    session.commit()
```

### Connection Pooling

```python
# backend/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,

    # Pool size (per instance)
    pool_size=10,           # Keep 10 connections alive
    max_overflow=20,        # Allow 20 additional connections

    # Connection lifecycle
    pool_timeout=30,        # Wait 30s for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connection before using

    # Performance tuning
    echo=False,             # Don't log all SQL
    echo_pool=False,        # Don't log pool events
)

# Calculate total connections needed
# With 3 application servers:
# Total = (pool_size + max_overflow) * num_servers
# Total = (10 + 20) * 3 = 90 connections
# Set PostgreSQL max_connections > 90 (e.g., 150)
```

### Database Partitioning

```sql
-- Partition user_progress table by date
CREATE TABLE user_progress (
    id SERIAL,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    -- other columns
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE user_progress_2024_q1 PARTITION OF user_progress
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE user_progress_2024_q2 PARTITION OF user_progress
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE user_progress_2024_q3 PARTITION OF user_progress
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE user_progress_2024_q4 PARTITION OF user_progress
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Index on partitioned table
CREATE INDEX idx_user_progress_user_id ON user_progress (user_id);
```

### Sharding (Advanced)

```python
# Shard by user_id
def get_shard_for_user(user_id: int) -> str:
    """Determine which database shard to use"""
    shard_count = 4
    shard_id = user_id % shard_count
    return f"shard_{shard_id}"

# Shard configuration
SHARDS = {
    "shard_0": "postgresql://host1:5432/shard_0",
    "shard_1": "postgresql://host2:5432/shard_1",
    "shard_2": "postgresql://host3:5432/shard_2",
    "shard_3": "postgresql://host4:5432/shard_3",
}

def get_db_for_user(user_id: int):
    shard = get_shard_for_user(user_id)
    return create_engine(SHARDS[shard])
```

---

## Caching Strategy

### Multi-Layer Caching

```
┌─────────────────────────────────────────┐
│         Browser Cache (Client)          │  ← 1 year for static assets
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│              CDN Cache                   │  ← 1 hour for pages
│         (CloudFlare/Vercel)              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Application Cache                │  ← In-memory (Python)
│           (LRU Cache)                    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Redis Cache                    │  ← 15min - 24 hours
│    (Distributed, Shared)                 │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Database Query Cache              │  ← PostgreSQL cache
└─────────────────────────────────────────┘
```

### Redis Caching Implementation

```python
# backend/services/cache.py
import json
import redis
from datetime import timedelta
from functools import wraps

class CacheService:
    def __init__(self):
        self.redis = redis.Redis.from_url(settings.redis_url)

    def get(self, key: str):
        """Get cached value"""
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: any, ttl: int = 3600):
        """Set cached value with TTL"""
        self.redis.setex(
            key,
            timedelta(seconds=ttl),
            json.dumps(value)
        )

    def delete(self, key: str):
        """Delete cached value"""
        self.redis.delete(key)

    def cache_decorator(self, ttl: int = 3600):
        """Decorator for caching function results"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

                # Check cache
                cached = self.get(cache_key)
                if cached:
                    return cached

                # Execute function
                result = func(*args, **kwargs)

                # Cache result
                self.set(cache_key, result, ttl)

                return result
            return wrapper
        return decorator

# Usage
cache = CacheService()

@cache.cache_decorator(ttl=3600)
def get_exercises_by_type(exercise_type: str):
    # This will be cached for 1 hour
    return db.query(Exercise).filter_by(type=exercise_type).all()
```

### Cache Invalidation

```python
# backend/services/cache.py

class CacheInvalidation:
    @staticmethod
    def invalidate_user_cache(user_id: int):
        """Invalidate all cache entries for a user"""
        patterns = [
            f"user:{user_id}:*",
            f"progress:{user_id}:*",
            f"stats:{user_id}:*"
        ]
        for pattern in patterns:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)

    @staticmethod
    def invalidate_exercise_cache(exercise_id: int):
        """Invalidate exercise cache"""
        redis_client.delete(f"exercise:{exercise_id}")
        # Also invalidate list caches
        redis_client.delete("exercises:all")

# Event-based invalidation
@app.post("/api/v1/users/{user_id}/progress")
async def update_progress(user_id: int, data: dict):
    # Update database
    result = update_user_progress(user_id, data)

    # Invalidate cache
    CacheInvalidation.invalidate_user_cache(user_id)

    return result
```

---

## Load Balancing

### Load Balancer Setup

```nginx
# nginx.conf - Load Balancer Configuration

upstream backend_servers {
    # Load balancing method
    least_conn;  # Route to server with fewest connections
    # Other options: round_robin, ip_hash

    # Application servers
    server app1.subjunctivepractice.com:8000 weight=3 max_fails=3 fail_timeout=30s;
    server app2.subjunctivepractice.com:8000 weight=3 max_fails=3 fail_timeout=30s;
    server app3.subjunctivepractice.com:8000 weight=2 max_fails=3 fail_timeout=30s;  # Smaller instance

    # Health check
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name api.subjunctivepractice.com;

    # SSL configuration
    ssl_certificate /etc/ssl/certs/api.subjunctivepractice.com.crt;
    ssl_certificate_key /etc/ssl/private/api.subjunctivepractice.com.key;

    # Proxy to backend
    location / {
        proxy_pass http://backend_servers;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;

        # Health check
        proxy_next_upstream error timeout http_500 http_502 http_503;
    }

    # Health check endpoint (doesn't go through proxy)
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
```

---

## Performance Optimization

### Database Query Optimization

```python
# BEFORE: N+1 Query Problem
def get_user_dashboard_slow(user_id: int):
    user = db.query(User).filter_by(id=user_id).first()

    # N+1: One query per exercise
    exercises = []
    for exercise_id in user.completed_exercise_ids:
        exercise = db.query(Exercise).filter_by(id=exercise_id).first()
        exercises.append(exercise)

    return {"user": user, "exercises": exercises}

# AFTER: Optimized with join
def get_user_dashboard_fast(user_id: int):
    result = db.query(User).filter_by(id=user_id)\
        .options(
            joinedload(User.completed_exercises)
        )\
        .first()

    return {"user": result, "exercises": result.completed_exercises}
```

### API Response Compression

```python
# backend/main.py
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Database Connection Optimization

```sql
-- Optimize PostgreSQL configuration
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '8MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET effective_io_concurrency = 200;
ALTER SYSTEM SET max_connections = 200;

SELECT pg_reload_conf();
```

---

## Capacity Planning

### Monitoring Growth Metrics

```python
# Script to track growth metrics
import psycopg2
from datetime import datetime

def collect_metrics():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    metrics = {
        "timestamp": datetime.now(),
        "total_users": 0,
        "active_users_today": 0,
        "total_exercises": 0,
        "requests_per_minute": 0,
        "database_size_gb": 0,
        "avg_response_time_ms": 0
    }

    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    metrics["total_users"] = cur.fetchone()[0]

    # Active users today
    cur.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM user_sessions
        WHERE created_at >= CURRENT_DATE
    """)
    metrics["active_users_today"] = cur.fetchone()[0]

    # Database size
    cur.execute("""
        SELECT pg_size_pretty(pg_database_size('subjunctive_practice'))
    """)
    metrics["database_size_gb"] = cur.fetchone()[0]

    # Save metrics
    save_metrics(metrics)

    return metrics
```

### Capacity Forecasting

```python
# Simple linear forecast
def forecast_capacity(current_users, growth_rate, months):
    """
    Forecast future capacity needs

    Args:
        current_users: Current user count
        growth_rate: Monthly growth rate (e.g., 0.2 for 20%)
        months: Months to forecast

    Returns:
        dict with forecasted metrics
    """
    forecasts = []

    for month in range(1, months + 1):
        users = current_users * ((1 + growth_rate) ** month)

        # Estimate resources needed
        # Assuming 100 users per server instance
        servers = math.ceil(users / 100)

        # Assuming 100 MB per 1000 users
        db_size_gb = (users / 1000) * 0.1

        forecasts.append({
            "month": month,
            "users": int(users),
            "servers_needed": servers,
            "db_size_gb": round(db_size_gb, 2),
            "estimated_cost": servers * 10 + db_size_gb * 5  # Rough estimate
        })

    return forecasts

# Example
forecasts = forecast_capacity(
    current_users=1000,
    growth_rate=0.20,  # 20% monthly growth
    months=12
)

for f in forecasts:
    print(f"Month {f['month']}: {f['users']} users, "
          f"{f['servers_needed']} servers, "
          f"{f['db_size_gb']} GB DB, "
          f"${f['estimated_cost']}/month")
```

---

## Scaling Checklist

### Before Scaling

- [ ] Identify bottleneck (CPU, memory, database, network)
- [ ] Review monitoring dashboards
- [ ] Check error logs
- [ ] Verify current resource utilization
- [ ] Estimate cost impact
- [ ] Plan rollback strategy

### During Scaling

- [ ] Schedule during low-traffic period
- [ ] Enable monitoring
- [ ] Make incremental changes
- [ ] Test after each change
- [ ] Document changes made

### After Scaling

- [ ] Verify performance improvement
- [ ] Monitor for issues (24 hours)
- [ ] Update documentation
- [ ] Review costs
- [ ] Plan next scaling threshold

---

This scaling guide should be reviewed quarterly and updated based on actual growth patterns and performance data.
