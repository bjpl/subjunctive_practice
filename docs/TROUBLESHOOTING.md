# Troubleshooting Guide

## Overview

This guide helps you resolve common issues encountered when developing, deploying, or using the Spanish Subjunctive Practice application.

## Table of Contents

1. [Setup Issues](#setup-issues)
2. [Backend Problems](#backend-problems)
3. [Frontend Problems](#frontend-problems)
4. [Database Issues](#database-issues)
5. [Authentication Errors](#authentication-errors)
6. [API Connection Problems](#api-connection-problems)
7. [Build and Deployment Issues](#build-and-deployment-issues)
8. [Performance Issues](#performance-issues)

---

## Setup Issues

### Problem: Python Virtual Environment Not Activating

**Symptoms:**
- `venv\Scripts\activate` not found
- Command not recognized

**Solutions:**

**Windows:**
```bash
# Try PowerShell activation
venv\Scripts\Activate.ps1

# Or use cmd
venv\Scripts\activate.bat

# If execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
# Make sure you're in the backend directory
cd backend
source venv/bin/activate

# Check Python version
python --version  # Should be 3.10+
```

---

### Problem: Node Modules Installation Fails

**Symptoms:**
- `npm install` errors
- Permission denied
- EACCES errors

**Solutions:**

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If permission issues (Linux/macOS)
sudo npm install -g npm@latest
```

**Windows specific:**
```bash
# Run as Administrator
npm install --force

# Or use yarn instead
npm install -g yarn
yarn install
```

---

### Problem: Environment Variables Not Loading

**Symptoms:**
- `NEXT_PUBLIC_API_URL` is undefined
- Backend can't find `SECRET_KEY`
- Database connection fails

**Solutions:**

**Backend (.env):**
```bash
# Ensure .env file exists in backend/
ls backend/.env

# Check file format (no spaces around =)
SECRET_KEY=your-secret-key  # Correct
SECRET_KEY = your-secret-key  # Wrong!

# Verify environment is loaded
python -c "from core.config import get_settings; print(get_settings().SECRET_KEY)"
```

**Frontend (.env.local):**
```bash
# Ensure .env.local exists in frontend/
ls frontend/.env.local

# Must start with NEXT_PUBLIC_ for client access
NEXT_PUBLIC_API_URL=http://localhost:8000/api  # Correct
API_URL=http://localhost:8000/api  # Wrong! Won't work in browser

# Restart dev server after changing env vars
npm run dev
```

---

## Backend Problems

### Problem: Port 8000 Already in Use

**Symptoms:**
- `Address already in use`
- `OSError: [Errno 48] Address already in use`

**Solutions:**

**Find and kill process:**

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or one-liner
kill -9 $(lsof -t -i:8000)
```

**Or use different port:**
```bash
uvicorn main:app --port 8001
```

---

### Problem: Module Import Errors

**Symptoms:**
- `ModuleNotFoundError: No module named 'fastapi'`
- Import errors for installed packages

**Solutions:**

```bash
# Verify virtual environment is activated
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt

# If still failing, check Python path
python -c "import sys; print(sys.path)"

# Rebuild virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Problem: Database Migration Fails

**Symptoms:**
- `alembic upgrade head` fails
- Migration version conflicts
- Table already exists errors

**Solutions:**

```bash
# Check current migration version
alembic current

# Check migration history
alembic history

# Reset database (WARNING: deletes all data)
python scripts/init_db.py --reset

# Or manually drop and recreate
# PostgreSQL:
psql -U postgres
DROP DATABASE subjunctive_practice;
CREATE DATABASE subjunctive_practice;
\q

# Then run migrations
alembic upgrade head

# If version conflict, downgrade first
alembic downgrade base
alembic upgrade head
```

---

### Problem: SQLAlchemy Connection Errors

**Symptoms:**
- `OperationalError: could not connect to server`
- Database connection timeout
- Authentication failed for user

**Solutions:**

**PostgreSQL:**
```bash
# Check PostgreSQL is running
# macOS:
brew services list
brew services start postgresql

# Linux:
sudo systemctl status postgresql
sudo systemctl start postgresql

# Windows:
# Check Services app for PostgreSQL service

# Test connection
psql -U postgres -h localhost

# Check DATABASE_URL format
# Correct:
DATABASE_URL=postgresql://username:password@localhost:5432/db_name

# Verify credentials
psql -U username -d db_name
```

**SQLite (Development):**
```bash
# Use SQLite for quick testing
DATABASE_URL=sqlite:///./dev.db

# Check file permissions
ls -la dev.db
chmod 644 dev.db
```

---

## Frontend Problems

### Problem: Next.js Build Fails

**Symptoms:**
- `npm run build` errors
- TypeScript compilation errors
- Module not found

**Solutions:**

```bash
# Clear Next.js cache
rm -rf .next

# Clear node_modules
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run type-check

# Build with verbose output
npm run build -- --debug

# Check for missing dependencies
npm list
```

---

### Problem: Hydration Errors

**Symptoms:**
- `Warning: Text content did not match`
- `Error: Hydration failed`
- Content mismatch between server and client

**Solutions:**

```tsx
// Suppress specific hydration warnings
<div suppressHydrationWarning>
  {typeof window !== 'undefined' ? clientValue : serverValue}
</div>

// Use useEffect for client-only rendering
const [mounted, setMounted] = useState(false);

useEffect(() => {
  setMounted(true);
}, []);

if (!mounted) return null;
```

---

### Problem: Redux State Not Persisting

**Symptoms:**
- State resets on page reload
- localStorage not saving
- Hydration warnings with redux-persist

**Solutions:**

```typescript
// Check localStorage quota
if (typeof window !== 'undefined') {
  const used = new Blob(Object.values(localStorage)).size;
  console.log(`LocalStorage used: ${used / 1024}KB`);
}

// Clear persisted state
localStorage.removeItem('persist:root');
localStorage.clear();

// Verify persist config
const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth', 'settings'], // Only persist these
  blacklist: ['api'] // Don't persist these
};
```

---

### Problem: Tailwind Styles Not Applying

**Symptoms:**
- Classes not working
- Styles not updating
- Production build missing styles

**Solutions:**

```bash
# Restart dev server
npm run dev

# Clear build cache
rm -rf .next
npm run dev

# Check tailwind.config.ts content paths
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  // ...
}

# Rebuild CSS
npm run build
```

---

## Database Issues

### Problem: Database Connection Refused

**Symptoms:**
- `Connection refused`
- `could not connect to server`

**Solutions:**

```bash
# Check database is running
# PostgreSQL:
pg_isready
sudo systemctl status postgresql

# Check connection parameters
# Verify host, port, username, password
psql -h localhost -p 5432 -U postgres

# Check firewall rules
# Allow port 5432 for PostgreSQL
sudo ufw allow 5432

# Update pg_hba.conf for local connections
# Find pg_hba.conf
sudo find / -name pg_hba.conf

# Add line:
# local   all             all                                     trust
# host    all             all             127.0.0.1/32            md5
```

---

### Problem: Permission Denied for Database

**Symptoms:**
- `permission denied for database`
- `role "user" does not exist`

**Solutions:**

```sql
-- Connect as postgres superuser
psql -U postgres

-- Create user
CREATE USER your_username WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE subjunctive_practice TO your_username;

-- Grant schema permissions
\c subjunctive_practice
GRANT ALL ON SCHEMA public TO your_username;
GRANT ALL ON ALL TABLES IN SCHEMA public TO your_username;
```

---

## Authentication Errors

### Problem: 401 Unauthorized on All Requests

**Symptoms:**
- All API calls return 401
- Token appears valid
- Login successful but subsequent requests fail

**Solutions:**

```typescript
// Check token is being sent
apiClient.interceptors.request.use((config) => {
  const token = store.getState().auth.accessToken;
  console.log('Token:', token); // Debug
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Verify token format
// Should be: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
// NOT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (missing "Bearer")

// Check token expiration
const payload = JSON.parse(atob(token.split('.')[1]));
console.log('Expires:', new Date(payload.exp * 1000));
```

---

### Problem: Token Refresh Loop

**Symptoms:**
- Infinite refresh requests
- 401 errors in loop
- Browser hangs

**Solutions:**

```typescript
// Add flag to prevent refresh loop
let isRefreshing = false;

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !isRefreshing) {
      isRefreshing = true;
      try {
        await store.dispatch(refreshAccessToken());
        // Retry original request
        return apiClient.request(error.config);
      } catch (refreshError) {
        // Refresh failed, logout user
        store.dispatch(logout());
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);
```

---

### Problem: CORS Errors

**Symptoms:**
- `Access to fetch blocked by CORS policy`
- `No 'Access-Control-Allow-Origin' header`
- Preflight request fails

**Solutions:**

**Backend (.env):**
```env
# Add frontend URL to allowed origins
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
CORS_ALLOW_CREDENTIALS=true
```

**Backend (main.py):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Check browser console:**
```javascript
// Verify request headers
console.log('Origin:', window.location.origin);

// Check response headers
fetch('http://localhost:8000/api/health')
  .then(res => {
    console.log('CORS headers:', res.headers.get('access-control-allow-origin'));
  });
```

---

## API Connection Problems

### Problem: Frontend Can't Connect to Backend

**Symptoms:**
- `Network Error`
- `ERR_CONNECTION_REFUSED`
- API requests timeout

**Solutions:**

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check backend logs
tail -f backend/backend.log

# Verify API URL in frontend
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Check for typos
# Wrong: http://localhost:8000/api/v1
# Right: http://localhost:8000/api

# Test with browser
# Open: http://localhost:8000/api/docs

# Check firewall
# Temporarily disable and test
```

---

### Problem: API Returns 404 for Valid Endpoints

**Symptoms:**
- `/api/exercises` returns 404
- Swagger docs work but requests fail
- Routes not found

**Solutions:**

```python
# Check router prefix in main.py
app.include_router(exercises.router, prefix="/api")
# NOT: prefix="/api/v1" (unless that's intended)

# Check route definition
@router.get("/exercises")  # Correct
@router.get("/api/exercises")  # Wrong! Double prefix

# Verify in Swagger
# http://localhost:8000/api/docs
# Check listed endpoints

# Test with curl
curl -v http://localhost:8000/api/exercises
```

---

## Build and Deployment Issues

### Problem: Docker Build Fails

**Symptoms:**
- `docker build` errors
- Permission denied
- Network timeout

**Solutions:**

```bash
# Check Docker is running
docker ps

# Build with no cache
docker build --no-cache -t app .

# Check Dockerfile syntax
docker build --dry-run -t app .

# View build logs
docker build -t app . 2>&1 | tee build.log

# Common fixes:
# 1. Update base image
FROM python:3.10-slim  # Use specific version

# 2. Clear Docker cache
docker system prune -a

# 3. Check .dockerignore
# Make sure not ignoring required files
```

---

### Problem: Production Build Errors

**Symptoms:**
- `npm run build` works locally but fails in CI/CD
- Missing environment variables
- Out of memory

**Solutions:**

```bash
# Increase Node memory
NODE_OPTIONS=--max_old_space_size=4096 npm run build

# Check environment variables
env | grep NEXT_PUBLIC

# Disable linting during build (temporary)
# next.config.js
module.exports = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true, // Not recommended!
  }
}

# Build with verbose logging
npm run build -- --debug
```

---

## Performance Issues

### Problem: Slow API Responses

**Symptoms:**
- Requests take > 1 second
- Timeout errors
- Database queries slow

**Solutions:**

```python
# Add request timing middleware
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.url.path} took {process_time:.2f}s")
    return response

# Check database queries
# Use SQLAlchemy query logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Add indexes
# See DATABASE_SCHEMA.md for index recommendations

# Use connection pooling
# PostgreSQL DATABASE_URL with pool settings
DATABASE_URL=postgresql://user:pass@localhost/db?pool_size=10&max_overflow=20
```

---

### Problem: Frontend Performance Issues

**Symptoms:**
- Slow page loads
- UI freezes
- High memory usage

**Solutions:**

```typescript
// Use React.memo for expensive components
export const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* Complex rendering */}</div>;
});

// Lazy load components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Loading />,
  ssr: false
});

// Optimize images
import Image from 'next/image';

<Image
  src="/image.png"
  width={500}
  height={300}
  alt="Description"
  loading="lazy"
/>

// Use useMemo for expensive calculations
const expensiveValue = useMemo(() => {
  return complexCalculation(data);
}, [data]);

// Check bundle size
npm run build
# Look for large chunks

// Analyze bundle
npm install --save-dev @next/bundle-analyzer
ANALYZE=true npm run build
```

---

## Getting Help

### Debugging Checklist

1. ☐ Check error messages carefully
2. ☐ Review relevant logs (backend.log, browser console)
3. ☐ Verify environment variables
4. ☐ Check service status (database, backend, frontend)
5. ☐ Test in isolation (API with curl, components with Storybook)
6. ☐ Review recent changes (git diff)
7. ☐ Search documentation and GitHub issues

### Log Locations

**Backend:**
- Application logs: `backend/backend.log`
- Uvicorn logs: Console output
- Database logs: PostgreSQL logs directory

**Frontend:**
- Browser console: F12 → Console
- Network tab: F12 → Network
- Next.js logs: Terminal running `npm run dev`

### Useful Commands

```bash
# Backend health check
curl http://localhost:8000/health

# Frontend build check
npm run build && npm start

# Database connection test
psql -U postgres -c "SELECT version();"

# View running processes
ps aux | grep python
ps aux | grep node

# Check ports
netstat -an | grep 8000
netstat -an | grep 3000

# View logs
tail -f backend/backend.log
tail -f /var/log/postgresql/postgresql.log
```

---

## Additional Resources

- [Integration Guide](./INTEGRATION_GUIDE.md)
- [API Documentation](./API_DOCUMENTATION.md)
- [Database Schema](./DATABASE_SCHEMA.md)
- [Development Guide](./DEVELOPMENT.md)
- GitHub Issues: Report bugs and feature requests
