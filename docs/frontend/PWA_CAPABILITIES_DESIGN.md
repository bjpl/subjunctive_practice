# Progressive Web App (PWA) Capabilities Design
## Spanish Subjunctive Practice Application

**Date:** August 26, 2025  
**Author:** System Architecture Designer  
**Version:** 1.0

---

## Executive Summary

This document outlines the Progressive Web App (PWA) implementation strategy for the Spanish subjunctive practice application. The PWA capabilities ensure users can access learning content offline, receive practice reminders, and enjoy an app-like experience across all platforms.

### Core PWA Features
- **Offline-First Architecture**: Full functionality without internet connection
- **App-Like Experience**: Native app behavior on mobile and desktop
- **Push Notifications**: Practice reminders and progress updates
- **Background Sync**: Automatic data synchronization when online
- **Install Prompts**: Easy installation across all platforms

---

## PWA Architecture Overview

### Service Worker Strategy
The service worker acts as a network proxy, implementing sophisticated caching strategies to ensure reliable offline functionality.

```typescript
// sw.ts - Service Worker Implementation
const CACHE_VERSION = 'v1.2.0';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;
const EXERCISES_CACHE = `exercises-${CACHE_VERSION}`;
const API_CACHE = `api-${CACHE_VERSION}`;

// Cache strategies by resource type
const CACHE_STRATEGIES = {
  static: 'cache-first',      // App shell, CSS, JS
  exercises: 'network-first', // Exercise content
  api: 'network-first',       // API responses
  images: 'cache-first',      // Images and assets
  fallback: 'cache-only'      // Offline fallbacks
};

self.addEventListener('install', (event) => {
  event.waitUntil(
    Promise.all([
      cacheStaticAssets(),
      cacheEssentialExercises(),
      setupOfflineFallbacks()
    ])
  );
});
```

### App Shell Architecture
```typescript
// App shell contains the minimal HTML, CSS, and JS required to power the UI
const APP_SHELL_RESOURCES = [
  '/',
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/js/vendor.js',
  '/manifest.json',
  '/offline.html',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

const cacheStaticAssets = async () => {
  const cache = await caches.open(STATIC_CACHE);
  return cache.addAll(APP_SHELL_RESOURCES);
};
```

---

## Offline Capabilities

### Exercise Content Caching
```typescript
interface CachedExercise {
  id: string;
  type: ExerciseType;
  difficulty: DifficultyLevel;
  content: ExerciseContent;
  cachedAt: string;
  priority: number; // 1-5, higher means more likely to be cached
}

class ExerciseCacheManager {
  private readonly maxCachedExercises = 500;
  private readonly cacheStrategies = {
    beginner: { count: 100, priority: 5 },
    intermediate: { count: 150, priority: 4 },
    advanced: { count: 100, priority: 3 },
    review: { count: 150, priority: 5 } // User's review items
  };

  async cacheEssentialExercises(): Promise<void> {
    const cache = await caches.open(EXERCISES_CACHE);
    
    // Cache exercises based on user level and progress
    const userLevel = await this.getUserLevel();
    const essentialExercises = await this.getEssentialExercises(userLevel);
    
    for (const exercise of essentialExercises) {
      await cache.put(
        `/api/exercises/${exercise.id}`,
        new Response(JSON.stringify(exercise), {
          headers: { 'Content-Type': 'application/json' }
        })
      );
    }
  }

  async getEssentialExercises(userLevel: string): Promise<CachedExercise[]> {
    // Prioritize exercises based on:
    // 1. User's current difficulty level
    // 2. Previously incorrect answers (review queue)
    // 3. Most common conjugation patterns
    // 4. Spaced repetition schedule
    
    const exercises = await fetch('/api/exercises/essential', {
      method: 'POST',
      body: JSON.stringify({
        userLevel,
        includeReviewItems: true,
        maxCount: this.maxCachedExercises
      })
    });
    
    return exercises.json();
  }
}
```

