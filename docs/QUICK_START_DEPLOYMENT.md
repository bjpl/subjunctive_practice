# Quick Start Deployment Guide

**Fastest path from code to production in 3-4 hours**

---

## 🚀 TL;DR

1. **You do manually (1.5-2 hours):**
   - Revoke exposed API key, get new one
   - Create Railway + Vercel accounts
   - Configure 18 GitHub secrets

2. **I do programmatically (1.5 hours):**
   - Clean up code
   - Run CI/CD tests
   - Deploy to staging
   - Deploy to production

3. **We verify together (30 minutes):**
   - Test production
   - Monitor for issues

---

## 📋 Your Manual Checklist

### Critical (Do First - 15 minutes)

- [ ] **Revoke API Key**: Go to https://platform.openai.com/api-keys → Delete key `sk-proj-Rv5J8LTz...`
- [ ] **Get New Key**: Create new key → Save it securely
- [ ] **Tell me**: Say "Start Phase 1"

### External Services (30-45 minutes)

- [ ] **Railway** (15 min): https://railway.app
  - Create 2 projects: staging + production
  - Add PostgreSQL + Redis to each
  - Save 4 connection strings + 2 tokens

- [ ] **Vercel** (10 min): https://vercel.com
  - Create 2 projects: staging + production
  - Get 1 token + 1 org ID + 2 project IDs

- [ ] **Sentry** (10 min): https://sentry.io
  - Create 2 projects: backend + frontend
  - Save 2 DSNs

### GitHub Secrets (20-30 minutes)

Go to: `https://github.com/[user]/subjunctive_practice/settings/secrets/actions`

Add these 18 secrets (copy/paste from your notes):

**Backend (6):**
```
RAILWAY_TOKEN_STAGING
RAILWAY_TOKEN_PRODUCTION
DATABASE_URL_STAGING
DATABASE_URL_PRODUCTION
OPENAI_API_KEY (new key)
SECRET_KEY_PRODUCTION (generate: openssl rand -hex 32)
```

**Frontend (6):**
```
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID_STAGING
VERCEL_PROJECT_ID_PRODUCTION
NEXT_PUBLIC_API_URL_STAGING
NEXT_PUBLIC_API_URL_PRODUCTION
```

**Monitoring (3):**
```
SENTRY_DSN_BACKEND
SENTRY_DSN_FRONTEND
CODECOV_TOKEN (optional)
```

**Cache (2):**
```
REDIS_URL_STAGING
REDIS_URL_PRODUCTION
```

**Notifications (1):**
```
SLACK_WEBHOOK_URL (optional)
```

### Production Approval (5 minutes)

- [ ] Test staging: Visit staging URL
- [ ] Review: Check logs, errors, performance
- [ ] Approve: Go to GitHub Actions → Approve deployment

---

## 🤖 What I'll Do Automatically

### Phase 1: Security (5 min)
- Remove exposed API key from .env.production
- Create .env.production.template
- Update .gitignore
- Git commit

### Phase 3: Code Cleanup (30 min)
- Consolidate duplicate components
- Standardize ports (backend:8000, frontend:3000)
- Archive legacy tests
- Update environment templates

### Phase 5: CI/CD Verification (15 min)
- Run backend tests
- Run frontend tests
- Run security scans
- Generate reports

### Phase 6: Staging Deployment (30 min)
- Deploy backend to Railway staging
- Deploy frontend to Vercel staging
- Run database migrations
- Run integration tests

### Phase 7: Production Deployment (auto after your approval)
- Deploy backend to Railway production
- Deploy frontend to Vercel production
- Run production migrations
- Execute smoke tests

---

## 💬 What to Say to Me

| When | Say This |
|------|----------|
| After revoking API key | "Start Phase 1" |
| After creating Railway/Vercel | "Start Phase 3" |
| After adding GitHub secrets | "Start Phase 5" |
| After CI passes | "Start Phase 6" |
| After testing staging | "Ready for Phase 8" |

---

## ⏱️ Timeline

```
Hour 1: You set up external services
Hour 2: You configure GitHub secrets | I clean up code (parallel)
Hour 3: I verify CI/CD and deploy staging
Hour 4: You approve, I deploy production, we verify together
```

---

## 🆘 Quick Troubleshooting

**"Railway database won't connect"**
→ Check DATABASE_URL format: `postgresql://user:pass@host:port/db`

**"Vercel build fails"**
→ Check NEXT_PUBLIC_API_URL is set in Vercel project settings

**"GitHub Actions fail"**
→ Run `./scripts/verify-ci-setup.sh` to check all 18 secrets

**"Need to rollback"**
→ Railway: `railway rollback`
→ Vercel: Dashboard → Deployments → Promote previous

---

## 📚 Full Documentation

- **Detailed Walkthrough**: `/docs/DEPLOYMENT_WALKTHROUGH.md`
- **CI/CD Reference**: `/docs/CI-CD-QUICK-REFERENCE.md`
- **Troubleshooting**: `/docs/TROUBLESHOOTING.md`
- **API Docs**: `/docs/API_DOCUMENTATION.md`

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Backend health: `curl https://[prod-backend]/health`
- [ ] Frontend loads: Visit production URL
- [ ] Can register new user
- [ ] Can login
- [ ] Can start practice session
- [ ] Progress saves correctly
- [ ] No errors in Sentry

---

**Ready? Tell me: "Start Phase 1"**
