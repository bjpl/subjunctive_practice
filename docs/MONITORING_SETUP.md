# Monitoring and Logging Setup Guide

## Spanish Subjunctive Practice Application

Comprehensive guide for setting up monitoring, logging, and alerting for production deployments.

---

## Table of Contents

1. [Overview](#overview)
2. [Sentry Error Tracking](#sentry-error-tracking)
3. [Application Performance Monitoring](#application-performance-monitoring)
4. [Log Aggregation](#log-aggregation)
5. [Uptime Monitoring](#uptime-monitoring)
6. [Performance Metrics](#performance-metrics)
7. [Alerting Configuration](#alerting-configuration)
8. [Dashboard Setup](#dashboard-setup)

---

## Overview

### Monitoring Stack

```
┌────────────────────────────────────────────────┐
│         Monitoring & Observability Stack        │
├────────────────────────────────────────────────┤
│                                                 │
│  Sentry        → Error Tracking & Performance  │
│  Railway Logs  → Backend Logs & Metrics        │
│  Vercel Logs   → Frontend Logs & Analytics     │
│  UptimeRobot   → Uptime Monitoring             │
│  DataDog       → (Optional) Advanced APM       │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Metrics to Track

1. **Error Tracking**
   - Unhandled exceptions
   - API errors
   - Frontend errors

2. **Performance Metrics**
   - API response times
   - Database query performance
   - Frontend page load times
   - Core Web Vitals

3. **Business Metrics**
   - User registrations
   - Exercise completions
   - Session duration
   - Feature usage

4. **Infrastructure Metrics**
   - CPU usage
   - Memory usage
   - Network bandwidth
   - Database connections

---

## Sentry Error Tracking

### Setup Sentry Account

1. Sign up at https://sentry.io
2. Create organization (if first time)
3. Create two projects:
   - **Backend**: Select "FastAPI" or "Python"
   - **Frontend**: Select "Next.js" or "React"

### Backend Integration

#### Step 1: Install Sentry SDK

Already included in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
sentry-sdk = {extras = ["fastapi"], version = "^1.40.3"}
```

#### Step 2: Configure Sentry

In `backend/core/config.py` (already configured):

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

def init_sentry():
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
            profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ],
        )
```

#### Step 3: Set Environment Variables

In Railway dashboard:

```bash
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1  # Sample 10% of transactions
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

#### Step 4: Test Sentry Integration

```python
# Add to backend/main.py for testing
@app.get("/sentry-test")
def trigger_error():
    raise Exception("This is a test error for Sentry")
```

Visit: `https://your-backend.railway.app/sentry-test`

Check Sentry dashboard for the error.

### Frontend Integration

#### Step 1: Install Sentry SDK

```bash
cd frontend
npm install @sentry/nextjs
```

#### Step 2: Initialize Sentry

Create `frontend/sentry.client.config.ts`:

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT,
  tracesSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay(),
  ],
});
```

Create `frontend/sentry.server.config.ts`:

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT,
  tracesSampleRate: 0.1,
});
```

#### Step 3: Configure Next.js

Update `frontend/next.config.js`:

```javascript
const { withSentryConfig } = require("@sentry/nextjs");

const nextConfig = {
  // Your existing config
};

module.exports = withSentryConfig(
  nextConfig,
  {
    silent: true,
    org: "your-org",
    project: "your-frontend-project",
  },
  {
    hideSourceMaps: true,
    widenClientFileUpload: true,
  }
);
```

#### Step 4: Set Environment Variables

In Vercel dashboard:

```bash
NEXT_PUBLIC_SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
NEXT_PUBLIC_ENVIRONMENT=production
SENTRY_AUTH_TOKEN=your_auth_token_here  # For source maps
```

#### Step 5: Test Frontend Integration

Create test page `frontend/app/sentry-test/page.tsx`:

```typescript
'use client';

export default function SentryTest() {
  const throwError = () => {
    throw new Error("Frontend Sentry test error");
  };

  return (
    <button onClick={throwError}>
      Trigger Sentry Error
    </button>
  );
}
```

### Sentry Best Practices

1. **Set Up Alerts**
   - Go to Sentry Project → Alerts
   - Configure alerts for:
     - New issues
     - Issue frequency spikes
     - Performance degradation

2. **Configure Release Tracking**
   ```bash
   # Backend (in CI/CD)
   sentry-cli releases new "$VERSION"
   sentry-cli releases set-commits "$VERSION" --auto

   # Frontend (automatic with @sentry/nextjs)
   # Configure in next.config.js
   ```

3. **Filter Noise**
   - Ignore known errors (e.g., browser extensions)
   - Set up sampling for high-volume events
   - Configure issue grouping rules

4. **Use Breadcrumbs**
   ```python
   # Backend
   from sentry_sdk import add_breadcrumb

   add_breadcrumb(
       category="exercise",
       message="User started exercise",
       level="info",
   )
   ```

---

## Application Performance Monitoring

### Railway Built-in Metrics

Railway provides built-in metrics:

1. **Access Metrics**
   - Go to Railway dashboard
   - Select your backend service
   - Click "Metrics" tab

2. **Available Metrics**
   - CPU usage (%)
   - Memory usage (MB)
   - Network bandwidth (MB/s)
   - Request rate (req/s)
   - Response time (ms)

3. **Custom Metrics**

Create `backend/utils/metrics.py`:

```python
import time
from functools import wraps
import structlog

logger = structlog.get_logger()

def track_performance(operation_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time

                logger.info(
                    "operation_completed",
                    operation=operation_name,
                    duration_ms=duration * 1000,
                    success=True
                )

                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "operation_failed",
                    operation=operation_name,
                    duration_ms=duration * 1000,
                    error=str(e),
                    success=False
                )
                raise
        return wrapper
    return decorator

# Usage
@track_performance("generate_exercise")
async def generate_exercise(user_id: int):
    # Your logic here
    pass
```

### Vercel Analytics

1. **Enable Vercel Analytics**
   - Go to Vercel project settings
   - Navigate to "Analytics"
   - Click "Enable Analytics"

2. **Available Metrics**
   - Page views
   - Unique visitors
   - Top pages
   - Geographic distribution
   - Device breakdown

3. **Web Vitals**

Vercel automatically tracks:
- **LCP** (Largest Contentful Paint)
- **FID** (First Input Delay)
- **CLS** (Cumulative Layout Shift)
- **FCP** (First Contentful Paint)
- **TTFB** (Time to First Byte)

4. **Custom Events** (Optional)

```typescript
// frontend/lib/analytics.ts
import { Analytics } from '@vercel/analytics/react';

export function trackEvent(name: string, properties?: object) {
  if (typeof window !== 'undefined' && window.va) {
    window.va('track', name, properties);
  }
}

// Usage
trackEvent('exercise_completed', {
  exerciseType: 'subjunctive',
  difficulty: 'medium',
  score: 85,
});
```

---

## Log Aggregation

### Backend Logging (Railway)

#### Structured Logging Setup

Already configured in `backend/core/logging.py`:

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

#### Log Levels

```python
import structlog

logger = structlog.get_logger()

# Debug (development only)
logger.debug("Debugging info", extra_data=value)

# Info (normal operations)
logger.info("User logged in", user_id=123)

# Warning (potential issues)
logger.warning("Rate limit approaching", current_rate=50)

# Error (recoverable errors)
logger.error("Failed to send email", user_id=123, error=str(e))

# Critical (immediate attention)
logger.critical("Database connection lost")
```

#### Viewing Logs

```bash
# View live logs
railway logs

# View logs with filters
railway logs --filter "error"

# View logs for specific time range
railway logs --since 1h

# Export logs
railway logs --json > logs.json
```

### Frontend Logging (Vercel)

#### View Frontend Logs

1. Go to Vercel dashboard
2. Select deployment
3. Click "Functions" → View logs
4. Filter by severity, function, or time range

#### Custom Logging

Create `frontend/lib/logger.ts`:

```typescript
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

class Logger {
  private log(level: LogLevel, message: string, data?: any) {
    const logEntry = {
      level,
      message,
      timestamp: new Date().toISOString(),
      environment: process.env.NEXT_PUBLIC_ENVIRONMENT,
      ...data,
    };

    // Console logging
    console[level](message, logEntry);

    // Send to external service (optional)
    if (level === 'error' && process.env.NODE_ENV === 'production') {
      // Send to logging service
      fetch('/api/logs', {
        method: 'POST',
        body: JSON.stringify(logEntry),
      }).catch(() => {});
    }
  }

  debug(message: string, data?: any) {
    if (process.env.NODE_ENV !== 'production') {
      this.log('debug', message, data);
    }
  }

  info(message: string, data?: any) {
    this.log('info', message, data);
  }

  warn(message: string, data?: any) {
    this.log('warn', message, data);
  }

  error(message: string, data?: any) {
    this.log('error', message, data);
  }
}

export const logger = new Logger();
```

---

## Uptime Monitoring

### UptimeRobot Setup

1. **Create Account**
   - Sign up at https://uptimerobot.com
   - Free plan: 50 monitors, 5-minute intervals

2. **Add Monitors**

   **Backend Health Check:**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Backend API Health
   URL: https://your-backend.railway.app/health
   Monitoring Interval: 5 minutes
   ```

   **Frontend Homepage:**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Frontend Homepage
   URL: https://your-frontend.vercel.app/
   Monitoring Interval: 5 minutes
   ```

   **API Endpoint:**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: API Endpoint
   URL: https://your-backend.railway.app/api/v1/exercises
   Monitoring Interval: 5 minutes
   HTTP Method: GET
   Expected Status Code: 200 or 401
   ```

3. **Configure Alerts**
   - Email notifications
   - Slack webhook (optional)
   - SMS (premium)
   - PagerDuty integration (premium)

4. **Status Page** (Optional)
   - Create public status page
   - Share link with users
   - Example: https://stats.uptimerobot.com/your-page

### Alternative: Better Uptime

```bash
# More features, better interface
# https://betteruptime.com/

# Free tier: 10 monitors, 3-minute intervals
# Includes incident management
```

---

## Performance Metrics

### Backend Performance Tracking

Create `backend/middleware/performance.py`:

```python
import time
from fastapi import Request
import structlog

logger = structlog.get_logger()

async def performance_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=process_time * 1000,
    )

    response.headers["X-Process-Time"] = str(process_time)

    return response
```

### Database Query Monitoring

```python
from sqlalchemy import event
from sqlalchemy.engine import Engine
import structlog

logger = structlog.get_logger()

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - conn.info["query_start_time"].pop()

    if total_time > 1.0:  # Log slow queries (>1s)
        logger.warning(
            "slow_query",
            duration_s=total_time,
            query=statement[:100],  # First 100 chars
        )
```

---

## Alerting Configuration

### Sentry Alerts

1. **Error Rate Alert**
   - Trigger: Error rate increases by 25% compared to previous period
   - Action: Email + Slack notification

2. **New Issue Alert**
   - Trigger: New error type detected
   - Action: Email notification

3. **Performance Degradation**
   - Trigger: P95 response time > 2 seconds
   - Action: Email notification

### Custom Alerts

Create `backend/utils/alerts.py`:

```python
import httpx
import structlog
from typing import Dict, Any

logger = structlog.get_logger()

class AlertManager:
    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    async def send_alert(
        self,
        severity: str,
        title: str,
        message: str,
        metadata: Dict[str, Any] = None
    ):
        """Send alert to configured channels"""

        # Log the alert
        logger.warning(
            "alert_triggered",
            severity=severity,
            title=title,
            message=message,
            metadata=metadata
        )

        # Send to Slack
        if self.slack_webhook:
            await self._send_slack_alert(severity, title, message, metadata)

    async def _send_slack_alert(self, severity, title, message, metadata):
        color = {
            "critical": "#FF0000",
            "warning": "#FFA500",
            "info": "#0000FF"
        }.get(severity, "#808080")

        payload = {
            "attachments": [{
                "color": color,
                "title": title,
                "text": message,
                "fields": [
                    {"title": k, "value": str(v), "short": True}
                    for k, v in (metadata or {}).items()
                ],
                "footer": "Spanish Subjunctive Practice",
                "ts": int(time.time())
            }]
        }

        async with httpx.AsyncClient() as client:
            await client.post(self.slack_webhook, json=payload)

# Usage
alert_manager = AlertManager()

await alert_manager.send_alert(
    severity="critical",
    title="Database Connection Lost",
    message="Unable to connect to PostgreSQL database",
    metadata={"service": "backend", "environment": "production"}
)
```

---

## Dashboard Setup

### Grafana Dashboard (Advanced)

For advanced monitoring, set up Grafana:

1. **Setup Grafana Cloud**
   - Sign up at https://grafana.com
   - Free tier available

2. **Configure Data Sources**
   - Add Prometheus for metrics
   - Add Loki for logs

3. **Import Dashboards**
   - FastAPI dashboard
   - PostgreSQL dashboard
   - Redis dashboard

4. **Create Custom Dashboard**
   ```json
   {
     "dashboard": {
       "title": "Spanish Subjunctive Practice",
       "panels": [
         {
           "title": "Request Rate",
           "type": "graph",
           "targets": [
             {
               "expr": "rate(http_requests_total[5m])"
             }
           ]
         }
       ]
     }
   }
   ```

### Simple Dashboard Alternative

Create simple status dashboard at `/admin/status`:

```python
# backend/api/routes/admin.py

@router.get("/status")
async def system_status():
    return {
        "database": await check_database(),
        "redis": await check_redis(),
        "openai": await check_openai(),
        "disk_usage": await check_disk_usage(),
        "memory_usage": await check_memory(),
    }
```

---

## Monitoring Checklist

- [ ] Sentry error tracking configured for backend
- [ ] Sentry error tracking configured for frontend
- [ ] Uptime monitoring configured (UptimeRobot/Better Uptime)
- [ ] Log aggregation working (Railway/Vercel)
- [ ] Performance metrics tracked (Sentry/Railway/Vercel)
- [ ] Alerts configured (email, Slack)
- [ ] Status page created (optional)
- [ ] Dashboard setup (Grafana or custom)
- [ ] Regular review process established
- [ ] Incident response plan documented

---

**Monitoring Setup Version:** 1.0.0
**Last Updated:** October 2, 2025
**Maintained By:** Development Team
