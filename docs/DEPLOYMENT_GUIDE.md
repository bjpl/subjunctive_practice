# 🚀 Deployment Guide - Spanish Subjunctive Practice

## Quick Setup (15 Minutes)

This guide will get you from zero to deployed in 15 minutes using GitHub Actions, Railway, and Vercel.

### Prerequisites

- GitHub account
- Railway account (free tier available)
- Vercel account (free tier available) 
- Git CLI installed
- Node.js 18+ installed
- Python 3.11+ installed

### 1. Fork and Clone Repository

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/subjunctive_practice.git
cd subjunctive_practice
```

### 2. Setup Railway (Backend + Database)

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Create Railway Project**
   ```bash
   railway new spanish-subjunctive-backend
   cd backend
   railway link
   ```

3. **Add PostgreSQL Database**
   ```bash
   railway add postgresql
   railway add redis
   ```

4. **Deploy Backend**
   ```bash
   railway up
   ```

### 3. Setup Vercel (Frontend)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   vercel login
   ```

2. **Deploy Frontend**
   ```bash
   vercel --prod
   ```

### 4. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and Variables → Actions

Add these secrets:

#### Railway Secrets
```
RAILWAY_TOKEN=your_railway_token
RAILWAY_SERVICE_ID_STAGING=your_staging_service_id
RAILWAY_SERVICE_ID_PRODUCTION=your_production_service_id
```

#### Vercel Secrets
```
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
```

#### Environment URLs
```
STAGING_FRONTEND_URL=https://your-app-staging.vercel.app
STAGING_API_URL=https://your-backend-staging.railway.app
PRODUCTION_FRONTEND_URL=https://your-app.vercel.app
PRODUCTION_API_URL=https://your-backend.railway.app
```

#### Monitoring (Optional)
```
SENTRY_DSN=your_sentry_dsn
LHCI_GITHUB_APP_TOKEN=your_lighthouse_token
```

### 5. Environment Configuration

1. **Copy environment templates**
   ```bash
   cp config/environments/.env.example .env.local
   # Edit .env.local with your local development settings
   ```

2. **Set Railway Environment Variables**
   ```bash
   railway variables set DATABASE_URL=${{PostgreSQL.DATABASE_URL}}
   railway variables set REDIS_URL=${{Redis.REDIS_URL}}
   railway variables set ENVIRONMENT=production
   ```

3. **Set Vercel Environment Variables**
   ```bash
   vercel env add REACT_APP_API_URL production
   vercel env add REACT_APP_ENVIRONMENT production
   ```

### 6. Test Deployment

Push to main branch to trigger deployment:

```bash
git add .
git commit -m "Initial deployment setup"
git push origin main
```

## 🔄 Environments

### Development
- **Frontend**: `http://localhost:3000`
- **Backend**: `http://localhost:8000`
- **Database**: Local PostgreSQL or SQLite

### Staging
- **Branch**: `develop` or `staging`
- **Frontend**: Auto-deployed to Vercel preview
- **Backend**: Auto-deployed to Railway staging service
- **Database**: Shared staging PostgreSQL

### Production
- **Branch**: `main`
- **Frontend**: Auto-deployed to Vercel production
- **Backend**: Auto-deployed to Railway production service
- **Database**: Production PostgreSQL with backups

## 🚦 Deployment Pipeline

### Automatic Deployments

1. **Pull Request**: Runs tests and quality checks
2. **Staging Branch**: Auto-deploys to staging environment
3. **Main Branch**: Auto-deploys to production with additional security scans

### Manual Deployments

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production

# Rollback production
./scripts/rollback.sh production
```

### Zero-Downtime Strategy

- **Frontend**: Vercel provides automatic zero-downtime deployments
- **Backend**: Railway uses rolling deployments
- **Database**: Migrations run before app deployment

## 📊 Monitoring

### Health Checks

- **API Health**: `GET /health`
- **Detailed Health**: `GET /health/detailed`
- **Database**: `GET /health/db`
- **Readiness**: `GET /health/ready`

### Monitoring Dashboards

1. **Railway Dashboard**: Backend metrics and logs
2. **Vercel Analytics**: Frontend performance and usage
3. **GitHub Actions**: Deployment status and history
4. **Sentry** (optional): Error tracking and performance

### Alerts

- Automatic health checks every 15 minutes
- Performance degradation detection
- Error rate monitoring
- Resource usage alerts

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Fails**
   ```bash
   # Check Railway database status
   railway status
   railway logs
   ```

2. **Frontend Build Fails**
   ```bash
   # Check Vercel deployment logs
   vercel logs
   npm run build  # Test locally
   ```

3. **CI/CD Pipeline Fails**
   ```bash
   # Check GitHub Actions logs
   # Common fixes:
   - Update Node/Python versions
   - Clear npm/pip cache
   - Check environment variables
   ```

### Debug Commands

```bash
# Local development
npm run dev                 # Start frontend
cd backend && uvicorn main:app --reload  # Start backend

# Test deployments
npm run test               # Run all tests
npm run lint              # Check code quality
npm run type-check        # TypeScript validation

# Database operations
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 🔐 Security

### Secrets Management

- Never commit secrets to repository
- Use environment variables for all sensitive data
- Rotate secrets regularly
- Use Railway/Vercel secret management

### Security Headers

Automatically configured via `vercel.json`:
- Content Security Policy
- X-Frame-Options
- X-XSS-Protection
- And more...

## 📈 Performance

### Frontend Optimization

- Automatic code splitting (Vite)
- Image optimization (Vercel)
- CDN distribution (Vercel Edge Network)
- Lighthouse monitoring

### Backend Optimization

- Database connection pooling
- Redis caching
- Async request handling
- Resource monitoring

## 🚨 Emergency Procedures

### Immediate Rollback

```bash
# Option 1: Use rollback script
./scripts/rollback.sh production

# Option 2: Revert via Railway
railway rollback

# Option 3: Redeploy previous version
git revert HEAD
git push origin main
```

### Emergency Contacts

1. Check GitHub Actions for deployment status
2. Check Railway/Vercel dashboards for service health
3. Review Sentry for error details
4. Contact team via configured alerts

## 📝 Maintenance

### Regular Tasks

- **Weekly**: Review deployment metrics and error rates
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Review and optimize database performance
- **As needed**: Scale resources based on usage

### Backup Strategy

- **Database**: Automatic daily backups (Railway)
- **Code**: Git repository with branch protection
- **Configs**: Environment variables backed up separately

---

## 🎯 Success Checklist

After following this guide, you should have:

- ✅ Automated CI/CD pipeline
- ✅ Staging and production environments  
- ✅ Database migrations automated
- ✅ Health monitoring setup
- ✅ Zero-downtime deployments
- ✅ Emergency rollback procedures
- ✅ Security best practices implemented

**Total setup time**: ~15 minutes for basic setup, ~30 minutes including monitoring

Need help? Check the troubleshooting section or create an issue in the repository.