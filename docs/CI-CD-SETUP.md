# CI/CD Pipeline Setup Guide

## Overview

This document provides comprehensive documentation for the CI/CD pipelines configured for the Spanish Subjunctive Practice application.

## Architecture

The CI/CD setup consists of the following components:

### 1. Continuous Integration (CI)
- **Backend CI**: Python testing, linting, and security scanning
- **Frontend CI**: Node.js testing, type checking, and E2E tests
- **Security Scanning**: CodeQL, dependency scanning, secret detection
- **Integration Testing**: Full-stack integration and performance tests

### 2. Continuous Deployment (CD)
- **Backend Deployment**: Automated deployment to Railway
- **Frontend Deployment**: Automated deployment to Vercel
- **Release Automation**: GitHub releases with changelogs

### 3. Dependency Management
- **Dependabot**: Automated dependency updates
- **License Compliance**: License checking for all dependencies

## Workflows

### Backend CI (`backend-ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches (backend files only)
- Pull requests to `main` or `develop` (backend files only)

**Jobs:**
1. **Test** - Runs on Python 3.10, 3.11, 3.12
   - Sets up PostgreSQL and Redis
   - Runs pytest with coverage
   - Uploads coverage to Codecov
   - Matrix testing across Python versions

2. **Lint** - Code quality checks
   - Black (code formatting)
   - isort (import sorting)
   - Flake8 (linting)
   - MyPy (type checking)
   - Pylint (code analysis)

3. **Security** - Security scanning
   - Bandit (Python security scanner)
   - TruffleHog (secret detection)
   - Security reports uploaded as artifacts

4. **Build** - Docker image build
   - Builds Docker image for backend
   - Uses BuildKit caching for speed

**Required Secrets:**
- `CODECOV_TOKEN` - Codecov upload token

### Frontend CI (`frontend-ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches (frontend files only)
- Pull requests to `main` or `develop` (frontend files only)

**Jobs:**
1. **Test** - Runs on Node.js 18, 20
   - TypeScript type checking
   - ESLint linting
   - Jest unit tests with coverage
   - Coverage uploaded to Codecov

2. **E2E** - End-to-end testing
   - Playwright E2E tests
   - Multiple browser testing
   - Test reports uploaded as artifacts

3. **Build** - Next.js build
   - Production build
   - Bundle size analysis
   - Build artifacts uploaded

4. **Accessibility** - A11y testing
   - jest-axe accessibility tests
   - Reports uploaded as artifacts

5. **Lint/Format** - Code quality
   - Prettier formatting check
   - ESLint with zero warnings

**Required Secrets:**
- `CODECOV_TOKEN` - Codecov upload token

### Backend Deployment (`deploy-backend.yml`)

**Triggers:**
- Push to `main` branch (backend files only)
- Manual workflow dispatch

**Jobs:**
1. **Deploy to Staging** - Automatic staging deployment
   - Runs tests before deployment
   - Deploys to Railway staging environment
   - Runs database migrations
   - Health check verification
   - Slack notification

2. **Deploy to Production** - Manual production deployment
   - Requires manual approval
   - Comprehensive testing (80% coverage required)
   - Database backup before deployment
   - Deployment to Railway production
   - Database migrations
   - Smoke tests
   - Automatic rollback on failure
   - GitHub release creation

**Required Secrets:**
- `RAILWAY_STAGING_TOKEN` - Railway staging token
- `RAILWAY_PRODUCTION_TOKEN` - Railway production token
- `STAGING_DATABASE_URL` - Staging database URL
- `STAGING_REDIS_URL` - Staging Redis URL
- `STAGING_SECRET_KEY` - Staging secret key
- `OPENAI_API_KEY` - OpenAI API key
- `SLACK_WEBHOOK` - Slack webhook for notifications

### Frontend Deployment (`deploy-frontend.yml`)

**Triggers:**
- Push to `main` branch (frontend files only)
- Manual workflow dispatch

**Jobs:**
1. **Deploy to Preview** - Automatic preview deployment
   - Runs tests and builds
   - Deploys to Vercel preview
   - Comments PR with preview URL
   - Runs Lighthouse CI performance audits

2. **Deploy to Production** - Manual production deployment
   - Requires manual approval
   - Comprehensive testing including E2E
   - Production build with analytics
   - Bundle size analysis
   - Deployment to Vercel production
   - Verification and smoke tests
   - Lighthouse CI audits
   - GitHub release creation

