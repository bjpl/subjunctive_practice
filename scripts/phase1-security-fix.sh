#!/bin/bash
# Phase 1: Critical Security Fix - Remove Exposed API Key
# Usage: ./scripts/phase1-security-fix.sh

set -e

echo "=================================================="
echo "Phase 1: Critical Security Fix"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Backup current .env.production
echo -e "${YELLOW}Step 1: Backing up .env.production...${NC}"
if [ -f .env.production ]; then
    cp .env.production .env.production.backup.$(date +%Y%m%d_%H%M%S)
    echo -e "${GREEN}✓ Backup created${NC}"
else
    echo -e "${YELLOW}⚠ No .env.production file found${NC}"
fi

# Step 2: Remove exposed key and create template
echo -e "${YELLOW}Step 2: Creating .env.production.template...${NC}"
cat > .env.production.template << 'EOF'
# Production Environment Configuration
# DO NOT commit this file with real values!
# Copy to .env.production and fill in real values

# CRITICAL: OpenAI API Key
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Application Settings
ENVIRONMENT=production
DEBUG=false

# Security
# Generate with: openssl rand -hex 32
SECRET_KEY=your-super-secret-production-key-change-this

# Database (from Railway)
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port

# CORS & Allowed Hosts
# Update with your actual domain
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# OpenAI Rate Limiting
OPENAI_REQUESTS_PER_MINUTE=60
OPENAI_MAX_RETRIES=3
OPENAI_REQUEST_TIMEOUT=30

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production

# Frontend URL
FRONTEND_URL=https://yourdomain.com

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
EOF

echo -e "${GREEN}✓ Template created${NC}"

# Step 3: Remove .env.production (it should not be committed)
echo -e "${YELLOW}Step 3: Removing .env.production from repository...${NC}"
if [ -f .env.production ]; then
    rm .env.production
    echo -e "${GREEN}✓ .env.production removed${NC}"
fi

# Step 4: Update .gitignore
echo -e "${YELLOW}Step 4: Updating .gitignore...${NC}"
if ! grep -q "^\.env\.production$" .gitignore 2>/dev/null; then
    echo ".env.production" >> .gitignore
    echo -e "${GREEN}✓ Added .env.production to .gitignore${NC}"
else
    echo -e "${GREEN}✓ .env.production already in .gitignore${NC}"
fi

# Step 5: Check for other potential secrets
echo -e "${YELLOW}Step 5: Scanning for other potential secrets...${NC}"
echo "Checking common secret patterns..."

# Scan for potential API keys (excluding node_modules and .git)
if command -v grep &> /dev/null; then
    echo "Scanning for potential exposed secrets..."
    grep -r "sk-[a-zA-Z0-9_-]\{20,\}" --exclude-dir={node_modules,.git,build,dist,.next} . || echo "No additional OpenAI keys found"
    grep -r "api[_-]key.*=.*['\"][a-zA-Z0-9]\{20,\}" --exclude-dir={node_modules,.git,build,dist,.next} . || echo "No generic API keys found"
fi

# Step 6: Git commit changes
echo -e "${YELLOW}Step 6: Committing changes...${NC}"
git add .gitignore .env.production.template
if [ -f .env.production ]; then
    git add .env.production
fi

git commit -m "security: Remove exposed API key and create environment template

- Remove .env.production with exposed OpenAI API key
- Create .env.production.template with placeholders
- Ensure .env.production is in .gitignore
- Security fix for exposed credentials

BREAKING: .env.production must be manually created from template" || echo "No changes to commit"

echo ""
echo -e "${GREEN}=================================================="
echo "Phase 1 Complete!"
echo "==================================================${NC}"
echo ""
echo -e "${RED}IMPORTANT: Next Steps (MANUAL)${NC}"
echo "1. Go to https://platform.openai.com/api-keys"
echo "2. REVOKE the old key: sk-proj-Rv5J8LTzGbP3..."
echo "3. CREATE a new secret key"
echo "4. Add the new key to GitHub Secrets as OPENAI_API_KEY"
echo "5. Never commit .env.production to Git again!"
echo ""
echo -e "${YELLOW}Optional: Clean Git History${NC}"
echo "To remove the key from Git history:"
echo "  1. Install BFG: brew install bfg"
echo "  2. Run: bfg --replace-text <(echo 'sk-proj-Rv5J8LTzGbP3...===>REMOVED')"
echo "  3. Run: git reflog expire --expire=now --all && git gc --prune=now --aggressive"
echo "  4. Run: git push --force"
echo ""
