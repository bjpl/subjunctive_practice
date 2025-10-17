# Windows/WSL Setup Guide - Spanish Subjunctive Practice

## ✅ Completed Steps

### What's Already Done
1. ✅ **Environment Configuration**
   - `backend/.env` created with SQLite configuration
   - `frontend/.env.local` configured for local development

2. ✅ **Frontend Setup**
   - npm dependencies installed (855 packages)
   - Node.js v22.20.0 available
   - npm 10.9.3 available

3. ✅ **Docker Available**
   - Docker version 27.5.1 installed and ready

---

## 🚀 Quick Start (Docker Method - Recommended for WSL)

Since sudo is disabled on your WSL and python3-venv/pip are not available, **Docker is the best solution** for running the backend.

### Option 1: Docker Compose (Full Stack)

```bash
# From project root
cd /mnt/c/Users/brand/Development/Project_Workspace/active-development/language-learning/subjunctive_practice

# Start both backend and database with Docker
cd backend
docker-compose up -d

# Backend will be available at http://localhost:8000
```

### Option 2: Run Backend Docker Container Manually

```bash
# Build backend Docker image
cd backend
docker build -t subjunctive-backend:latest .

# Run backend container
docker run -d \
  --name subjunctive-api \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd):/app \
  subjunctive-backend:latest

# Check logs
docker logs -f subjunctive-api
```

### Option 3: Frontend Only (Mock Backend)

Since the frontend is ready, you can start it independently:

```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:3000**

Note: API calls will fail without backend, but you can see the UI.

---

## 🔧 Alternative: Enable WSL Sudo (If You Want Native Python)

### Enable Sudo in Windows Settings

1. Open **Windows Settings**
2. Go to **Privacy & Security** → **For Developers**
3. Enable **Developer Mode**
4. This should enable sudo in WSL

### Then Install Python Tools

```bash
sudo apt update
sudo apt install python3.12-venv python3-pip
```

### Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📋 Current System Status

| Component | Status | Version | Notes |
|-----------|--------|---------|-------|
| Python | ⚠️ Limited | 3.12.3 | No venv/pip modules |
| Node.js | ✅ Ready | 22.20.0 | Fully functional |
| npm | ✅ Ready | 10.9.3 | Fully functional |
| Docker | ✅ Ready | 27.5.1 | **Recommended for backend** |
| Frontend Dependencies | ✅ Installed | - | 855 packages installed |
| Backend .env | ✅ Created | - | SQLite configured |
| Frontend .env | ✅ Configured | - | API URL set |
| WSL Sudo | ❌ Disabled | - | Need to enable in Settings |

---

## 🎯 Recommended Approach

**Use Docker for backend + npm for frontend:**

1. **Start Backend with Docker:**
   ```bash
   cd backend
   docker-compose up -d
   ```

2. **Start Frontend with npm:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

---

## 🐛 Troubleshooting

### Issue: Docker command not found
**Solution:** Start Docker Desktop for Windows

### Issue: Port already in use
**Solution:**
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Issue: Frontend can't connect to backend
**Solution:** Check that:
1. Backend Docker container is running: `docker ps`
2. Backend is on port 8000: `curl http://localhost:8000/health`
3. Frontend .env.local has correct API URL

---

## ⏭️ Next Steps After Setup

1. **Test Backend Health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Register Test User:**
   - Open: http://localhost:3000/auth/register
   - Create account
   - Login and test

3. **Run Tests:**
   ```bash
   # Backend (in Docker)
   docker exec -it subjunctive-api pytest

   # Frontend
   cd frontend
   npm test
   ```

4. **Set Up Git Workflow:**
   ```bash
   git checkout -b develop
   git push -u origin develop
   ```

---

**Estimated Setup Time:** 5-10 minutes with Docker
