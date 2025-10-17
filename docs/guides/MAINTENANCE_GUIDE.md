# Maintenance Guide

Comprehensive guide for maintaining the Spanish Subjunctive Practice Application infrastructure, including database maintenance, dependency updates, security patches, performance optimization, and cost management.

## Table of Contents

1. [Database Maintenance](#database-maintenance)
2. [Dependency Updates](#dependency-updates)
3. [Security Patch Management](#security-patch-management)
4. [Performance Optimization](#performance-optimization)
5. [Cost Optimization](#cost-optimization)
6. [System Health Monitoring](#system-health-monitoring)

---

## Database Maintenance

### Regular Maintenance Schedule

| Task | Frequency | Duration | Best Time |
|------|-----------|----------|-----------|
| Vacuum | Daily | 5-10 min | 2 AM UTC |
| Analyze | Daily | 5 min | 2 AM UTC |
| Reindex | Weekly | 15-30 min | Sunday 2 AM |
| Full Vacuum | Monthly | 1-2 hours | First Sunday 2 AM |
| Statistics Update | Weekly | 10 min | Sunday 3 AM |

### Automated Vacuum

```sql
-- Configure autovacuum (PostgreSQL)
ALTER SYSTEM SET autovacuum = on;
ALTER SYSTEM SET autovacuum_max_workers = 3;
ALTER SYSTEM SET autovacuum_naptime = '1min';
ALTER SYSTEM SET autovacuum_vacuum_threshold = 50;
ALTER SYSTEM SET autovacuum_analyze_threshold = 50;
ALTER SYSTEM SET autovacuum_vacuum_scale_factor = 0.2;
ALTER SYSTEM SET autovacuum_analyze_scale_factor = 0.1;

-- Reload configuration
SELECT pg_reload_conf();
```

### Manual Vacuum Procedure

```bash
#!/bin/bash
# vacuum-database.sh

# Configuration
DB_NAME="subjunctive_practice"
LOG_FILE="/var/log/subjunctive/vacuum.log"

echo "$(date): Starting database vacuum..." | tee -a $LOG_FILE

# Vacuum analyze (regular maintenance)
psql -d $DB_NAME -c "VACUUM ANALYZE VERBOSE;" 2>&1 | tee -a $LOG_FILE

# Check table bloat
echo "$(date): Checking table bloat..." | tee -a $LOG_FILE
psql -d $DB_NAME << 'EOF' | tee -a $LOG_FILE
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS external_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
EOF

echo "$(date): Vacuum completed" | tee -a $LOG_FILE
```

### Reindexing

```bash
#!/bin/bash
# reindex-database.sh

DB_NAME="subjunctive_practice"

# Reindex tables one by one to avoid locking entire database
psql -d $DB_NAME << 'EOF'
-- Reindex each table
REINDEX TABLE users;
REINDEX TABLE exercises;
REINDEX TABLE user_progress;
REINDEX TABLE user_sessions;

-- Reindex indexes concurrently (PostgreSQL 12+)
REINDEX INDEX CONCURRENTLY idx_users_email;
REINDEX INDEX CONCURRENTLY idx_exercises_type;
REINDEX INDEX CONCURRENTLY idx_user_progress_user_id;
EOF
```

### Database Statistics

```sql
-- Update table statistics
ANALYZE VERBOSE users;
ANALYZE VERBOSE exercises;
ANALYZE VERBOSE user_progress;

-- View statistics age
SELECT
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE schemaname = 'public';
```

### Index Maintenance

```sql
-- Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find duplicate indexes
SELECT
    pg_size_pretty(SUM(pg_relation_size(idx))::BIGINT) AS size,
    (array_agg(idx))[1] AS idx1,
    (array_agg(idx))[2] AS idx2,
    (array_agg(idx))[3] AS idx3,
    (array_agg(idx))[4] AS idx4
FROM (
    SELECT
        indexrelid::regclass AS idx,
        (indrelid::text ||E'\n'|| indclass::text ||E'\n'|| indkey::text ||E'\n'||
        COALESCE(indexprs::text,'')||E'\n' || COALESCE(indpred::text,'')) AS KEY
    FROM pg_index
) sub
GROUP BY KEY HAVING COUNT(*) > 1
ORDER BY SUM(pg_relation_size(idx)) DESC;
```

### Query Performance Monitoring

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slow queries
SELECT
    substring(query, 1, 100) AS short_query,
    round(total_time::numeric, 2) AS total_time,
    calls,
    round(mean_time::numeric, 2) AS mean,
    round((100 * total_time / sum(total_time) OVER ())::numeric, 2) AS percentage_cpu
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

---

## Dependency Updates

### Update Strategy

**Security Updates**: Immediate (within 24 hours)
**Patch Updates**: Weekly
**Minor Updates**: Monthly
**Major Updates**: Quarterly (with thorough testing)

### Backend Dependencies (Python)

#### Check for Updates

```bash
cd backend

# Check for outdated packages
pip list --outdated

# Check for security vulnerabilities
pip install safety
safety check

# Generate updated requirements
pip freeze > requirements-updated.txt
```

#### Update Procedure

```bash
# 1. Create update branch
git checkout -b update/backend-dependencies

# 2. Update dependencies
cd backend

# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade fastapi

# 3. Update requirements file
pip freeze > requirements.txt

# 4. Run tests
pytest

# 5. Check for breaking changes
# Review CHANGELOG for each updated package

# 6. Commit and test
git add requirements.txt
git commit -m "chore: update backend dependencies"

# 7. Deploy to staging first
git push origin update/backend-dependencies

# 8. After staging verification, merge to develop
```

#### Dependency Monitoring

```bash
#!/bin/bash
# check-dependencies.sh

cd backend

echo "Checking for security vulnerabilities..."
safety check --json > security-report.json

echo "Checking for outdated packages..."
pip list --outdated > outdated-packages.txt

# Send report
if [ -s outdated-packages.txt ]; then
    echo "Outdated packages found:"
    cat outdated-packages.txt
    # Send notification (e.g., Slack, email)
fi
```

### Frontend Dependencies (npm)

#### Check for Updates

```bash
cd frontend

# Check for outdated packages
npm outdated

# Check for security vulnerabilities
npm audit

# Check for available updates (interactive)
npx npm-check-updates
```

#### Update Procedure

```bash
# 1. Create update branch
git checkout -b update/frontend-dependencies

# 2. Update dependencies
cd frontend

# Update patch versions (safe)
npm update

# Update minor versions
npx npm-check-updates -u -t minor
npm install

# Update major versions (careful!)
npx npm-check-updates -u
npm install

# 3. Run tests
npm run test
npm run test:e2e

# 4. Build and verify
npm run build

# 5. Check bundle size
npm run build
ls -lh .next/static

# 6. Commit
git add package.json package-lock.json
git commit -m "chore: update frontend dependencies"

# 7. Deploy to staging and verify
```

#### Automated Dependency Updates (Dependabot)

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Backend dependencies
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    reviewers:
      - "backend-team"
    assignees:
      - "backend-lead"
    labels:
      - "dependencies"
      - "backend"

  # Frontend dependencies
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    reviewers:
      - "frontend-team"
    assignees:
      - "frontend-lead"
    labels:
      - "dependencies"
      - "frontend"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

---

## Security Patch Management

### Security Monitoring

```bash
#!/bin/bash
# security-scan.sh

echo "=== Security Scan Report $(date) ==="

# Backend
echo -e "\n--- Backend Security ---"
cd backend
safety check --full-report

# Frontend
echo -e "\n--- Frontend Security ---"
cd ../frontend
npm audit --audit-level=high

# Docker images
echo -e "\n--- Docker Image Security ---"
docker scan subjunctive-backend:latest

# Check SSL/TLS
echo -e "\n--- SSL/TLS Check ---"
echo | openssl s_client -servername api.subjunctivepractice.com \
  -connect api.subjunctivepractice.com:443 2>/dev/null | \
  openssl x509 -noout -dates

echo -e "\n=== End Report ==="
```

### Critical Security Update Process

```
┌─────────────────────┐
│ Security Advisory  │
│     Received        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Assess Impact     │
│ - Severity          │
│ - Affected systems  │
│ - Exploit available?│
└──────────┬──────────┘
           │
    ┌──────▼──────┐
    │  Critical?  │
    └──┬───────┬──┘
   Yes │       │ No
       │       │
       │       ▼
       │  ┌────────────────┐
       │  │ Schedule patch │
       │  │  next cycle    │
       │  └────────────────┘
       │
       ▼
┌─────────────────────┐
│ Immediate Action    │
│ - Create hotfix     │
│ - Test patch        │
│ - Deploy to staging │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Deploy to Prod      │
│ - Off-hours         │
│ - Monitor closely   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Verify & Document   │
│ - Confirm fix       │
│ - Update runbook    │
└─────────────────────┘
```

### Security Patch Checklist

**Critical (0-24 hours):**
- [ ] Verify vulnerability affects our system
- [ ] Review patch notes and breaking changes
- [ ] Create hotfix branch
- [ ] Apply patch
- [ ] Run security tests
- [ ] Deploy to staging
- [ ] Verify fix
- [ ] Get approval for production deployment
- [ ] Deploy to production
- [ ] Monitor for issues
- [ ] Document in security log

**High (1-7 days):**
- [ ] Assess impact and priority
- [ ] Schedule patch window
- [ ] Test patch thoroughly
- [ ] Update documentation
- [ ] Deploy via normal release process

---

## Performance Optimization

### Regular Performance Audits

#### Database Performance

```sql
-- Query performance audit
SELECT
    substring(query, 1, 60) AS short_query,
    round(total_time::numeric, 2) AS total_ms,
    calls,
    round(mean_time::numeric, 2) AS mean_ms,
    round((100 * total_time / sum(total_time) OVER ())::numeric, 2) AS pct
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY total_time DESC
LIMIT 20;

-- Table size audit
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS indexes_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage audit
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan AS index_scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;
```

#### Application Performance

```bash
#!/bin/bash
# performance-audit.sh

echo "=== Performance Audit $(date) ==="

# API response times
echo -e "\n--- API Response Times ---"
for endpoint in "/health" "/api/v1/exercises" "/api/v1/auth/me"; do
    echo "Testing $endpoint..."
    curl -w "\nTime: %{time_total}s\n" -s -o /dev/null \
        "https://api.subjunctivepractice.com$endpoint"
done

# Database connection pool
echo -e "\n--- Database Connections ---"
psql -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';"
psql -c "SELECT max_conn, used, idle FROM (SELECT count(*) used FROM pg_stat_activity) t1, (SELECT setting::int max_conn FROM pg_settings WHERE name='max_connections') t2, (SELECT count(*) idle FROM pg_stat_activity WHERE state='idle') t3;"

# Redis memory usage
echo -e "\n--- Redis Memory ---"
redis-cli INFO memory | grep -E "used_memory_human|maxmemory_human|mem_fragmentation_ratio"

# Application memory
echo -e "\n--- Application Memory ---"
ps aux | grep -E "gunicorn|uvicorn" | awk '{print $6/1024 " MB"}'

echo -e "\n=== End Audit ==="
```

### Optimization Strategies

#### Query Optimization

```python
# backend/services/performance.py

# Before: N+1 query problem
def get_user_exercises_slow(user_id: int):
    exercises = db.query(Exercise).all()
    for exercise in exercises:
        progress = db.query(UserProgress).filter_by(
            user_id=user_id,
            exercise_id=exercise.id
        ).first()
        exercise.user_progress = progress
    return exercises

# After: Single query with join
def get_user_exercises_fast(user_id: int):
    return db.query(Exercise).outerjoin(
        UserProgress,
        and_(
            UserProgress.exercise_id == Exercise.id,
            UserProgress.user_id == user_id
        )
    ).options(
        contains_eager(Exercise.user_progress)
    ).all()
```

#### Caching Strategy

```python
# Implement multi-level caching
from functools import lru_cache
import redis

redis_client = redis.Redis()

# Level 1: In-memory cache (Python)
@lru_cache(maxsize=1000)
def get_exercise_by_id(exercise_id: int):
    # This will cache in Python memory
    return fetch_exercise_from_db(exercise_id)

# Level 2: Redis cache
def get_exercises_by_type(exercise_type: str):
    cache_key = f"exercises:type:{exercise_type}"

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Fetch from database
    exercises = fetch_from_db(exercise_type)

    # Store in cache (1 hour TTL)
    redis_client.setex(
        cache_key,
        3600,
        json.dumps(exercises)
    )

    return exercises
```

---

## Cost Optimization

### Cost Monitoring

```bash
#!/bin/bash
# cost-report.sh

echo "=== Monthly Cost Report ==="

# Railway costs (example)
railway costs --format json > railway-costs.json

# Database size (affects cost)
echo -e "\n--- Database Size ---"
psql -c "SELECT pg_size_pretty(pg_database_size('subjunctive_practice'));"

# Data transfer (estimate)
echo -e "\n--- Estimated Data Transfer ---"
# Monitor through platform dashboard

# Storage usage
echo -e "\n--- Storage Usage ---"
df -h | grep -E "/$|/var"

echo -e "\n=== Optimization Recommendations ==="
# Add cost optimization suggestions
```

### Optimization Strategies

#### Database Costs

```sql
-- Archive old data
CREATE TABLE user_progress_archive AS
SELECT * FROM user_progress
WHERE updated_at < NOW() - INTERVAL '1 year';

DELETE FROM user_progress
WHERE updated_at < NOW() - INTERVAL '1 year';

-- Optimize storage
VACUUM FULL;
```

#### API Costs (Rate Limiting)

```python
# Implement rate limiting to reduce costs
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/exercises")
@limiter.limit("60/minute")  # Limit to 60 requests per minute
async def get_exercises(request: Request):
    # ...
```

#### CDN Optimization

```javascript
// frontend/next.config.js
module.exports = {
    images: {
        domains: ['cdn.subjunctivepractice.com'],
        formats: ['image/avif', 'image/webp'],  // Modern formats
        deviceSizes: [640, 750, 828, 1080, 1200],  // Responsive sizes
    },
    // Enable compression
    compress: true,
    // Cache static pages
    generateEtags: true,
}
```

---

## System Health Monitoring

### Daily Health Check Script

```bash
#!/bin/bash
# daily-health-check.sh

REPORT_FILE="/var/log/subjunctive/health-$(date +%Y%m%d).log"

exec > >(tee -a $REPORT_FILE)
exec 2>&1

echo "=============================================="
echo "Daily Health Check - $(date)"
echo "=============================================="

# 1. Application Health
echo -e "\n1. APPLICATION HEALTH"
curl -s https://api.subjunctivepractice.com/health | jq .

# 2. Database Health
echo -e "\n2. DATABASE HEALTH"
psql -c "SELECT version();"
psql -c "SELECT pg_database_size('subjunctive_practice');"
psql -c "SELECT count(*) FROM pg_stat_activity;"

# 3. Redis Health
echo -e "\n3. REDIS HEALTH"
redis-cli PING
redis-cli INFO server | grep redis_version
redis-cli INFO memory | grep used_memory_human

# 4. System Resources
echo -e "\n4. SYSTEM RESOURCES"
echo "CPU Usage:"
mpstat 1 1 | awk '/Average/ {print "CPU: " 100-$NF"%"}'
echo "Memory Usage:"
free -h | awk '/^Mem:/ {print "Used: "$3" / Total: "$2}'
echo "Disk Usage:"
df -h | grep -E "^/dev/"

# 5. SSL Certificate
echo -e "\n5. SSL CERTIFICATE"
echo | openssl s_client -servername api.subjunctivepractice.com \
    -connect api.subjunctivepractice.com:443 2>/dev/null | \
    openssl x509 -noout -dates

# 6. Recent Errors
echo -e "\n6. RECENT ERRORS (Last 24 hours)"
journalctl -u subjunctive-backend --since "24 hours ago" | \
    grep -i error | tail -10

# 7. Backup Status
echo -e "\n7. BACKUP STATUS"
ls -lht /backups/subjunctive/ | head -5

# 8. Performance Metrics
echo -e "\n8. PERFORMANCE METRICS"
echo "Average Response Time (last hour):"
# Query from monitoring system

echo -e "\n=============================================="
echo "Health Check Complete"
echo "=============================================="

# Send report if critical issues found
if grep -q "ERROR\|CRITICAL\|FAILED" $REPORT_FILE; then
    echo "Critical issues detected! Sending alert..."
    # Send notification
fi
```

### Automated Alerts

```yaml
# alerts.yml
alerts:
  - name: HighErrorRate
    condition: error_rate > 5%
    duration: 5m
    action: page_oncall
    severity: critical

  - name: SlowResponseTime
    condition: p95_response_time > 500ms
    duration: 10m
    action: slack_notification
    severity: warning

  - name: DatabaseConnectionsHigh
    condition: db_connections > 80%
    duration: 5m
    action: slack_notification
    severity: warning

  - name: DiskSpaceLow
    condition: disk_usage > 85%
    duration: 1m
    action: email_alert
    severity: warning

  - name: CertificateExpiring
    condition: cert_days_until_expiry < 7
    duration: 1h
    action: email_alert
    severity: high
```

---

## Maintenance Calendar

### Weekly Tasks

| Day | Task | Owner |
|-----|------|-------|
| Monday | Review weekend incidents | Ops Lead |
| Monday | Dependency check | DevOps |
| Tuesday | Performance review | Backend Lead |
| Wednesday | Security scan | Security Team |
| Thursday | Cost review | Engineering Manager |
| Friday | Weekly backup verification | Ops Lead |
| Sunday | Database maintenance window | Auto/DBA |

### Monthly Tasks

| Week | Task | Owner |
|------|------|-------|
| Week 1 | Full security audit | Security Team |
| Week 1 | Database optimization | DBA |
| Week 2 | Dependency updates | Dev Team |
| Week 3 | Disaster recovery test | Ops Team |
| Week 4 | Performance benchmarking | Engineering |

### Quarterly Tasks

- Major dependency updates
- Architecture review
- Capacity planning
- Cost optimization review
- Security penetration testing
- Documentation audit
- Team training on new tools/processes

---

This maintenance guide should be reviewed and updated quarterly to reflect changes in infrastructure, tools, and best practices.
