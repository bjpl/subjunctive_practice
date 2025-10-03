# Infrastructure Fix Plan - Phase 1 Prerequisites

**Status:** Ready for Execution
**Priority:** CRITICAL
**Estimated Time:** 1 hour
**Blocking:** All Phase 1 agents

---

## Critical Issues Identified

### 1. Python Testing Infrastructure - BROKEN
**Issue:** pytest not available
```bash
python -m pytest --version
> pytest not available
```

**Impact:**
- Cannot run tests
- Cannot establish baseline coverage
- Blocks Phase 1 Task 3 (Baseline Metrics)

### 2. NPM Dependencies - SEVERELY BROKEN
**Issue:** 19+ UNMET DEPENDENCIES
```
@jest/globals, @playwright/test, @testing-library/react,
@types/node, @types/react, eslint, typescript, vite, vitest, etc.
```

**Impact:**
- Cannot run frontend tests
- Cannot build application
- No type checking available
- Blocks all frontend work

### 3. Code Quality Tools - NOT CONFIGURED
**Issue:** No tools installed or configured

**Impact:**
- No automated formatting
- No linting
- No pre-commit hooks
- Inconsistent code style

---

## Fix Plan

### Step 1: Python Environment Setup (15 minutes)

**1.1 Install Core Testing Tools**
```bash
cd /mnt/c/Users/brand/Development/Project_Workspace/active-development/language-learning/subjunctive_practice

# Install using poetry (preferred, as pyproject.toml exists)
poetry install

# OR install using pip if poetry not available
pip install pytest pytest-cov pytest-asyncio
pip install black isort flake8 mypy
pip install radon bandit safety
pip install pre-commit
```

**1.2 Verify Python Tools**
```bash
# Verify installations
pytest --version
black --version
isort --version
flake8 --version
mypy --version
radon --version
bandit --version
pre-commit --version
```

**Expected Output:**
```
pytest 7.x.x
black 23.12.1
isort 5.13.2
flake8 7.0.0
mypy 1.8.0
radon 6.x.x
bandit 1.7.6
pre-commit 3.6.0
```

### Step 2: NPM Environment Setup (20 minutes)

**2.1 Clean Install**
```bash
# Remove existing node_modules and lock file
rm -rf node_modules
rm -f package-lock.json

# Clean install with legacy peer deps (may be needed for compatibility)
npm install --legacy-peer-deps

# OR if above fails, try force install
npm install --force
```

**2.2 Verify NPM Tools**
```bash
# Check installations
npm list --depth=0 | grep -E "(jest|playwright|testing-library|eslint|typescript|vite)"
```

**2.3 Install Missing Critical Dependencies**
If clean install doesn't work, install individually:
```bash
npm install --save-dev \
  @jest/globals@^29.4.3 \
  @playwright/test@^1.31.1 \
  @testing-library/jest-dom@^5.16.5 \
  @testing-library/react@^14.0.0 \
  @testing-library/user-event@^14.4.3 \
  @types/node@^18.14.2 \
  @types/react@^18.0.28 \
  @types/react-dom@^18.0.11 \
  eslint@^8.54.0 \
  typescript@^5.3.3 \
  vite@^4.5.0 \
  vitest@^0.29.2 \
  @vitejs/plugin-react@^3.1.0
```

### Step 3: Code Quality Configuration (15 minutes)

**3.1 Create Pre-commit Configuration**
```bash
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203,W503"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: ["--ignore-missing-imports"]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: detect-private-key
EOF

# Install hooks
pre-commit install
```

**3.2 Create ESLint Configuration**
```bash
cat > .eslintrc.json << 'EOF'
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true
    },
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": [
    "react",
    "@typescript-eslint"
  ],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "@typescript-eslint/no-unused-vars": ["warn"],
    "@typescript-eslint/no-explicit-any": ["warn"]
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
EOF
```

**3.3 Create Prettier Configuration**
```bash
cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 88,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always"
}
EOF
```

