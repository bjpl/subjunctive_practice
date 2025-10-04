# Backend Quick Reference Card
Spanish Subjunctive Practice - FastAPI Backend

## Essential Commands

### Local Development
```bash
# First time setup
cd backend
cp .env.example .env
pip install -r requirements-dev.txt
docker-compose up -d postgres redis
alembic upgrade head
uvicorn main:app --reload

# Daily development
make dev              # Start dev server
make test             # Run tests
make format           # Format code
make lint             # Run linters
```

### Docker Commands
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Reset everything
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Commands
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View status
alembic current
alembic history
```

### Railway Deployment
```bash
# Install CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# View logs
railway logs

# Open dashboard
railway open
```

### Render Deployment
```bash
# Just push to main branch
git add .
git commit -m "Deploy to Render"
git push origin main

# Render auto-deploys from GitHub
```

## Essential Files

| File | Purpose |
|------|---------|
| `.env` | Your local configuration (DO NOT COMMIT) |
| `requirements.txt` | Production dependencies |
| `Dockerfile` | Container build instructions |
| `docker-compose.yml` | Local development stack |
| `railway.toml` | Railway deployment config |
| `render.yaml` | Render deployment config |
| `Makefile` | Development shortcuts |

## Environment Variables (Required)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379/0

# Security
JWT_SECRET_KEY=your-secret-key-here
SESSION_SECRET_KEY=your-session-key-here

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# CORS
CORS_ORIGINS=http://localhost:3000
```

## Generate Secrets
```bash
# Generate secure keys
openssl rand -hex 32

# Or in Python
python -c "import secrets; print(secrets.token_hex(32))"
```

## API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API documentation
http://localhost:8000/docs

# Alternative docs
http://localhost:8000/redoc
```

## Troubleshooting

### Port Already in Use
```bash
# Find process on port 8000
lsof -i :8000          # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps
pg_isready -h localhost -p 5432

# Restart database
docker-compose restart postgres
```

### Redis Connection Failed
```bash
# Check Redis is running
docker-compose ps
redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Clear Everything
```bash
# Remove all containers and volumes
docker-compose down -v

# Remove Python cache
make clean

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific test
pytest tests/test_api.py::test_health_check

# Verbose
pytest -v -s
```

## Code Quality

```bash
# Format code
black .
isort .

# Or use make
make format

# Check formatting
black --check .

# Run linters
flake8 .
mypy .
pylint **/*.py

# Or use make
make lint
```

## Deployment Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Generate secure JWT_SECRET_KEY
- [ ] Generate secure SESSION_SECRET_KEY
- [ ] Set OPENAI_API_KEY
- [ ] Configure CORS_ORIGINS
- [ ] Update DATABASE_URL
- [ ] Update REDIS_URL
- [ ] Run database migrations
- [ ] Test all endpoints
- [ ] Enable HTTPS
- [ ] Set up monitoring (optional)
- [ ] Configure custom domain (optional)

## Resource Links

- **API Docs**: http://localhost:8000/docs
- **Railway**: https://railway.app/dashboard
- **Render**: https://dashboard.render.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Deployment Guide**: See `backend-deployment.md`

## Common Issues

**Import errors**: Run `pip install -r requirements.txt`
**Database errors**: Run `alembic upgrade head`
**Port conflicts**: Change PORT in .env or kill process
**Docker errors**: Run `docker-compose down -v && docker-compose up -d`
**Test failures**: Check TEST_DATABASE_URL in .env

## Quick File Reference

```
backend/
├── core/
│   ├── logging_config.py    # Structured logging
│   ├── config.py            # App configuration
│   ├── security.py          # Auth & security
│   └── middleware.py        # Request middleware
├── utils/
│   ├── helpers.py           # Utility functions
│   └── spanish_grammar.py   # Spanish language rules
├── scripts/
│   └── init-db.sql          # Database init
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── Dockerfile               # Container build
├── docker-compose.yml       # Local dev stack
├── railway.toml             # Railway config
├── render.yaml              # Render config
├── Makefile                 # Dev commands
└── pyproject.toml           # Poetry config
```

---

**Need help?** Check the full deployment guide: `docs/backend-deployment.md`
