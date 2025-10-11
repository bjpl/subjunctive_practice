#!/bin/bash

# Frontend Testing Suite Verification Script

echo "========================================"
echo "Frontend Testing Suite Verification"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo -e "${RED}Error: Must be run from frontend directory${NC}"
    exit 1
fi

echo "1. Checking Dependencies..."
echo "----------------------------"

# Check for required dependencies
dependencies=(
    "jest"
    "@testing-library/react"
    "@testing-library/jest-dom"
    "@testing-library/user-event"
    "jest-axe"
    "jest-environment-jsdom"
    "@playwright/test"
    "msw"
    "next-router-mock"
)

missing_deps=0
for dep in "${dependencies[@]}"; do
    if npm list "$dep" &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $dep installed"
    else
        echo -e "  ${RED}✗${NC} $dep missing"
        missing_deps=$((missing_deps + 1))
    fi
done

if [ $missing_deps -gt 0 ]; then
    echo -e "${RED}Error: $missing_deps dependencies missing${NC}"
    echo "Run: npm install"
    exit 1
fi

echo ""
echo "2. Checking Test Files..."
echo "----------------------------"

# Count test files
unit_tests=$(find tests/unit -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l)
integration_tests=$(find tests/integration -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l)
e2e_tests=$(find tests/e2e -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l)
a11y_tests=$(find tests/accessibility -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l)

total_tests=$((unit_tests + integration_tests + e2e_tests + a11y_tests))

echo "  Unit Tests: $unit_tests files"
echo "  Integration Tests: $integration_tests files"
echo "  E2E Tests: $e2e_tests files"
echo "  Accessibility Tests: $a11y_tests files"
echo -e "  ${GREEN}Total: $total_tests test files${NC}"

if [ $total_tests -lt 15 ]; then
    echo -e "${YELLOW}Warning: Expected at least 15 test files${NC}"
fi

echo ""
echo "3. Checking Configuration..."
echo "----------------------------"

if [ -f "jest.config.js" ]; then
    echo -e "  ${GREEN}✓${NC} jest.config.js exists"
else
    echo -e "  ${RED}✗${NC} jest.config.js missing"
fi

if [ -f "jest.setup.js" ]; then
    echo -e "  ${GREEN}✓${NC} jest.setup.js exists"
else
    echo -e "  ${RED}✗${NC} jest.setup.js missing"
fi

if [ -f "playwright.config.ts" ]; then
    echo -e "  ${GREEN}✓${NC} playwright.config.ts exists"
else
    echo -e "  ${RED}✗${NC} playwright.config.ts missing"
fi

echo ""
echo "4. Checking Mock Setup..."
echo "----------------------------"

if [ -f "tests/mocks/handlers.ts" ]; then
    echo -e "  ${GREEN}✓${NC} MSW handlers exist"
else
    echo -e "  ${RED}✗${NC} MSW handlers missing"
fi

if [ -f "tests/mocks/server.ts" ]; then
    echo -e "  ${GREEN}✓${NC} MSW server exists"
else
    echo -e "  ${RED}✗${NC} MSW server missing"
fi

echo ""
echo "5. Checking Documentation..."
echo "----------------------------"

if [ -f "tests/README.md" ]; then
    echo -e "  ${GREEN}✓${NC} tests/README.md exists"
else
    echo -e "  ${RED}✗${NC} tests/README.md missing"
fi

if [ -f "tests/QUICK_REFERENCE.md" ]; then
    echo -e "  ${GREEN}✓${NC} tests/QUICK_REFERENCE.md exists"
else
    echo -e "  ${RED}✗${NC} tests/QUICK_REFERENCE.md missing"
fi

if [ -f "tests/TEST_SUMMARY.md" ]; then
    echo -e "  ${GREEN}✓${NC} tests/TEST_SUMMARY.md exists"
else
    echo -e "  ${RED}✗${NC} tests/TEST_SUMMARY.md missing"
fi

echo ""
echo "6. Checking npm Scripts..."
echo "----------------------------"

scripts=(
    "test"
    "test:watch"
    "test:coverage"
    "test:unit"
    "test:integration"
    "test:a11y"
    "test:e2e"
    "test:all"
)

for script in "${scripts[@]}"; do
    if grep -q "\"$script\"" package.json; then
        echo -e "  ${GREEN}✓${NC} npm run $script"
    else
        echo -e "  ${RED}✗${NC} npm run $script missing"
    fi
done

echo ""
echo "========================================"
echo "Verification Summary"
echo "========================================"
echo ""

if [ $missing_deps -eq 0 ] && [ $total_tests -ge 15 ]; then
    echo -e "${GREEN}✓ Testing suite is properly configured!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Run: npm run test"
    echo "  2. Run: npm run test:e2e"
    echo "  3. Run: npm run test:coverage"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some issues found. Please review above.${NC}"
    echo ""
    exit 1
fi
