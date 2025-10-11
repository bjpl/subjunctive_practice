#!/bin/bash

# CI/CD Setup Verification Script
# Verifies that all required files and configurations are in place

set -e

echo "=================================="
echo "CI/CD Setup Verification"
echo "=================================="
echo ""

ERRORS=0
WARNINGS=0

# Function to check file existence
check_file() {
    local file=$1
    local description=$2

    if [ -f "$file" ]; then
        echo "✓ $description: $file"
    else
        echo "✗ $description: $file (MISSING)"
        ((ERRORS++))
    fi
}

# Function to check directory existence
check_directory() {
    local dir=$1
    local description=$2

    if [ -d "$dir" ]; then
        echo "✓ $description: $dir"
    else
        echo "✗ $description: $dir (MISSING)"
        ((ERRORS++))
    fi
}

# Function to check command availability
check_command() {
    local cmd=$1
    local description=$2

    if command -v "$cmd" &> /dev/null; then
        echo "✓ $description installed"
    else
        echo "⚠ $description not installed (OPTIONAL)"
        ((WARNINGS++))
    fi
}

echo "=== Checking Workflow Files ==="
check_file ".github/workflows/backend-ci.yml" "Backend CI workflow"
check_file ".github/workflows/frontend-ci.yml" "Frontend CI workflow"
check_file ".github/workflows/deploy-backend.yml" "Backend deployment workflow"
check_file ".github/workflows/deploy-frontend.yml" "Frontend deployment workflow"
check_file ".github/workflows/security.yml" "Security scanning workflow"
check_file ".github/workflows/integration.yml" "Integration testing workflow"
check_file ".github/workflows/release.yml" "Release automation workflow"
check_file ".github/workflows/pr-checks.yml" "PR checks workflow"
check_file ".github/dependabot.yml" "Dependabot configuration"
check_file ".github/labeler.yml" "Labeler configuration"
echo ""

echo "=== Checking Backend Files ==="
check_directory "backend" "Backend directory"
check_file "backend/requirements.txt" "Backend requirements"
check_file "backend/requirements-dev.txt" "Backend dev requirements"
check_file "backend/pytest.ini" "Pytest configuration"
check_file "backend/Dockerfile" "Backend Dockerfile"
echo ""

echo "=== Checking Frontend Files ==="
check_directory "frontend" "Frontend directory"
check_file "frontend/package.json" "Frontend package.json"
check_file "frontend/next.config.js" "Next.js configuration"
check_file "frontend/tsconfig.json" "TypeScript configuration"
check_file "frontend/jest.config.js" "Jest configuration"
check_file "frontend/playwright.config.ts" "Playwright configuration"
echo ""

echo "=== Checking Documentation ==="
check_file "docs/CI-CD-SETUP.md" "CI/CD setup documentation"
check_file "README.md" "Project README"
echo ""

echo "=== Checking Required Tools ==="
check_command "git" "Git"
check_command "python" "Python"
check_command "node" "Node.js"
check_command "npm" "npm"
check_command "gh" "GitHub CLI"
check_command "docker" "Docker"
echo ""

echo "=== Checking GitHub CLI Authentication ==="
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null; then
        echo "✓ GitHub CLI authenticated"
    else
        echo "⚠ GitHub CLI not authenticated (run 'gh auth login')"
        ((WARNINGS++))
    fi
else
    echo "⚠ GitHub CLI not installed"
fi
echo ""

echo "=== Checking Python Dependencies ==="
if [ -f "backend/requirements-dev.txt" ]; then
    if python -c "import pytest" 2>/dev/null; then
        echo "✓ pytest installed"
    else
        echo "⚠ pytest not installed (run 'pip install -r backend/requirements-dev.txt')"
        ((WARNINGS++))
    fi

    if python -c "import black" 2>/dev/null; then
        echo "✓ black installed"
    else
        echo "⚠ black not installed"
        ((WARNINGS++))
    fi

    if python -c "import flake8" 2>/dev/null; then
        echo "✓ flake8 installed"
    else
        echo "⚠ flake8 not installed"
        ((WARNINGS++))
    fi
fi
echo ""

echo "=== Checking Frontend Dependencies ==="
if [ -f "frontend/package.json" ]; then
    if [ -d "frontend/node_modules" ]; then
        echo "✓ node_modules exists"
    else
        echo "⚠ node_modules not found (run 'npm install' in frontend/)"
        ((WARNINGS++))
    fi
fi
echo ""

echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✓ CI/CD setup verification passed!"
    echo ""
    echo "Next steps:"
    echo "1. Configure GitHub secrets (run scripts/setup-ci-secrets.sh)"
    echo "2. Set up Railway and Vercel projects"
    echo "3. Enable GitHub Actions in repository settings"
    echo "4. Test with a pull request"
    exit 0
else
    echo "✗ CI/CD setup verification failed with $ERRORS errors"
    echo "Please fix the errors above and run this script again"
    exit 1
fi
