# Production Deployment Walkthrough
## Spanish Subjunctive Practice Application

**Last Updated:** October 3, 2025
**Estimated Time:** 2-3 hours (manual tasks) + 1-2 hours (verification)
**Risk Level:** LOW (after completing critical security task)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Critical Security Fix (IMMEDIATE)](#phase-1-critical-security-fix)
4. [Phase 2: External Services Setup (MANUAL)](#phase-2-external-services-setup)
5. [Phase 3: Code Cleanup (PROGRAMMATIC)](#phase-3-code-cleanup)
6. [Phase 4: GitHub Secrets Configuration (MANUAL)](#phase-4-github-secrets-configuration)
7. [Phase 5: CI/CD Verification (PROGRAMMATIC)](#phase-5-cicd-verification)
8. [Phase 6: Staging Deployment (PROGRAMMATIC)](#phase-6-staging-deployment)
9. [Phase 7: Production Deployment (MANUAL)](#phase-7-production-deployment)
10. [Phase 8: Post-Deployment (VERIFICATION)](#phase-8-post-deployment)
11. [Rollback Procedures](#rollback-procedures)

---

## Overview

This walkthrough separates tasks into three categories:

- 🔴 **MANUAL TASKS** - You must complete these yourself
- 🟢 **PROGRAMMATIC TASKS** - I can do these for you
- 🔵 **VERIFICATION TASKS** - We verify together

**Critical Path:** Phases 1-2-4-6-7-8 (others can be done in parallel)

---

## Prerequisites

### Required Accounts (You Must Create)
- [ ] GitHub account with admin access to repository
- [ ] Railway account (backend hosting) - https://railway.app
- [ ] Vercel account (frontend hosting) - https://vercel.com
- [ ] OpenAI account with API access - https://platform.openai.com
- [ ] Sentry account (error tracking) - https://sentry.io
- [ ] Codecov account (optional) - https://codecov.io

### Required Tools (You Must Install)
```bash
# Railway CLI
npm i -g @railway/cli

# Vercel CLI
npm i -g vercel

# GitHub CLI (optional but recommended)
brew install gh  # macOS
# OR
winget install GitHub.cli  # Windows
```

### Verify Tool Installation
```bash
railway --version  # Should show version
vercel --version   # Should show version
gh --version       # Should show version (optional)
```

---

## Phase 1: Critical Security Fix (IMMEDIATE)

### 🔴 TASK 1.1: Revoke Exposed OpenAI API Key (MANUAL - 5 minutes)

**Why:** Your API key is exposed in `.env.production` and pushed to Git history

**Steps:**
1. Go to https://platform.openai.com/api-keys
2. Find the key starting with `sk-proj-Rv5J8LTzGbP3...`
3. Click "Revoke" or delete the key
4. Click "Create new secret key"
5. Copy the new key (you won't see it again!)
6. Save it temporarily in a password manager or secure note

**Verification:**
```bash
# Test the OLD key should fail (after revocation)
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-proj-Rv5J8LTzGbP3..." \
  -H "Content-Type: application/json"
# Should return: {"error": {"message": "Invalid API key"}}
```

### 🟢 TASK 1.2: Remove Exposed Key from Repository (PROGRAMMATIC)

**What I'll do:**
- Remove the exposed key from `.env.production`
- Add `.env.production` to `.gitignore` (if not already)
- Create `.env.production.template` with placeholder
- Git commit the changes

**Ready for me to execute?** (Say "yes" when ready)

### 🟢 TASK 1.3: Clean Git History (PROGRAMMATIC - Optional)

**What I'll do:**
- Use git-filter-repo or BFG Repo-Cleaner to remove key from history
- This is OPTIONAL but recommended for complete security
- ⚠️ **Warning:** This rewrites Git history (force push required)

**Want me to do this?** (Say "yes" or "skip")

---

## Phase 2: External Services Setup (MANUAL)

### 🔴 TASK 2.1: Railway Setup (15-20 minutes)

**Backend Hosting on Railway**

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub
   - Verify your email

2. **Create Two Projects**
   - **Project 1: subjunctive-practice-staging**
   - **Project 2: subjunctive-practice-production**

3. **For EACH Project, Add Services:**

   a. **PostgreSQL Database**
   ```
   - Click "New" → "Database" → "PostgreSQL"
   - Name: subjunctive-db-[staging/production]
   - Plan: Hobby ($5/month) or Developer ($10/month)
   - Wait for provisioning (~2 minutes)
   ```

   b. **Redis Cache**
   ```
   - Click "New" → "Database" → "Redis"
   - Name: subjunctive-redis-[staging/production]
   - Plan: Hobby ($5/month)
   - Wait for provisioning (~1 minute)
   ```

4. **Get Connection Strings**

   For EACH project, click on PostgreSQL service:
   - Go to "Variables" tab
   - Copy `DATABASE_URL` (format: `postgresql://user:pass@host:port/db`)
   - Save to your notes as `RAILWAY_DATABASE_URL_STAGING` and `RAILWAY_DATABASE_URL_PRODUCTION`

   For EACH project, click on Redis service:
   - Go to "Variables" tab
   - Copy `REDIS_URL` (format: `redis://host:port`)
   - Save to your notes

5. **Get Railway Tokens**

   ```bash
   # Login to Railway
   railway login

   # Link to staging project
   cd /path/to/project
   railway link
   # Select: subjunctive-practice-staging

   # Get staging token
   railway variables
   # Copy RAILWAY_TOKEN value
   # Save as RAILWAY_TOKEN_STAGING

   # Link to production project
   railway link
   # Select: subjunctive-practice-production

   # Get production token
   railway variables
   # Save as RAILWAY_TOKEN_PRODUCTION
   ```

**What You'll Have:**
- ✅ 2 Railway projects (staging + production)
- ✅ 2 PostgreSQL databases
- ✅ 2 Redis instances
- ✅ 4 connection strings
- ✅ 2 Railway tokens

### 🔴 TASK 2.2: Vercel Setup (10-15 minutes)

**Frontend Hosting on Vercel**

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub
   - Import your repository

2. **Create Two Projects**

   a. **Staging Project:**
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Login to Vercel
   vercel login

   # Create staging project
   vercel --name subjunctive-practice-staging
   # Answer prompts:
   # - Set up and deploy? Yes
   # - Which scope? Your account
   # - Link to existing project? No
   # - What's your project's name? subjunctive-practice-staging
   # - In which directory is your code? ./
   # - Want to override settings? No

   # Get staging project ID and token
   vercel project ls
   # Save project ID
   ```

   b. **Production Project:**
   ```bash
   vercel --name subjunctive-practice-production
   # Same prompts as above but with "production" name
   ```

3. **Get Vercel Tokens**

   - Go to https://vercel.com/account/tokens
   - Click "Create Token"
   - Name: `SUBJUNCTIVE_PRACTICE_CI`
   - Scope: Full Account
   - Expiration: No expiration (or 1 year)
   - Copy token immediately (save as `VERCEL_TOKEN`)

4. **Get Vercel Org/Team ID**

   ```bash
   # Get your organization ID
   vercel teams ls
   # OR
   # Go to Vercel dashboard → Settings → General
   # Copy "Team ID" or "User ID"
   # Save as VERCEL_ORG_ID
   ```

**What You'll Have:**
- ✅ 2 Vercel projects (staging + production)
- ✅ 1 Vercel token
- ✅ 1 Org ID
- ✅ 2 Project IDs

### 🔴 TASK 2.3: Sentry Setup (10 minutes)

**Error Tracking with Sentry**

1. **Create Sentry Account**
   - Go to https://sentry.io
   - Sign up (free plan available)

2. **Create Two Projects**

   a. **Backend Project:**
   ```
   - Click "Create Project"
   - Platform: Python → FastAPI
   - Alert frequency: Default
   - Project name: subjunctive-practice-backend
   - Team: Default
   - Click "Create Project"
   - Copy DSN (starts with https://...@sentry.io/...)
   - Save as SENTRY_DSN_BACKEND
   ```

   b. **Frontend Project:**
   ```
   - Click "Create Project"
   - Platform: JavaScript → Next.js
   - Project name: subjunctive-practice-frontend
   - Copy DSN
   - Save as SENTRY_DSN_FRONTEND
   ```

**What You'll Have:**
- ✅ 2 Sentry projects
- ✅ 2 Sentry DSNs

### 🔴 TASK 2.4: Optional Services (5-10 minutes)

**Codecov (Optional - Code Coverage)**

1. Go to https://codecov.io
2. Sign up with GitHub
3. Enable repository: `subjunctive_practice`
4. Copy upload token
5. Save as `CODECOV_TOKEN`

**Slack Notifications (Optional)**

1. Go to your Slack workspace
2. Create new app: https://api.slack.com/apps
3. Enable Incoming Webhooks
4. Create webhook for channel (e.g., #deployments)
5. Copy webhook URL
6. Save as `SLACK_WEBHOOK_URL`

---

## Phase 3: Code Cleanup (PROGRAMMATIC)

### 🟢 TASK 3.1: Consolidate Duplicate Components (PROGRAMMATIC)

**What I'll do:**
- Analyze `/components` vs `/src/components`
- Identify duplicates and conflicts
- Merge to single `/components` directory
- Update all imports across the codebase
- Remove old `/src/components` directory
- Test that build still works

**Estimated time:** 10-15 minutes
**Ready for me to execute?** (Say "yes")

### 🟢 TASK 3.2: Standardize Port Configuration (PROGRAMMATIC)

**What I'll do:**
- Set standard ports:
  - Backend dev: 8000
  - Backend prod: 8000
  - Frontend dev: 3000
  - Frontend prod: 3000
- Update all documentation
- Update all config files
- Update docker-compose.yml
- Update .env.example files

**Ready for me to execute?** (Say "yes")

### 🟢 TASK 3.3: Clean Legacy Test Directory (PROGRAMMATIC)

**What I'll do:**
- Archive `/tests` to `/tests-legacy`
- Update test scripts to use backend/tests and frontend/tests
- Update CI workflows
- Add README explaining migration

**Ready for me to execute?** (Say "yes")

### 🟢 TASK 3.4: Update Environment Templates (PROGRAMMATIC)

**What I'll do:**
- Create comprehensive `.env.production.template`
- Create comprehensive `.env.staging.template`
- Add detailed comments for each variable
- Document required vs optional variables
- Create setup validation script

**Ready for me to execute?** (Say "yes")

---

## Phase 4: GitHub Secrets Configuration (MANUAL)

### 🔴 TASK 4.1: Configure GitHub Secrets (20-30 minutes)

**18 Secrets Required**

1. **Go to GitHub Repository Settings**
   ```
   https://github.com/[your-username]/subjunctive_practice/settings/secrets/actions
   ```

2. **Add Each Secret** (Click "New repository secret" for each)

#### Backend Secrets (6 secrets)

```bash
Name: RAILWAY_TOKEN_STAGING
Value: [from Task 2.1 - Railway staging token]

Name: RAILWAY_TOKEN_PRODUCTION
Value: [from Task 2.1 - Railway production token]

Name: DATABASE_URL_STAGING
Value: [from Task 2.1 - PostgreSQL staging connection string]

Name: DATABASE_URL_PRODUCTION
Value: [from Task 2.1 - PostgreSQL production connection string]

Name: OPENAI_API_KEY
Value: [from Task 1.1 - New OpenAI key]

Name: SECRET_KEY_PRODUCTION
Value: [Generate with: openssl rand -hex 32]
```

#### Frontend Secrets (6 secrets)

```bash
Name: VERCEL_TOKEN
Value: [from Task 2.2 - Vercel token]

Name: VERCEL_ORG_ID
Value: [from Task 2.2 - Vercel org/team ID]

Name: VERCEL_PROJECT_ID_STAGING
Value: [from Task 2.2 - Staging project ID]

Name: VERCEL_PROJECT_ID_PRODUCTION
Value: [from Task 2.2 - Production project ID]

Name: NEXT_PUBLIC_API_URL_STAGING
Value: https://[your-railway-staging-url].up.railway.app

Name: NEXT_PUBLIC_API_URL_PRODUCTION
Value: https://[your-railway-production-url].up.railway.app
```

#### Monitoring Secrets (3 secrets)

```bash
Name: SENTRY_DSN_BACKEND
Value: [from Task 2.3 - Backend Sentry DSN]

Name: SENTRY_DSN_FRONTEND
Value: [from Task 2.3 - Frontend Sentry DSN]

Name: CODECOV_TOKEN
Value: [from Task 2.4 - Optional, skip if not using]
```

#### Notification Secrets (1 secret)

```bash
Name: SLACK_WEBHOOK_URL
Value: [from Task 2.4 - Optional, skip if not using]
```

#### Redis Secrets (2 secrets)

```bash
Name: REDIS_URL_STAGING
Value: [from Task 2.1 - Redis staging URL]

Name: REDIS_URL_PRODUCTION
Value: [from Task 2.1 - Redis production URL]
```

### 🟢 TASK 4.2: Verify Secrets Configuration (PROGRAMMATIC)

**What I'll do:**
- Run the verification script: `scripts/verify-ci-setup.sh`
- Check that all 18 secrets are configured
- Validate secret format (URLs, tokens, etc.)
- Test GitHub Actions can access secrets
- Generate verification report

**Ready for me to execute?** (Say "yes" after Task 4.1 complete)

---

## Phase 5: CI/CD Verification (PROGRAMMATIC)

### 🟢 TASK 5.1: Run Backend CI Pipeline (PROGRAMMATIC)

**What I'll do:**
- Create test branch: `test/ci-verification`
- Make small change to trigger CI
- Push to GitHub
- Monitor backend-ci.yml workflow
- Verify: tests pass, coverage reports, Docker build
- Share results with you

**Ready for me to execute?** (Say "yes")

### 🟢 TASK 5.2: Run Frontend CI Pipeline (PROGRAMMATIC)

**What I'll do:**
- Use same test branch
- Trigger frontend-ci.yml workflow
- Verify: tests pass, type checking, E2E tests, bundle analysis
- Share results with you

**Ready for me to execute?** (Say "yes")

### 🟢 TASK 5.3: Run Security Scan (PROGRAMMATIC)

**What I'll do:**
- Trigger security.yml workflow
- Run: CodeQL, Snyk, TruffleHog, Trivy
- Review scan results
- Fix any critical/high severity issues
- Share security report

**Ready for me to execute?** (Say "yes")

---

## Phase 6: Staging Deployment (PROGRAMMATIC)

### 🟢 TASK 6.1: Deploy Backend to Staging (PROGRAMMATIC)

**What I'll do:**
- Run: `./scripts/deploy.sh backend staging`
- Deploy to Railway staging environment
- Run database migrations
- Wait for health checks
- Verify API endpoints
- Test authentication endpoints
- Test exercise endpoints

**Ready for me to execute?** (Say "yes")

### 🟢 TASK 6.2: Deploy Frontend to Staging (PROGRAMMATIC)

**What I'll do:**
- Run: `./scripts/deploy.sh frontend staging`
- Deploy to Vercel staging
- Configure environment variables
- Wait for build completion
- Run Lighthouse CI
- Verify deployment URL
- Test frontend loads and connects to backend

**Ready for me to execute?** (Say "yes")

### 🟢 TASK 6.3: Run Integration Tests on Staging (PROGRAMMATIC)

**What I'll do:**
- Run E2E tests against staging environment
- Test: authentication flow, practice sessions, progress tracking
- Verify: API integration, database persistence, Redis caching
- Generate test report
- Fix any integration issues

**Ready for me to execute?** (Say "yes")

---

## Phase 7: Production Deployment (MANUAL)

### 🔴 TASK 7.1: Manual Production Approval (MANUAL - 5 minutes)

**What You'll Do:**

1. **Review Staging Environment**
   - Visit staging URL: https://[staging-frontend].vercel.app
   - Test major features:
     - [ ] User registration
     - [ ] User login
     - [ ] Practice session
     - [ ] Progress tracking
     - [ ] Settings updates
   - Check Sentry for errors: https://sentry.io
   - Review logs on Railway/Vercel

2. **Approve Production Deployment**
   - Go to GitHub Actions
   - Find pending deployment workflow
   - Review changes
   - Click "Approve" button

### 🟢 TASK 7.2: Execute Production Deployment (PROGRAMMATIC)

**What I'll do:**
- Trigger production deployment workflow
- Deploy backend to Railway production
- Deploy frontend to Vercel production
- Run production database migrations
- Execute smoke tests
- Monitor health checks
- Verify all services are up

**This runs automatically after your approval in Task 7.1**

### 🔴 TASK 7.3: DNS Configuration (MANUAL - Optional)

**If you want a custom domain:**

1. **For Backend (Railway):**
   ```
   - Go to Railway project → Settings → Domains
   - Click "Generate Domain" (free .railway.app domain)
   - OR add custom domain and configure DNS:
     - Type: CNAME
     - Name: api (or backend)
     - Value: [railway-provided-domain]
   ```

2. **For Frontend (Vercel):**
   ```
   - Go to Vercel project → Settings → Domains
   - Click "Add Domain"
   - Enter your domain: subjunctive-practice.com
   - Follow DNS configuration instructions:
     - Type: A
     - Name: @
     - Value: 76.76.21.21
     - Type: CNAME
     - Name: www
     - Value: cname.vercel-dns.com
   ```

---

## Phase 8: Post-Deployment Verification (VERIFICATION)

### 🔵 TASK 8.1: Production Health Checks (VERIFICATION)

**We'll verify together:**

```bash
# Backend health
curl https://[production-backend-url]/health
# Should return: {"status": "healthy"}

# Backend API
curl https://[production-backend-url]/api/health
# Should return database and redis status

# Frontend
curl -I https://[production-frontend-url]
# Should return: HTTP/2 200

# Test endpoints
curl https://[production-backend-url]/api/exercises
# Should return exercises list (may require auth)
```

### 🔵 TASK 8.2: Monitor First 24 Hours (VERIFICATION)

**We'll check:**

- [ ] Sentry for errors (aim for <1% error rate)
- [ ] Railway logs for exceptions
- [ ] Vercel logs for frontend errors
- [ ] Database connection pool usage
- [ ] Redis hit rate
- [ ] API response times (<500ms p95)
- [ ] Frontend Core Web Vitals

### 🟢 TASK 8.3: Set Up Monitoring Alerts (PROGRAMMATIC)

**What I'll do:**
- Configure Sentry alerts for error spikes
- Set up Railway resource alerts
- Configure Vercel build failure notifications
- Create uptime monitoring (UptimeRobot)
- Set up daily digest emails

**Ready for me to execute?** (Say "yes")

---

## Rollback Procedures

### 🔴 Emergency Rollback (MANUAL - 2 minutes)

**If production is broken:**

1. **Rollback Backend (Railway):**
   ```bash
   railway rollback
   # OR via dashboard:
   # Go to Deployments → Find last working deployment → Click "Redeploy"
   ```

2. **Rollback Frontend (Vercel):**
   ```bash
   vercel rollback [deployment-url]
   # OR via dashboard:
   # Go to Deployments → Find last working deployment → Click "Promote to Production"
   ```

3. **Notify Team:**
   ```bash
   # Post to Slack (if configured)
   curl -X POST $SLACK_WEBHOOK_URL \
     -H 'Content-Type: application/json' \
     -d '{"text":"🚨 Production rollback executed"}'
   ```

### 🟢 Database Rollback (PROGRAMMATIC)

**What I'll do if database migration fails:**
- Stop application
- Restore database from latest backup
- Rollback Alembic migrations
- Verify data integrity
- Restart application

---

## Timeline Summary

| Phase | Type | Time | When |
|-------|------|------|------|
| Phase 1 | Manual | 5 min | NOW |
| Phase 2 | Manual | 30-45 min | After Phase 1 |
| Phase 3 | Programmatic | 30 min | Parallel with Phase 2 |
| Phase 4 | Manual | 20-30 min | After Phase 2 |
| Phase 5 | Programmatic | 15 min | After Phase 4 |
| Phase 6 | Programmatic | 30 min | After Phase 5 |
| Phase 7 | Manual + Auto | 10 min | After Phase 6 |
| Phase 8 | Verification | Ongoing | After Phase 7 |

**Total Manual Time:** ~1.5-2 hours
**Total Programmatic Time:** ~1.5 hours
**Total Time to Production:** 3-4 hours

---

## Next Steps

**Tell me when you're ready for each phase:**

1. Say **"Start Phase 1"** - I'll remove the exposed API key
2. Complete Phase 2 manually (external services)
3. Say **"Start Phase 3"** - I'll clean up the code
4. Complete Phase 4 manually (GitHub secrets)
5. Say **"Start Phase 5"** - I'll verify CI/CD
6. Say **"Start Phase 6"** - I'll deploy to staging
7. Approve production in GitHub (Phase 7)
8. Say **"Start Phase 8"** - We'll verify together

---

## Support & Troubleshooting

If you encounter issues:

1. Check `/docs/TROUBLESHOOTING.md`
2. Check `/docs/CI-CD-QUICK-REFERENCE.md`
3. Check platform status pages:
   - Railway: https://status.railway.app
   - Vercel: https://www.vercel-status.com
   - GitHub: https://www.githubstatus.com

---

**Ready to begin? Say "Start Phase 1" when you're ready!**
