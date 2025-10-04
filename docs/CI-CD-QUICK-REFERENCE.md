# CI/CD Quick Reference Guide

## Quick Start

### 1. Initial Setup (One-time)
```bash
# Verify setup
./scripts/verify-ci-setup.sh

# Configure secrets
./scripts/setup-ci-secrets.sh
```

### 2. Common Commands

#### Run Tests Locally
```bash
# Backend
cd backend
pytest --cov=backend --cov-report=term-missing
black --check .
flake8 .
mypy .

# Frontend
cd frontend
npm run type-check
npm run lint
npm run test:coverage
npm run test:e2e
```

#### Build Locally
```bash
# Backend
cd backend
docker build -t backend:local .

# Frontend
cd frontend
npm run build
```

## Workflow Triggers

| Workflow | Trigger | Description |
|----------|---------|-------------|
| Backend CI | Push/PR to main/develop (backend/**) | Tests, linting, security |
| Frontend CI | Push/PR to main/develop (frontend/**) | Tests, linting, E2E |
| Security | Push/PR, Daily 2 AM UTC | Security scans |
| Integration | Push/PR, Nightly 3 AM UTC | Full-stack tests |
| Deploy Backend | Push to main, Manual | Railway deployment |
| Deploy Frontend | Push to main, Manual | Vercel deployment |
| Release | Version tag (v*.*.*) | Release automation |
| PR Checks | PR open/update | PR validation |

## Required Secrets

### Backend (8)
- `RAILWAY_STAGING_TOKEN`
- `RAILWAY_PRODUCTION_TOKEN`
- `STAGING_DATABASE_URL`
- `STAGING_REDIS_URL`
- `STAGING_SECRET_KEY`
- `OPENAI_API_KEY`
- `CODECOV_TOKEN`
- `SLACK_WEBHOOK`

### Frontend (8)
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `PREVIEW_API_URL`
- `PRODUCTION_API_URL`
- `PRODUCTION_FRONTEND_URL`
- `ANALYTICS_ID`
- `SLACK_WEBHOOK`

### Security (2)
- `CODECOV_TOKEN`
- `SNYK_TOKEN`

## Manual Deployments

### Deploy to Staging
```bash
# Via GitHub CLI
gh workflow run deploy-backend.yml -f environment=staging
gh workflow run deploy-frontend.yml -f environment=preview
```

### Deploy to Production
```bash
# Via GitHub UI (requires approval)
# 1. Go to Actions tab
# 2. Select deployment workflow
# 3. Click "Run workflow"
# 4. Select "production"
# 5. Wait for approval notification
# 6. Approve deployment
```

### Create Release
```bash
# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Or via workflow
gh workflow run release.yml -f version=v1.0.0
```

## Common Issues

### Test Failures
```bash
# Check logs in GitHub Actions
# Run locally to debug
pytest -v --tb=short  # Backend
npm test -- --verbose  # Frontend
```

### Build Failures
```bash
# Check environment variables
# Verify dependencies
npm ci  # Frontend
pip install -r requirements-dev.txt  # Backend
```

### Deployment Failures
```bash
# Check service status
railway status  # Backend
vercel inspect  # Frontend

# Check logs
railway logs  # Backend
vercel logs  # Frontend
```

## PR Workflow

1. Create feature branch
2. Make changes
3. Run tests locally
4. Push to GitHub
5. Create PR
6. CI runs automatically
7. Review and address feedback
8. Merge when approved
9. Auto-deploy to staging
10. Manual deploy to production

## Monitoring

### Check Workflow Status
```bash
# List recent runs
gh run list

# View specific run
gh run view <run-id>

# Watch current run
gh run watch
```

### View Logs
```bash
# Download logs
gh run download <run-id>

# View logs in browser
gh run view <run-id> --web
```

## Best Practices

### Before Pushing
- [ ] Run tests locally
- [ ] Check linting
- [ ] Update documentation
- [ ] Write meaningful commit messages

### PR Guidelines
- [ ] Keep PRs small (<500 lines)
- [ ] Write descriptive title
- [ ] Fill out PR template
- [ ] Link related issues
- [ ] Request reviews

### Release Checklist
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Tag with semantic version
- [ ] Test on staging first
- [ ] Monitor after deployment

## Useful Links

- [GitHub Actions](https://github.com/your-org/subjunctive-practice/actions)
- [Railway Dashboard](https://railway.app)
- [Vercel Dashboard](https://vercel.com/dashboard)
- [Codecov Dashboard](https://codecov.io)
- [Full Documentation](./CI-CD-SETUP.md)

## Emergency Procedures

### Rollback Deployment
```bash
# Backend (Railway)
railway rollback

# Frontend (Vercel)
# Use Vercel dashboard to redeploy previous version
```

### Disable Workflow
```yaml
# Add to workflow file temporarily
on:
  workflow_dispatch: {}  # Manual only
```

### Emergency Hotfix
```bash
# Create hotfix branch
git checkout -b hotfix/critical-fix main

# Make fix
# ...

# Push and deploy immediately
git push origin hotfix/critical-fix

# Create PR and deploy
gh pr create --title "Hotfix: Critical fix" --base main
gh workflow run deploy-backend.yml -f environment=production
```

## Support

- **Documentation**: `docs/CI-CD-SETUP.md`
- **Scripts**: `scripts/`
- **Issues**: Create GitHub issue with `ci-cd` label
- **Slack**: #devops channel (if configured)
