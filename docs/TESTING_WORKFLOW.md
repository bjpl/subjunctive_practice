# Incremental Test Fixing Workflow

## Overview

This document describes the "Morning Test Fixes, Afternoon Features" workflow for maintaining test health while continuing development.

## Daily Workflow

### Morning (8:00 AM - 12:00 PM): Test Fixes

#### 1. Morning Test Run (8:00-8:30 AM)

```bash
# Run full test suite and collect metrics
python scripts/test_metrics.py

# Review yesterday's metrics
cat test_metrics.json | jq '.[-2:]'
```

#### 2. Prioritize Failures (8:30-9:00 AM)

Review test failures and categorize:

- **P0 (Critical)**: Blocking production features, security issues
- **P1 (High)**: Core functionality broken, API tests failing
- **P2 (Medium)**: Edge cases, non-critical features
- **P3 (Low)**: Cosmetic issues, optimization opportunities

#### 3. Fix High-Priority Tests (9:00-12:00 PM)

Target: Fix 3-5 P0/P1 tests per day

**Process:**
1. Pick highest priority failing test
2. Reproduce the failure locally
3. Identify root cause
4. Implement fix
5. Verify fix doesn't break other tests
6. Commit with descriptive message

**Example:**
```bash
# Run specific test
pytest tests/api/test_auth_api.py::TestAuthAPI::test_login_success -v

# After fixing
git add <changed files>
git commit -m "fix: resolve login token expiration issue

- Added proper timezone handling for token creation
- Updated test fixtures to use consistent datetime
- Fixes test_login_success and test_refresh_token_success"
```

### Afternoon (1:00 PM - 5:00 PM): Feature Development

#### 1. Pre-Development Check (1:00-1:15 PM)

```bash
# Quick sanity check
pytest tests/ -k "not slow" --tb=no -q

# Should see improvement from morning fixes
```

#### 2. Feature Development with Test-First Approach (1:15-4:45 PM)

When adding new features:

1. **Write test first** (TDD approach)
2. Implement feature to pass test
3. Run related test suite
4. Run full suite before commit

```bash
# Example: Adding new feature
pytest tests/api/test_new_feature.py -v  # Should fail initially
# ... implement feature ...
pytest tests/api/test_new_feature.py -v  # Should pass
pytest tests/api/ --tb=short             # Check related tests
pytest tests/ --tb=no -q                 # Full suite check
```

#### 3. End-of-Day Commit (4:45-5:00 PM)

```bash
# Ensure all tests pass for your changes
pytest tests/ --tb=short

# Commit with comprehensive message
git add .
git commit -m "feat: add user profile customization

- Added profile avatar upload endpoint
- Implemented avatar validation and storage
- Added comprehensive test coverage (15 tests)
- All tests passing (306/306)"

# Push to trigger CI
git push
```

### CI/CD Integration

The GitHub Actions workflow (`.github/workflows/test.yml`) automatically:

1. **On Push/PR**: Run full test suite
2. **Daily at 8 AM UTC**: Run tests and collect metrics
3. **Generate Reports**: Test coverage, metrics, trends

### Test Metrics Dashboard

View test health trends:

```bash
# Generate metrics report
python scripts/test_metrics.py

# View trends
cat test_metrics.json | jq -r '.[] | "\(.timestamp): \(.pass_rate)% (\(.passed)/\(.total_tests))"'
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)

- **Fast**: Run in < 5 seconds
- **Isolated**: No external dependencies
- **Focused**: Test single functions/classes

**Morning Priority**: P1 (fix these first)

### 2. Integration Tests (`tests/integration/`)

- **Medium Speed**: Run in < 30 seconds
- **Database**: Use test database
- **Multi-component**: Test service interactions

**Morning Priority**: P1-P2

### 3. API Tests (`tests/api/`)

- **End-to-End**: Full request/response cycle
- **Authentication**: Test auth flows
- **Validation**: Test error handling

**Morning Priority**: P0-P1 (production critical)

## Common Test Failures and Fixes

### 1. Database Connection Issues

**Symptom**: `OperationalError: unable to open database file`

**Fix**:
```python
# In conftest.py - ensure proper DB cleanup
@pytest.fixture(scope="function")
def db_session(db_engine):
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
```

### 2. Async/Await Issues

**Symptom**: `RuntimeError: Event loop is closed`

**Fix**:
```python
# Ensure proper async fixture usage
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None
```

### 3. Mock Cleanup Issues

**Symptom**: `Mock called with unexpected arguments`

**Fix**:
```python
# Reset mocks between tests
@pytest.fixture(autouse=True)
def reset_mocks():
    yield
    # Cleanup happens here