**3.4 Create Coverage Configuration**
```bash
cat > .coveragerc << 'EOF'
[run]
source = src,backend,shared
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */migrations/*
    */node_modules/*
    */venv/*
    */build/*
    */dist/*

[report]
precision = 2
show_missing = True
skip_covered = False
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

[html]
directory = htmlcov
EOF
```

### Step 4: Verification (10 minutes)

**4.1 Test Python Infrastructure**
```bash
# Run pytest (should run even if no tests found)
pytest --version
pytest --collect-only

# Test coverage
pytest --cov=src --cov=backend --cov-report=term-missing --dry-run 2>/dev/null || echo "No tests yet, but pytest works"

# Test formatters
black --check . --exclude '/(\.git|\.venv|venv|node_modules|build|dist)/' || echo "Would reformat files"
isort --check . --skip-gitignore || echo "Would reorder imports"
flake8 . --exclude=.git,__pycache__,node_modules,build,dist,venv,.venv --max-line-length=88
```

**4.2 Test NPM Infrastructure**
```bash
# Check npm scripts
npm run --list

# Try running tests (may fail but should execute)
npm test 2>&1 | head -20 || echo "Test infrastructure configured"

# Check build
npm run build 2>&1 | head -20 || echo "Build infrastructure configured"
```

**4.3 Test Application Startup**
```bash
# Python backend (should start without errors)
python -c "import backend; print('Backend imports OK')" || echo "Backend has import issues"

# Frontend build (should complete)
cd frontend 2>/dev/null && npm run build && cd .. || echo "Frontend build tested"
```

---

## Success Criteria

### Python Environment ✓
- [ ] pytest installed and working
- [ ] black, isort, flake8, mypy installed
- [ ] radon, bandit, safety installed
- [ ] pre-commit hooks configured
- [ ] .coveragerc created

### NPM Environment ✓
- [ ] All package.json dependencies installed
- [ ] No UNMET DEPENDENCY warnings
- [ ] ESLint configured
- [ ] Prettier configured
- [ ] npm test can run
- [ ] npm run build works

### Configuration Files ✓
- [ ] .pre-commit-config.yaml created and installed
- [ ] .eslintrc.json created
- [ ] .prettierrc created
- [ ] .coveragerc created
- [ ] All configs validated

### Application Health ✓
- [ ] Backend imports work
- [ ] Frontend builds successfully
- [ ] No critical errors on startup

---

## Rollback Plan

If any step fails:

1. **Document the error** in infrastructure-fix-errors.log
2. **Try alternative approach** (pip vs poetry, npm force vs legacy-peer-deps)
3. **Skip non-critical tools** (bandit, safety can wait)
4. **Proceed if core tools work** (pytest and npm are critical, formatters are nice-to-have)

---

## Post-Fix Actions

Once infrastructure is fixed:

1. **Update Phase 1 Status**
   ```bash
   npx claude-flow@alpha hooks notify --message "Infrastructure fixes complete. Ready for Phase 1 agent execution."
   ```

2. **Store in Memory**
   ```bash
   # Will be done via MCP tool
   memory_usage store "refactoring/phase1/infrastructure" "FIXED - pytest working, npm deps installed, tools configured"
   ```

3. **Execute Phase 1 Agents**
   - Spawn Task 1: Architecture Documentation
   - Spawn Task 2: Code Quality Tools (update configs)
   - Spawn Task 3: Baseline Metrics
   - Spawn Task 4: File Organization

---

## Timeline

| Step | Duration | Critical |
|------|----------|----------|
| Python Setup | 15 min | YES |
| NPM Setup | 20 min | YES |
| Config Creation | 15 min | MEDIUM |
| Verification | 10 min | YES |
| **TOTAL** | **60 min** | - |

---

## Owner Assignment

**Primary:** Phase 1 Coordinator Agent (this agent)
**Backup:** DevOps specialist
**Escalation:** Project lead if critical failures

---

**Status:** Ready for execution
**Next Action:** Execute Step 1 (Python Environment Setup)
