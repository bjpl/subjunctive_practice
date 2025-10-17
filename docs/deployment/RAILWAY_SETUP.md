# Railway Setup Guide - Spanish Subjunctive Practice

Complete guide for deploying the Spanish Subjunctive Practice backend to Railway.

## Prerequisites

- Railway account (free tier available): https://railway.app
- GitHub repository connected to Railway
- Railway CLI installed (optional, but recommended)
- PostgreSQL and Redis plugins (added via Railway dashboard)

## Quick Setup (15 Minutes)

### 1. Install Railway CLI

```bash
# Using npm
npm install -g @railway/cli

# Using Homebrew (macOS)
brew install railway

# Using Scoop (Windows)
scoop install railway

# Verify installation
railway --version
```

### 2. Login to Railway

```bash
railway login
```

This will open your browser for authentication.

### 3. Create Railway Project

**Option A: Using Railway CLI**

```bash
cd backend
railway init
# Select: "Create new project"
# Name: spanish-subjunctive-backend
railway link
```

**Option B: Using Railway Dashboard**

1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect the backend directory

### 4. Add Database Services

#### Add PostgreSQL

```bash
railway add --plugin postgresql

# OR via Dashboard:
# 1. Go to your project
# 2. Click "New" -> "Database" -> "Add PostgreSQL"
```

Railway automatically creates and injects `DATABASE_URL`.

#### Add Redis (Optional but Recommended)

```bash
railway add --plugin redis

# OR via Dashboard:
# 1. Click "New" -> "Database" -> "Add Redis"
```

Railway automatically creates and injects `REDIS_URL`.

### 5. Configure Environment Variables

**Critical Variables (Set in Railway Dashboard)**

Go to: Project -> Variables -> Raw Editor

```bash
# Security Keys (REQUIRED - Generate secure random strings)
JWT_SECRET_KEY=your-secure-jwt-secret-min-32-chars
SESSION_SECRET_KEY=your-secure-session-secret-min-32-chars

# OpenAI API Key (REQUIRED for AI features)
OPENAI_API_KEY=sk-your-openai-api-key

# CORS Configuration (REQUIRED - Update with your Vercel domain)
CORS_ORIGINS=https://your-app.vercel.app

# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json
WORKERS=4

# Python Configuration
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Database (AUTO-SET by Railway PostgreSQL plugin)
# DATABASE_URL is automatically injected - DO NOT SET MANUALLY

# Redis (AUTO-SET by Railway Redis plugin)
# REDIS_URL is automatically injected - DO NOT SET MANUALLY

# Optional: Monitoring
SENTRY_DSN=your-sentry-dsn-if-using-sentry
SENTRY_ENVIRONMENT=production

# Optional: Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

**Generate Secure Keys**

```bash
# Using Python
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('SESSION_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 6. Deploy Backend

**Option A: Automatic Deployment (Recommended)**

Railway auto-deploys when you push to your main branch:

```bash
git add .
git commit -m "Configure Railway deployment"
git push origin main
```

**Option B: Manual Deployment**

```bash
cd backend
railway up
```

### 7. Run Database Migrations

After the first deployment:

```bash
cd backend
railway run alembic upgrade head
```

### 8. Get Your Backend URL

```bash
railway status

# OR
railway domain
```

Your backend will be available at: `https://your-app.up.railway.app`

### 9. Update Frontend Configuration

Update `frontend/vercel.json` with your Railway backend URL:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-app.up.railway.app/api/:path*"
    }
  ]
}
```

## Railway Project Structure

```
Railway Project: spanish-subjunctive-backend
├── Backend Service (FastAPI)
│   ├── Environment: production
│   ├── Region: us-west1
│   └── Domain: your-app.up.railway.app
├── PostgreSQL Database
│   ├── DATABASE_URL (auto-injected)
│   └── Automatic backups
└── Redis Cache
    └── REDIS_URL (auto-injected)
```

## Environment Management

### Staging Environment

Create a separate staging environment:

```bash
# Create staging environment
railway environment create staging

# Switch to staging
railway environment staging

# Add staging database
railway add --plugin postgresql
railway add --plugin redis

# Deploy to staging
railway up
```

### Production Environment

```bash
# Switch to production
railway environment production

# Deploy to production
railway up
```

## Configuration Files

Railway uses these configuration files in the `backend/` directory:

- `railway.toml` - Main Railway configuration (build & deploy settings)
- `railway.json` - Alternative JSON format configuration
- `requirements.txt` - Python dependencies
- `Dockerfile` - Custom Docker build (optional, Nixpacks auto-detected)

## Common Commands

```bash
# View logs
railway logs

# Open dashboard
railway open

# View service status
railway status

# Run commands in Railway environment
railway run python manage.py migrate
railway run alembic upgrade head

# Shell access
railway shell