### Offline Data Synchronization
```typescript
interface OfflineAction {
  id: string;
  type: 'answer_submitted' | 'progress_updated' | 'settings_changed';
  data: any;
  timestamp: string;
  synced: boolean;
  retryCount: number;
}

class OfflineSyncManager {
  private readonly dbName = 'spanish-practice-offline';
  private readonly version = 1;
  
  async queueAction(action: Omit<OfflineAction, 'id' | 'synced' | 'retryCount'>): Promise<void> {
    const db = await this.getDatabase();
    const transaction = db.transaction(['actions'], 'readwrite');
    const store = transaction.objectStore('actions');
    
    await store.add({
      ...action,
      id: crypto.randomUUID(),
      synced: false,
      retryCount: 0
    });
  }

  async syncPendingActions(): Promise<void> {
    if (!navigator.onLine) return;
    
    const db = await this.getDatabase();
    const transaction = db.transaction(['actions'], 'readwrite');
    const store = transaction.objectStore('actions');
    const index = store.index('synced');
    
    const pendingActions = await index.getAll(false);
    
    for (const action of pendingActions) {
      try {
        await this.syncAction(action);
        
        // Mark as synced
        action.synced = true;
        await store.put(action);
        
      } catch (error) {
        console.error('Sync failed for action:', action.id, error);
        
        // Increment retry count
        action.retryCount++;
        if (action.retryCount >= 3) {
          // Move to failed actions or discard
          console.warn('Action failed to sync after 3 attempts:', action);
        }
        await store.put(action);
      }
    }
  }

  private async syncAction(action: OfflineAction): Promise<void> {
    switch (action.type) {
      case 'answer_submitted':
        await fetch('/api/exercises/answer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(action.data)
        });
        break;
        
      case 'progress_updated':
        await fetch('/api/progress', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(action.data)
        });
        break;
        
      case 'settings_changed':
        await fetch('/api/settings', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(action.data)
        });
        break;
    }
  }
}
```

---

## Installation and App-Like Experience

### Web App Manifest
```json
{
  "name": "Spanish Subjunctive Practice",
  "short_name": "Subjuntivo",
  "description": "Master Spanish subjunctive conjugations with interactive exercises",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "orientation": "portrait-primary",
  
  "icons": [
    {
      "src": "/icons/icon-72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  
  "categories": ["education", "languages"],
  "lang": "es",
  "dir": "ltr",
  
  "shortcuts": [
    {
      "name": "Start Practice",
      "short_name": "Practice",
      "description": "Begin a new practice session",
      "url": "/practice",
      "icons": [{ "src": "/icons/practice-96.png", "sizes": "96x96" }]
    },
    {
      "name": "Review Mistakes",
      "short_name": "Review",
      "description": "Review previously incorrect answers",
      "url": "/review",
      "icons": [{ "src": "/icons/review-96.png", "sizes": "96x96" }]
    },
    {
      "name": "Progress",
      "short_name": "Stats",
      "description": "View your learning progress",
      "url": "/progress",
      "icons": [{ "src": "/icons/stats-96.png", "sizes": "96x96" }]
    }
  ],
  
  "screenshots": [
    {
      "src": "/screenshots/mobile-1.png",
      "sizes": "390x844",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/screenshots/desktop-1.png",
      "sizes": "1280x800",
      "type": "image/png",
      "form_factor": "wide"
    }
  ]
}
```

