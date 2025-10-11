# Frontend Quick Reference Guide
## Spanish Subjunctive Practice - Developer Cheat Sheet

## Common Commands

### Development
```bash
npm run dev              # Start dev server (http://localhost:3000)
npm run build            # Build for production
npm run start            # Start production server
```

### Code Quality
```bash
npm run lint             # Check linting
npm run lint:fix         # Auto-fix linting issues
npm run format           # Format code with Prettier
npm run format:check     # Check formatting
npm run type-check       # TypeScript validation
npm run validate         # Run all checks
```

### Testing
```bash
npm run test             # Run unit tests
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
npm run test:e2e         # E2E tests (Playwright)
npm run test:a11y        # Accessibility tests
```

### Build Analysis
```bash
npm run analyze          # Analyze bundle size
ANALYZE=true npm run build
```

### Docker
```bash
npm run docker:build     # Build Docker image
npm run docker:run       # Run Docker container
```

## File Structure

```
frontend/
├── app/                 # Next.js App Router
│   ├── (auth)/         # Route groups
│   ├── api/            # API routes
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Home page
├── components/          # Reusable components
│   ├── ui/             # UI primitives (Button, Input, etc.)
│   └── features/       # Feature components
├── lib/                # Utility functions
├── hooks/              # Custom React hooks
├── store/              # State management (Redux)
├── types/              # TypeScript definitions
└── public/             # Static assets
```

## Enhanced Configuration Files

### Package Management
- `package.enhanced.json` - Enhanced dependencies and scripts
- `.npmrc` - npm configuration

### TypeScript
- `tsconfig.json` - Already configured with strict mode
- Path aliases: `@/*`, `@/components/*`, `@/lib/*`, etc.

### Linting & Formatting
- `.eslintrc.enhanced.json` - ESLint with accessibility rules
- `.prettierrc.enhanced` - Prettier with Tailwind plugin
- `.lintstagedrc.json` - Lint-staged configuration

### Styling
- `tailwind.config.enhanced.ts` - Enhanced Tailwind with a11y utilities
- `postcss.config.js` - PostCSS configuration

### Build & Deploy
- `next.config.enhanced.js` - Enhanced Next.js config
- `vercel.json` - Vercel deployment
- `netlify.toml` - Netlify deployment
- `Dockerfile` - Docker configuration
- `.dockerignore` - Docker ignore rules

### Testing
- `jest.config.js` - Jest configuration
- `jest.setup.js` - Jest setup with accessibility matchers
- `playwright.config.ts` - Playwright E2E configuration

### Git Hooks
- `.husky/pre-commit` - Pre-commit hook
- `.husky/pre-push` - Pre-push hook

## Environment Variables

### Development (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_ENABLE_DEBUG=true
```

### Production
```bash
NEXT_PUBLIC_API_URL=https://api.production.com
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_GA_ID=your-ga-id
```

## Path Aliases

```typescript
import { Button } from '@/components/ui/Button'
import { useAuth } from '@/hooks/useAuth'
import { cn } from '@/lib/utils'
import type { User } from '@/types/user'
```

## Accessibility Utilities (Tailwind)

```jsx
<div className="sr-only">Screen reader only content</div>
<button className="focus-visible-ring">Accessible button</button>
<div className="reduced-motion">Respects motion preference</div>
<div className="high-contrast">High contrast support</div>
```

## Testing Patterns

### Unit Test with Accessibility
```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('should be accessible', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### E2E Test
```typescript
import { test, expect } from '@playwright/test';

test('should navigate to practice page', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Start Practice');
  await expect(page).toHaveURL('/practice');
});
```

## Deployment

### Vercel
```bash
vercel                   # Deploy to preview
vercel --prod           # Deploy to production
```

### Netlify
```bash
netlify deploy          # Deploy to preview
netlify deploy --prod   # Deploy to production
```

### Docker
```bash
docker build -t subjunctive-frontend .
docker run -p 3000:3000 subjunctive-frontend
```

## Code Quality Checklist

Before committing:
- [ ] `npm run type-check` passes
- [ ] `npm run lint` passes
- [ ] `npm run format:check` passes
- [ ] `npm run test` passes
- [ ] No console.log statements (except console.error/warn)
- [ ] All accessibility rules followed

## Accessibility Checklist

- [ ] All interactive elements have accessible labels
- [ ] Keyboard navigation works
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Alternative text for images
- [ ] Forms have proper labels
- [ ] Error messages are announced
- [ ] Touch targets are 44px minimum

## Performance Optimization

### Image Optimization
```jsx
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={800}
  height={600}
  loading="lazy"
  quality={85}
/>
```

### Code Splitting
```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./Heavy'), {
  loading: () => <Skeleton />,
  ssr: false
});
```

### Font Optimization
```typescript
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

## Common Issues & Solutions

### Issue: Type errors
```bash
rm -rf .next && npm run build
```

### Issue: Husky not working
```bash
npm run prepare
chmod +x .husky/*
```

### Issue: ESLint errors
```bash
npm run lint:fix
```

### Issue: Build fails
```bash
rm -rf .next node_modules
npm install
npm run build
```

## Useful Links

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Radix UI](https://www.radix-ui.com)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [TypeScript](https://www.typescriptlang.org/docs/)

---

**Pro Tip:** Use `npm run validate` before pushing to catch all issues early!
