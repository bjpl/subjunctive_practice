# UX Features Quick Reference

Quick reference guide for using the UX enhancement features.

---

## Toast Notifications

```typescript
import { useEnhancedToast } from '@/hooks/useEnhancedToast';

const { success, error, warning, info, promise } = useEnhancedToast();

// Simple notifications
success('Title', 'Description');
error('Error!', 'Something went wrong');
warning('Warning!');
info('Info');

// Track async operations
promise(apiCall(), {
  loading: 'Saving...',
  success: 'Saved!',
  error: 'Failed'
});
```

---

## Loading States

```typescript
import {
  Skeleton,
  LoadingSpinner,
  LoadingOverlay,
  CardSkeleton
} from '@/components/layout/LoadingSkeleton';

// Skeleton placeholders
<Skeleton width="100%" height={16} />
<CardSkeleton />

// Spinners
<LoadingSpinner size="md" />
<LoadingOverlay message="Loading..." />
```

---

## Error Handling

```typescript
import { ErrorBoundary } from '@/components/layout/ErrorBoundary';

<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>
```

---

## Confirmation Modals

```typescript
import { useConfirmModal } from '@/components/feedback/ConfirmModal';

const { confirm, ConfirmModal } = useConfirmModal();

const confirmed = await confirm({
  title: 'Delete?',
  description: 'Cannot be undone',
  variant: 'danger'
});

return <ConfirmModal />;
```

---

## Keyboard Shortcuts

```typescript
import { useKeyboardShortcuts, commonShortcuts } from '@/hooks/useKeyboardShortcuts';

useKeyboardShortcuts([
  commonShortcuts.submit(() => handleSubmit()),
  commonShortcuts.escape(() => handleCancel()),
  {
    key: 'n',
    ctrl: true,
    callback: () => next()
  }
]);
```

---

## Swipe Gestures

```typescript
import { useSwipeNavigation } from '@/hooks/useSwipeGesture';

const ref = useSwipeNavigation({
  onNext: () => next(),
  onPrevious: () => previous()
});

return <div ref={ref}>Swipeable</div>;
```

---

## Help Tooltips

```typescript
import { HelpTooltip } from '@/components/feedback/HelpTooltip';

<HelpTooltip content="Help text">
  <button>Help</button>
</HelpTooltip>
```

---

## Animations

```typescript
import { motion } from 'framer-motion';
import { fadeInVariants, cardVariants } from '@/lib/animations';

<motion.div
  variants={fadeInVariants}
  initial="hidden"
  animate="visible"
>
  Content
</motion.div>
```

---

## Page Transitions

```typescript
import { PageTransition } from '@/components/layout/PageTransition';

export default function Page() {
  return (
    <PageTransition>
      {/* Page content */}
    </PageTransition>
  );
}
```

---

## Common Patterns

### Form Submission with Feedback
```typescript
const { success, error } = useEnhancedToast();
const { confirm, ConfirmModal } = useConfirmModal();

const handleSubmit = async () => {
  try {
    await api.submit(data);
    success('Submitted!');
  } catch (err) {
    error('Failed', err.message);
  }
};

const handleDelete = async () => {
  const confirmed = await confirm({
    title: 'Delete?',
    variant: 'danger'
  });

  if (confirmed) {
    await api.delete();
    success('Deleted!');
  }
};

return <ConfirmModal />;
```

### Loading with Skeleton
```typescript
const [loading, setLoading] = useState(true);

if (loading) {
  return <CardSkeleton />;
}

return <Card {...data} />;
```

### Keyboard Navigation
```typescript
useKeyboardShortcuts([
  { key: 'ArrowRight', callback: () => next() },
  { key: 'ArrowLeft', callback: () => previous() },
  { key: 'Enter', callback: () => submit() },
  { key: 'Escape', callback: () => close() }
]);
```

---

## Best Practices

1. **Always wrap async operations with toast.promise()**
2. **Use ErrorBoundary for component trees**
3. **Provide keyboard shortcuts for power users**
4. **Show loading states for >200ms operations**
5. **Confirm destructive actions**
6. **Use tooltips for complex UI elements**
7. **Enable swipe gestures on mobile**

---

## Accessibility

- All components have ARIA labels
- Keyboard navigation supported
- Focus management automatic
- Screen reader friendly
- Reduced motion respected

---

## Performance Tips

1. Disable animations in tests:
```typescript
import { MotionGlobalConfig } from 'framer-motion';
MotionGlobalConfig.skipAnimations = true;
```

2. Lazy load heavy components:
```typescript
const HeavyComponent = lazy(() => import('./Heavy'));
```

3. Memoize animation variants:
```typescript
const variants = useMemo(() => cardVariants, []);
```