### Install Prompt Management
```typescript
class InstallPromptManager {
  private deferredPrompt: BeforeInstallPromptEvent | null = null;
  private installPromptShown = false;
  
  constructor() {
    this.setupInstallPrompt();
  }
  
  private setupInstallPrompt(): void {
    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent default install prompt
      e.preventDefault();
      
      // Store the event for later use
      this.deferredPrompt = e as BeforeInstallPromptEvent;
      
      // Show custom install prompt after user engagement
      this.showInstallPromptWhenAppropriate();
    });
    
    window.addEventListener('appinstalled', () => {
      console.log('PWA was installed');
      this.trackInstallation();
      this.deferredPrompt = null;
    });
  }
  
  private showInstallPromptWhenAppropriate(): void {
    // Show install prompt after:
    // 1. User has completed at least 3 exercises
    // 2. User has been using the app for more than 2 minutes
    // 3. User hasn't dismissed the prompt recently
    
    const shouldShowPrompt = this.shouldShowInstallPrompt();
    
    if (shouldShowPrompt && this.deferredPrompt) {
      this.showCustomInstallPrompt();
    }
  }
  
  private shouldShowInstallPrompt(): boolean {
    const userMetrics = this.getUserMetrics();
    const lastDismissed = localStorage.getItem('install-prompt-dismissed');
    
    // Don't show if dismissed in last 7 days
    if (lastDismissed) {
      const dismissedDate = new Date(lastDismissed);
      const daysSinceDismissed = (Date.now() - dismissedDate.getTime()) / (1000 * 60 * 60 * 24);
      if (daysSinceDismissed < 7) return false;
    }
    
    return (
      userMetrics.exercisesCompleted >= 3 &&
      userMetrics.sessionDuration >= 120000 && // 2 minutes
      !this.installPromptShown
    );
  }
  
  async showCustomInstallPrompt(): Promise<void> {
    if (!this.deferredPrompt) return;
    
    this.installPromptShown = true;
    
    // Show custom install UI
    const installBanner = document.createElement('div');
    installBanner.innerHTML = `
      <div class="install-prompt">
        <div class="install-content">
          <h3>Install Spanish Practice</h3>
          <p>Get the full app experience with offline access!</p>
          <div class="install-buttons">
            <button id="install-yes">Install</button>
            <button id="install-no">Maybe Later</button>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(installBanner);
    
    // Handle install button click
    installBanner.querySelector('#install-yes')?.addEventListener('click', async () => {
      const choiceResult = await this.deferredPrompt!.prompt();
      console.log('User choice:', choiceResult.outcome);
      
      this.deferredPrompt = null;
      document.body.removeChild(installBanner);
    });
    
    // Handle dismiss button
    installBanner.querySelector('#install-no')?.addEventListener('click', () => {
      localStorage.setItem('install-prompt-dismissed', new Date().toISOString());
      document.body.removeChild(installBanner);
    });
  }
}
```

---

## Push Notifications

### Notification Strategy
```typescript
interface NotificationConfig {
  type: 'practice_reminder' | 'streak_milestone' | 'review_reminder';
  title: string;
  body: string;
  icon: string;
  badge: string;
  tag: string;
  data: any;
  actions?: NotificationAction[];
}

class PushNotificationManager {
  private readonly vapidPublicKey = process.env.VITE_VAPID_PUBLIC_KEY!;
  
  async requestPermission(): Promise<boolean> {
    if (!('Notification' in window) || !('serviceWorker' in navigator)) {
      return false;
    }
    
    const permission = await Notification.requestPermission();
    return permission === 'granted';
  }
  
  async subscribeToPush(): Promise<PushSubscription | null> {
    const registration = await navigator.serviceWorker.ready;
    
    try {
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(this.vapidPublicKey)
      });
      
      // Send subscription to server
      await this.sendSubscriptionToServer(subscription);
      
