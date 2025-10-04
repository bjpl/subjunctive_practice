# Operational Runbook

Day-to-day operational procedures, monitoring, incident response, and troubleshooting for the Spanish Subjunctive Practice Application.

## Table of Contents

1. [Daily Operations](#daily-operations)
2. [Monitoring & Alerting](#monitoring--alerting)
3. [Incident Response](#incident-response)
4. [Common Issues & Solutions](#common-issues--solutions)
5. [Performance Tuning](#performance-tuning)
6. [Backup & Restore](#backup--restore)
7. [Scaling Procedures](#scaling-procedures)

---

## Daily Operations

### Morning Health Check (9 AM)

```bash
#!/bin/bash
# Daily health check script

echo "========================================="
echo "Daily Health Check - $(date)"
echo "========================================="

# 1. Check application health
echo -e "\n1. Application Health:"
curl -s https://api.subjunctivepractice.com/health | jq .

# 2. Check database connections
echo -e "\n2. Database Status:"
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# 3. Check Redis
echo -e "\n3. Redis Status:"
redis-cli INFO | grep -E "used_memory_human|connected_clients|ops_per_sec"

# 4. Check disk space
echo -e "\n4. Disk Space:"
df -h | grep -E "/$|/var"

# 5. Check recent errors
echo -e "\n5. Recent Errors (last hour):"
journalctl -u subjunctive-backend --since "1 hour ago" | grep -i error | wc -l

# 6. Check SSL certificate expiry
echo -e "\n6. SSL Certificate:"
echo | openssl s_client -servername api.subjunctivepractice.com \
  -connect api.subjunctivepractice.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# 7. Check backup status
echo -e "\n7. Last Backup:"
ls -lh /backups/subjunctive/ | head -5

echo -e "\n========================================="
```

### Weekly Tasks

**Monday**
- Review error logs from previous week
- Check database performance metrics
- Review user feedback and support tickets
- Plan maintenance windows

**Wednesday**
- Review and update dependencies
- Check for security advisories
- Database index maintenance
- Review scaling metrics

**Friday**
- Review weekly statistics
- Check backup integrity
- Update documentation
- Deploy non-critical updates

### Monthly Tasks

**First Monday**
- Review monthly metrics and KPIs
- Database vacuum and analyze
- Security audit
- Dependency updates
- Cost optimization review

**Third Monday**
- Disaster recovery test
- Load testing
- Certificate renewal check
- Review and update runbooks

---

## Monitoring & Alerting

### Key Metrics to Monitor

#### Application Metrics

```yaml
Response Time:
  Warning: > 200ms (p95)
  Critical: > 500ms (p95)
  Action: Check database queries, Redis cache hit rate

Error Rate:
  Warning: > 1%
  Critical: > 5%
  Action: Check logs, review recent deployments

Request Rate:
  Warning: Unexpected spike (> 2x normal)
  Critical: > 10x normal
  Action: Check for DDoS attack, review traffic sources

Active Users:
  Warning: Drop > 30%
  Critical: Drop > 50%
  Action: Check frontend availability, authentication service
```

#### System Metrics

```yaml
CPU Usage:
  Warning: > 70%
  Critical: > 85%
  Action: Scale horizontally, optimize code

Memory Usage:
  Warning: > 80%
  Critical: > 90%
  Action: Check for memory leaks, restart services if needed

Disk Usage:
  Warning: > 80%
  Critical: > 90%
  Action: Clean logs, expand storage, review data retention

Network I/O:
  Warning: Sustained high usage
  Critical: Bandwidth limit approaching
  Action: Check for unusual traffic patterns
```

#### Database Metrics

```yaml
Connection Pool:
  Warning: > 80% used
  Critical: > 95% used
  Action: Increase pool size, check for connection leaks

Query Time:
  Warning: > 100ms (p95)
  Critical: > 500ms (p95)
  Action: Review slow queries, optimize indexes

Replication Lag:
  Warning: > 5 seconds
  Critical: > 30 seconds
  Action: Check replica health, network connectivity

Deadlocks:
  Warning: > 5 per hour
  Critical: > 20 per hour
  Action: Review transaction logic, optimize queries
```

### Monitoring Tools Setup

#### Sentry (Error Tracking)

```python
# backend/core/monitoring.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1,
    integrations=[FastApiIntegration()],
    before_send=filter_sensitive_data
)
```

#### Application Logging

```python
# backend/core/logging_config.py
import logging
import structlog

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("/var/log/subjunctive/app.log"),
        logging.StreamHandler()
    ]
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
```

#### Database Monitoring

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slow queries
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 20;

-- Active connections
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

### Alert Configuration

#### Critical Alerts (Immediate Response)

```yaml
Application Down:
  Condition: Health check fails for 2 minutes
  Notification: PagerDuty, SMS, Email
  Escalation: 5 minutes

Database Down:
  Condition: Connection failures
  Notification: PagerDuty, SMS, Email
  Escalation: Immediate

High Error Rate:
  Condition: > 5% error rate for 5 minutes
  Notification: Slack, Email
  Escalation: 10 minutes

SSL Certificate Expiring:
  Condition: < 7 days until expiry
  Notification: Email
  Escalation: 3 days
```

#### Warning Alerts (Business Hours Response)

```yaml
Slow Response Time:
  Condition: p95 > 200ms for 10 minutes
  Notification: Slack

High CPU:
  Condition: > 70% for 15 minutes
  Notification: Slack

Low Disk Space:
  Condition: < 20% free
  Notification: Email

Backup Failed:
  Condition: Backup job failed
  Notification: Email, Slack
```

---

## Incident Response

### Incident Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| P0 - Critical | Complete service outage | 15 minutes | Database down, app crash |
| P1 - High | Major feature broken | 1 hour | Authentication failing |
| P2 - Medium | Minor feature broken | 4 hours | Exercise type unavailable |
| P3 - Low | Cosmetic issues | Next business day | UI glitch |

### Incident Response Process

```
┌─────────────────┐
│  Alert Fired    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Acknowledge   │  ◄── Within 5 minutes
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Investigate   │  ◄── Gather information
│  - Check logs   │      Review metrics
│  - Review       │      Identify root cause
│    metrics      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Triage       │  ◄── Determine severity
│  - Assess       │      Assign owner
│    impact       │      Notify stakeholders
│  - Prioritize   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Mitigate     │  ◄── Immediate fix
│  - Rollback     │      Hotfix deploy
│  - Failover     │      Workaround
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Resolve      │  ◄── Permanent fix
│  - Deploy fix   │      Verify resolution
│  - Verify       │      Monitor
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Post-Mortem    │  ◄── Within 48 hours
│  - Document     │      Action items
│  - Learn        │      Update runbook
└─────────────────┘
```

### On-Call Procedures

#### On-Call Responsibilities

1. **Acknowledge** alerts within 5 minutes
2. **Triage** incident within 15 minutes
3. **Communicate** status updates every 30 minutes
4. **Escalate** if cannot resolve within SLA
5. **Document** all actions taken

#### On-Call Rotation

```
Week 1: Engineer A (Primary), Engineer B (Secondary)
Week 2: Engineer B (Primary), Engineer C (Secondary)
Week 3: Engineer C (Primary), Engineer A (Secondary)
```

#### Escalation Path

```
Level 1: On-call Engineer (0-30 min)
   ↓
Level 2: Team Lead (30-60 min)
   ↓
Level 3: Engineering Manager (60-120 min)
   ↓
Level 4: CTO (> 120 min or critical business impact)
```

---

## Common Issues & Solutions

### Issue: High Database CPU

**Symptoms:**
- Slow query responses
- Timeout errors
- High database CPU usage

**Investigation:**
```sql
-- Find slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY total_time DESC
LIMIT 10;

-- Check for locks
SELECT * FROM pg_locks WHERE NOT granted;

-- Check active queries
SELECT pid, query_start, state, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;
```

**Solutions:**
1. **Immediate:** Kill long-running queries
```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active' AND query_start < now() - interval '5 minutes';
```

2. **Short-term:** Add missing indexes
```sql
-- Identify missing indexes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY n_distinct DESC;
```

3. **Long-term:** Optimize queries, add read replicas

### Issue: Redis Memory Full

**Symptoms:**
- OOM errors
- Eviction warnings
- Cache misses increasing

**Investigation:**
```bash
# Check memory usage
redis-cli INFO memory

# Check key distribution
redis-cli --bigkeys

# Monitor evictions
redis-cli INFO stats | grep evicted
```

**Solutions:**
1. **Immediate:** Increase maxmemory or flush non-critical keys
```bash
redis-cli CONFIG SET maxmemory 512mb
```

2. **Short-term:** Review TTL settings
```bash
# Find keys with no TTL
redis-cli KEYS * | while read key; do
    ttl=$(redis-cli TTL "$key")
    if [ "$ttl" -eq -1 ]; then
        echo "$key has no TTL"
    fi
done
```

3. **Long-term:** Implement better eviction policy, scale Redis

### Issue: Application Slow Response

**Symptoms:**
- High response times
- Timeout errors
- User complaints

**Investigation:**
```bash
# Check application logs
tail -f /var/log/subjunctive/app.log | grep -i "slow\|timeout"

# Check CPU and memory
htop

# Check network
netstat -an | grep ESTABLISHED | wc -l

# Check database connections
psql -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"
```

**Solutions:**
1. **Immediate:** Restart application if necessary
```bash
sudo systemctl restart subjunctive-backend
```

2. **Short-term:** Enable caching, optimize queries

3. **Long-term:** Scale horizontally, optimize code

### Issue: SSL Certificate Expiry

**Symptoms:**
- Certificate warnings in browser
- API calls failing with SSL errors

**Investigation:**
```bash
# Check certificate expiry
echo | openssl s_client -servername api.subjunctivepractice.com \
  -connect api.subjunctivepractice.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

**Solutions:**
1. **Immediate:** Renew certificate
```bash
# Let's Encrypt renewal
sudo certbot renew --force-renewal
sudo systemctl reload nginx
```

2. **Prevention:** Set up auto-renewal
```bash
# Add to crontab
0 0 * * 0 certbot renew --quiet && systemctl reload nginx
```

### Issue: Disk Space Full

**Symptoms:**
- Write errors
- Application crashes
- Backup failures

**Investigation:**
```bash
# Check disk usage
df -h

# Find large files
du -ah /var/log | sort -rh | head -20
du -ah /var/lib | sort -rh | head -20

# Check log sizes
ls -lh /var/log/subjunctive/
```

**Solutions:**
1. **Immediate:** Clean up logs
```bash
# Compress old logs
find /var/log/subjunctive -name "*.log" -mtime +7 -exec gzip {} \;

# Delete old compressed logs
find /var/log/subjunctive -name "*.gz" -mtime +30 -delete

# Truncate current log if too large
> /var/log/subjunctive/app.log
```

2. **Short-term:** Set up log rotation
```bash
# /etc/logrotate.d/subjunctive
/var/log/subjunctive/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 appuser appuser
    sharedscripts
    postrotate
        systemctl reload subjunctive-backend
    endscript
}
```

3. **Long-term:** Expand disk, implement log shipping

---

## Performance Tuning

### Database Optimization

#### Connection Pooling

```python
# backend/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

#### Query Optimization

```python
# Use indexes
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    type = Column(String, index=True)  # Index frequently queried
    difficulty = Column(Integer, index=True)
    created_at = Column(DateTime, index=True)

    __table_args__ = (
        Index('idx_type_difficulty', 'type', 'difficulty'),  # Composite index
    )
```

#### Batch Operations

```python
# Instead of N+1 queries
for exercise in exercises:
    user_progress = session.query(UserProgress).filter_by(
        user_id=user_id,
        exercise_id=exercise.id
    ).first()

# Use join and load in one query
exercises_with_progress = session.query(Exercise).join(
    UserProgress,
    and_(
        UserProgress.exercise_id == Exercise.id,
        UserProgress.user_id == user_id
    )
).all()
```

### Redis Optimization

#### Caching Strategy

```python
import json
from datetime import timedelta

class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_exercises(self, exercise_type: str, difficulty: int):
        cache_key = f"exercises:{exercise_type}:{difficulty}"

        # Try cache first
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Fetch from database
        exercises = fetch_from_db(exercise_type, difficulty)

        # Store in cache with TTL
        self.redis.setex(
            cache_key,
            timedelta(hours=1),
            json.dumps(exercises)
        )

        return exercises
```

### Application Optimization

#### Async Operations

```python
# Use async for I/O operations
from fastapi import FastAPI
import asyncio

@app.get("/exercises")
async def get_exercises():
    # Parallel database queries
    exercises, user_progress = await asyncio.gather(
        fetch_exercises(),
        fetch_user_progress()
    )

    return combine_results(exercises, user_progress)
```

#### Response Compression

```python
# Enable gzip compression
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## Backup & Restore

### Automated Backup Script

```bash
#!/bin/bash
# /usr/local/bin/backup-database.sh

set -e

# Configuration
BACKUP_DIR="/backups/subjunctive"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
S3_BUCKET="s3://subjunctive-backups"

# Database credentials (from env)
DB_HOST="${POSTGRES_HOST}"
DB_USER="${POSTGRES_USER}"
DB_NAME="${POSTGRES_DB}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
echo "$(date): Starting database backup..."
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
    -F c -b -v -f "$BACKUP_DIR/backup_$DATE.dump"

# Compress backup
gzip "$BACKUP_DIR/backup_$DATE.dump"

# Upload to S3
if [ -n "$S3_BUCKET" ]; then
    echo "$(date): Uploading to S3..."
    aws s3 cp "$BACKUP_DIR/backup_$DATE.dump.gz" \
        "$S3_BUCKET/database/backup_$DATE.dump.gz"
fi

# Cleanup old backups
find "$BACKUP_DIR" -name "*.dump.gz" -mtime +$RETENTION_DAYS -delete

# Verify backup
if [ -f "$BACKUP_DIR/backup_$DATE.dump.gz" ]; then
    echo "$(date): Backup completed successfully"
    SIZE=$(ls -lh "$BACKUP_DIR/backup_$DATE.dump.gz" | awk '{print $5}')
    echo "Backup size: $SIZE"
else
    echo "$(date): ERROR - Backup failed!"
    exit 1
fi
```

### Restore Procedure

```bash
#!/bin/bash
# Restore from backup

# Variables
BACKUP_FILE="$1"
DB_NAME="subjunctive_practice"

# Validation
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Confirm
read -p "This will OVERWRITE the database. Continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Stop application
echo "Stopping application..."
sudo systemctl stop subjunctive-backend

# Drop connections
echo "Dropping active connections..."
psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB_NAME';"

# Restore
echo "Restoring database..."
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c "$BACKUP_FILE" | pg_restore -d "$DB_NAME" -c -v
else
    pg_restore -d "$DB_NAME" -c -v "$BACKUP_FILE"
fi

# Start application
echo "Starting application..."
sudo systemctl start subjunctive-backend

# Verify
sleep 5
curl -f http://localhost:8000/health || echo "WARNING: Health check failed"

echo "Restore completed"
```

---

## Scaling Procedures

### Horizontal Scaling (Add Application Server)

```bash
# 1. Provision new server
# 2. Install application
git clone https://github.com/yourorg/subjunctive-practice.git
cd subjunctive-practice/backend

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with production settings

# 5. Start application
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000

# 6. Add to load balancer
# Update load balancer configuration to include new server

# 7. Verify
curl http://new-server-ip:8000/health

# 8. Monitor
# Watch logs and metrics for any issues
```

### Vertical Scaling (Increase Resources)

```bash
# 1. Schedule maintenance window
# 2. Take server out of load balancer rotation

# 3. Increase resources (depends on hosting platform)
# Railway: Upgrade plan in dashboard
# AWS: Resize EC2 instance
# Docker: Update resource limits

# 4. Restart application
sudo systemctl restart subjunctive-backend

# 5. Verify
curl http://localhost:8000/health

# 6. Monitor performance metrics

# 7. Add back to load balancer
```

### Database Scaling

#### Add Read Replica

```bash
# 1. Create replica (platform-specific)
# Railway: Add replica in dashboard
# AWS RDS: Create read replica
# Manual: Set up streaming replication

# 2. Update application configuration
# Add read replica connection string

# 3. Implement read/write splitting
```

```python
# backend/core/database.py
from sqlalchemy import create_engine

# Write operations
write_engine = create_engine(PRIMARY_DB_URL)

# Read operations
read_engine = create_engine(REPLICA_DB_URL)

def get_db_session(readonly=False):
    engine = read_engine if readonly else write_engine
    return Session(bind=engine)
```

---

## Maintenance Windows

### Scheduled Maintenance Checklist

**1 Week Before:**
- [ ] Announce maintenance window
- [ ] Review change plan
- [ ] Prepare rollback plan
- [ ] Test changes in staging

**1 Day Before:**
- [ ] Send reminder notification
- [ ] Backup database
- [ ] Prepare monitoring dashboards
- [ ] Brief team on roles

**During Maintenance:**
- [ ] Enable maintenance mode
- [ ] Stop application
- [ ] Perform changes
- [ ] Test functionality
- [ ] Disable maintenance mode
- [ ] Monitor for issues

**After Maintenance:**
- [ ] Send completion notification
- [ ] Document changes made
- [ ] Review metrics
- [ ] Post-mortem if issues occurred
