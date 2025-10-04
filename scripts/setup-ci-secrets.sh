#!/bin/bash

# CI/CD Secrets Setup Script
# This script helps configure all required GitHub secrets for CI/CD pipelines

set -e

echo "=================================="
echo "CI/CD Secrets Setup for Spanish Subjunctive Practice"
echo "=================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✓ GitHub CLI is installed and authenticated"
echo ""

# Function to set secret
set_secret() {
    local secret_name=$1
    local secret_description=$2

    echo "Setting secret: $secret_name"
    echo "Description: $secret_description"
    read -sp "Enter value for $secret_name: " secret_value
    echo ""

    if [ -z "$secret_value" ]; then
        echo "Warning: Skipping empty value for $secret_name"
        return
    fi

    echo "$secret_value" | gh secret set "$secret_name"
    echo "✓ Secret $secret_name set successfully"
    echo ""
}

# Backend secrets
echo "=== Backend Secrets ==="
set_secret "RAILWAY_STAGING_TOKEN" "Railway staging environment token"
set_secret "RAILWAY_PRODUCTION_TOKEN" "Railway production environment token"
set_secret "STAGING_DATABASE_URL" "Staging PostgreSQL database URL"
set_secret "STAGING_REDIS_URL" "Staging Redis URL"
set_secret "STAGING_SECRET_KEY" "Staging secret key for JWT"
set_secret "OPENAI_API_KEY" "OpenAI API key"

# Frontend secrets
echo "=== Frontend Secrets ==="
set_secret "VERCEL_TOKEN" "Vercel authentication token"
set_secret "VERCEL_ORG_ID" "Vercel organization ID"
set_secret "VERCEL_PROJECT_ID" "Vercel project ID"
set_secret "PREVIEW_API_URL" "Preview/staging API URL"
set_secret "PRODUCTION_API_URL" "Production API URL"
set_secret "PRODUCTION_FRONTEND_URL" "Production frontend URL"
set_secret "ANALYTICS_ID" "Analytics tracking ID (optional)"

# Security secrets
echo "=== Security Secrets ==="
set_secret "CODECOV_TOKEN" "Codecov upload token"
set_secret "SNYK_TOKEN" "Snyk security scanning token"

# Notification secrets
echo "=== Notification Secrets ==="
set_secret "SLACK_WEBHOOK" "Slack webhook URL for notifications"

echo ""
echo "=================================="
echo "✓ All secrets have been configured!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Verify secrets in your GitHub repository settings"
echo "2. Configure Railway and Vercel projects"
echo "3. Test CI/CD pipelines with a test commit"
echo ""
