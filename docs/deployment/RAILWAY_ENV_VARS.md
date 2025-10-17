# Railway Environment Variables - Complete Reference

This document lists all required and optional environment variables for the Spanish Subjunctive Practice backend on Railway.

## Quick Setup Checklist

Copy and paste these into Railway Dashboard -> Variables -> Raw Editor:

```bash
# === REQUIRED VARIABLES ===

# Security Keys (GENERATE NEW VALUES - DO NOT USE THESE EXAMPLES)
JWT_SECRET_KEY=REPLACE_WITH_OUTPUT_FROM_python_-c_import_secrets_print_secrets.token_urlsafe_32
SESSION_SECRET_KEY=REPLACE_WITH_OUTPUT_FROM_python_-c_import_secrets_print_secrets.token_urlsafe_32

# OpenAI API Key (Get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-your-openai-api-key-here

# CORS Origins (Update with your actual Vercel frontend URL)
CORS_ORIGINS=https://your-app.vercel.app

# Application Environment
ENVIRONMENT=production
DEBUG=false

# === AUTO-SET BY RAILWAY (DO NOT SET MANUALLY) ===
# DATABASE_URL (Set automatically by PostgreSQL plugin)
# REDIS_URL (Set automatically by Redis plugin)
# PORT (Set automatically by Railway)
```

## Detailed Variable Reference

### 1. Security & Authentication (REQUIRED)

#### JWT_SECRET_KEY
- **Required**: YES
- **Description**: Secret key for JWT token signing
- **Format**: Minimum 32 characters, cryptographically secure
- **Generate**:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **Example**: `kJ8n_9mL2pQ5rT7vX-zA3bC4dE6fG8hI9jK0lM1nO2pQ3rS4tU5v`

#### SESSION_SECRET_KEY
- **Required**: YES
- **Description**: Secret key for session encryption
- **Format**: Minimum 32 characters, cryptographically secure
- **Generate**:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **Example**: `aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV1wX2yZ3aB4cD5eF6gH7i`

#### JWT_ALGORITHM
- **Required**: NO (has default)
- **Default**: `HS256`
- **Options**: `HS256`, `HS384`, `HS512`, `RS256`
- **Recommended**: Keep default unless you know what you're doing

#### JWT_ACCESS_TOKEN_EXPIRE_MINUTES
- **Required**: NO (has default)
- **Default**: `30`
- **Description**: Access token validity in minutes
- **Recommended**: 15-60 minutes

#### JWT_REFRESH_TOKEN_EXPIRE_DAYS
- **Required**: NO (has default)
- **Default**: `7`
- **Description**: Refresh token validity in days
- **Recommended**: 7-30 days

### 2. External APIs (REQUIRED)

#### OPENAI_API_KEY
- **Required**: YES (if using AI features)
- **Description**: OpenAI API key for AI-powered features
- **Get From**: https://platform.openai.com/api-keys
- **Format**: `sk-...` (starts with sk-)
- **Example**: `sk-proj-abc123xyz789...`
- **Cost**: Pay-per-use (see OpenAI pricing)

#### OPENAI_MODEL
- **Required**: NO (has default)
- **Default**: `gpt-4o-mini`
- **Options**: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Cost Impact**: gpt-4o-mini is cheapest

#### OPENAI_MAX_TOKENS
- **Required**: NO (has default)
- **Default**: `1000`
- **Description**: Maximum tokens per API request
- **Range**: 1-4096

#### OPENAI_TEMPERATURE
- **Required**: NO (has default)
- **Default**: `0.7`
- **Description**: Creativity/randomness (0.0 = deterministic, 1.0 = creative)
- **Range**: 0.0-1.0

### 3. Database Configuration

#### DATABASE_URL
- **Required**: AUTO-SET BY RAILWAY
- **Description**: PostgreSQL connection string
- **Format**: `postgresql+asyncpg://user:password@host:port/database`
- **Set By**: Railway PostgreSQL plugin (automatic)
- **DO NOT SET MANUALLY**: Railway injects this automatically

#### DB_POOL_SIZE
- **Required**: NO (has default)
- **Default**: `10`
- **Description**: Number of database connections in pool
- **Recommended**: 5-20 for Railway

#### DB_MAX_OVERFLOW
- **Required**: NO (has default)
- **Default**: `20`
- **Description**: Additional connections beyond pool size
- **Recommended**: 10-30

#### DB_POOL_TIMEOUT
- **Required**: NO (has default)
- **Default**: `30`
- **Description**: Seconds to wait for connection from pool
- **Range**: 10-60

