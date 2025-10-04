# Frontend DevOps Setup Guide
## Spanish Subjunctive Practice Application

This document provides comprehensive instructions for setting up, configuring, and deploying the frontend application.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Configuration Files](#configuration-files)
5. [Development Workflow](#development-workflow)
6. [Build Optimization](#build-optimization)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The frontend is built with:
- **Next.js 14+** - React framework with App Router
- **TypeScript 5+** - Type-safe development
- **Tailwind CSS 3+** - Utility-first styling
- **Radix UI** - Accessible component primitives
- **WCAG 2.1 AA** - Full accessibility compliance

## Prerequisites

- **Node.js**: >= 18.0.0
- **npm**: >= 9.0.0
- **Git**: Latest version

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env.local

# Edit with your values
nano .env.local
```

### 3. Run Development Server

```bash
npm run dev
```

Visit http://localhost:3000

---

## Configuration Files

### Package Configuration

#### Enhanced package.json
Located at: `frontend/package.enhanced.json`

**Key Features:**
- Comprehensive scripts for all workflows
- Testing setup with Jest and Playwright
- Accessibility testing with jest-axe
- Bundle analysis tools
- Git hooks with Husky

**Available Scripts:**
```bash
npm run dev              # Development server
npm run build            # Production build
npm run start            # Production server
npm run lint             # Run ESLint
npm run lint:fix         # Fix ESLint issues
npm run format           # Format with Prettier
npm run format:check     # Check formatting
npm run type-check       # TypeScript validation
npm run test             # Run tests
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
npm run test:e2e         # E2E tests
npm run test:a11y        # Accessibility tests
npm run analyze          # Bundle analysis
npm run validate         # All checks
npm run docker:build     # Build Docker image
npm run docker:run       # Run Docker container
```

### TypeScript Configuration

**Current:** `frontend/tsconfig.json` (already configured)
- Strict mode enabled
- Path aliases configured
- Next.js plugin included

**Path Aliases:**
```typescript
@/*                  // Root
@/components/*       // Components
@/lib/*             // Utilities
@/store/*           // State management
@/types/*           // Type definitions
@/hooks/*           // Custom hooks
@/app/*             // App directory
```

### ESLint Configuration

**Enhanced:** `frontend/.eslintrc.enhanced.json`

**Features:**
- TypeScript rules with strict checking
- React and React Hooks rules
- **Accessibility rules (WCAG 2.1 AA)**
- Import order and organization
- Prettier integration

**Key Rules:**
- All `jsx-a11y` rules enforced
- No unused variables (strict)
- Consistent type imports
- Import order alphabetization
- Console warnings (allow error/warn only)

### Prettier Configuration

**Enhanced:** `frontend/.prettierrc.enhanced`

**Features:**
- Tailwind CSS plugin integration
- Automatic class sorting
- Consistent formatting rules

**Settings:**
- Semi-colons: true
- Single quotes: false
- Print width: 100
- Tab width: 2
- Trailing commas: ES5

### Tailwind Configuration

**Enhanced:** `frontend/tailwind.config.enhanced.ts`

**Accessibility Features:**
- Touch target utilities (44px minimum)
- Screen reader utilities
- Focus ring styles
- Reduced motion support
- High contrast support
- Scalable font sizes

**Custom Utilities:**
```css
.sr-only              /* Screen reader only */
.not-sr-only          /* Remove SR only */
.focus-visible-ring   /* Accessible focus */
.reduced-motion       /* Respect motion preference */
.high-contrast        /* High contrast support */
```

**Color System:**
- Semantic color tokens
- Light/Dark/High-contrast themes
- Success/Warning/Error states
- Accessible contrast ratios

### Next.js Configuration

**Enhanced:** `frontend/next.config.enhanced.js`

**Optimizations:**
- Bundle analyzer integration
- Security headers
- Image optimization
- Code splitting strategy
- CSS optimization
- Webpack customization

**Security Headers:**
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Referrer-Policy
- Permissions-Policy
- Strict-Transport-Security

---

## Development Workflow

### 1. Git Hooks (Husky)

**Pre-commit Hook:**
```bash
# Located: frontend/.husky/pre-commit
- Runs lint-staged
- Performs type checking
```

**Pre-push Hook:**
```bash
# Located: frontend/.husky/pre-push
- Runs full validation
- Ensures code quality
```

**Setup:**
```bash
npm run prepare
```

### 2. Lint-staged Configuration

Located: `frontend/.lintstagedrc.json`

**Actions:**
- Auto-fix ESLint issues
- Format with Prettier
- Type check TypeScript

### 3. Code Quality Workflow

```bash
# Before committing
npm run validate

# This runs:
# - Type checking
# - Linting
# - Format checking
# - Test coverage
```

---

## Build Optimization

### Bundle Analysis

```bash
# Generate bundle analysis
ANALYZE=true npm run build

# View the analysis report
```

### Code Splitting

**Automatic:**
- Route-based splitting
- Component lazy loading
- Dynamic imports

**Manual:**
```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSkeleton />,
  ssr: false
});
```

### Image Optimization

```typescript
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={800}
  height={600}
  priority={false}
  loading="lazy"
  quality={85}
/>
```

### Performance Targets

- **LCP**: < 2.5s
- **FID**: < 100ms
- **CLS**: < 0.1
- **Bundle Size**: Monitor with analyzer

---

## Testing

### Unit Tests (Jest)

```bash
# Run tests
npm run test

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

**Configuration:** (Add `jest.config.js`)
```javascript
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
};
```

### E2E Tests (Playwright)

```bash
# Run E2E tests
npm run test:e2e

# Interactive mode
npx playwright test --ui
```

**Configuration:** (Add `playwright.config.ts`)
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:3000',
  },
});
```

### Accessibility Tests

```bash
# Run accessibility tests
npm run test:a11y
```

**Example:**
```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('should have no accessibility violations', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

---

## Deployment

### Vercel Deployment

**Configuration:** `frontend/vercel.json`

**Setup:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deploy
vercel --prod
```

**Environment Variables:**
1. Go to Vercel dashboard
2. Add environment variables:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_ENVIRONMENT=production`

### Netlify Deployment

**Configuration:** `frontend/netlify.toml`

**Setup:**
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy

# Production deploy
netlify deploy --prod
```

**Environment Variables:**
1. Go to Netlify dashboard
2. Site settings > Environment variables
3. Add production values

### Docker Deployment

**Configuration:** `frontend/Dockerfile`

**Build & Run:**
```bash
# Build image
npm run docker:build

# Run container
npm run docker:run

# Or manually:
docker build -t subjunctive-frontend .
docker run -p 3000:3000 subjunctive-frontend
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api
    depends_on:
      - backend
```

---

## Environment Variables

### Development (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_ENABLE_DEBUG=true
```

### Production

```bash
NEXT_PUBLIC_API_URL=https://api.yourapp.com
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_ENABLE_DEBUG=false
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_GA_ID=your-ga-id
```

**Security Notes:**
- Never commit `.env` files
- Use platform-specific secret management
- Only `NEXT_PUBLIC_*` vars are exposed to browser
- Rotate secrets regularly

---

## Troubleshooting

### Common Issues

**1. Type Errors**
```bash
# Clear Next.js cache
rm -rf .next

# Rebuild
npm run build
```

**2. ESLint Errors**
```bash
# Auto-fix
npm run lint:fix

# Check specific file
npx eslint --fix path/to/file.tsx
```

**3. Build Failures**
```bash
# Clear all caches
rm -rf .next node_modules
npm install
npm run build
```

**4. Husky Not Working**
```bash
# Reinstall hooks
npm run prepare
chmod +x .husky/*
```

**5. Docker Issues**
```bash
# Clean Docker
docker system prune -a

# Rebuild without cache
docker build --no-cache -t subjunctive-frontend .
```

### Performance Debugging

**1. Bundle Size**
```bash
ANALYZE=true npm run build
```

**2. Lighthouse Audit**
```bash
# Install Lighthouse
npm i -g lighthouse

# Run audit
lighthouse http://localhost:3000 --view
```

**3. React DevTools Profiler**
- Install React DevTools extension
- Use Profiler tab
- Record rendering performance

---

## Best Practices

### Code Organization

```
frontend/
├── app/              # Next.js App Router
│   ├── (auth)/      # Route groups
│   ├── api/         # API routes
│   └── layout.tsx   # Root layout
├── components/       # Reusable components
│   ├── ui/          # UI primitives
│   └── features/    # Feature components
├── lib/             # Utilities
├── hooks/           # Custom hooks
├── store/           # State management
└── types/           # TypeScript types
```

### Component Guidelines

1. **Accessibility First**
   - Always add ARIA labels
   - Keyboard navigation
   - Screen reader support

2. **Performance**
   - Use React.memo wisely
   - Lazy load heavy components
   - Optimize images

3. **Type Safety**
   - Full TypeScript coverage
   - Export all types
   - No `any` types

### Git Workflow

```bash
# Feature branch
git checkout -b feature/your-feature

# Make changes, test, commit
npm run validate
git add .
git commit -m "feat: your feature"

# Push (pre-push hook runs validate)
git push origin feature/your-feature
```

---

## Maintenance

### Dependency Updates

```bash
# Check outdated packages
npm outdated

# Update dependencies
npm update

# Major updates
npx npm-check-updates -u
npm install
```

### Security Audits

```bash
# Run security audit
npm audit

# Fix vulnerabilities
npm audit fix

# Force fix
npm audit fix --force
```

### Performance Monitoring

- Set up Vercel Analytics
- Configure Sentry for error tracking
- Monitor Core Web Vitals
- Track bundle size over time

---

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## Support

For issues and questions:
1. Check this documentation
2. Review existing GitHub issues
3. Create new issue with template
4. Contact DevOps team

---

**Last Updated:** October 2, 2025
**Version:** 1.0.0