      return subscription;
    } catch (error) {
      console.error('Failed to subscribe to push notifications:', error);
      return null;
    }
  }
  
  private async sendSubscriptionToServer(subscription: PushSubscription): Promise<void> {
    await fetch('/api/notifications/subscribe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        subscription,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString()
      })
    });
  }
  
  setupNotificationTypes(): void {
    const notificationConfigs: NotificationConfig[] = [
      {
        type: 'practice_reminder',
        title: '¡Hora de practicar!',
        body: '5 minutos de práctica mantendrán tu racha activa',
        icon: '/icons/notification-practice.png',
        badge: '/icons/badge.png',
        tag: 'practice-reminder',
        data: { url: '/practice' },
        actions: [
          {
            action: 'practice-now',
            title: 'Practicar Ahora',
            icon: '/icons/action-practice.png'
          },
          {
            action: 'remind-later',
            title: 'Más Tarde',
            icon: '/icons/action-later.png'
          }
        ]
      },
      {
        type: 'streak_milestone',
        title: '¡Felicidades! 🎉',
        body: 'Has mantenido tu racha por {days} días consecutivos',
        icon: '/icons/notification-streak.png',
        badge: '/icons/badge.png',
        tag: 'streak-milestone',
        data: { url: '/progress' }
      },
      {
        type: 'review_reminder',
        title: 'Tiempo de Repasar',
        body: 'Tienes {count} ejercicios listos para repasar',
        icon: '/icons/notification-review.png',
        badge: '/icons/badge.png',
        tag: 'review-reminder',
        data: { url: '/review' },
        actions: [
          {
            action: 'review-now',
            title: 'Repasar',
            icon: '/icons/action-review.png'
          }
        ]
      }
    ];
    
    // Register notification configs on service worker
    this.registerNotificationConfigs(notificationConfigs);
  }
}
```

### Service Worker Notification Handling
```typescript
// In service worker
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    const notificationConfig = getNotificationConfig(data.type);
    
    const notificationOptions = {
      body: data.body || notificationConfig.body,
      icon: notificationConfig.icon,
      badge: notificationConfig.badge,
      tag: notificationConfig.tag,
      data: { ...notificationConfig.data, ...data.data },
      actions: notificationConfig.actions,
      requireInteraction: data.type === 'streak_milestone',
      vibrate: [200, 100, 200]
    };
    
    event.waitUntil(
      self.registration.showNotification(
        data.title || notificationConfig.title,
        notificationOptions
      )
    );
  }
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  const { action, data } = event;
  
  switch (action) {
    case 'practice-now':
      event.waitUntil(clients.openWindow('/practice'));
      break;
      
    case 'review-now':
      event.waitUntil(clients.openWindow('/review'));
      break;
      
    case 'remind-later':
      // Schedule a reminder for later
      event.waitUntil(scheduleReminder(30)); // 30 minutes
      break;
      
    default:
      // Open the app to the appropriate page
      event.waitUntil(clients.openWindow(data.url || '/'));
  }
});
```

---

## Background Sync

### Sync Strategy Implementation
```typescript
// Service Worker background sync
self.addEventListener('sync', (event) => {
  switch (event.tag) {
    case 'background-sync-progress':
      event.waitUntil(syncProgress());
      break;
      
    case 'background-sync-exercises':
      event.waitUntil(syncExerciseData());
      break;
      
    case 'background-sync-settings':
      event.waitUntil(syncUserSettings());
      break;
      
    case 'background-sync-streak':
      event.waitUntil(syncStreakData());
      break;
  }
});

const syncProgress = async () => {
  try {
    const db = await openDB('spanish-practice-offline', 1);
    const tx = db.transaction('progress', 'readwrite');
    const store = tx.objectStore('progress');
    
    const unsyncedProgress = await store.index('synced').getAll(false);
    
    for (const progress of unsyncedProgress) {
      await fetch('/api/progress/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(progress.data)
      });
      
      // Mark as synced
      progress.synced = true;
      progress.syncedAt = new Date().toISOString();
      await store.put(progress);
    }
    
    await tx.complete;
    console.log(`Synced ${unsyncedProgress.length} progress records`);
    
  } catch (error) {
    console.error('Background sync failed:', error);
    // The sync will be retried automatically
  }
};

const syncExerciseData = async () => {
  // Fetch latest exercises and update cache
  try {
    const response = await fetch('/api/exercises/updates');
    const updates = await response.json();
    
    const cache = await caches.open(EXERCISES_CACHE);
    
    for (const exercise of updates.exercises) {
      await cache.put(
        `/api/exercises/${exercise.id}`,
        new Response(JSON.stringify(exercise))
      );
    }
    
    console.log(`Updated ${updates.exercises.length} exercises in cache`);
    
  } catch (error) {
    console.error('Failed to sync exercise data:', error);
  }
};
```

### Periodic Background Sync
```typescript
// Register periodic background sync (where supported)
class PeriodicSyncManager {
  async requestPeriodicSync(): Promise<boolean> {
    const registration = await navigator.serviceWorker.ready;
    
    if ('periodicSync' in registration) {
      try {
        await registration.periodicSync.register('daily-sync', {
          minInterval: 24 * 60 * 60 * 1000 // 24 hours
        });
        return true;
      } catch (error) {
        console.error('Periodic sync registration failed:', error);
        return false;
      }
    }
    
    return false;
  }
}

// In service worker
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'daily-sync') {
    event.waitUntil(performDailySync());
  }
});