#### DB_POOL_RECYCLE
- **Required**: NO (has default)
- **Default**: `3600`
- **Description**: Seconds before recycling connections (prevents stale connections)
- **Recommended**: 1800-7200

### 4. Redis Cache Configuration

#### REDIS_URL
- **Required**: AUTO-SET BY RAILWAY (if Redis plugin added)
- **Description**: Redis connection string
- **Format**: `redis://default:password@host:port`
- **Set By**: Railway Redis plugin (automatic)
- **DO NOT SET MANUALLY**: Railway injects this automatically

#### CACHE_TTL
- **Required**: NO (has default)
- **Default**: `3600`
- **Description**: Default cache expiration in seconds
- **Range**: 300-86400

#### CACHE_PREFIX
- **Required**: NO (has default)
- **Default**: `subjunctive:prod:`
- **Description**: Prefix for all cache keys

### 5. CORS Configuration (REQUIRED)

#### CORS_ORIGINS
- **Required**: YES
- **Description**: Allowed frontend domains (comma-separated)
- **Format**: `https://domain1.com,https://domain2.com`
- **Example**: `https://subjunctive-practice.vercel.app,https://www.yourapp.com`
- **Security**: Only include your actual frontend domains

#### CORS_ALLOW_CREDENTIALS
- **Required**: NO (has default)
- **Default**: `true`
- **Description**: Allow cookies/auth headers in CORS requests

#### CORS_ALLOW_METHODS
- **Required**: NO (has default)
- **Default**: `GET,POST,PUT,DELETE,PATCH,OPTIONS`
- **Description**: Allowed HTTP methods

#### CORS_ALLOW_HEADERS
- **Required**: NO (has default)
- **Default**: `*`
- **Description**: Allowed HTTP headers

### 6. Application Settings

#### ENVIRONMENT
- **Required**: YES
- **Default**: N/A
- **Options**: `development`, `staging`, `production`
- **Railway**: Set to `production`

#### DEBUG
- **Required**: YES
- **Default**: N/A
- **Options**: `true`, `false`
- **Railway**: Set to `false` in production

#### APP_NAME
- **Required**: NO
- **Default**: `Spanish Subjunctive Practice API`
- **Description**: Application name for logging/monitoring

#### VERSION
- **Required**: NO
- **Default**: `1.0.0`
- **Description**: API version

#### API_V1_PREFIX
- **Required**: NO (has default)
- **Default**: `/api/v1`
- **Description**: API route prefix
- **Note**: Current app uses `/api` (no version)

### 7. Server Configuration

#### PORT
- **Required**: AUTO-SET BY RAILWAY
- **Description**: Port the application listens on
- **Set By**: Railway automatically (usually 8000 or dynamic)
- **DO NOT SET MANUALLY**: Railway injects this

#### HOST
- **Required**: NO (has default)
- **Default**: `0.0.0.0`
- **Description**: Host interface to bind to
- **Railway**: Keep as `0.0.0.0` (all interfaces)

#### WORKERS
- **Required**: NO (has default)
- **Default**: `4`
- **Description**: Number of Gunicorn worker processes
- **Recommended**: `2 * CPU_COUNT + 1`
- **Railway**: 2-4 workers

### 8. Logging & Monitoring

#### LOG_LEVEL
- **Required**: NO (has default)
- **Default**: `INFO`
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Production**: Use `INFO` or `WARNING`

#### LOG_FORMAT
- **Required**: NO (has default)
- **Default**: `json`
- **Options**: `json`, `text`
- **Railway**: Use `json` for better log parsing

#### SENTRY_DSN
- **Required**: NO (recommended for production)
- **Description**: Sentry error tracking DSN
- **Get From**: https://sentry.io
- **Format**: `https://public_key@o0.ingest.sentry.io/project_id`
- **Example**: `https://abc123@o123456.ingest.sentry.io/789012`

#### SENTRY_ENVIRONMENT
- **Required**: NO (if using Sentry)
- **Default**: `production`
- **Options**: `development`, `staging`, `production`

#### SENTRY_TRACES_SAMPLE_RATE
- **Required**: NO
- **Default**: `0.1`
- **Description**: Percentage of transactions to trace (0.0-1.0)
- **Cost Impact**: Higher = more Sentry events = higher cost

### 9. Rate Limiting

#### RATE_LIMIT_ENABLED
- **Required**: NO (has default)
- **Default**: `true`
- **Description**: Enable API rate limiting
- **Production**: Keep `true`

#### RATE_LIMIT_PER_MINUTE
- **Required**: NO (has default)
- **Default**: `60`
- **Description**: Max requests per minute per IP
- **Recommended**: 30-100

