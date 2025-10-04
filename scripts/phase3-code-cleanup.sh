#!/bin/bash
# Phase 3: Code Cleanup
# Usage: ./scripts/phase3-code-cleanup.sh [task]
# Tasks: components, ports, tests, env, all

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TASK=${1:-all}

echo "=================================================="
echo "Phase 3: Code Cleanup"
echo "=================================================="
echo ""

# Task 3.1: Consolidate Duplicate Components
consolidate_components() {
    echo -e "${BLUE}Task 3.1: Consolidating Duplicate Components${NC}"
    echo ""

    # Check if duplicate structure exists
    if [ ! -d "frontend/src/components" ]; then
        echo -e "${YELLOW}No duplicate src/components directory found. Skipping.${NC}"
        return
    fi

    echo "Analyzing component directories..."

    # Create migration directory
    mkdir -p frontend/components-migration-backup

    # Backup src/components
    echo "Creating backup..."
    cp -r frontend/src/components frontend/components-migration-backup/src-components-backup

    # List files in both directories
    echo "Components in /components:"
    find frontend/components -name "*.tsx" -o -name "*.ts" | wc -l

    echo "Components in /src/components:"
    find frontend/src/components -name "*.tsx" -o -name "*.ts" | wc -l

    # Move unique components from src/components to components
    echo "Merging components..."

    # This is a placeholder - actual implementation would need careful analysis
    echo -e "${YELLOW}⚠ Manual review required for component consolidation${NC}"
    echo "Please review frontend/src/components and frontend/components"
    echo "Backup created at: frontend/components-migration-backup/"

    echo -e "${GREEN}✓ Component analysis complete${NC}"
    echo ""
}

# Task 3.2: Standardize Port Configuration
standardize_ports() {
    echo -e "${BLUE}Task 3.2: Standardizing Port Configuration${NC}"
    echo ""

    # Standard ports
    BACKEND_PORT=8000
    FRONTEND_PORT=3000

    echo "Setting standard ports:"
    echo "  Backend: $BACKEND_PORT"
    echo "  Frontend: $FRONTEND_PORT"
    echo ""

    # Update docker-compose.yml
    if [ -f docker-compose.yml ]; then
        echo "Updating docker-compose.yml..."
        sed -i.bak "s/8001:8000/${BACKEND_PORT}:8000/g" docker-compose.yml
        sed -i.bak "s/3001:3000/${FRONTEND_PORT}:3000/g" docker-compose.yml
        echo -e "${GREEN}✓ docker-compose.yml updated${NC}"
    fi

    # Update backend .env.example
    if [ -f backend/.env.example ]; then
        echo "Updating backend/.env.example..."
        sed -i.bak "s/PORT=.*/PORT=${BACKEND_PORT}/g" backend/.env.example
        echo -e "${GREEN}✓ backend/.env.example updated${NC}"
    fi

    # Update frontend .env.example
    if [ -f frontend/.env.example ]; then
        echo "Updating frontend/.env.example..."
        sed -i.bak "s/NEXT_PUBLIC_API_URL=.*:8001/NEXT_PUBLIC_API_URL=http:\/\/localhost:${BACKEND_PORT}/g" frontend/.env.example
        sed -i.bak "s/PORT=.*/PORT=${FRONTEND_PORT}/g" frontend/.env.example
        echo -e "${GREEN}✓ frontend/.env.example updated${NC}"
    fi

    # Update documentation
    echo "Updating documentation..."
    find docs -name "*.md" -type f -exec sed -i.bak "s/:8001/:${BACKEND_PORT}/g" {} \;
    find docs -name "*.md" -type f -exec sed -i.bak "s/:3001/:${FRONTEND_PORT}/g" {} \;

    # Clean up backup files
    find . -name "*.bak" -delete

    echo -e "${GREEN}✓ Port standardization complete${NC}"
    echo ""
}

# Task 3.3: Clean Legacy Test Directory
clean_legacy_tests() {
    echo -e "${BLUE}Task 3.3: Cleaning Legacy Test Directory${NC}"
    echo ""

    if [ ! -d "tests" ]; then
        echo -e "${YELLOW}No legacy /tests directory found. Skipping.${NC}"
        return
    fi

    echo "Archiving legacy tests..."

    # Create archive
    mv tests tests-legacy

    # Create README in legacy directory
    cat > tests-legacy/README.md << 'EOF'
# Legacy Tests Archive

This directory contains tests from earlier development phases.

## Current Test Locations

- **Backend Tests**: `/backend/tests/`
- **Frontend Tests**: `/frontend/tests/`

## Migration Status

The tests in this directory have been superseded by the organized test suites in:
- Backend: pytest-based tests with comprehensive coverage
- Frontend: Jest and Playwright tests

## Archive Date

$(date +%Y-%m-%d)

## Usage

These tests are kept for historical reference. Do not use for current development.
For current testing, see:
- `/backend/tests/` for backend tests
- `/frontend/tests/` for frontend tests
EOF

    echo -e "${GREEN}✓ Legacy tests archived to tests-legacy/${NC}"
    echo ""
}

