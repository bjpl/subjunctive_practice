# Spanish Subjunctive Practice - Frontend

Modern React/Next.js frontend for the Spanish Subjunctive Practice application.

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit with RTK Query
- **Form Handling**: React Hook Form + Zod
- **UI Components**: Radix UI
- **HTTP Client**: Axios
- **Icons**: Lucide React

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── auth/              # Authentication pages
│   ├── dashboard/         # Dashboard page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── providers.tsx      # Redux and other providers
├── components/            # React components
│   └── ui/               # UI component library
├── hooks/                # Custom React hooks
├── lib/                  # Utilities and helpers
│   ├── api-client.ts    # API client configuration
│   └── utils.ts         # Utility functions
├── store/                # Redux store
│   ├── slices/          # Redux slices
│   ├── services/        # RTK Query services
│   └── store.ts         # Store configuration
├── styles/              # Global styles
│   └── globals.css      # Tailwind + custom styles
├── types/               # TypeScript definitions
│   └── index.ts         # Type definitions
└── public/              # Static assets

```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Update the `.env` file with your API URL:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking

## Environment Variables

Create a `.env` file based on `.env.example`:

- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_APP_NAME` - Application name
- `NEXT_PUBLIC_APP_VERSION` - Application version

## Key Features

### State Management

- Redux Toolkit for global state
- RTK Query for API data fetching and caching
- Redux Persist for persistent storage
- Type-safe hooks (`useAppDispatch`, `useAppSelector`)

### API Integration

- Centralized API client with Axios
- Automatic token injection via interceptors
- Error handling and retry logic
- Request/response transformers

### Authentication

- JWT token-based authentication
- Automatic token refresh
- Protected routes
- Persistent login state

### UI Components

- Pre-built UI components using Radix UI
- Fully accessible components
- Consistent design system
- Dark mode support (ready to implement)

### Form Handling

- React Hook Form for performance
- Zod schema validation
- Type-safe form data
- Automatic error handling

## Code Style

- ESLint configuration for Next.js
- Prettier for code formatting
- TypeScript strict mode
- Consistent import ordering

## Path Aliases

The project uses TypeScript path aliases for cleaner imports:

- `@/*` - Root directory
- `@/components/*` - Components
- `@/lib/*` - Libraries and utilities
- `@/store/*` - Redux store
- `@/types/*` - TypeScript types
- `@/hooks/*` - Custom hooks
- `@/styles/*` - Styles

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Hook Form Documentation](https://react-hook-form.com/)
- [Radix UI Documentation](https://www.radix-ui.com/)