#### RATE_LIMIT_PER_HOUR
- **Required**: NO (has default)
- **Default**: `1000`
- **Description**: Max requests per hour per IP
- **Recommended**: 500-2000

### 10. Feature Flags

#### ENABLE_REGISTRATION
- **Required**: NO (has default)
- **Default**: `true`
- **Description**: Allow new user registration

#### ENABLE_EMAIL_VERIFICATION
- **Required**: NO (has default)
- **Default**: `false`
- **Description**: Require email verification for new users

#### ENABLE_API_DOCS
- **Required**: NO (has default)
- **Default**: `true`
- **Description**: Enable Swagger UI at /api/docs
- **Production**: Can disable for security

#### ENABLE_ANALYTICS
- **Required**: NO (has default)
- **Default**: `true`
- **Description**: Enable usage analytics

### 11. Railway-Specific Variables (AUTO-SET)

These are automatically set by Railway - DO NOT SET MANUALLY:

- `RAILWAY_DEPLOYMENT_ID` - Unique deployment identifier
- `RAILWAY_GIT_COMMIT_SHA` - Git commit hash
- `RAILWAY_GIT_BRANCH` - Git branch name
- `RAILWAY_GIT_COMMIT_MESSAGE` - Commit message
- `RAILWAY_ENVIRONMENT_NAME` - Environment name (production/staging)
- `RAILWAY_SERVICE_NAME` - Service name
- `RAILWAY_PROJECT_NAME` - Project name
- `RAILWAY_PUBLIC_DOMAIN` - Public domain for the service

## Setup Scripts

### Generate All Required Secrets

```bash
# Run this to generate all security keys at once
python -c "
import secrets
print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))
print('SESSION_SECRET_KEY=' + secrets.token_urlsafe(32))
"
```

### Minimal Production Configuration

Copy this into Railway Variables -> Raw Editor:

```bash
# Required Security Keys (REPLACE VALUES)
JWT_SECRET_KEY=YOUR_GENERATED_JWT_SECRET_HERE
SESSION_SECRET_KEY=YOUR_GENERATED_SESSION_SECRET_HERE

# Required API Keys (REPLACE VALUES)
OPENAI_API_KEY=sk-your-openai-key-here

# Required CORS (UPDATE WITH YOUR DOMAIN)
CORS_ORIGINS=https://your-app.vercel.app

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

### Full Production Configuration

For a complete production setup, add these optional but recommended variables:

```bash
# ... All required variables from above ...

# Performance Tuning
WORKERS=4
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Monitoring (Recommended)
SENTRY_DSN=https://your-sentry-dsn-here
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

## Verification

### Check Variables Are Set

```bash
# Using Railway CLI
railway variables

# Check specific variable
railway variables | grep JWT_SECRET_KEY

# Set variable
railway variables set JWT_SECRET_KEY=your-value-here

# Delete variable
railway variables delete JWT_SECRET_KEY
```

### Test Configuration

After setting variables, test the deployment:

```bash
# Deploy
railway up

# Check health endpoint
curl https://your-app.up.railway.app/health

# Check logs for errors
railway logs
```

## Security Checklist

Before going to production:

- [ ] `JWT_SECRET_KEY` is set to a cryptographically secure random string
- [ ] `SESSION_SECRET_KEY` is set to a different secure random string
- [ ] `OPENAI_API_KEY` is valid and has billing enabled
- [ ] `CORS_ORIGINS` is set to only your frontend domain (not `*`)
- [ ] `DEBUG` is set to `false`
- [ ] `ENVIRONMENT` is set to `production`
- [ ] `DATABASE_URL` is automatically set by Railway PostgreSQL
- [ ] `REDIS_URL` is automatically set by Railway Redis (if using cache)
- [ ] No secrets are committed to git (.env files are in .gitignore)
- [ ] Sentry is configured for error monitoring (recommended)
- [ ] Rate limiting is enabled

## Troubleshooting

### Variable Not Taking Effect

```bash
# Restart service after changing variables
railway restart

# Check deployment logs
railway logs
```

### Missing Required Variable

Error: `KeyError: 'JWT_SECRET_KEY'`

**Solution**: Set the variable in Railway dashboard

```bash
railway variables set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### Database Connection Fails

Error: `Could not connect to database`

**Solution**: Ensure PostgreSQL plugin is added

```bash
railway add --plugin postgresql
railway restart
```

### CORS Errors in Frontend

Error: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**: Update CORS_ORIGINS with your frontend URL

```bash
railway variables set CORS_ORIGINS=https://your-app.vercel.app
```

---

**Need Help?**
- Railway Docs: https://docs.railway.app/develop/variables
- Project Docs: See `/docs/deployment/RAILWAY_SETUP.md`