const performDailySync = async () => {
  await Promise.all([
    syncProgress(),
    syncExerciseData(),
    updateStreakStatus(),
    cleanupOldCacheEntries()
  ]);
};
```

---

## Offline Fallbacks and Error Handling

### Offline Page
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sin Conexión - Spanish Practice</title>
  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-align: center;
      padding: 20px;
    }
    .offline-content {
      max-width: 400px;
    }
    .offline-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
    }
    .retry-button {
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid rgba(255, 255, 255, 0.3);
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="offline-content">
    <div class="offline-icon">📚</div>
    <h1>¡Ups! Sin Conexión</h1>
    <p>No hay problema, puedes seguir practicando con los ejercicios guardados en tu dispositivo.</p>
    
    <div class="offline-actions">
      <button class="retry-button" onclick="window.location.reload()">
        Intentar de Nuevo
      </button>
      <br><br>
      <a href="/practice" style="color: rgba(255,255,255,0.8)">
        Continuar sin conexión →
      </a>
    </div>
  </div>
  
  <script>
    // Automatically retry when connection is restored
    window.addEventListener('online', () => {
      window.location.reload();
    });
  </script>
</body>
</html>
```

### Network Status Handling
```typescript
class NetworkStatusManager {
  private isOnline: boolean = navigator.onLine;
  private listeners: Array<(online: boolean) => void> = [];
  
  constructor() {
    this.setupEventListeners();
    this.updateUI();
  }
  
  private setupEventListeners(): void {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.notifyListeners();
      this.handleOnlineStatus();
    });
    
    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.notifyListeners();
      this.handleOfflineStatus();
    });
  }
  
  private handleOnlineStatus(): void {
    // Show connection restored message
    this.showStatusMessage('Conexión restaurada', 'success');
    
    // Trigger background sync
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.ready.then(registration => {
        registration.sync.register('background-sync-progress');
      });
    }
    
    // Update cached content
    this.updateCachedContent();
  }
  
  private handleOfflineStatus(): void {
    // Show offline message
    this.showStatusMessage('Trabajando sin conexión', 'info');
    
    // Switch to offline mode
    this.enableOfflineMode();
  }
  
  private showStatusMessage(message: string, type: 'success' | 'info' | 'error'): void {
    const statusBar = document.createElement('div');
    statusBar.className = `status-bar status-${type}`;
    statusBar.textContent = message;
    
    document.body.appendChild(statusBar);
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
      if (document.body.contains(statusBar)) {
        document.body.removeChild(statusBar);
      }
    }, 3000);
  }
  
  onStatusChange(callback: (online: boolean) => void): void {
    this.listeners.push(callback);
  }
  
  private notifyListeners(): void {
    this.listeners.forEach(callback => callback(this.isOnline));
  }
  
  get online(): boolean {
    return this.isOnline;
  }
}
```

---

## Performance Optimization

### Cache Management
```typescript
class CacheManager {
  private readonly cacheLifetime = {
    static: 7 * 24 * 60 * 60 * 1000, // 7 days
    exercises: 24 * 60 * 60 * 1000,   // 1 day
    api: 5 * 60 * 1000,               // 5 minutes
    images: 30 * 24 * 60 * 60 * 1000  // 30 days
  };
  
  async cleanupOldCaches(): Promise<void> {
    const cacheNames = await caches.keys();
    
    for (const cacheName of cacheNames) {
      if (this.isOldCache(cacheName)) {
        await caches.delete(cacheName);
        console.log(`Deleted old cache: ${cacheName}`);
      }
    }
  }
  
  async limitCacheSize(cacheName: string, maxSize: number): Promise<void> {
    const cache = await caches.open(cacheName);
    const requests = await cache.keys();
    
    if (requests.length > maxSize) {
      // Sort by date and remove oldest entries
      const entries = await Promise.all(
        requests.map(async request => {
          const response = await cache.match(request);
          return {
            request,
            date: response?.headers.get('date') || '1970-01-01'
          };
        })
      );
      
      entries.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
      
      const toDelete = entries.slice(0, entries.length - maxSize);
      for (const entry of toDelete) {
        await cache.delete(entry.request);
      }
    }
  }
  
  private isOldCache(cacheName: string): boolean {
    const pattern = /-(v\d+\.\d+\.\d+)$/;
    const match = cacheName.match(pattern);
    
    if (match) {
      const cacheVersion = match[1];
      return cacheVersion !== CACHE_VERSION;
    }
    
    return false;
  }
}
```

