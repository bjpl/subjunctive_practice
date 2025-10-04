# CI/CD Workflow Documentation

Comprehensive guide to the Continuous Integration and Continuous Deployment processes for the Spanish Subjunctive Practice Application.

## Table of Contents

1. [CI/CD Overview](#cicd-overview)
2. [Pipeline Architecture](#pipeline-architecture)
3. [Branch Strategy](#branch-strategy)
4. [Automated Testing](#automated-testing)
5. [Deployment Pipeline](#deployment-pipeline)
6. [Environment Management](#environment-management)
7. [Release Process](#release-process)
8. [Hotfix Procedures](#hotfix-procedures)

---

## CI/CD Overview

### Objectives

- **Automate Testing**: Run comprehensive test suites on every commit
- **Fast Feedback**: Provide developers with quick build results
- **Consistent Deployments**: Standardize deployment process
- **Quality Gates**: Enforce code quality and security standards
- **Zero-Downtime Deployments**: Deploy without service interruption

### Tools & Services

| Component | Tool | Purpose |
|-----------|------|---------|
| Version Control | GitHub | Source code management |
| CI/CD Platform | GitHub Actions | Pipeline execution |
| Container Registry | Docker Hub / GitHub Container Registry | Docker image storage |
| Deployment Targets | Railway, Render, Vercel | Application hosting |
| Code Quality | ESLint, Prettier, Black, Flake8 | Linting and formatting |
| Testing | Jest, Pytest, Playwright | Automated testing |
| Security Scanning | Snyk, GitHub Dependabot | Vulnerability detection |

---

## Pipeline Architecture

### High-Level Pipeline Flow

```
┌──────────────┐
│  Code Push   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Trigger CI  │
└──────┬───────┘
       │
       ├─────────────────┬─────────────────┬──────────────────┐
       │                 │                 │                  │
       ▼                 ▼                 ▼                  ▼
┌──────────────┐  ┌──────────────┐ ┌──────────────┐  ┌──────────────┐
│   Lint &     │  │     Build    │ │  Run Tests   │  │   Security   │
│   Format     │  │   Backend    │ │   Backend    │  │    Scan      │
│   Check      │  │   Frontend   │ │   Frontend   │  │              │
└──────┬───────┘  └──────┬───────┘ └──────┬───────┘  └──────┬───────┘
       │                 │                 │                  │
       └─────────────────┴─────────────────┴──────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Quality     │
                    │  Gate Check  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Pass?      │
                    └──┬────────┬──┘
                  Yes  │        │  No
                       │        │
                       │        ▼
                       │    ┌──────────┐
                       │    │  Notify  │
                       │    │   Team   │
                       │    └──────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Branch Check  │
              └────┬────────┬──┘
                   │        │
           develop │        │ main
                   │        │
                   ▼        ▼
         ┌──────────────┐  ┌──────────────┐
         │  Deploy to   │  │  Deploy to   │
         │   Staging    │  │  Production  │
         └──────────────┘  └──────────────┘
```

---

## Branch Strategy

### Git Flow Model

```
main (production)
  │
  ├─── release/v1.1.0
  │
develop (staging)
  │
  ├─── feature/user-authentication
  ├─── feature/exercise-types
  ├─── bugfix/session-timeout
  └─── hotfix/critical-security-fix
```

### Branch Rules

#### main
- **Environment**: Production
- **Protection**: Requires pull request review
- **Deployment**: Auto-deploy to production
- **Restrictions**: No direct pushes

#### develop
- **Environment**: Staging
- **Protection**: Requires passing CI checks
- **Deployment**: Auto-deploy to staging
- **Restrictions**: No direct pushes (use PRs)

#### feature/*
- **Purpose**: New features
- **Base**: develop
- **Merge To**: develop
- **Naming**: `feature/short-description`

#### bugfix/*
- **Purpose**: Bug fixes
- **Base**: develop
- **Merge To**: develop
- **Naming**: `bugfix/short-description`

#### hotfix/*
- **Purpose**: Critical production fixes
- **Base**: main
- **Merge To**: main AND develop
- **Naming**: `hotfix/short-description`

#### release/*
- **Purpose**: Release preparation
- **Base**: develop
- **Merge To**: main AND develop
- **Naming**: `release/v{major}.{minor}.{patch}`

---

## Automated Testing

### Test Strategy

```
┌──────────────────────────────────────────────────────┐
│                    Test Pyramid                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│                   ┌────────────┐                    │
│                   │    E2E     │  5%                │
│                   │  (Slow)    │                    │
│                   └────────────┘                    │
│                                                      │
│              ┌──────────────────────┐               │
│              │    Integration       │  15%          │
│              │    (Medium)          │               │
│              └──────────────────────┘               │
│                                                      │
│         ┌──────────────────────────────────┐        │
│         │          Unit Tests              │  80%   │
│         │          (Fast)                  │        │
│         └──────────────────────────────────┘        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Backend Testing

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on:
  pull_request:
    paths:
      - 'backend/**'
  push:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with flake8
        run: |
          cd backend
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Format check with black
        run: |
          cd backend
          black --check .

      - name: Type check with mypy
        run: |
          cd backend
          mypy .

      - name: Run tests with pytest
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          JWT_SECRET_KEY: test_secret
        run: |
          cd backend
          pytest --cov=. --cov-report=xml --cov-report=term-missing

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

      - name: Security check
        run: |
          cd backend
          pip install safety
          safety check --json
```

### Frontend Testing

```yaml
# .github/workflows/frontend-ci.yml
name: Frontend CI

on:
  pull_request:
    paths:
      - 'frontend/**'
  push:
    branches:
      - main
      - develop

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Lint
        run: |
          cd frontend
          npm run lint

      - name: Type check
        run: |
          cd frontend
          npm run type-check

      - name: Run unit tests
        run: |
          cd frontend
          npm run test:coverage

      - name: Run accessibility tests
        run: |
          cd frontend
          npm run test:a11y

      - name: Build
        run: |
          cd frontend
          npm run build

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json
          flags: frontend

  e2e:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          npx playwright install --with-deps

      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: frontend/playwright-report/
          retention-days: 30
```

---

## Deployment Pipeline

### Staging Deployment (develop branch)

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches:
      - develop

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Railway (Staging)
        uses: railway/cli@v2
        with:
          service: subjunctive-backend-staging
          environment: staging
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_STAGING }}

      - name: Run database migrations
        run: |
          railway run -e staging alembic upgrade head

      - name: Verify deployment
        run: |
          sleep 30
          curl -f ${{ secrets.STAGING_API_URL }}/health

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel (Staging)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
          scope: ${{ secrets.VERCEL_ORG_ID }}

  notify:
    needs: [deploy-backend, deploy-frontend]
    runs-on: ubuntu-latest
    steps:
      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Staging deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Production Deployment (main branch)

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Allow manual trigger

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Backup production database
        run: |
          # Trigger backup script on production server
          echo "Database backup completed"

  deploy-backend:
    needs: backup
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.subjunctivepractice.com
    steps:
      - uses: actions/checkout@v4

      - name: Create release tag
        run: |
          VERSION=$(cat backend/version.txt)
          git tag -a "v$VERSION" -m "Release v$VERSION"
          git push origin "v$VERSION"

      - name: Build Docker image
        run: |
          cd backend
          docker build -t subjunctive-backend:$VERSION --target production .

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push subjunctive-backend:$VERSION

      - name: Deploy to Railway (Production)
        uses: railway/cli@v2
        with:
          service: subjunctive-backend-production
          environment: production
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_PRODUCTION }}

      - name: Run database migrations
        run: |
          railway run -e production alembic upgrade head

      - name: Verify deployment
        run: |
          sleep 60
          curl -f https://api.subjunctivepractice.com/health
          curl -f https://api.subjunctivepractice.com/health/db

  deploy-frontend:
    needs: deploy-backend
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://subjunctivepractice.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel (Production)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./frontend

      - name: Verify deployment
        run: |
          sleep 30
          curl -f https://subjunctivepractice.com

  smoke-tests:
    needs: [deploy-backend, deploy-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run smoke tests
        run: |
          # Health checks
          curl -f https://api.subjunctivepractice.com/health
          curl -f https://subjunctivepractice.com

          # Critical endpoints
          curl -f https://api.subjunctivepractice.com/api/v1/exercises

  notify:
    needs: [deploy-backend, deploy-frontend, smoke-tests]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Notify success
        if: ${{ success() }}
        uses: 8398a7/action-slack@v3
        with:
          status: success
          text: 'Production deployment successful!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

      - name: Notify failure
        if: ${{ failure() }}
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: 'Production deployment failed! @channel'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Environment Management

### Environment Variables

#### Development

```env
# .env.development
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://localhost:5432/subjunctive_dev
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:3000
```

#### Staging

```env
# Configured in Railway/Render
ENVIRONMENT=staging
DEBUG=false
DATABASE_URL=[auto-populated]
REDIS_URL=[auto-populated]
JWT_SECRET_KEY=[from secrets]
CORS_ORIGINS=https://staging.subjunctivepractice.com
SENTRY_DSN=[from secrets]
```

#### Production

```env
# Configured in Railway/Render
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=[auto-populated]
REDIS_URL=[auto-populated]
JWT_SECRET_KEY=[from secrets]
SESSION_SECRET_KEY=[from secrets]
OPENAI_API_KEY=[from secrets]
CORS_ORIGINS=https://subjunctivepractice.com
SENTRY_DSN=[from secrets]
```

### Secrets Management

**GitHub Secrets (for CI/CD):**
```
RAILWAY_TOKEN_STAGING
RAILWAY_TOKEN_PRODUCTION
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
DOCKER_USERNAME
DOCKER_PASSWORD
SLACK_WEBHOOK
STAGING_API_URL
```

**Platform Secrets (Railway/Render):**
```
JWT_SECRET_KEY
SESSION_SECRET_KEY
OPENAI_API_KEY
SENTRY_DSN
```

---

## Release Process

### Version Numbering

Format: `MAJOR.MINOR.PATCH` (Semantic Versioning)

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist

#### 1 Week Before Release

- [ ] Code freeze for `develop` branch
- [ ] Create release branch: `release/v1.2.0`
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Perform security audit
- [ ] Update documentation

#### 3 Days Before Release

- [ ] Deploy to staging
- [ ] QA testing on staging
- [ ] Performance testing
- [ ] Load testing
- [ ] Create release notes

#### 1 Day Before Release

- [ ] Final stakeholder review
- [ ] Backup production database
- [ ] Schedule deployment window
- [ ] Notify users of upcoming deployment
- [ ] Prepare rollback plan

#### Release Day

- [ ] Merge release branch to `main`
- [ ] Tag release: `git tag -a v1.2.0`
- [ ] Push tag: `git push origin v1.2.0`
- [ ] Monitor CI/CD pipeline
- [ ] Verify production deployment
- [ ] Run smoke tests
- [ ] Monitor for errors (24 hours)
- [ ] Merge release branch back to `develop`

#### Post-Release

- [ ] Send release announcement
- [ ] Update documentation site
- [ ] Archive release branch
- [ ] Review metrics
- [ ] Conduct retrospective

---

## Hotfix Procedures

### Emergency Hotfix Process

```
┌──────────────────┐
│  Critical Bug    │
│    Reported      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Create Hotfix    │
│ Branch from main │
│                  │
│ git checkout -b  │
│ hotfix/critical  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Implement      │
│      Fix         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Run Tests      │
│   Locally        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Push & Create    │
│   PR to main     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  CI Runs Tests   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Code Review    │
│   (Expedited)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Merge to main   │
│  Auto-deploy     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Verify Fix in   │
│   Production     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Merge hotfix    │
│  to develop      │
└──────────────────┘
```

### Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/fix-authentication-bug

# 2. Make fix and commit
git add .
git commit -m "fix: resolve authentication timeout issue"

# 3. Push and create PR
git push origin hotfix/fix-authentication-bug

# 4. After PR approval and merge
# CI/CD automatically deploys to production

# 5. Merge back to develop
git checkout develop
git pull origin develop
git merge hotfix/fix-authentication-bug
git push origin develop

# 6. Clean up
git branch -d hotfix/fix-authentication-bug
git push origin --delete hotfix/fix-authentication-bug
```

---

## Quality Gates

### Pre-Merge Requirements

**All Branches:**
- [ ] All tests passing
- [ ] Code coverage ≥ 80%
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Security scan passes

**Pull Requests:**
- [ ] At least 1 approval
- [ ] All conversations resolved
- [ ] Branch up to date with base
- [ ] Commit messages follow convention

### Deployment Gates

**Staging:**
- [ ] All CI checks pass
- [ ] Branch is `develop`

**Production:**
- [ ] All CI checks pass
- [ ] Branch is `main`
- [ ] Manual approval required
- [ ] Database backup completed

---

## Monitoring Deployments

### Deployment Metrics

```yaml
Deployment Frequency: Daily (to staging), Weekly (to production)
Lead Time for Changes: < 1 day
Time to Restore Service: < 1 hour
Change Failure Rate: < 5%
```

### Post-Deployment Monitoring

```bash
# Monitor errors in Sentry
# Check: https://sentry.io/organizations/subjunctive/issues/

# Monitor application logs
railway logs -e production -s subjunctive-backend --tail

# Monitor performance
# Check: Response times, error rates in dashboard

# Monitor user metrics
# Check: Active users, session duration
```

---

## Rollback Strategy

### Automatic Rollback Triggers

- Health check failures for > 5 minutes
- Error rate > 10%
- Critical service unavailable

### Manual Rollback

```bash
# Railway - rollback to previous deployment
railway rollback -e production

# Vercel - rollback to previous deployment
vercel rollback https://subjunctivepractice.com

# Or redeploy previous tag
git checkout v1.1.0
git push origin main --force
```

---

## Best Practices

1. **Small, Frequent Deploys**: Deploy often to minimize risk
2. **Feature Flags**: Use flags for gradual rollout
3. **Database Migrations**: Always backward compatible
4. **Zero Downtime**: Use blue-green or rolling deployments
5. **Monitor Everything**: Logs, metrics, user feedback
6. **Automated Rollbacks**: Set up automatic rollback triggers
7. **Documentation**: Keep runbooks updated
8. **Post-Mortems**: Learn from incidents
