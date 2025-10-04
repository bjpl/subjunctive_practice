# ⚡ Quick Start Deployment Checklist
## Get Your App Live in 60 Minutes

**Use this checklist to deploy step-by-step without missing anything.**

Print this out or keep it open in a second window as you work through deployment.

---

## 🎯 Pre-Deployment (10 minutes)

### Create Accounts

- [ ] GitHub account created → https://github.com/signup
- [ ] Railway account created → https://railway.app (sign in with GitHub)
- [ ] Vercel account created → https://vercel.com (sign in with GitHub)

### Install Tools

```bash
# Railway CLI
npm install -g @railway/cli

# Vercel CLI
npm install -g vercel

# Verify installations
railway --version
vercel --version
```

- [ ] Railway CLI installed
- [ ] Vercel CLI installed

---

## 📦 Step 1: Git Setup (5 minutes)

### Initialize Repository

```bash
cd subjunctive_practice
git init
git add .
git commit -m "Initial commit: Spanish Subjunctive Practice"
```

- [ ] Git repository initialized
- [ ] All files committed

### Push to GitHub

```bash
# Create repo on GitHub: https://github.com/new
# Name: spanish-subjunctive-practice
# Private repository

# Then push:
git remote add origin https://github.com/YOUR_USERNAME/spanish-subjunctive-practice.git
git branch -M main
git push -u origin main
```

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Repository visible at github.com/YOUR_USERNAME/spanish-subjunctive-practice

---

## 🗄️ Step 2: Backend Deployment - Railway (20 minutes)

### Create Project

- [ ] Login to Railway: `railway login`
- [ ] Link project: `railway init` (select "Create new project")
- [ ] Name project: "subjunctive-practice-backend"

### Add Database

In Railway web dashboard:
- [ ] Click "+ New" → "Database" → "Add PostgreSQL"
- [ ] Wait for provisioning (30 seconds)
- [ ] Verify DATABASE_URL appears in "Variables" tab

### Set Environment Variables

In Railway dashboard → Your service → Variables tab:

```
ENVIRONMENT=production
DEBUG=false
API_V1_PREFIX=/api
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

**Generate JWT Secret:**
```bash
openssl rand -hex 32
# Copy output and add as:
JWT_SECRET_KEY=<paste_output_here>
```

- [ ] All environment variables set
- [ ] JWT_SECRET_KEY is at least 32 characters
- [ ] DATABASE_URL is present (auto-added by Railway)

### Create railway.json

**Ask Claude Code:**
```
Create railway.json configuration file for Python FastAPI app in backend/ directory.
Include:
- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
- Health check endpoint: /health
- Set working directory to backend/
```

- [ ] `railway.json` created
- [ ] Committed and pushed to GitHub

### Deploy Backend

```bash
git add railway.json backend/
git commit -m "Add Railway deployment config"
git push origin main
```

In Railway dashboard:
- [ ] Click your service → "Settings" → "Service"
- [ ] Root Directory: `/backend`
- [ ] Click "Deploy"
- [ ] Wait for build (3-5 minutes)
- [ ] Check "Deployments" tab for status
- [ ] Green checkmark = success

### Verify Backend

Railway provides a public URL like: `https://subjunctive-practice-backend-production.up.railway.app`

Test it:
```bash
curl https://YOUR_BACKEND_URL/health
# Expected: {"status":"healthy",...}
```

- [ ] Backend URL obtained: `________________`
- [ ] Health endpoint returns 200 OK
- [ ] Database connection shows true

---

## 🎨 Step 3: Frontend Deployment - Vercel (15 minutes)

### Update Frontend Environment

Edit `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=https://YOUR_BACKEND_URL/api
NEXT_PUBLIC_APP_NAME=Spanish Subjunctive Practice
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=false
```

- [ ] `.env.local` updated with Railway backend URL

**Ask Claude Code (optional):**
```
Create vercel.json configuration with:
- Proper routing for Next.js 14
- Security headers
- Caching rules for static assets
- Redirect rules
Save to frontend/ directory
```

- [ ] `vercel.json` created (if using Claude Code)

### Deploy Frontend

