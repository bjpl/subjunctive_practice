# Quick Setup Instructions - Spanish Subjunctive Practice

## Phase 1 Complete Status Report

### ✅ COMPLETED: Environment Configuration Files Created

**Backend `.env` file created** at: `backend/.env`
- Configured for SQLite (development-friendly, no PostgreSQL required)
- JWT secret key set for development
- CORS configured for localhost:3000
- OpenAI integration ready (optional, commented out)

**Frontend `.env.local` file verified** at: `frontend/.env.local`
- API URL pointing to localhost:8000/api
- Development mode enabled

---

## Next Steps to Complete Setup

### Prerequisites Required

1. **Python 3.10+** ✅ (Python 3.12.3 detected)
2. **Node.js 18+** (needs verification)
3. **pip/venv** ❌ (python3-venv not installed)

### Step-by-Step Setup Guide

#### 1. Install Python venv (Required)

```bash
# On Ubuntu/Debian/WSL
sudo apt update
sudo apt install python3.12-venv

# On macOS (using Homebrew)
brew install python@3.12
```

#### 2. Set Up Backend

```bash
# Navigate to project root
cd /mnt/c/Users/brand/Development/Project_Workspace/active-development/language-learning/subjunctive_practice

# Create virtual environment
python3 -m venv backend/venv

# Activate virtual environment
# On Windows/WSL:
source backend/venv/bin/activate
# On Windows CMD:
# backend\venv\Scripts\activate.bat

# Install dependencies
pip install -r backend/requirements.txt

# Run Alembic migrations (create database schema)
cd backend
alembic upgrade head

# Start backend server
uvicorn main:app --reload
```

Backend will be available at: **http://localhost:8000**
API Docs: **http://localhost:8000/api/docs**

#### 3. Set Up Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

#### 4. Verify Setup

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy",...}`

2. **Frontend Access:**
   - Open browser: http://localhost:3000
   - Should see the landing page

3. **Register Test User:**
   - Go to: http://localhost:3000/auth/register
   - Create an account
   - Login and start practicing!

---

## Current Project Status

### ✅ Completed
- [x] Environment configuration files created
- [x] SQLite database configured (no PostgreSQL needed for dev)
- [x] CORS and security settings configured
- [x] Frontend environment configured

### 🔄 In Progress
- [ ] Python venv installation (blocked by system dependency)
- [ ] Backend dependencies installation
- [ ] Database migration execution
- [ ] Backend server startup verification

### ⏳ Pending
- [ ] Frontend npm install
- [ ] End-to-end integration test
- [ ] Git workflow setup (develop branch)

---

## Troubleshooting

### Issue: `python3-venv not available`
**Solution:** Install python3-venv:
```bash
sudo apt install python3.12-venv
```

### Issue: `alembic: command not found`
**Solution:** Ensure virtual environment is activated and dependencies installed:
```bash
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### Issue: Database connection errors
**Solution:** Check that:
1. `.env` file exists in `backend/` directory
2. `DATABASE_URL` is set to SQLite: `sqlite+aiosqlite:///./subjunctive_practice.db`
3. Alembic migrations have been run: `alembic upgrade head`

### Issue: CORS errors in frontend
**Solution:** Check that:
1. Backend is running on port 8000
2. Frontend `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
3. Backend `.env` has CORS_ORIGINS including `http://localhost:3000`

---

## What Was Done in Phase 1, Step 1

1. ✅ **Analyzed project structure** - Confirmed FastAPI backend, Next.js frontend
2. ✅ **Created backend/.env** - Configured for SQLite with development settings
3. ✅ **Verified frontend/.env.local** - Already existed with correct configuration
4. ✅ **Documented setup process** - Created this guide
5. ⚠️ **Identified blocker** - python3-venv not installed on system

## Next Immediate Action

**Install python3-venv:**
```bash
sudo apt install python3.12-venv
```

Then continue with:
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

---

**Estimated Time to Running Application:** 15-30 minutes (after installing python3-venv)
