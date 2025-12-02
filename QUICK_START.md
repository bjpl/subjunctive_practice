# Quick Start Guide - AVES Test Infrastructure

## For New Team Members

Welcome to the AVES Test Infrastructure! This guide will get you up and running in 5 minutes.

## Prerequisites

- Python 3.12+
- Git

## Setup (2 minutes)

```bash
# 1. Navigate to project directory
cd /mnt/wsl/docker-desktop-bind-mounts/Ubuntu/03bf857aab00b15d5d7ac5a1f09940d3eaf136884d26805e9c54ffbafb045de8

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run Tests (1 minute)

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/api/test_auth_api.py

# Run with coverage
pytest tests/ --cov=.

# Quick check (no coverage, faster)
pytest tests/ --tb=no -q --no-cov
```

## Check Test Metrics (30 seconds)

```bash
# Collect and display metrics
python scripts/test_metrics.py

# Current status (as of last run):
# - Total: 306 tests
# - Passing: 288 (94.1%)
# - Failing: 18 (5.9%)
```

## Current Status

✅ **Working:**
- All unit tests for conjugation engine
- All unit tests for exercise generator  
- Most feedback and learning algorithm tests
- CI/CD pipeline with GitHub Actions
- Automated test metrics tracking

🟡 **In Progress (18 tests):**
- Auth API tests (user_id field mismatch)
- Exercise API validation tests
- Some feedback encouragement tests

## Daily Workflow

### Morning (Test Fixes)
```bash
# 1. Check test status
python scripts/test_metrics.py

# 2. Run failing tests
pytest tests/api/test_auth_api.py -v

# 3. Fix issues, then verify
pytest tests/ --tb=no -q
```

### Afternoon (Feature Development)
```bash
# 1. Write test first
# tests/test_new_feature.py

# 2. Run test (should fail)
pytest tests/test_new_feature.py

# 3. Implement feature

# 4. Verify test passes
pytest tests/test_new_feature.py

# 5. Run full suite before commit
pytest tests/ --tb=short
```

## Important Files

- `pytest.ini` - Test configuration
- `tests/conftest.py` - Shared test fixtures
- `.github/workflows/test.yml` - CI/CD configuration
- `scripts/test_metrics.py` - Metrics tracking
- `docs/TESTING_WORKFLOW.md` - Detailed workflow guide

## Need Help?

- **Test failures?** → See `docs/TESTING_WORKFLOW.md` section "Common Test Failures"
- **CI/CD questions?** → Check `.github/workflows/test.yml`
- **Full project status?** → Read `DEVOPS_SPRINT_REPORT.md`

## Next Steps to Fix Remaining 18 Tests

1. **Fix Auth API (6 tests, ~2 hours)**
   - Problem: user_id vs id field inconsistency
   - File: `api/routes/auth.py`
   - Line: 175-179

2. **Fix Exercise API (8 tests, ~2 hours)**
   - Problem: Missing input validation
   - File: `api/routes/exercises.py`

3. **Fix Unit Tests (4 tests, ~1 hour)**
   - Various minor issues

**Estimated time to 0 failures: 5 hours**

---

Happy Testing! 🧪
