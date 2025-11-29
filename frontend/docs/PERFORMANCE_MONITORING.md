# Web Vitals Performance Monitoring

This project includes comprehensive Web Vitals performance monitoring using Google's `web-vitals` library.

## Features

- **Real-time Metrics Collection**: Tracks 5 Core Web Vitals metrics
- **Development Debug Panel**: Visual panel showing metrics in real-time (dev mode only)
- **Production Analytics**: Sends metrics to analytics endpoint in production
- **Performance Ratings**: Color-coded ratings (good/needs-improvement/poor)

## Metrics Tracked

### Core Web Vitals (CWV)

1. **CLS (Cumulative Layout Shift)** - Visual stability
   - Good: ≤ 0.1
   - Needs Improvement: ≤ 0.25
   - Poor: > 0.25

2. **FCP (First Contentful Paint)** - Time to first visual content
   - Good: ≤ 1.8s
   - Needs Improvement: ≤ 3.0s
   - Poor: > 3.0s

3. **LCP (Largest Contentful Paint)** - Time to main content
   - Good: ≤ 2.5s
   - Needs Improvement: ≤ 4.0s
   - Poor: > 4.0s

4. **TTFB (Time to First Byte)** - Server response time
   - Good: ≤ 800ms
   - Needs Improvement: ≤ 1.8s
   - Poor: > 1.8s

5. **INP (Interaction to Next Paint)** - Responsiveness (replaces FID)
   - Good: ≤ 200ms
   - Needs Improvement: ≤ 500ms
   - Poor: > 500ms

## Development Mode

### Debug Panel

In development mode, a floating performance panel appears in the bottom-right corner:

- Shows all metrics in real-time
- Color-coded ratings (green/yellow/red)
- Can be minimized or closed
- Can be reopened by clicking the "Web Vitals" button

### Console Logging

All metrics are also logged to the browser console in development:

```
[Web Vitals] LCP: {
  value: 1234.5,
  rating: "good",
  delta: 1234.5,
  id: "v3-1234567890-1234567890",
  navigationType: "navigate"
}
```

## Production Mode

### Analytics Integration

In production, metrics are automatically sent to `/api/analytics/vitals` using:

- **Primary**: `navigator.sendBeacon()` for reliability (works even during page unload)
- **Fallback**: `fetch()` with `keepalive: true`

### Backend Endpoint

Create an API endpoint to receive metrics:

```typescript
// app/api/analytics/vitals/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const metric = await request.json();

    // Store in database, send to analytics service, etc.
    console.log('Web Vital:', metric);

    // Example: Send to Google Analytics 4
    // await fetch('https://www.google-analytics.com/mp/collect', {
    //   method: 'POST',
    //   body: JSON.stringify({
    //     client_id: 'YOUR_CLIENT_ID',
    //     events: [{
    //       name: 'web_vitals',
    //       params: metric
    //     }]
    //   })
    // });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Failed to process web vital:', error);
    return NextResponse.json({ error: 'Failed to process metric' }, { status: 500 });
  }
}
```

## Implementation Details

### Files

- `lib/performance.ts` - Core performance monitoring utilities
- `app/web-vitals.tsx` - Web Vitals reporter component
- `components/debug/PerformancePanel.tsx` - Debug panel component (dev only)
- `app/layout.tsx` - Integration point

### How It Works

1. **Layout Integration**: The root layout includes both the reporter and debug panel
2. **Metric Collection**: Uses Next.js `useReportWebVitals` hook + web-vitals library
3. **Reporting**: Metrics are sent to both console (dev) and analytics (prod)
4. **Visualization**: Debug panel shows real-time metrics in development

## Usage

### Basic Setup (Already Done)

The performance monitoring is already integrated in `app/layout.tsx`:

```tsx
import { WebVitalsReporter } from "./web-vitals";
import { PerformancePanel } from "../components/debug/PerformancePanel";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
        <WebVitalsReporter />
        <PerformancePanel />
      </body>
    </html>
  );
}
```

### Custom Analytics

To customize where metrics are sent, edit `lib/performance.ts`:

```typescript
const sendToAnalytics = async (metric: Metric) => {
  // Only send in production
  if (process.env.NODE_ENV !== 'production') return;

  try {
    // Your custom analytics logic here
    await yourAnalyticsService.track('web_vital', metric);
  } catch (error) {
    console.error('Failed to send web vitals:', error);
  }
};
```

### Disable Debug Panel

To disable the debug panel, remove it from `app/layout.tsx`:

```tsx
// Remove this line:
<PerformancePanel />
```

## Performance Impact

- **Bundle Size**: ~3KB gzipped (web-vitals library)
- **Runtime Overhead**: Minimal (passive observation)
- **Production**: Debug panel is automatically disabled

## Best Practices

1. **Monitor Trends**: Track metrics over time, not just individual values
2. **Set Alerts**: Alert on metrics exceeding "poor" thresholds
3. **A/B Testing**: Use metrics to validate performance improvements
4. **Real User Monitoring**: These are real user metrics, not lab metrics
5. **Segment Data**: Analyze metrics by device type, geography, etc.

## Troubleshooting

### Metrics Not Showing

- Check browser console for errors
- Ensure you're in development mode for the debug panel
- Some metrics (LCP, INP) require user interaction

### High LCP Values

- Optimize images (use Next.js Image component)
- Reduce render-blocking resources
- Use CDN for static assets
- Enable caching

### High CLS Values

- Set explicit dimensions for images/videos
- Avoid inserting content above existing content
- Use CSS transforms for animations

### High INP Values

- Reduce JavaScript execution time
- Use `requestIdleCallback` for non-critical work
- Debounce/throttle event handlers
- Code-split large components

## Resources

- [Web Vitals Documentation](https://web.dev/vitals/)
- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

## Migration Notes

- **FID Deprecated**: First Input Delay (FID) has been replaced by Interaction to Next Paint (INP) as of March 2024
- **INP is Now a Core Web Vital**: Focus on optimizing INP instead of FID
- This implementation uses the latest web-vitals v4 with INP support
