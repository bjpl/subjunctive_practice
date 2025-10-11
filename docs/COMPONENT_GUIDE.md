# Component Usage Guide

## Overview

This guide provides comprehensive documentation for using and creating components in the Spanish Subjunctive Practice frontend application.

## Component Architecture

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── auth/                # Authentication pages
│   ├── dashboard/           # Dashboard page
│   ├── practice/            # Practice interface
│   ├── progress/            # Progress tracking
│   └── settings/            # Settings page
├── components/              # React components
│   ├── ui/                 # Base UI components
│   ├── features/           # Feature-specific components
│   ├── layout/             # Layout components
│   └── common/             # Shared components
├── hooks/                   # Custom React hooks
└── lib/                    # Utilities and helpers
```

## UI Components (Radix UI + Tailwind)

### Button

A versatile button component with multiple variants.

**Location:** `components/ui/button.tsx`

**Variants:**
- `default`: Primary action button
- `destructive`: Dangerous actions
- `outline`: Secondary actions
- `ghost`: Minimal visibility
- `link`: Link-style button

**Sizes:**
- `sm`: Small button
- `md`: Default size
- `lg`: Large button
- `icon`: Icon-only button

**Usage:**
```tsx
import { Button } from '@/components/ui/button';

function MyComponent() {
  return (
    <>
      <Button variant="default">Primary Action</Button>
      <Button variant="outline" size="sm">Secondary</Button>
      <Button variant="destructive">Delete</Button>
      <Button variant="ghost">Cancel</Button>
      <Button variant="link">Learn More</Button>
    </>
  );
}
```

**With Icons:**
```tsx
import { Button } from '@/components/ui/button';
import { Plus, Trash2 } from 'lucide-react';

<Button>
  <Plus className="mr-2 h-4 w-4" />
  Add Exercise
</Button>

<Button variant="destructive" size="icon">
  <Trash2 className="h-4 w-4" />
</Button>
```

---

### Card

Container component for grouping related content.

**Location:** `components/ui/card.tsx`

**Sub-components:**
- `Card`: Main container
- `CardHeader`: Header section
- `CardTitle`: Title text
- `CardDescription`: Description text
- `CardContent`: Main content
- `CardFooter`: Footer section

**Usage:**
```tsx
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter
} from '@/components/ui/card';

function ExerciseCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Present Subjunctive</CardTitle>
        <CardDescription>Practice basic conjugations</CardDescription>
      </CardHeader>
      <CardContent>
        <p>Espero que tú _____ (hablar) español.</p>
      </CardContent>
      <CardFooter>
        <Button>Submit Answer</Button>
      </CardFooter>
    </Card>
  );
}
```

---

### Input

Text input component with validation support.

**Location:** `components/ui/input.tsx`

**Usage:**
```tsx
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

function LoginForm() {
  return (
    <div className="space-y-4">
      <div>
        <Label htmlFor="username">Username</Label>
        <Input
          id="username"
          type="text"
          placeholder="Enter username"
          required
        />
      </div>
      <div>
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="Enter password"
          required
        />
      </div>
    </div>
  );
}
```

**With React Hook Form:**
```tsx
import { useForm } from 'react-hook-form';
import { Input } from '@/components/ui/input';

function Form() {
  const { register, handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('username', { required: true })} />
    </form>
  );
}
```

---

### Dialog

Modal dialog component.

**Location:** `components/ui/dialog.tsx`

**Sub-components:**
- `Dialog`: Main container
- `DialogTrigger`: Trigger button
- `DialogContent`: Dialog content
- `DialogHeader`: Header section
- `DialogTitle`: Title text
- `DialogDescription`: Description
- `DialogFooter`: Footer section

**Usage:**
```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog';

function ExerciseDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>View Explanation</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Exercise Explanation</DialogTitle>
          <DialogDescription>
            Learn why this answer is correct.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <p>The present subjunctive is used after "espero que"...</p>
        </div>
        <DialogFooter>
          <Button>Got it!</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

---

### Toast

Notification toast component.

**Location:** `components/ui/toast.tsx`

**Usage:**
```tsx
import { useToast } from '@/hooks/useToast';

function MyComponent() {
  const { success, error, info, warning } = useToast();

  const handleSuccess = () => {
    success('Exercise completed successfully!');
  };

  const handleError = () => {
    error('Failed to submit answer. Please try again.');
  };

  const handleInfo = () => {
    info('New exercises available!');
  };

  const handleWarning = () => {
    warning('Your session will expire in 5 minutes.');
  };

  return (
    <>
      <Button onClick={handleSuccess}>Show Success</Button>
      <Button onClick={handleError}>Show Error</Button>
      <Button onClick={handleInfo}>Show Info</Button>
      <Button onClick={handleWarning}>Show Warning</Button>
    </>
  );
}
```

