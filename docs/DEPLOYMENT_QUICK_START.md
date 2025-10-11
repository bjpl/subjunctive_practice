# Production Deployment Quick Start

## Spanish Subjunctive Practice - 10-Minute Deployment Guide

This guide will get you from zero to production in approximately 10 minutes (excluding account setup).

---

## Prerequisites (5 minutes)

### 1. Install Required Tools

```bash
# Railway CLI
npm install -g @railway/cli

# Vercel CLI
npm install -g vercel
```

### 2. Create Accounts (if not already done)

- Railway: https://railway.app (GitHub login)
- Vercel: https://vercel.com (GitHub login)
- Sentry: https://sentry.io (optional, for monitoring)

---

## Backend Deployment (3 minutes)

### Step 1: Login to Railway

```bash
railway login
```

### Step 2: Create Project and Deploy

```bash
cd backend
railway init
railway add postgresql  # Adds PostgreSQL database
railway add redis       # Adds Redis (optional)
railway up              # Deploys backend
```

### Step 3: Set Environment Variables

In Railway dashboard (https://railway.app):

```bash
# Required
JWT_SECRET_KEY=<run: python -c "import secrets; print(secrets.token_urlsafe(32))">
SESSION_SECRET_KEY=<run: python -c "import secrets; print(secrets.token_urlsafe(32))">
OPENAI_API_KEY=sk-your-key-here

# Update after frontend deployment
CORS_ORIGINS=https://your-app.vercel.app
```

### Step 4: Run Migrations

```bash
railway run alembic upgrade head
```

### Step 5: Get Backend URL

```bash
railway status  # Copy the URL
```

---

## Frontend Deployment (2 minutes)

### Step 1: Login to Vercel

```bash
vercel login
```

### Step 2: Configure and Deploy

```bash
cd frontend

# Set environment variables in .env.production
echo "NEXT_PUBLIC_API_URL=https://your-backend.railway.app" > .env.production

# Deploy
vercel --prod
```

### Step 3: Update Backend CORS

In Railway dashboard, update:

```bash
CORS_ORIGINS=https://your-app.vercel.app
```

---

## Verification (1 minute)

### Test Backend

```bash
curl https://your-backend.railway.app/health

# Expected output:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "database_connected": true
# }
```

### Test Frontend

Visit: `https://your-frontend.vercel.app`

Test flow:
1. Homepage loads ✓
2. Register new user ✓
3. Login ✓
4. Generate exercise ✓

---

## One-Command Deployment (Alternative)

Use the automated deployment script:

```bash
# Set required environment variables first
export RAILWAY_TOKEN=your_railway_token
export VERCEL_TOKEN=your_vercel_token

# Deploy everything
./scripts/deploy.sh all
```

---

## Monitoring Setup (Optional, +5 minutes)

### Sentry Error Tracking

1. Create projects at https://sentry.io
2. Copy DSN from project settings
3. Add to Railway:
   ```bash
   SENTRY_DSN=https://your-dsn@sentry.io/project-id
   ```

### Uptime Monitoring

1. Sign up at https://uptimerobot.com
2. Add monitor:
   - URL: `https://your-backend.railway.app/health`
   - Interval: 5 minutes

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
railway logs

# Common issues:
# - Missing environment variables
# - Database migration failed
# - Port binding error
```

### Frontend build fails

```bash
# Check build logs in Vercel dashboard
# Common issues:
# - Missing NEXT_PUBLIC_API_URL
# - TypeScript errors
# - Dependency issues
```

### CORS errors

```bash
# Ensure CORS_ORIGINS matches your Vercel URL exactly
# In Railway dashboard:
CORS_ORIGINS=https://your-exact-vercel-url.vercel.app
```

---

## Post-Deployment Checklist

- [ ] Backend health endpoint responding
- [ ] Frontend homepage loads
- [ ] User registration works
- [ ] Login works
- [ ] Exercise generation works
- [ ] Monitoring configured (Sentry, Uptime)
- [ ] Backups scheduled
- [ ] Team notified

---

## Cost Summary

### Free Tier Usage
- Railway: $5 credit/month (first month free)
- Vercel: Free hobby plan (generous limits)
- Sentry: Free tier (5k errors/month)
- UptimeRobot: Free tier (50 monitors)

**Total**: Free for first month, ~$10-30/month after

---

## Next Steps

1. ✅ Review [Full Deployment Guide](./DEPLOYMENT_GUIDE_PRODUCTION.md)
2. ✅ Complete [Production Checklist](./PRODUCTION_READINESS_CHECKLIST.md)
3. ✅ Set up [Monitoring](./MONITORING_SETUP.md)
4. ✅ Configure custom domain (optional)
5. ✅ Schedule automated backups

---

## Need Help?

- Full Guide: [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md)
- Troubleshooting: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Railway Support: https://help.railway.app
- Vercel Support: https://vercel.com/support

---

**Quick Start Version**: 1.0.0
**Estimated Time**: 10 minutes
**Last Updated**: October 2, 2025