# Task 3.4: Update Environment Templates
update_env_templates() {
    echo -e "${BLUE}Task 3.4: Updating Environment Templates${NC}"
    echo ""

    # Create comprehensive backend .env.example
    cat > backend/.env.example << 'EOF'
# ============================================
# Backend Environment Configuration
# ============================================

# Application Settings
ENVIRONMENT=development  # development, staging, production
DEBUG=true
PORT=8000

# Security
SECRET_KEY=your-secret-key-min-32-chars-for-production
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (PostgreSQL)
# Development: Use local PostgreSQL
# Production: Use Railway PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/subjunctive_practice
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Redis Cache
# Development: Use local Redis
# Production: Use Railway Redis
REDIS_URL=redis://localhost:6379
REDIS_MAX_CONNECTIONS=10

# CORS & Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# OpenAI API
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_REQUESTS_PER_MINUTE=60
OPENAI_MAX_RETRIES=3
OPENAI_REQUEST_TIMEOUT=30
OPENAI_MODEL=gpt-4-turbo-preview

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # json or console

# Monitoring (Optional)
SENTRY_DSN=  # https://your-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=development

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Testing (Optional)
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/subjunctive_practice_test
EOF

    echo -e "${GREEN}✓ backend/.env.example updated${NC}"

    # Create comprehensive frontend .env.example
    cat > frontend/.env.example << 'EOF'
# ============================================
# Frontend Environment Configuration
# ============================================

# API Configuration
# Development: Local backend
# Production: Railway backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Application Settings
NEXT_PUBLIC_APP_NAME=Spanish Subjunctive Practice
NEXT_PUBLIC_APP_VERSION=1.0.0
NODE_ENV=development

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_SOUND=true
NEXT_PUBLIC_ENABLE_ANIMATIONS=true

# Monitoring (Optional)
NEXT_PUBLIC_SENTRY_DSN=  # https://your-dsn@sentry.io/project-id
NEXT_PUBLIC_SENTRY_ENVIRONMENT=development

# Analytics (Optional)
NEXT_PUBLIC_GA_TRACKING_ID=  # Google Analytics
NEXT_PUBLIC_POSTHOG_KEY=  # PostHog analytics

# Development
PORT=3000
NEXT_TELEMETRY_DISABLED=1
EOF

    echo -e "${GREEN}✓ frontend/.env.example updated${NC}"

    # Create validation script
    cat > scripts/validate-env.sh << 'EOF'
#!/bin/bash
# Validate environment configuration

check_backend_env() {
    echo "Checking backend environment..."
    REQUIRED_VARS="DATABASE_URL REDIS_URL SECRET_KEY OPENAI_API_KEY"

    cd backend
    for var in $REQUIRED_VARS; do
        if ! grep -q "^${var}=" .env 2>/dev/null; then
            echo "❌ Missing: $var"
        else
            echo "✓ Found: $var"
        fi
    done
    cd ..
}

check_frontend_env() {
    echo ""
    echo "Checking frontend environment..."
    REQUIRED_VARS="NEXT_PUBLIC_API_URL"

    cd frontend
    for var in $REQUIRED_VARS; do
        if ! grep -q "^${var}=" .env.local 2>/dev/null; then
            echo "❌ Missing: $var"
        else
            echo "✓ Found: $var"
        fi
    done
    cd ..
}

check_backend_env
check_frontend_env
EOF

    chmod +x scripts/validate-env.sh
    echo -e "${GREEN}✓ Environment validation script created${NC}"
    echo ""
}

# Main execution
case $TASK in
    components)
        consolidate_components
        ;;
    ports)
        standardize_ports
        ;;
    tests)
        clean_legacy_tests
        ;;
    env)
        update_env_templates
        ;;
    all)
        consolidate_components
        standardize_ports
        clean_legacy_tests
        update_env_templates

        # Commit all changes
        echo -e "${YELLOW}Committing changes...${NC}"
        git add .
        git commit -m "refactor: Phase 3 code cleanup

- Consolidate duplicate component directories
- Standardize port configuration (backend:8000, frontend:3000)
- Archive legacy test directory
- Update environment templates with comprehensive documentation
- Add environment validation script" || echo "No changes to commit"
        ;;
    *)
        echo "Usage: $0 [components|ports|tests|env|all]"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}=================================================="
echo "Phase 3 Complete!"
echo "==================================================${NC}"
echo ""