**Required Secrets:**
- `VERCEL_TOKEN` - Vercel authentication token
- `VERCEL_ORG_ID` - Vercel organization ID
- `VERCEL_PROJECT_ID` - Vercel project ID
- `PREVIEW_API_URL` - Preview API URL
- `PRODUCTION_API_URL` - Production API URL
- `PRODUCTION_FRONTEND_URL` - Production frontend URL
- `ANALYTICS_ID` - Analytics tracking ID
- `SLACK_WEBHOOK` - Slack webhook for notifications

### Security Scanning (`security.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests
- Daily schedule (2 AM UTC)
- Manual workflow dispatch

**Jobs:**
1. **CodeQL** - Security analysis
   - Python and JavaScript analysis
   - Security and quality queries

2. **Dependency Scan** - Vulnerability scanning
   - Snyk scanning for Python and JavaScript
   - SARIF upload to GitHub Security

3. **Secret Scan** - Secret detection
   - TruffleHog secret scanning
   - Verified secrets only

4. **Docker Scan** - Container security
   - Trivy vulnerability scanner
   - Critical and high severity issues

5. **License Compliance** - License checking
   - pip-licenses for Python
   - license-checker for JavaScript
   - Fails on GPL licenses

6. **SAST** - Static application security testing
   - Semgrep security rules
   - OWASP Top 10 checks

7. **Security Report** - Summary generation
   - Aggregates all scan results
   - Slack notification on failures

**Required Secrets:**
- `SNYK_TOKEN` - Snyk authentication token
- `SLACK_WEBHOOK` - Slack webhook for notifications

### Integration Testing (`integration.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests
- Nightly schedule (3 AM UTC)
- Manual workflow dispatch

**Jobs:**
1. **Integration** - Full-stack integration tests
   - Sets up PostgreSQL and Redis
   - Starts backend and frontend servers
   - Runs backend integration tests
   - Runs E2E integration tests
   - API integration tests

2. **Performance** - Performance testing
   - Performance benchmark tests
   - Locust load testing (optional)
   - Results uploaded as artifacts

3. **Compatibility** - Browser compatibility
   - Tests on Chromium, Firefox, WebKit
   - Matrix testing across browsers

### Release Automation (`release.yml`)

**Triggers:**
- Push of version tags (`v*.*.*`)
- Manual workflow dispatch with version input

**Jobs:**
1. **Create Release** - GitHub release creation
   - Automated changelog generation
   - Categorized changes (features, fixes, docs, etc.)
   - GitHub release creation

2. **Build Artifacts** - Release artifacts
   - Backend package build
   - Frontend build
   - Distribution archives creation

3. **Deploy Release** - Production deployment
   - Downloads build artifacts
   - Deploys to Railway (backend)
   - Deploys to Vercel (frontend)
   - Verification checks

4. **Docker Publish** - Container publishing
   - Builds and publishes Docker images
   - GitHub Container Registry
   - Semantic versioning tags

5. **Post-Release** - Follow-up tasks
   - Documentation updates
   - Monitoring issues creation
   - Triggers documentation builds

**Required Secrets:**
- All deployment secrets from backend/frontend workflows
- `GITHUB_TOKEN` - Automatically provided by GitHub

### Dependabot (`dependabot.yml`)

**Configuration:**
- **Backend (pip)**: Weekly updates on Mondays
  - Groups production and development dependencies
  - Ignores major version updates for stable packages

- **Frontend (npm)**: Weekly updates on Mondays
  - Groups React, Next.js, testing, and UI dependencies
  - Ignores major version updates for React and Next.js

- **GitHub Actions**: Weekly updates
  - Updates action versions

- **Docker**: Weekly updates
  - Updates base images

## Setup Instructions

### 1. GitHub Repository Setup

1. **Enable GitHub Actions:**
   - Go to repository Settings > Actions > General
   - Enable "Allow all actions and reusable workflows"

2. **Configure Branch Protection:**
   - Settings > Branches
   - Add rule for `main` branch:
     - Require pull request reviews
     - Require status checks to pass
     - Require conversation resolution

3. **Enable Dependabot:**
   - Settings > Security > Dependabot
   - Enable Dependabot alerts
   - Enable Dependabot security updates

### 2. Required Secrets Configuration

Navigate to Settings > Secrets and variables > Actions

#### Backend Secrets:
```
RAILWAY_STAGING_TOKEN=<railway-staging-token>
RAILWAY_PRODUCTION_TOKEN=<railway-production-token>
STAGING_DATABASE_URL=<staging-db-url>
STAGING_REDIS_URL=<staging-redis-url>
STAGING_SECRET_KEY=<staging-secret-key>
OPENAI_API_KEY=<openai-api-key>
```