---

### Select

Dropdown select component.

**Location:** `components/ui/select.tsx`

**Usage:**
```tsx
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';

function DifficultySelector() {
  return (
    <Select onValueChange={(value) => console.log(value)}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select difficulty" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="1">Easy</SelectItem>
        <SelectItem value="2">Medium</SelectItem>
        <SelectItem value="3">Hard</SelectItem>
        <SelectItem value="4">Expert</SelectItem>
      </SelectContent>
    </Select>
  );
}
```

---

### Progress

Progress bar component.

**Location:** `components/ui/progress.tsx`

**Usage:**
```tsx
import { Progress } from '@/components/ui/progress';

function ProgressDisplay() {
  const progress = 65; // 65%

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>Progress to Level 6</span>
        <span>{progress}%</span>
      </div>
      <Progress value={progress} />
    </div>
  );
}
```

---

## Feature Components

### ExerciseCard

Displays a single exercise with input and validation.

**Location:** `components/features/ExerciseCard.tsx`

**Props:**
```typescript
interface ExerciseCardProps {
  exercise: Exercise;
  onSubmit: (answer: string) => void;
  isSubmitting?: boolean;
  lastValidation?: Validation | null;
}
```

**Usage:**
```tsx
import { ExerciseCard } from '@/components/features/ExerciseCard';
import { useExercise } from '@/hooks';

function PracticePage() {
  const { currentExercise, submitAnswer, isSubmitting, lastValidation } = useExercise();

  const handleSubmit = async (answer: string) => {
    await submitAnswer(answer);
  };

  if (!currentExercise) return <div>Loading...</div>;

  return (
    <ExerciseCard
      exercise={currentExercise}
      onSubmit={handleSubmit}
      isSubmitting={isSubmitting}
      lastValidation={lastValidation}
    />
  );
}
```

---

### ProgressDashboard

Comprehensive progress tracking dashboard.

**Location:** `components/features/ProgressDashboard.tsx`

**Usage:**
```tsx
import { ProgressDashboard } from '@/components/features/ProgressDashboard';
import { useProgress } from '@/hooks';

function ProgressPage() {
  const { progress, statistics } = useProgress();

  return (
    <ProgressDashboard
      progress={progress}
      statistics={statistics}
    />
  );
}
```

---

### StatsCard

Display statistics in a card format.

**Location:** `components/features/StatsCard.tsx`

**Props:**
```typescript
interface StatsCardProps {
  title: string;
  value: string | number;
  icon?: ReactNode;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}
```

**Usage:**
```tsx
import { StatsCard } from '@/components/features/StatsCard';
import { Trophy, Target, Flame } from 'lucide-react';

function StatsDisplay() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <StatsCard
        title="Total Exercises"
        value={125}
        icon={<Target className="h-4 w-4" />}
        trend={{ value: 12, isPositive: true }}
      />
      <StatsCard
        title="Accuracy Rate"
        value="78.4%"
        icon={<Trophy className="h-4 w-4" />}
        trend={{ value: 5, isPositive: true }}
      />
      <StatsCard
        title="Current Streak"
        value={7}
        icon={<Flame className="h-4 w-4" />}
      />
    </div>
  );
}
```

---

### AuthForm

Reusable authentication form component.

**Location:** `components/features/AuthForm.tsx`

**Props:**
```typescript
interface AuthFormProps {
  type: 'login' | 'register';
  onSubmit: (data: LoginData | RegisterData) => Promise<void>;
  isLoading?: boolean;
  error?: string | null;
}
```

**Usage:**
```tsx
import { AuthForm } from '@/components/features/AuthForm';
import { useAuth } from '@/hooks';

function LoginPage() {
  const { login, isLoading, error } = useAuth();

  return (
    <AuthForm
      type="login"
      onSubmit={login}
      isLoading={isLoading}
      error={error}
    />
  );
}
```

---

## Layout Components

### AppLayout

Main application layout with navigation.

**Location:** `components/layout/AppLayout.tsx`

**Usage:**
```tsx
import { AppLayout } from '@/components/layout/AppLayout';

function DashboardPage() {
  return (
    <AppLayout>
      <h1>Dashboard</h1>
      {/* Page content */}
    </AppLayout>
  );
}
```

---

### Navbar

Top navigation bar.

**Location:** `components/layout/Navbar.tsx`

**Usage:**
```tsx
import { Navbar } from '@/components/layout/Navbar';

function Layout({ children }) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  );
}
```

---

### Sidebar

Sidebar navigation.

**Location:** `components/layout/Sidebar.tsx`

