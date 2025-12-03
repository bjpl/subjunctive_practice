# CI/CD Pipeline Documentation

## Overview

This document describes the comprehensive GitHub Actions CI/CD pipeline for the Spanish Subjunctive Practice backend application.

## Workflows

### 1. Main CI Pipeline (`test.yml`)

**Triggers:**
- Push to main, master, or develop branches
- Pull requests to main, master, or develop
- Daily scheduled run at 8 AM UTC

**Jobs:**

#### Test Job
- **Services:** PostgreSQL 15, Redis 7
- **Steps:**
  - Checkout code
  - Set up Python 3.11 with pip caching
  - Install dependencies
  - Run database migrations
  - Execute unit tests (marked with `@pytest.mark.unit`)
  - Execute integration tests (marked with `@pytest.mark.integration`)
  - Execute API tests (marked with `@pytest.mark.api`)
  - Generate coverage reports (XML, HTML, terminal)
  - Upload results to Codecov
  - Comment test summary on PRs

#### Lint Job
- **Tools:** Black, isort, Flake8, MyPy, pylint
- **Checks:**
  - Code formatting (Black)
  - Import ordering (isort)
  - Style violations (Flake8)
  - Type checking (MyPy)

#### Security Job
- **Tools:** Bandit, Safety
- **Scans:**
  - Source code security issues (Bandit)
  - Dependency vulnerabilities (Safety)

#### Build Job
- **Depends on:** Test, Lint
- **Actions:**
  - Build Docker image with Buildx
  - Cache layers for faster builds
  - Tag with commit SHA

#### Test Metrics Job
- **Depends on:** Test
- **Actions:**
  - Generate test execution metrics
  - Upload metrics as artifacts

#### Notify Job
- **Depends on:** All jobs
- **Actions:**
  - Aggregate job statuses
  - Send notifications on failure

---

### 2. Coverage Reporting (`coverage.yml`)

**Triggers:**
- Push to main, master, or develop branches
- Pull requests
- Weekly on Monday at 00:00 UTC

**Features:**
- Full test suite with branch coverage
- HTML coverage report generation
- Coverage badge generation
- Codecov integration with token
- PR comments with coverage details
- Coverage threshold enforcement (70% minimum)

**Artifacts:**
- HTML coverage report (30-day retention)
- Coverage badge SVG (90-day retention)

---

### 3. PR Validation (`pr-checks.yml`)

**Triggers:**
- Pull request events (opened, synchronize, reopened, edited)

**Jobs:**

#### PR Metadata Validation
- Enforces semantic commit format (feat, fix, docs, etc.)
- Checks PR size (warns if >1000 changes)

#### Quick Test Suite
- Fast unit tests only (excludes slow tests)
- Fast lint checks (Black, isort)
- Fails fast on first 3 errors

#### Changed Files Analysis
- Lists all changed Python files
- Warns if backend code changed without tests
- Provides file count statistics

#### Dependency Check
- Detects dependency file changes
- Validates requirements files
- Runs security scans on new dependencies

#### Auto Label
- Automatically labels PRs based on changed files
- Uses `.github/labeler.yml` configuration

#### PR Checklist
- Validates PR description length (>50 characters)
- Checks for test plan mention

#### Ready to Merge Check
- Aggregates all job statuses
- Final go/no-go decision

---

### 4. Nightly Build (`nightly.yml`)

**Triggers:**
- Daily at 2:00 AM UTC
- Manual workflow dispatch

**Jobs:**

#### Full Test Suite
- Complete test execution (all markers)
- Detailed coverage analysis
- Top 20 slowest tests reported
- 7-day artifact retention

#### Performance Tests
- Load testing with Locust
- Benchmark tests with pytest-benchmark
- Performance metrics collection

#### Security Audit
- Comprehensive Bandit scan
- Safety vulnerability check
- pip-audit for dependency issues
- Security reports as artifacts

#### Dependency Update Check
- Lists outdated packages
- Generates update recommendations
- Saved as artifact for review

---

### 5. Dependency Review (`dependency-review.yml`)

**Triggers:**
- PRs that modify dependency files

**Features:**
- Automated dependency scanning
- License compliance checking
- Vulnerability severity thresholds (moderate+)
- PR comments with review summary
- License report generation

---

### 6. CodeQL Security Analysis (`codeql.yml`)

**Triggers:**
- Push to main, master, or develop
- Pull requests
- Weekly on Monday at 00:00 UTC

**Features:**
- Advanced static code analysis
- Security vulnerability detection
- Quality issue identification
- Extended security queries
- Automated security alerts

---

## Caching Strategy

### Pip Dependencies
```yaml
cache: 'pip'
cache-dependency-path: |
  requirements.txt
  requirements-dev.txt
```