### Preloading Strategy
```typescript
class PreloadManager {
  private readonly preloadStrategies = {
    immediate: ['app-shell', 'critical-css'],
    onIdle: ['common-exercises', 'user-progress'],
    onInteraction: ['advanced-exercises', 'statistics']
  };
  
  async preloadCriticalResources(): Promise<void> {
    // Preload immediately needed resources
    await this.preloadResources(this.preloadStrategies.immediate);
    
    // Preload when browser is idle
    if ('requestIdleCallback' in window) {
      requestIdleCallback(() => {
        this.preloadResources(this.preloadStrategies.onIdle);
      });
    } else {
      setTimeout(() => {
        this.preloadResources(this.preloadStrategies.onIdle);
      }, 2000);
    }
  }
  
  private async preloadResources(resources: string[]): Promise<void> {
    const cache = await caches.open(DYNAMIC_CACHE);
    
    const requests = resources.map(resource => {
      const url = this.getResourceUrl(resource);
      return fetch(url).then(response => {
        if (response.ok) {
          cache.put(url, response.clone());
        }
        return response;
      });
    });
    
    await Promise.allSettled(requests);
  }
}
```

---

## Security Considerations

### Content Security Policy for PWA
```typescript
// CSP headers for PWA
const CSP_POLICY = {
  "default-src": "'self'",
  "script-src": "'self' 'unsafe-inline'",
  "style-src": "'self' 'unsafe-inline' fonts.googleapis.com",
  "font-src": "'self' fonts.gstatic.com",
  "img-src": "'self' data: blob:",
  "connect-src": "'self' wss: ws:",
  "worker-src": "'self'",
  "manifest-src": "'self'",
  "media-src": "'self'"
};
```

### Service Worker Security
```typescript
// Validate origins for security
const ALLOWED_ORIGINS = [
  'https://spanish-practice.app',
  'https://www.spanish-practice.app'
];

self.addEventListener('message', (event) => {
  if (!ALLOWED_ORIGINS.includes(event.origin)) {
    console.warn('Message from unauthorized origin:', event.origin);
    return;
  }
  
  // Handle secure messages
  handleSecureMessage(event.data);
});

// Validate cache requests
const isValidCacheRequest = (request: Request): boolean => {
  const url = new URL(request.url);
  return ALLOWED_ORIGINS.some(origin => url.origin === origin);
};
```

---

## Testing Strategy

### PWA Testing Checklist
- [ ] **Service Worker**: Registration, updates, error handling
- [ ] **Caching**: Static assets, API responses, fallbacks
- [ ] **Offline**: Full functionality without network
- [ ] **Sync**: Background sync when connection restored
- [ ] **Install**: Add to homescreen on all platforms
- [ ] **Notifications**: Permission, display, actions
- [ ] **Performance**: Lighthouse PWA score > 90
- [ ] **Security**: HTTPS, CSP, secure contexts

### Automated PWA Testing
```typescript
// PWA testing with Playwright
describe('PWA Functionality', () => {
  test('should register service worker', async ({ page }) => {
    await page.goto('/');
    
    const swRegistration = await page.evaluate(() => {
      return 'serviceWorker' in navigator;
    });
    
    expect(swRegistration).toBe(true);
  });
  
  test('should work offline', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Go offline
    await page.context().setOffline(true);
    
    // Navigate to exercise page
    await page.click('[data-testid="start-practice"]');
    
    // Should still load from cache
    await expect(page.locator('[data-testid="exercise-content"]')).toBeVisible();
  });
  
  test('should show install prompt', async ({ page }) => {
    await page.goto('/');
    
    // Simulate beforeinstallprompt event
    await page.evaluate(() => {
      const event = new Event('beforeinstallprompt');
      window.dispatchEvent(event);
    });
    
    // Complete exercises to trigger install prompt
    await completeExercises(page, 3);
    
    await expect(page.locator('.install-prompt')).toBeVisible();
  });
});
```

---

## Implementation Timeline

### Phase 1: Core PWA Infrastructure (Week 1-2)
- Service worker implementation
- Web app manifest
- Basic caching strategies
- Offline fallback pages

### Phase 2: Offline Functionality (Week 3-4)
- Exercise content caching
- Offline data storage
- Background sync implementation
- Network status handling

### Phase 3: App-Like Features (Week 5-6)
- Install prompts
- Push notifications
- Shortcut actions
- Platform-specific optimizations

### Phase 4: Performance & Testing (Week 7-8)
- Cache optimization
- Performance tuning
- Comprehensive PWA testing
- Security audit

This PWA implementation ensures users can access the Spanish subjunctive practice application anywhere, anytime, with or without an internet connection, while providing a native app-like experience across all platforms.