**Usage:**
```tsx
import { Sidebar } from '@/components/layout/Sidebar';

function Layout({ children }) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

---

## Custom Hooks

### useAuth

Authentication hook.

**Location:** `hooks/useAuth.ts`

**Usage:**
```tsx
import { useAuth } from '@/hooks/useAuth';

function MyComponent() {
  const {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    refreshAccessToken
  } = useAuth();

  const handleLogin = async () => {
    try {
      await login({ username: 'user', password: 'pass' });
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div>
      {isAuthenticated ? (
        <>
          <p>Welcome, {user?.username}!</p>
          <Button onClick={logout}>Logout</Button>
        </>
      ) : (
        <Button onClick={handleLogin}>Login</Button>
      )}
    </div>
  );
}
```

---

### useExercise

Exercise management hook.

**Location:** `hooks/useExercise.ts`

**Usage:**
```tsx
import { useExercise } from '@/hooks/useExercise';

function ExercisePage() {
  const {
    currentExercise,
    currentAnswer,
    lastValidation,
    isSubmitting,
    updateAnswer,
    submitAnswer,
    getNextExercise
  } = useExercise();

  const handleSubmit = async () => {
    const validation = await submitAnswer();
    if (validation.is_correct) {
      setTimeout(() => getNextExercise(), 2000);
    }
  };

  return (
    <div>
      <p>{currentExercise?.prompt}</p>
      <Input
        value={currentAnswer}
        onChange={(e) => updateAnswer(e.target.value)}
      />
      <Button onClick={handleSubmit} disabled={isSubmitting}>
        Submit
      </Button>
    </div>
  );
}
```

---

### useProgress

Progress tracking hook.

**Location:** `hooks/useProgress.ts`

**Usage:**
```tsx
import { useProgress } from '@/hooks/useProgress';

function ProgressPage() {
  const {
    progress,
    statistics,
    isLoading,
    refreshProgress,
    trackExerciseCompletion
  } = useProgress();

  const handleExerciseComplete = (isCorrect: boolean, score: number) => {
    trackExerciseCompletion(isCorrect, score);
  };

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Level: {progress?.level}</h2>
      <p>XP: {progress?.experience_points}</p>
      <p>Accuracy: {progress?.accuracy_rate}%</p>
      <Button onClick={refreshProgress}>Refresh</Button>
    </div>
  );
}
```

---

## Styling Guidelines

### Tailwind CSS Classes

**Spacing:**
```tsx
<div className="p-4 m-2">           {/* Padding and margin */}
<div className="px-6 py-4">         {/* Horizontal and vertical */}
<div className="space-y-4">         {/* Vertical spacing between children */}
<div className="gap-4">             {/* Grid/flex gap */}
```

**Layout:**
```tsx
<div className="flex items-center justify-between">
<div className="grid grid-cols-3 gap-4">
<div className="container mx-auto max-w-7xl">
```

**Typography:**
```tsx
<h1 className="text-3xl font-bold">
<p className="text-sm text-gray-600">
<span className="text-muted-foreground">
```

**Colors:**
```tsx
<div className="bg-primary text-primary-foreground">
<div className="bg-secondary text-secondary-foreground">
<div className="bg-muted text-muted-foreground">
<div className="bg-destructive text-destructive-foreground">
```

**Responsive Design:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
<div className="text-sm md:text-base lg:text-lg">
<div className="hidden md:block">  {/* Hide on mobile */}
```

---

## Component Composition

### Example: Complete Exercise Component

```tsx
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/useToast';
import { useState } from 'react';

export function ExerciseComponent({ exercise, onSubmit }) {
  const [answer, setAnswer] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { success, error } = useToast();

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const validation = await onSubmit(answer);
      if (validation.is_correct) {
        success('Correct! Well done!');
      } else {
        error('Incorrect. Try again!');
      }
    } catch (err) {
      error('Failed to submit answer');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Exercise</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-lg">{exercise.prompt}</p>
        <Input
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Enter your answer"
          onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
        />
      </CardContent>
      <CardFooter>
        <Button
          onClick={handleSubmit}
          disabled={isSubmitting || !answer}
          className="w-full"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Answer'}
        </Button>
      </CardFooter>
    </Card>
  );
}
```

---

## Best Practices

1. **Use TypeScript**: Always type your components and props
2. **Accessibility**: Include ARIA labels and keyboard navigation
3. **Responsive**: Design mobile-first, scale up
4. **Performance**: Use React.memo for expensive components
5. **Reusability**: Extract common patterns into shared components
6. **Testing**: Write unit tests for complex components
7. **Documentation**: Document props and usage examples

---

## Next Steps

- Review [State Management](./STATE_MANAGEMENT.md)
- Check [API Documentation](./API_DOCUMENTATION.md)
- See [Development Guide](./DEVELOPMENT.md)
