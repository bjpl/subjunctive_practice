# Accessibility Components

This directory contains all accessibility-related components for the Spanish Subjunctive Practice application, ensuring WCAG 2.1 AA compliance.

## Components

### A11ySettings
**File:** `A11ySettings.tsx`

Accessibility settings panel allowing users to customize their experience.

**Features:**
- Dark mode toggle
- High contrast mode
- Font size control (12-24px)
- Line height adjustment (1.0-2.5)
- Letter spacing control (0-0.3em)
- Reduced motion toggle
- Keyboard navigation enhancement
- Screen reader announcements toggle

**Usage:**
```tsx
import { A11ySettings } from '@/components/accessibility';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <A11ySettings
      isOpen={isOpen}
      onClose={() => setIsOpen(false)}
    />
  );
}
```

**Keyboard Shortcut:** `Alt+A`

---

### FocusIndicator
**File:** `FocusIndicator.tsx`

Global focus indicator styles and keyboard user detection.

**Features:**
- 3px yellow outline for keyboard users
- 4px outline in high contrast mode
- Automatic keyboard user detection
- Enhanced focus for all interactive elements

**Usage:**
```tsx
import { FocusIndicator } from '@/components/accessibility';

function App() {
  return (
    <>
      <FocusIndicator />
      {/* Rest of your app */}
    </>
  );
}
```

**Auto-applied:** Should be included in root layout

---

### KeyboardHelp
**File:** `KeyboardHelp.tsx`

Keyboard shortcuts help dialog.

**Features:**
- Complete list of shortcuts
- Organized by category
- Keyboard accessible
- Focus trap
- Escape to close

**Usage:**
```tsx
import { KeyboardHelp } from '@/components/accessibility';

function App() {
  const [showHelp, setShowHelp] = useState(false);

  return (
    <KeyboardHelp
      isOpen={showHelp}
      onClose={() => setShowHelp(false)}
    />
  );
}
```

**Keyboard Shortcut:** `?`

**Categories:**
- Navigation
- General
- Practice
- Accessibility

---

### LiveRegion
**File:** `LiveRegion.tsx`

Screen reader announcement system.

**Components:**
- `LiveRegion` - Individual announcement
- `LiveRegionContainer` - Global container

**Features:**
- Polite announcements (status updates)
- Assertive announcements (errors)
- Auto-clear after delay
- ARIA live regions

**Usage:**
```tsx
import { LiveRegion, LiveRegionContainer } from '@/components/accessibility';

// In root layout
function RootLayout() {
  return (
    <>
      <LiveRegionContainer />
      {/* Rest of app */}
    </>
  );
}

// In component
function Component() {
  const [message, setMessage] = useState('');

  const announceSuccess = () => {
    setMessage('Action completed successfully');
  };

  return (
    <>
      <LiveRegion message={message} priority="polite" />
      {/* Component content */}
    </>
  );
}
```

**Or use the hook:**
```tsx
import { useLiveRegion } from '@/hooks/accessibility';

function Component() {
  const { announcePolite, announceAssertive } = useLiveRegion();

  const handleSuccess = () => {
    announcePolite('Action completed successfully');
  };

  const handleError = () => {
    announceAssertive('Error occurred. Please try again.');
  };
}
```

---

### SkipLinks
**File:** `SkipLinks.tsx`

Skip navigation links for keyboard users.

**Features:**
- Skip to main content
- Skip to navigation
- Skip to footer
- Visible only on focus
- High contrast support

**Usage:**
```tsx
import { SkipLinks } from '@/components/accessibility';

function Layout({ children }) {
  return (
    <>
      <SkipLinks />
      <nav id="navigation">{/* Navigation */}</nav>
      <main id="main-content">{children}</main>
      <footer id="footer">{/* Footer */}</footer>
    </>
  );
}
```

**Required IDs:**
- `#main-content` on `<main>`
- `#navigation` on `<nav>`
- `#footer` on `<footer>`

---

## Installation

All components are already installed. Import from the accessibility directory:

```tsx
import {
  A11ySettings,
  FocusIndicator,
  KeyboardHelp,
  LiveRegion,
  LiveRegionContainer,
  SkipLinks,
} from '@/components/accessibility';
```

## Setup

### 1. Root Layout Setup

Add these components to your root layout:

```tsx
// app/layout.tsx
import {
  FocusIndicator,
  LiveRegionContainer,
  SkipLinks,
} from '@/components/accessibility';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <FocusIndicator />
        <LiveRegionContainer />
        <SkipLinks />

        <nav id="navigation">{/* Navigation */}</nav>
        <main id="main-content">{children}</main>
        <footer id="footer">{/* Footer */}</footer>
      </body>
    </html>
  );
}
```

### 2. Include Global Styles

Import the accessibility stylesheet:

```tsx
// app/layout.tsx or app/globals.css
import '@/styles/accessibility.css';
```

### 3. Add Keyboard Help

Add keyboard help to your app:

