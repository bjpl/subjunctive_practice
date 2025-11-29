# Web Vitals Quick Reference Card

## 🚀 Quick Start

### View Metrics (Development)
1. Run `npm run dev`
2. Open http://localhost:3000
3. Look for floating panel in bottom-right corner
4. Check browser console for detailed logs

### Production Setup
1. Create analytics endpoint: `app/api/analytics/vitals/route.ts`
2. Build and deploy: `npm run build && npm start`
3. Metrics automatically sent to endpoint

## 📊 Metrics Cheat Sheet

| Metric | Full Name | Measures | Good | Poor |
|--------|-----------|----------|------|------|
| **CLS** | Cumulative Layout Shift | Visual stability | ≤0.1 | >0.25 |
| **FCP** | First Contentful Paint | Initial render | ≤1.8s | >3.0s |
| **LCP** | Largest Contentful Paint | Loading speed | ≤2.5s | >4.0s |
| **TTFB** | Time to First Byte | Server response | ≤0.8s | >1.8s |
| **INP** | Interaction to Next Paint | Responsiveness | ≤200ms | >500ms |

## 🎨 Rating Colors

- 🟢 **Green** = Good (optimal performance)
- 🟡 **Yellow** = Needs Improvement (attention required)
- 🔴 **Red** = Poor (immediate action needed)

## 🔧 Common Fixes

### High LCP (Slow Loading)
```typescript
// ✅ DO: Use Next.js Image component
import Image from 'next/image';
<Image src="/hero.jpg" width={800} height={600} priority />

// ❌ DON'T: Use regular img tags
<img src="/hero.jpg" />
```

### High CLS (Layout Shifts)
```tsx
// ✅ DO: Set explicit dimensions
<div className="w-[400px] h-[300px]">
  <Image src="/image.jpg" fill />
</div>

// ❌ DON'T: Let images size themselves
<img src="/image.jpg" />
```

### High INP (Slow Interactions)
```typescript
// ✅ DO: Debounce expensive operations
import { debounce } from 'lodash';
const handleSearch = debounce((query) => {
  // Expensive search
}, 300);

// ❌ DON'T: Run expensive code on every keystroke
<input onChange={(e) => expensiveSearch(e.target.value)} />
```

### High TTFB (Slow Server)
```typescript
// ✅ DO: Use static generation when possible
export const dynamic = 'force-static';

// ✅ DO: Implement caching
export const revalidate = 3600; // 1 hour

// ❌ DON'T: Always use dynamic rendering
```

## 📁 File Locations

```
frontend/
├── lib/performance.ts                      # Core logic
├── app/web-vitals.tsx                      # Reporter
├── components/debug/PerformancePanel.tsx   # Debug UI
└── docs/
    ├── PERFORMANCE_MONITORING.md           # Full guide
    ├── PERFORMANCE_ARCHITECTURE.md         # Architecture
    └── WEB_VITALS_QUICK_REFERENCE.md      # This file
```

## 🎯 Console Commands

### Check Metric in DevTools
```javascript
// Run in browser console
performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd
performance.getEntriesByType('paint')
```

### Debug Panel Controls
- **Minimize**: Click `_` button
- **Close**: Click `×` button
- **Reopen**: Click "📊 Web Vitals" button

## 📱 Browser Support

| Browser | CLS | FCP | LCP | TTFB | INP |
|---------|-----|-----|-----|------|-----|
| Chrome 77+ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edge 79+ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Firefox 84+ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| Safari 14+ | ⚠️ | ✅ | ⚠️ | ✅ | ❌ |

✅ Full support | ⚠️ Partial support | ❌ Not supported

## 🐛 Troubleshooting

### Panel Not Showing
```bash
# Check you're in development mode
echo $NODE_ENV  # Should be 'development'

# Restart dev server
npm run dev
```

### Metrics Not Logging
```javascript
// Check web-vitals installed
npm list web-vitals

// Verify import in app/layout.tsx
import { WebVitalsReporter } from "./web-vitals";
```

### Analytics Not Working
```typescript
// 1. Create endpoint first
// app/api/analytics/vitals/route.ts

// 2. Verify production mode
process.env.NODE_ENV === 'production'

// 3. Check Network tab for POST requests
```

## 📈 Performance Optimization Checklist

### Images
- [ ] Use Next.js `<Image>` component
- [ ] Add `priority` to above-fold images
- [ ] Use WebP format
- [ ] Implement lazy loading

### Fonts
- [ ] Use `next/font` for optimization
- [ ] Preload critical fonts
- [ ] Use font-display: swap

### JavaScript
- [ ] Code split with dynamic imports
- [ ] Remove unused dependencies
- [ ] Minimize bundle size
- [ ] Use server components when possible

### CSS
- [ ] Remove unused CSS
- [ ] Use critical CSS
- [ ] Minimize render-blocking styles

### Server
- [ ] Enable caching headers
- [ ] Use CDN for static assets
- [ ] Implement HTTP/2
- [ ] Enable compression (gzip/brotli)

## 🔗 Useful Links

- [Web Vitals Website](https://web.dev/vitals/)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

## 💡 Pro Tips

1. **Focus on Real User Metrics**: Lab metrics (Lighthouse) are different from field metrics (Web Vitals)
2. **Monitor Trends**: One bad metric isn't critical, but trends matter
3. **Segment by Device**: Mobile vs Desktop performance differs significantly
4. **Test on Real Devices**: Emulators don't show real performance
5. **Use Performance Budgets**: Set thresholds and track in CI/CD

## 🎓 Metric Priorities

For this application (Spanish Subjunctive Practice):

1. **LCP** (Priority: High) - Fast content loading keeps users engaged
2. **INP** (Priority: High) - Responsive exercises improve learning experience
3. **CLS** (Priority: Medium) - Stable UI prevents disruption
4. **FCP** (Priority: Medium) - Quick first paint builds confidence
5. **TTFB** (Priority: Low) - Less critical for static-heavy app

## 📝 Reporting Template

When reporting performance issues:

```markdown
**Metric**: [CLS/FCP/LCP/TTFB/INP]
**Current Value**: [value]
**Target Value**: [good threshold]
**Page**: [URL]
**Device**: [Desktop/Mobile]
**Browser**: [Chrome/Firefox/Safari]
**Network**: [4G/3G/WiFi]
**Screenshot**: [attach if relevant]
**DevTools Profile**: [attach if available]
```

## 🚦 Performance Goals (This Project)

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| LCP | <2.5s | TBD | 🟡 |
| INP | <200ms | TBD | 🟡 |
| CLS | <0.1 | TBD | 🟡 |
| FCP | <1.8s | TBD | 🟡 |
| TTFB | <800ms | TBD | 🟡 |

---

**Last Updated**: November 28, 2025
**Version**: 1.0
**Maintained By**: Development Team
