#!/bin/bash

# Deployment Automation Script
# Spanish Subjunctive Practice Application
# Supports Railway (backend) and Vercel (frontend) deployments

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

check_env_var() {
    if [ -z "${!1:-}" ]; then
        log_error "Environment variable $1 is not set"
        return 1
    fi
    return 0
}

# Pre-deployment checks
pre_deployment_checks() {
    log_info "Running pre-deployment checks..."

    # Check required commands
    check_command "git"

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not in a git repository"
        exit 1
    fi

    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        log_warning "You have uncommitted changes. Consider committing them first."
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Check current branch
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    log_info "Current branch: $CURRENT_BRANCH"

    # Get current commit
    CURRENT_COMMIT=$(git rev-parse --short HEAD)
    log_info "Current commit: $CURRENT_COMMIT"

    log_success "Pre-deployment checks passed"
}

# Deploy backend to Railway
deploy_backend() {
    log_info "Deploying backend to Railway..."

    # Check for Railway CLI
    check_command "railway"

    cd "$BACKEND_DIR"

    # Run tests (optional, comment out if not needed)
    if [ "${SKIP_TESTS:-false}" != "true" ]; then
        log_info "Running backend tests..."
        if command -v poetry &> /dev/null; then
            poetry run pytest || {
                log_error "Backend tests failed. Deployment aborted."
                exit 1
            }
        else
            log_warning "Poetry not found. Skipping tests."
        fi
    fi

    # Deploy to Railway
    log_info "Pushing to Railway..."
    railway up || {
        log_error "Railway deployment failed"
        exit 1
    }

    # Get deployment URL
    BACKEND_URL=$(railway status --json | grep -o '"url":"[^"]*' | cut -d'"' -f4 || echo "URL not available")

    log_success "Backend deployed successfully"
    log_info "Backend URL: $BACKEND_URL"

    cd "$PROJECT_ROOT"
}

# Deploy frontend to Vercel
deploy_frontend() {
    log_info "Deploying frontend to Vercel..."

    # Check for Vercel CLI
    check_command "vercel"

    cd "$FRONTEND_DIR"

    # Run build test (optional)
    if [ "${SKIP_BUILD_TEST:-false}" != "true" ]; then
        log_info "Testing frontend build..."
        npm run build || {
            log_error "Frontend build failed. Deployment aborted."
            exit 1
        }
    fi

    # Deploy to Vercel
    log_info "Deploying to Vercel..."
    if [ "${VERCEL_PROD:-false}" == "true" ]; then
        vercel --prod || {
            log_error "Vercel deployment failed"
            exit 1
        }
    else
        vercel || {
            log_error "Vercel deployment failed"
            exit 1
        }
    fi

    log_success "Frontend deployed successfully"

    cd "$PROJECT_ROOT"
}

# Database migration
run_migrations() {
    log_info "Running database migrations..."

    cd "$BACKEND_DIR"

    # Check for alembic
    if [ ! -f "alembic.ini" ]; then
        log_warning "Alembic not configured. Skipping migrations."
        cd "$PROJECT_ROOT"
        return
    fi

    # Run migrations via Railway
    railway run alembic upgrade head || {
        log_error "Database migration failed"
        exit 1
    }

    log_success "Database migrations completed"

    cd "$PROJECT_ROOT"
}

# Health check
health_check() {
    local url=$1
    local max_attempts=30
    local attempt=1

    log_info "Performing health check on $url..."

    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "${url}/health" > /dev/null; then
            log_success "Health check passed"
            return 0
        fi

        log_info "Attempt $attempt/$max_attempts - Waiting for service to be ready..."
        sleep 5
        attempt=$((attempt + 1))
    done

    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Rollback function
rollback() {
    log_warning "Rolling back deployment..."

    if [ "${DEPLOY_TARGET}" == "backend" ] || [ "${DEPLOY_TARGET}" == "all" ]; then
        cd "$BACKEND_DIR"
        railway rollback || log_error "Backend rollback failed"
        cd "$PROJECT_ROOT"
    fi

    # Vercel rollback is manual through dashboard
    if [ "${DEPLOY_TARGET}" == "frontend" ] || [ "${DEPLOY_TARGET}" == "all" ]; then
        log_warning "Frontend rollback must be done through Vercel dashboard"
        log_info "Visit: https://vercel.com/dashboard"
    fi

    log_warning "Rollback initiated. Check dashboards for status."
}

# Main deployment workflow
main() {
    log_info "Spanish Subjunctive Practice - Deployment Script"
    log_info "================================================"

    # Parse arguments
    DEPLOY_TARGET="${1:-all}"  # backend, frontend, or all

    case "$DEPLOY_TARGET" in
        backend)
            log_info "Deployment target: Backend only"
            ;;
        frontend)
            log_info "Deployment target: Frontend only"
            ;;
        all)
            log_info "Deployment target: Full stack"
            ;;
        *)
            log_error "Invalid deployment target: $DEPLOY_TARGET"
            echo "Usage: $0 [backend|frontend|all]"
            exit 1
            ;;
    esac

    # Run pre-deployment checks
    pre_deployment_checks

    # Deploy based on target
    if [ "$DEPLOY_TARGET" == "backend" ] || [ "$DEPLOY_TARGET" == "all" ]; then
        deploy_backend

        # Run migrations
        if [ "${SKIP_MIGRATIONS:-false}" != "true" ]; then
            run_migrations
        fi

        # Health check
        if [ -n "${BACKEND_URL:-}" ]; then
            health_check "$BACKEND_URL" || {
                log_error "Backend health check failed. Consider rollback."
                read -p "Rollback? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rollback
                fi
                exit 1
            }
        fi
    fi

    if [ "$DEPLOY_TARGET" == "frontend" ] || [ "$DEPLOY_TARGET" == "all" ]; then
        deploy_frontend
    fi

    log_success "Deployment completed successfully!"
    log_info "================================================"

    # Summary
    echo ""
    log_info "Deployment Summary:"
    log_info "  Branch: $CURRENT_BRANCH"
    log_info "  Commit: $CURRENT_COMMIT"

    if [ "$DEPLOY_TARGET" == "backend" ] || [ "$DEPLOY_TARGET" == "all" ]; then
        log_info "  Backend: $BACKEND_URL"
    fi

    if [ "$DEPLOY_TARGET" == "frontend" ] || [ "$DEPLOY_TARGET" == "all" ]; then
        log_info "  Frontend: Check Vercel dashboard for URL"
    fi

    echo ""
    log_info "Next steps:"
    log_info "  1. Verify deployments are healthy"
    log_info "  2. Test critical user flows"
    log_info "  3. Monitor error tracking (Sentry)"
    log_info "  4. Check logs for any issues"
}

# Trap errors and offer rollback
trap 'log_error "Deployment failed. Run rollback if needed."; exit 1' ERR

# Run main function
main "$@"
