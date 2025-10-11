# Frontend Quick Start Guide

## Installation & Setup

### 1. Navigate to Frontend Directory
```bash
cd C:/Users/brand/Development/Project_Workspace/active-development/language-learning/subjunctive_practice/frontend
```

### 2. Install Dependencies
```bash
npm install
```

This will install approximately 1,000+ packages including:
- Next.js 14+
- React 18+
- Redux Toolkit
- Tailwind CSS
- TypeScript
- All UI components and utilities

**Expected time:** 2-5 minutes depending on internet speed

### 3. Verify Installation

Check that key files exist:
```bash
ls -la package.json tsconfig.json next.config.js tailwind.config.ts
```

### 4. Start Development Server
```bash
npm run dev
```

**Expected output:**
```
> subjunctive-practice-frontend@1.0.0 dev
> next dev

  ▲ Next.js 14.2.0
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.3s
```

### 5. Open in Browser

Navigate to: [http://localhost:3000](http://localhost:3000)

**Expected behavior:**
- You should be redirected to `/auth/login`
- Login form should be displayed
- No console errors

## File Structure Overview

```
frontend/
├── app/                    # Next.js App Router
│   ├── auth/login/        # Login page
│   ├── dashboard/         # Dashboard page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home (redirects)
│   └── providers.tsx      # Redux provider
│
├── components/ui/         # UI components
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   ├── label.tsx
│   ├── toast.tsx
│   └── toaster.tsx
│
├── hooks/                 # Custom hooks
│   ├── use-redux.ts      # Typed Redux hooks
│   └── use-toast.tsx     # Toast notifications
│
├── lib/                   # Utilities
│   ├── api-client.ts     # HTTP client
│   └── utils.ts          # Helper functions
│
├── store/                 # Redux store
│   ├── services/api.ts   # RTK Query
│   ├── slices/auth-slice.ts
│   └── store.ts          # Store config
│
├── styles/
│   └── globals.css       # Global styles
│
├── types/
│   └── index.ts          # TypeScript types
│
└── Configuration Files
    ├── .env.local        # Environment variables
    ├── .eslintrc.json   # ESLint config
    ├── .prettierrc      # Prettier config
    ├── next.config.js   # Next.js config
    ├── package.json     # Dependencies
    ├── tsconfig.json    # TypeScript config
    └── tailwind.config.ts
```

## Development Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Run production build |
| `npm run lint` | Lint code |
| `npm run format` | Format code |
| `npm run type-check` | Check TypeScript |

## Testing the Setup

### 1. Test Login Page

Navigate to: `http://localhost:3000/auth/login`

**Verify:**
- [x] Login form renders
- [x] Username and password fields present
- [x] Submit button present
- [x] No console errors

### 2. Test Type Safety

Try modifying `app/auth/login/page.tsx`:
```tsx
const { user } = useAppSelector((state) => state.nonexistent); // Should error
```

TypeScript should show an error.

### 3. Test Styling

The login page should have:
- Centered card layout
- Blue primary button
- Clean, modern design
- Responsive layout

### 4. Test API Client

Check browser DevTools Console when trying to login.
You should see network requests to the backend API.

## Environment Configuration

The `.env.local` file contains:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Spanish Subjunctive Practice
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=true
```

**Update if needed:**
- Change API URL if backend is on different port
- Enable/disable debug mode
- Configure analytics

## Common Issues & Solutions

### Issue: Port 3000 already in use
```bash
# Use different port
npm run dev -- -p 3001
```

### Issue: Module not found
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript errors
```bash
# Run type check
npm run type-check
```

### Issue: Build fails
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

## Next Steps

1. **Test Backend Connection**
   - Ensure backend is running on port 8000
   - Try logging in with test credentials
   - Verify API calls in Network tab

2. **Explore the Code**
   - Check `app/` for pages
   - Review `store/` for state management
   - Examine `lib/api-client.ts` for API setup

3. **Add Features**
   - Create new pages in `app/`
   - Add components in `components/`
   - Extend Redux store in `store/`

4. **Customize Styling**
   - Modify `tailwind.config.ts`
   - Update `styles/globals.css`
   - Customize component variants

## Additional Resources

- **Documentation:** See `docs/frontend-setup-guide.md` for detailed info
- **Next.js Docs:** https://nextjs.org/docs
- **Redux Toolkit:** https://redux-toolkit.js.org/
- **Tailwind CSS:** https://tailwindcss.com/docs

## Success Checklist

Before considering the frontend setup complete, verify:

- [x] Dependencies installed (`node_modules/` exists)
- [x] Dev server starts without errors
- [x] Login page renders at `/auth/login`
- [x] TypeScript compilation works
- [x] Tailwind CSS styles apply
- [x] Redux DevTools available (install extension)
- [x] No console errors
- [x] API client configured
- [x] Environment variables set

## Status: Ready for Development

The frontend is now fully configured and ready for:
- Feature development
- Component creation
- API integration
- Testing
- Deployment

**Start coding!** 🚀