**Option A: Vercel Dashboard (Easiest)**

1. Go to https://vercel.com/new
2. Import `spanish-subjunctive-practice` repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
4. Environment Variables:
   - Add all from `.env.local` above
5. Click "Deploy"
6. Wait 2-3 minutes

- [ ] Vercel project created
- [ ] Environment variables added
- [ ] Deployment started

**Option B: Vercel CLI (Faster for Re-deploys)**

```bash
cd frontend
vercel login
vercel --prod

# Follow prompts:
# Setup and deploy? Yes
# Which scope? (select your account)
# Link to existing project? No
# Project name: subjunctive-practice
# Which directory? ./
# Override settings? No
```

- [ ] Vercel CLI login successful
- [ ] Deployment initiated

### Verify Frontend

Vercel provides URL like: `https://subjunctive-practice.vercel.app`

- [ ] Frontend URL obtained: `________________`
- [ ] Page loads successfully
- [ ] Can navigate to /auth/register
- [ ] No console errors in browser DevTools

---

## 🔗 Step 4: Connect Frontend ↔ Backend (10 minutes)

### Update Backend CORS

In Railway dashboard → Variables:

```
CORS_ORIGINS=https://YOUR_VERCEL_URL,http://localhost:3000
```

- [ ] CORS_ORIGINS updated with Vercel URL
- [ ] Backend redeployed (happens automatically)
- [ ] Wait 1 minute for restart

### Test Integration

1. Open `https://YOUR_VERCEL_URL`
2. Click "Get Started" or "Sign Up"
3. Fill in registration form
4. Submit

**Expected Results:**
- [ ] No CORS errors in browser console (F12 → Console tab)
- [ ] Registration succeeds or shows validation errors (not network errors)
- [ ] Can login after registration
- [ ] Dashboard loads with your username

**If CORS Errors:**
```
Check:
1. CORS_ORIGINS includes exact Vercel URL (including https://)
2. No typos in URL
3. Backend restarted (Railway dashboard → Deployments → Latest should be after CORS change)
```

---

## ✅ Step 5: End-to-End Test (10 minutes)

### Complete User Journey

- [ ] **Register Account**
  - Open https://YOUR_VERCEL_URL/auth/register
  - Create account: username, email, password
  - Submission succeeds

- [ ] **Login**
  - Redirected to /auth/login
  - Enter credentials
  - Login succeeds
  - Redirected to /dashboard

- [ ] **Dashboard Loads**
  - See welcome message with your username
  - Stats show: 0 exercises, Level 1, 0 streak
  - No errors in console

- [ ] **Start Practice**
  - Click "Start Practice" or go to /practice
  - Exercise loads with Spanish question
  - Can type answer
  - Click submit
  - Feedback appears (correct/incorrect)

- [ ] **Check Progress**
  - Go to /progress or /dashboard
  - Stats updated (1 exercise completed)
  - Accuracy calculated
  - No errors

### Cross-Browser Test

- [ ] Chrome: Works
- [ ] Firefox: Works
- [ ] Safari (if on Mac): Works
- [ ] Mobile browser (phone): Works

### Performance Check

Open Chrome DevTools → Lighthouse:
- [ ] Run audit on homepage
- [ ] Performance score >85
- [ ] Accessibility score >90

---

## 🔒 Step 6: Security Checklist (5 minutes)

### Verify Security Settings

**Backend:**
- [ ] JWT_SECRET_KEY is random, not default value
- [ ] DEBUG=false in production
- [ ] CORS_ORIGINS only includes your domains (not `*`)
- [ ] Rate limiting enabled

**Frontend:**
- [ ] No API keys in client-side code
- [ ] HTTPS enabled (Vercel does automatically)
- [ ] Environment variables prefixed with `NEXT_PUBLIC_` only for public data

**Accounts:**
- [ ] Enable 2FA on GitHub
- [ ] Enable 2FA on Railway
- [ ] Enable 2FA on Vercel

### Test Rate Limiting

```bash
# Try to spam the API
for i in {1..70}; do
  curl https://YOUR_BACKEND_URL/api/exercises
done

# Expected: Last 10 requests should return 429 Too Many Requests
```