### Docker Build Layers
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

---

## Environment Variables

### Test Environment
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: Application secret key
- `ENVIRONMENT`: Set to "test"

### Service Containers
- **PostgreSQL:** postgres:15-alpine on port 5432
- **Redis:** redis:7-alpine on port 6379

---

## Required Secrets

To enable all features, configure these GitHub repository secrets:

1. `CODECOV_TOKEN` - For coverage reporting to Codecov
2. Optional: Notification service tokens

---

## Auto-Labeling Configuration

The `.github/labeler.yml` file defines automatic labels:

- `backend` - Backend code changes
- `api` - API endpoint changes
- `database` - Database/model changes
- `services` - Service layer changes
- `tests` - Test file changes
- `documentation` - Documentation updates
- `dependencies` - Dependency updates
- `ci-cd` - CI/CD configuration changes
- `config` - Configuration file changes
- `security` - Security-related changes

---

## Test Markers

Configure in `pytest.ini`:

- `unit` - Unit tests
- `integration` - Integration tests
- `api` - API endpoint tests
- `performance` - Performance tests
- `slow` - Slow-running tests
- `auth` - Authentication tests
- `conjugation` - Conjugation engine tests
- `exercise` - Exercise generation tests
- `learning` - Learning algorithm tests
- `feedback` - Feedback generation tests

---

## Best Practices

### 1. Branch Protection Rules

Recommended settings for main/master branch:
- Require PR reviews (1-2 reviewers)
- Require status checks to pass:
  - Test job
  - Lint job
  - Security job
  - Build job
- Require branches to be up to date
- Restrict force pushes

### 2. Writing Tests

```python
import pytest

@pytest.mark.unit
def test_example():
    assert True

@pytest.mark.integration
def test_database_integration():
    # Test with database
    pass

@pytest.mark.api
async def test_api_endpoint():
    # Test API endpoint
    pass
```

### 3. PR Title Format

Use conventional commits:
- `feat: Add new feature`
- `fix: Resolve bug`
- `docs: Update documentation`
- `refactor: Restructure code`
- `test: Add tests`
- `ci: Update CI/CD`

### 4. Coverage Requirements

- Minimum: 70% (enforced)
- Target: 80%+ (recommended)
- Critical paths: 90%+ (best practice)

---

## Troubleshooting

### Build Failures

1. **Dependency Installation Fails**
   - Check requirements.txt syntax
   - Verify package versions exist
   - Check for conflicting dependencies

2. **Tests Fail in CI but Pass Locally**
   - Check environment variables
   - Verify service containers are healthy
   - Check test isolation

3. **Docker Build Fails**
   - Verify Dockerfile syntax
   - Check base image availability
   - Review build context

### Performance Issues

1. **Slow Test Execution**
   - Use test markers to run subset
   - Enable parallel execution
   - Review slow tests with `--durations`

2. **Cache Not Working**
   - Check cache key patterns
   - Verify dependency file hashes
   - Review cache restore logs

---

## Metrics and Monitoring

### Available Metrics

1. **Test Execution Time**
   - Per test duration
   - Total suite time
   - Trend analysis

2. **Coverage Trends**
   - Line coverage
   - Branch coverage
   - File-level coverage

3. **Build Performance**
   - Dependency install time
   - Test execution time
   - Docker build time

### Viewing Reports

- **Coverage Reports:** Download from workflow artifacts
- **Test Results:** View in PR comments
- **Security Scans:** Check security alerts tab
- **CodeQL Results:** Security tab in repository

---

## Future Enhancements

### Planned Improvements

1. **Deployment Workflows**
   - Staging deployment on PR merge
   - Production deployment on release
   - Rollback automation

2. **Enhanced Notifications**
   - Slack integration
   - Email summaries
   - GitHub status badges

3. **Performance Testing**
   - Automated load testing
   - Performance regression detection
   - Response time monitoring

4. **Multi-Environment Testing**
   - Python 3.10, 3.11, 3.12 matrix
   - Multiple PostgreSQL versions
   - Different OS runners

---

## Maintenance

### Weekly Tasks
- Review nightly build results
- Check for outdated dependencies
- Review security scan findings

### Monthly Tasks
- Update GitHub Actions versions
- Review and optimize caching
- Analyze test performance trends

### Quarterly Tasks
- Dependency major version updates
- Workflow optimization review
- CI/CD cost analysis

---

## Support and Resources

- **GitHub Actions Docs:** https://docs.github.com/actions
- **pytest Documentation:** https://docs.pytest.org
- **Codecov Docs:** https://docs.codecov.com
- **Docker Docs:** https://docs.docker.com

---

**Last Updated:** 2025-10-17
**Maintained By:** DevOps Team
**Contact:** CI/CD Pipeline Engineer