```

### 4. Worker Process Instability

**Symptom**: `Worker exited before finishing task`

**Fix**:
```python
# In conftest.py - ensure proper worker cleanup
@pytest.fixture(autouse=True)
def cleanup_workers():
    yield
    # Terminate any hanging worker processes
    import psutil
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
        child.terminate()
```

## Success Metrics

### Daily Targets

- **Morning**: Fix 3-5 failing tests
- **Test Pass Rate**: > 95%
- **New Feature Coverage**: > 80%
- **Total Test Count**: Growing (good sign!)

### Weekly Targets

- **All P0/P1 Failures**: Resolved
- **Test Suite Speed**: < 2 minutes for full suite
- **Coverage**: Maintain > 80%

### Sprint Goals

- **Zero Failing Tests**: 100% pass rate
- **CI/CD**: Green on main branch
- **Documentation**: All test files documented

## Emergency Procedures

### If Test Suite is Red on Main

1. **Stop Feature Work**: Fix tests first
2. **Identify Culprit**: `git bisect` to find breaking commit
3. **Quick Fix or Revert**: Fix within 1 hour or revert
4. **Communicate**: Notify team in Slack/email

### If Multiple Tests Failing

1. **Triage**: Group by failure type
2. **Find Root Cause**: Often 1 change breaks many tests
3. **Fix Root Cause**: Don't fix symptoms
4. **Verify**: Run full suite multiple times

## Tools and Commands

### Quick Reference

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/api/test_auth_api.py

# Run specific test
pytest tests/api/test_auth_api.py::TestAuthAPI::test_login

# Run tests matching pattern
pytest tests/ -k "auth"

# Run with coverage
pytest tests/ --cov=.

# Run in parallel (faster)
pytest tests/ -n auto

# Generate metrics
python scripts/test_metrics.py

# Watch for changes and re-run
pytest-watch tests/
```

### Debugging Failing Tests

```bash
# Verbose output
pytest tests/failing_test.py -vv

# Show print statements
pytest tests/failing_test.py -s

# Drop into debugger on failure
pytest tests/failing_test.py --pdb

# Show locals in traceback
pytest tests/failing_test.py --showlocals
```

## Best Practices

### 1. Test Isolation

- Each test should be independent
- Use fixtures for setup/teardown
- Don't rely on test execution order

### 2. Descriptive Test Names

```python
# Good
def test_login_with_expired_token_returns_401():
    pass

# Bad
def test_login():
    pass
```

### 3. Arrange-Act-Assert Pattern

```python
def test_user_creation():
    # Arrange
    user_data = {"username": "test", "email": "test@example.com"}

    # Act
    user = create_user(user_data)

    # Assert
    assert user.username == "test"
    assert user.email == "test@example.com"
```

### 4. Test Data Factories

```python
# Use factories for complex test data
user = user_factory.create(username="custom_name")
```

## Continuous Improvement

### Weekly Review (Fridays)

- Review week's test metrics
- Identify patterns in failures
- Update this documentation
- Plan next week's priorities

### Monthly Review

- Analyze test suite performance
- Identify slow tests for optimization
- Review test coverage gaps
- Update testing infrastructure

---

**Remember**: Good tests are an investment in code quality and developer productivity. The time spent fixing tests saves exponentially more time in debugging production issues.
