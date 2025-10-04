# Production Deployment Guide

## Spanish Subjunctive Practice Application

This comprehensive guide covers deploying the Spanish Subjunctive Practice application to production using Railway (backend) and Vercel (frontend).

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Backend Deployment (Railway)](#backend-deployment-railway)
4. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
5. [Database Setup](#database-setup)
6. [Environment Variables](#environment-variables)
7. [Domain Configuration](#domain-configuration)
8. [SSL/TLS Certificates](#ssltls-certificates)
9. [Monitoring Setup](#monitoring-setup)
10. [Troubleshooting](#troubleshooting)

---

## Overview

### Architecture

```
┌─────────────────┐         ┌──────────────────┐
│                 │         │                  │
│  Vercel CDN     │────────▶│  Railway API     │
│  (Frontend)     │  HTTPS  │  (Backend)       │
│                 │         │                  │
└─────────────────┘         └──────────────────┘
                                      │
                                      ├──▶ PostgreSQL
                                      └──▶ Redis
```

### Technology Stack

- **Frontend**: Next.js 14 on Vercel Edge Network
- **Backend**: FastAPI on Railway
- **Database**: PostgreSQL (Railway Managed)
- **Cache**: Redis (Railway Managed)
- **Monitoring**: Sentry for error tracking
- **CI/CD**: GitHub Actions + Railway/Vercel webhooks

---

## Prerequisites

### Required Tools

Install the following before starting:

```bash
# Node.js and npm
node --version  # v18.0.0 or higher
npm --version   # v9.0.0 or higher

# Python
python --version  # v3.11 or higher
pip --version

# Railway CLI
npm install -g @railway/cli
railway --version

# Vercel CLI
npm install -g vercel
vercel --version

# Git
git --version
```

### Required Accounts

1. **Railway** (Backend hosting)
   - Sign up at https://railway.app
   - Free tier available ($5 credit/month)
   - Credit card required after trial

2. **Vercel** (Frontend hosting)
   - Sign up at https://vercel.com
   - Free tier available (generous limits)
   - No credit card required for hobby plan

3. **GitHub** (Code repository)
   - Repository for source code
   - GitHub Actions for CI/CD

4. **OpenAI** (AI Features)
   - API key from https://platform.openai.com
   - Pay-as-you-go pricing

5. **Sentry** (Monitoring - Optional)
   - Sign up at https://sentry.io
   - Free tier available

---

## Backend Deployment (Railway)

### Step 1: Create Railway Project

```bash
# Login to Railway
railway login

# Create new project
cd backend
railway init

# Link to existing project (if already created)
railway link
```

### Step 2: Add PostgreSQL Database

```bash
# Add PostgreSQL plugin
railway add postgresql

# Railway automatically sets DATABASE_URL environment variable
```

### Step 3: Add Redis Cache (Optional)

```bash
# Add Redis plugin
railway add redis

# Railway automatically sets REDIS_URL environment variable
```

### Step 4: Configure Environment Variables

Set these in the Railway dashboard (https://railway.app/project/<your-project>/variables):

**Critical Variables:**

```bash
# Security Keys (Generate using: python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=your_secure_random_string_here
SESSION_SECRET_KEY=your_secure_random_string_here

# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# CORS Origins (Update after deploying frontend)
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Optional Variables:**

```bash
# Sentry Error Tracking
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Custom Configuration
WORKERS=4
LOG_LEVEL=INFO
```

### Step 5: Deploy Backend

#### Option A: Automatic Deployment (Recommended)

```bash
# Connect GitHub repository
# Railway will auto-deploy on git push to main

# In Railway dashboard:
# 1. Go to Settings -> Connect Repo
# 2. Select your GitHub repository
# 3. Configure branch (main/master)
# 4. Enable auto-deploy
```

#### Option B: Manual Deployment

```bash
# Deploy current directory
railway up

# Deploy specific service
railway up --service backend
```

### Step 6: Run Database Migrations

```bash
# Run migrations via Railway
railway run alembic upgrade head

# Or set auto-migrations in railway.toml (already configured)
```

### Step 7: Verify Deployment

```bash
# Get deployment URL
railway status

# Test health endpoint
curl https://your-backend.railway.app/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "database_connected": true,
#   "redis_connected": true,
#   "openai_configured": true
# }
```

### Step 8: View Logs

```bash
# View live logs
railway logs

# View specific service logs
railway logs --service backend
```

---

## Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI

```bash
# Install globally
npm install -g vercel

# Login to Vercel
vercel login
```

### Step 2: Configure Environment Variables

Create `.env.production` in frontend directory or set in Vercel dashboard:

```bash
# Backend API URL (from Railway)
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# Environment
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_APP_NAME=Spanish Subjunctive Practice
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Step 3: Deploy Frontend

#### Option A: Automatic Deployment (Recommended)

```bash
# Import project from GitHub
vercel

# Follow prompts:
# - Link to existing project? No
# - What's your project's name? subjunctive-practice
# - In which directory is your code? ./frontend
# - Want to override settings? No

# Deploy to production
vercel --prod
```

#### Option B: GitHub Integration

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure:
   - Framework: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. Add environment variables
5. Deploy

### Step 4: Update Backend CORS

After frontend deployment, update backend CORS settings:

```bash
# In Railway dashboard, update:
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
```

### Step 5: Verify Frontend

Visit your Vercel URL and test:

1. Homepage loads correctly
2. API calls work (check browser console)
3. Authentication flow works
4. Exercise features work

---

## Database Setup

### Initial Schema Setup

```bash
# Generate migration
cd backend
alembic revision --autogenerate -m "Initial schema"

# Review migration in alembic/versions/

# Apply migration
railway run alembic upgrade head
```

### Backup Strategy

```bash
# Create backup
./scripts/db-backup.sh backup

# List backups
./scripts/db-backup.sh list

# Restore from backup
./scripts/db-backup.sh restore backups/backup_20250102_120000.sql.gz
```

### Automated Backups

Set up automated backups using Railway cron jobs or external service:

```bash
# Add to crontab for daily backups at 2 AM
0 2 * * * /path/to/scripts/db-backup.sh backup && \
          UPLOAD_TO_CLOUD=true /path/to/scripts/db-backup.sh backup
```

---

## Environment Variables

### Backend Environment Variables (Railway)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes (Auto) | PostgreSQL connection string | `postgresql://...` |
| `REDIS_URL` | No (Auto) | Redis connection string | `redis://...` |
| `JWT_SECRET_KEY` | **Yes** | JWT token signing key | `random_32_char_string` |
| `SESSION_SECRET_KEY` | **Yes** | Session encryption key | `random_32_char_string` |
| `OPENAI_API_KEY` | **Yes** | OpenAI API key | `sk-...` |
| `CORS_ORIGINS` | **Yes** | Allowed frontend origins | `https://app.vercel.app` |
| `SENTRY_DSN` | No | Sentry error tracking DSN | `https://...@sentry.io/...` |
| `LOG_LEVEL` | No | Logging level | `INFO` |
| `WORKERS` | No | Gunicorn workers | `4` |

### Frontend Environment Variables (Vercel)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | **Yes** | Backend API URL | `https://api.railway.app` |
| `NEXT_PUBLIC_ENVIRONMENT` | No | Environment name | `production` |
| `NEXT_PUBLIC_APP_NAME` | No | Application name | `Spanish Subjunctive` |

### Generating Secure Keys

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL method
openssl rand -base64 32

# Node.js method
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

---

## Domain Configuration

### Custom Domain for Backend (Railway)

1. Go to Railway project settings
2. Click "Generate Domain" for default Railway domain
3. For custom domain:
   - Click "Custom Domain"
   - Add your domain (e.g., `api.yourapp.com`)
   - Add CNAME record to your DNS:
     ```
     Type: CNAME
     Name: api
     Value: <your-railway-domain>.railway.app
     ```
   - Wait for DNS propagation (5-60 minutes)

### Custom Domain for Frontend (Vercel)

1. Go to Vercel project settings
2. Click "Domains"
3. Add domain (e.g., `www.yourapp.com`)
4. Configure DNS records:
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```
5. Vercel automatically provisions SSL certificate

---

## SSL/TLS Certificates

### Railway

- SSL certificates are **automatically provisioned** by Railway
- Valid for Railway domains and custom domains
- Auto-renewal handled by Railway
- No configuration required

### Vercel

- SSL certificates are **automatically provisioned** by Vercel
- Uses Let's Encrypt for free certificates
- Auto-renewal handled by Vercel
- Supports wildcard certificates for subdomains

### Verification

```bash
# Check SSL certificate
curl -vI https://your-backend.railway.app 2>&1 | grep -i ssl

# Test SSL rating
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=your-domain.com
```

---

## Monitoring Setup

See [MONITORING_SETUP.md](./MONITORING_SETUP.md) for detailed monitoring configuration.

### Quick Setup

1. **Sentry Error Tracking**
   ```bash
   # Sign up at https://sentry.io
   # Create new project (FastAPI for backend, Next.js for frontend)
   # Copy DSN
   # Add to Railway environment variables
   SENTRY_DSN=https://your-dsn@sentry.io/project-id
   ```

2. **Railway Metrics**
   - Built-in metrics available in Railway dashboard
   - CPU, Memory, Network usage
   - Request logs and errors

3. **Vercel Analytics**
   - Enable in Vercel project settings
   - Web vitals tracking
   - Real user monitoring

---

## Troubleshooting

### Common Issues

#### Backend Issues

**Issue: Database connection failed**

```bash
# Check DATABASE_URL is set
railway variables

# Test connection
railway run python -c "from sqlalchemy import create_engine; \
  import os; engine = create_engine(os.getenv('DATABASE_URL')); \
  conn = engine.connect(); print('Connected!')"
```

**Issue: Migrations failing**

```bash
# Check alembic version
railway run alembic current

# Reset to specific version
railway run alembic downgrade <revision>

# Reapply migrations
railway run alembic upgrade head
```

**Issue: High memory usage**

```bash
# Reduce workers in Railway dashboard
WORKERS=2

# Increase memory limit in railway.toml
memory = "1Gi"
```

#### Frontend Issues

**Issue: API calls failing (CORS)**

```bash
# Check CORS_ORIGINS in Railway backend
# Must include exact Vercel URL

# Update in Railway dashboard:
CORS_ORIGINS=https://your-app.vercel.app
```

**Issue: Environment variables not loading**

```bash
# Check Vercel dashboard -> Settings -> Environment Variables
# Ensure NEXT_PUBLIC_API_URL is set for Production

# Redeploy after changing env vars
vercel --prod
```

**Issue: Build failing**

```bash
# Check build logs in Vercel dashboard
# Common issues:
# - Missing dependencies (npm install)
# - TypeScript errors (npm run type-check)
# - ESLint errors (npm run lint)

# Test locally
npm run build
```

### Health Checks

```bash
# Backend health
curl https://your-backend.railway.app/health

# Frontend health
curl https://your-frontend.vercel.app/

# API connectivity test
curl https://your-frontend.vercel.app/api/test
```

### Getting Help

- Railway Support: https://help.railway.app
- Vercel Support: https://vercel.com/support
- GitHub Issues: Create issue in your repository
- Community: Railway Discord, Vercel Discord

---

## Next Steps

After successful deployment:

1. Review [MONITORING_SETUP.md](./MONITORING_SETUP.md)
2. Complete [PRODUCTION_CHECKLIST.md](./PRODUCTION_CHECKLIST.md)
3. Set up automated backups
4. Configure alerting and monitoring
5. Test disaster recovery procedures
6. Document runbook for common operations

---

## Deployment Automation

Use the provided deployment script for streamlined deployments:

```bash
# Full stack deployment
./scripts/deploy.sh all

# Backend only
./scripts/deploy.sh backend

# Frontend only
./scripts/deploy.sh frontend

# With environment variables
SKIP_TESTS=true ./scripts/deploy.sh all
```

---

## Security Best Practices

1. **Never commit secrets to git**
   - Use `.env` files (in `.gitignore`)
   - Set secrets in platform dashboards

2. **Rotate secrets regularly**
   - JWT keys every 90 days
   - API keys as recommended

3. **Use strong CORS policies**
   - Whitelist specific domains only
   - No wildcards in production

4. **Enable rate limiting**
   - Already configured in backend
   - Monitor for abuse

5. **Keep dependencies updated**
   ```bash
   # Backend
   poetry update

   # Frontend
   npm update
   ```

6. **Monitor security advisories**
   - GitHub Dependabot alerts
   - npm audit / safety check

---

**Deployment Guide Version:** 1.0.0
**Last Updated:** October 2, 2025
**Maintained By:** Development Team