```tsx
// app/layout.tsx
import { KeyboardHelp } from '@/components/accessibility';
import { useKeyboardShortcuts } from '@/hooks/accessibility';

function App() {
  const [showKeyboardHelp, setShowKeyboardHelp] = useState(false);

  useKeyboardShortcuts([
    {
      key: '?',
      description: 'Show keyboard shortcuts',
      action: () => setShowKeyboardHelp(true),
    },
  ]);

  return (
    <>
      <KeyboardHelp
        isOpen={showKeyboardHelp}
        onClose={() => setShowKeyboardHelp(false)}
      />
      {/* Rest of app */}
    </>
  );
}
```

### 4. Add Accessibility Settings

Add settings panel to your navigation or settings page:

```tsx
import { A11ySettings } from '@/components/accessibility';

function Navigation() {
  const [showA11ySettings, setShowA11ySettings] = useState(false);

  return (
    <nav>
      <button onClick={() => setShowA11ySettings(true)}>
        Accessibility Settings
      </button>

      <A11ySettings
        isOpen={showA11ySettings}
        onClose={() => setShowA11ySettings(false)}
      />
    </nav>
  );
}
```

## WCAG 2.1 AA Compliance

All components meet WCAG 2.1 AA standards:

| Component | Success Criteria | Status |
|-----------|-----------------|--------|
| A11ySettings | 1.4.4, 1.4.8, 2.3.3 | ✅ |
| FocusIndicator | 2.4.7 | ✅ |
| KeyboardHelp | 2.1.1 | ✅ |
| LiveRegion | 4.1.3 | ✅ |
| SkipLinks | 2.4.1 | ✅ |

## Testing

### Manual Testing

1. **Keyboard Navigation**
   ```
   - Unplug mouse
   - Press Tab to navigate
   - Verify focus indicators visible
   - Test all shortcuts
   ```

2. **Screen Reader**
   ```
   - Enable NVDA/JAWS/VoiceOver
   - Navigate with screen reader
   - Verify announcements
   - Test all interactive elements
   ```

3. **Visual Testing**
   ```
   - Zoom to 200%
   - Enable high contrast mode
   - Test dark mode
   - Verify color contrast
   ```

### Automated Testing

```bash
# Run accessibility tests
npm run test:a11y

# Run Lighthouse audit
npm run audit:lighthouse
```

## Keyboard Shortcuts

### Navigation
- `Tab` - Next element
- `Shift+Tab` - Previous element
- `Enter` - Activate
- `Space` - Activate/toggle
- `Escape` - Close/cancel

### General
- `?` - Show keyboard shortcuts
- `Ctrl+K` - Search
- `Alt+H` - Home
- `Alt+D` - Dashboard

### Practice
- `Enter` - Submit answer
- `Ctrl+H` - Show hint
- `Ctrl+N` - Next exercise
- `Ctrl+P` - Previous exercise

### Accessibility
- `Alt+A` - Settings
- `Ctrl++` - Increase font size
- `Ctrl+-` - Decrease font size

## Best Practices

### 1. Always Use Semantic HTML

```tsx
// ✅ Good
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// ❌ Bad
<div className="nav">
  <div onClick={...}>Home</div>
</div>
```

### 2. Provide Text Alternatives

```tsx
// ✅ Good
<button aria-label="Close dialog">
  <svg aria-hidden="true">×</svg>
</button>

// ❌ Bad
<button>
  <svg>×</svg>
</button>
```

### 3. Use ARIA Correctly

```tsx
// ✅ Good
<div
  role="alert"
  aria-live="assertive"
  aria-atomic="true"
>
  {errorMessage}
</div>

// ❌ Bad
<div className="error">
  {errorMessage}
</div>
```

### 4. Ensure Color Contrast

```tsx
// ✅ Good - 4.5:1 ratio
color: #1f2937; // Dark gray
background: #ffffff; // White

// ❌ Bad - 2.5:1 ratio
color: #9ca3af; // Light gray
background: #ffffff; // White
```

### 5. Support Keyboard Navigation

```tsx
// ✅ Good
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Click me
</button>

// ❌ Bad
<div onClick={handleClick}>
  Click me
</div>
```

## Troubleshooting

### Focus Indicators Not Showing

**Solution:** Ensure `FocusIndicator` is included in root layout and global accessibility styles are imported.

### Screen Reader Not Announcing

**Solution:**
1. Verify `LiveRegionContainer` is in root layout
2. Check ARIA live regions are properly configured
3. Ensure messages are not empty

### Keyboard Shortcuts Not Working

**Solution:**
1. Check `useKeyboardShortcuts` hook is registered
2. Verify no conflicts with browser shortcuts
3. Ensure keyboard navigation is enabled in settings

### Skip Links Not Visible

**Solution:**
1. Verify `SkipLinks` component is included
2. Check global styles are loaded
3. Ensure IDs match (`#main-content`, etc.)

## Resources

- [Accessibility Guide](../../../docs/ACCESSIBILITY_GUIDE.md)
- [WCAG Compliance Report](../../../docs/WCAG_COMPLIANCE_REPORT.md)
- [Implementation Summary](../../../docs/ACCESSIBILITY_IMPLEMENTATION_SUMMARY.md)

## Support

For accessibility issues:
- Report: [GitHub Issues](#)
- Email: accessibility@example.com
- Documentation: [Accessibility Guide](../../../docs/ACCESSIBILITY_GUIDE.md)

---

*Last Updated: October 2, 2025*
*WCAG Version: 2.1 Level AA*