#### Frontend Secrets:
```
VERCEL_TOKEN=<vercel-token>
VERCEL_ORG_ID=<vercel-org-id>
VERCEL_PROJECT_ID=<vercel-project-id>
PREVIEW_API_URL=<preview-api-url>
PRODUCTION_API_URL=<production-api-url>
PRODUCTION_FRONTEND_URL=<production-frontend-url>
ANALYTICS_ID=<analytics-id>
```

#### Security Secrets:
```
CODECOV_TOKEN=<codecov-token>
SNYK_TOKEN=<snyk-token>
```

#### Notification Secrets:
```
SLACK_WEBHOOK=<slack-webhook-url>
```

### 3. External Service Setup

#### Railway Setup:
1. Create Railway account and project
2. Create staging and production environments
3. Generate API tokens for each environment
4. Configure environment variables

#### Vercel Setup:
1. Create Vercel account and project
2. Get organization and project IDs
3. Generate Vercel token
4. Link GitHub repository

#### Codecov Setup:
1. Create Codecov account
2. Add repository
3. Get upload token

#### Snyk Setup:
1. Create Snyk account
2. Get API token
3. Configure organization

#### Slack Setup:
1. Create Slack app
2. Enable incoming webhooks
3. Get webhook URL

### 4. Environment Configuration

#### Backend Environment Variables (Railway):
```
DATABASE_URL=<postgresql-url>
REDIS_URL=<redis-url>
SECRET_KEY=<secret-key>
OPENAI_API_KEY=<openai-key>
ENVIRONMENT=production|staging
ALLOWED_ORIGINS=<frontend-urls>
```

#### Frontend Environment Variables (Vercel):
```
NEXT_PUBLIC_API_URL=<backend-api-url>
NEXT_PUBLIC_ENVIRONMENT=production|preview
NEXT_PUBLIC_ANALYTICS_ID=<analytics-id>
```

## Usage

### Running CI/CD Locally

#### Backend Testing:
```bash
cd backend
pip install -r requirements-dev.txt
pytest --cov=backend --cov-report=term-missing
black --check .
flake8 .
mypy .
```

#### Frontend Testing:
```bash
cd frontend
npm ci
npm run type-check
npm run lint
npm run test:coverage
npm run test:e2e
npm run build
```

### Manual Deployments

#### Backend to Staging:
```bash
# Triggered automatically on push to main
# Or manually via GitHub Actions UI
```

#### Backend to Production:
```bash
# Go to Actions > Deploy Backend to Railway
# Click "Run workflow"
# Select environment: production
# Requires manual approval
```

#### Frontend to Production:
```bash
# Go to Actions > Deploy Frontend to Vercel
# Click "Run workflow"
# Select environment: production
# Requires manual approval
```

### Creating Releases

1. **Create and push a version tag:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

2. **Or use manual workflow:**
- Go to Actions > Release Automation
- Click "Run workflow"
- Enter version (e.g., v1.0.0)

## Monitoring and Troubleshooting

### Viewing Workflow Runs

1. Go to repository Actions tab
2. Select workflow from left sidebar
3. Click on specific run to see details
4. Review logs for each job

### Common Issues

#### Failed Tests:
- Check test logs in workflow run
- Run tests locally to reproduce
- Fix issues and push changes

#### Deployment Failures:
- Check deployment logs
- Verify environment variables
- Check service health dashboards (Railway/Vercel)

#### Security Scan Failures:
- Review security scan artifacts
- Update vulnerable dependencies
- Fix security issues in code

### Downloading Artifacts

1. Go to workflow run
2. Scroll to "Artifacts" section
3. Download desired artifacts (coverage, reports, etc.)

## Best Practices

1. **Always run tests locally** before pushing
2. **Review Dependabot PRs** carefully before merging
3. **Monitor security alerts** and act promptly
4. **Keep secrets updated** and rotated regularly
5. **Review deployment logs** after each deployment
6. **Use feature branches** and pull requests
7. **Tag releases** with semantic versioning
8. **Document breaking changes** in release notes

## Maintenance

### Weekly Tasks:
- Review and merge Dependabot PRs
- Check security scan results
- Monitor deployment success rates

### Monthly Tasks:
- Review and update workflow configurations
- Rotate secrets and tokens
- Review and optimize build times
- Update documentation

### Quarterly Tasks:
- Audit all CI/CD configurations
- Review and update security policies
- Evaluate new tools and services
- Performance optimization review

## Support

For issues or questions:
1. Check workflow run logs
2. Review this documentation
3. Check GitHub Actions documentation
4. Contact DevOps team

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [CodeQL Documentation](https://codeql.github.com/docs/)