- [ ] Rate limiting works (429 errors after 60 requests/minute)

---

## 📊 Step 7: Monitoring Setup (5 minutes)

### Railway Monitoring

In Railway dashboard:
- [ ] Click your backend service
- [ ] Open "Metrics" tab
- [ ] Verify metrics are appearing:
  - CPU usage
  - Memory usage
  - Network traffic

### Vercel Analytics

In Vercel dashboard:
- [ ] Click your project
- [ ] Open "Analytics" tab
- [ ] Verify tracking enabled (may take 24h for first data)

### Database Backups

In Railway dashboard:
- [ ] Click PostgreSQL database
- [ ] Open "Backups" tab
- [ ] Verify auto-backups enabled
- [ ] Default: Daily backups, 7-day retention

---

## 🎉 Deployment Complete!

### Your Live URLs

**Frontend**: https://________________.vercel.app
**Backend**: https://________________.railway.app
**API Docs**: https://YOUR_BACKEND_URL/api/docs

### Save These for Reference

```
GitHub Repo: https://github.com/YOUR_USERNAME/spanish-subjunctive-practice
Railway Project: https://railway.app/project/YOUR_PROJECT_ID
Vercel Project: https://vercel.com/YOUR_TEAM/subjunctive-practice

Backend URL: https://________________
Frontend URL: https://________________

JWT Secret: ________________ (save to password manager!)
Stripe Keys (later): pk_live_____  sk_live_____
```

---

## 🚨 Troubleshooting Common Issues

### Issue: "Cannot connect to backend"

**Symptoms**: CORS errors, network errors in console

**Fix:**
1. Check Railway backend logs: `railway logs --tail 50`
2. Verify CORS_ORIGINS includes Vercel URL exactly
3. Restart backend: Railway dashboard → Redeploy

---

### Issue: "Database connection failed"

**Symptoms**: Backend returns 500 errors, health check shows database_connected: false

**Fix:**
1. Verify DATABASE_URL exists in Railway variables
2. Check PostgreSQL service is running (Railway dashboard → Database)
3. Restart both services

---

### Issue: "Vercel build failed"

**Symptoms**: Deployment shows red X

**Fix:**
1. Check build logs in Vercel dashboard
2. Common issues:
   - Missing dependencies: Run `npm install` locally and commit `package-lock.json`
   - TypeScript errors: Run `npm run type-check` locally and fix errors
   - Environment variables: Verify all NEXT_PUBLIC_ vars are set in Vercel

---

### Issue: "JWT token errors"

**Symptoms**: Login works but immediate logout, "Invalid token" errors

**Fix:**
1. Verify JWT_SECRET_KEY is same in Railway (backend uses it to sign)
2. Check token expiration not too short (1440 min = 24 hours)
3. Clear localStorage in browser: DevTools → Application → Local Storage → Clear
4. Login again

---

## 📝 Next Steps After Deployment

### Immediate (Next 24 Hours)

- [ ] Test app yourself - complete 10 exercises
- [ ] Note any bugs or UX issues
- [ ] Share link with 3 friends for feedback
- [ ] Set up error monitoring (optional: Sentry)

### This Week

- [ ] Fix top 3 bugs reported
- [ ] Add Google Analytics or PostHog
- [ ] Write down monetization plan (see MONETIZATION_ROADMAP.md)
- [ ] Create feedback form in app

### This Month

- [ ] Get to 25+ registered users
- [ ] Collect feedback on pricing
- [ ] Implement Stripe integration (if feedback is positive)
- [ ] Launch on Product Hunt or Reddit

---

## ✅ Deployment Verification Signature

**I confirm that:**

- [ ] App is live and accessible via public URL
- [ ] Registration → Login → Practice → Progress flow works
- [ ] No errors in browser console
- [ ] Backend health check returns healthy
- [ ] Database is connected and persisting data
- [ ] I can use this app to practice Spanish subjunctive right now

**Deployed on**: ________________ (date)
**Time taken**: _______ minutes
**Issues encountered**: ___________________________

---

**Congratulations! Your app is live! 🎊**

Now go practice some Spanish subjunctive on your own app! 🇪🇸