# Link to existing project
railway link

# Environment variables
railway variables
railway variables set KEY=value
railway variables delete KEY

# Rollback deployment
railway rollback
```

## Monitoring & Health Checks

### Health Check Endpoint

Railway automatically monitors: `https://your-app.up.railway.app/health`

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-16T12:00:00Z"
}
```

### View Metrics

- **Dashboard**: https://railway.app/project/your-project/metrics
- **Logs**: `railway logs` or via dashboard
- **Resource usage**: Memory, CPU, Network in dashboard

## Database Management

### Backup Database

```bash
# Using Railway CLI
railway run pg_dump $DATABASE_URL > backup.sql

# Using scripts
railway run python scripts/db-backup.py
```

### Restore Database

```bash
railway run psql $DATABASE_URL < backup.sql
```

### Connect to Database

```bash
# Using Railway shell
railway run psql $DATABASE_URL

# Get connection string
railway variables | grep DATABASE_URL
```

## Troubleshooting

### Deployment Fails

```bash
# Check build logs
railway logs --deployment

# Verify buildCommand
cat railway.toml

# Test locally
pip install -r requirements.txt
```

### Database Connection Issues

```bash
# Verify DATABASE_URL is set
railway variables | grep DATABASE_URL

# Check database status
railway status

# Restart database
railway restart --service postgresql
```

### Application Crashes

```bash
# View crash logs
railway logs --tail 100

# Check environment variables
railway variables

# Verify health endpoint
curl https://your-app.up.railway.app/health
```

### Port Binding Issues

Railway automatically sets `$PORT` environment variable. Ensure your app binds to:

```python
# main.py should use Railway's PORT
import os
port = int(os.getenv("PORT", 8000))
```

## Security Best Practices

### 1. Environment Variables

- ✅ Store all secrets in Railway Variables (not in code)
- ✅ Use separate environments for staging/production
- ✅ Rotate secrets regularly
- ❌ Never commit `.env` files with real secrets

### 2. Database Security

- ✅ Railway PostgreSQL includes SSL by default
- ✅ Use connection pooling
- ✅ Enable automatic backups
- ✅ Restrict IP access if needed

### 3. API Security

- ✅ Set CORS_ORIGINS to your frontend domain only
- ✅ Enable rate limiting
- ✅ Use HTTPS (Railway provides free SSL)
- ✅ Implement JWT token expiration

### 4. Monitoring

- ✅ Set up Sentry for error tracking
- ✅ Monitor Railway metrics
- ✅ Enable health checks
- ✅ Set up log aggregation

## Pricing & Resources

### Free Tier

- $5 free credit per month
- Suitable for development and small projects
- Includes:
  - Web service
  - PostgreSQL database
  - Redis cache

### Paid Plans

- **Hobby**: $5/month (after free credit)
- **Pro**: Pay as you go
- See: https://railway.app/pricing

### Resource Limits

Monitor usage in dashboard:
- Memory: Check for memory leaks
- CPU: Optimize slow endpoints
- Network: Monitor API traffic

## CI/CD Integration

Railway integrates with GitHub Actions. See:
- `.github/workflows/deploy-backend.yml`
- Automatic deployments on push to main branch
- Manual deployments via `railway up`

## Migration from Other Platforms

### From Render

1. Export database: `pg_dump`
2. Create Railway PostgreSQL
3. Import database: `psql`
4. Update environment variables
5. Deploy to Railway
6. Update DNS (if using custom domain)

### From Heroku

1. Use Railway's Heroku importer
2. Go to: New Project -> Deploy from Heroku
3. Select Heroku app
4. Railway migrates automatically

## Custom Domain Setup

### Add Custom Domain

```bash
# Generate domain
railway domain

# OR add custom domain via dashboard:
# 1. Project Settings -> Domains
# 2. Click "Custom Domain"
# 3. Enter: api.yourapp.com
# 4. Add CNAME record to your DNS
```

### DNS Configuration

```
Type: CNAME
Name: api (or subdomain)
Value: your-app.up.railway.app
TTL: 3600
```

## Support Resources

- **Documentation**: https://docs.railway.app
- **Discord Community**: https://discord.gg/railway
- **Status Page**: https://status.railway.app
- **Changelog**: https://railway.app/changelog

## Next Steps

After successful deployment:

1. ✅ Test all API endpoints
2. ✅ Run database migrations
3. ✅ Verify health checks
4. ✅ Update frontend with backend URL
5. ✅ Set up monitoring (Sentry)
6. ✅ Configure custom domain (optional)
7. ✅ Enable automatic backups
8. ✅ Document deployment process for team

---

**Need Help?**

- Check Railway Docs: https://docs.railway.app
- Join Discord: https://discord.gg/railway
- Create issue in repo: [GitHub Issues Link]
