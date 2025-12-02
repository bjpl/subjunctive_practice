# Settings API Documentation

## Overview

The Settings API allows authenticated users to manage their application preferences across multiple categories:
- **Notifications**: Email, push, and streak reminder preferences
- **Practice**: Daily goals, auto-advance, hints, and explanations
- **Accessibility**: Font size, high contrast, and reduced motion
- **Language**: Interface and practice language preferences

All endpoints require authentication via JWT Bearer token.

## Base URL

```
/api/settings
```

## Endpoints

### 1. Get User Settings

**GET** `/api/settings`

Retrieve all settings for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "user_id": "1",
  "settings": {
    "notifications": {
      "email": true,
      "push": false,
      "streakReminders": true
    },
    "practice": {
      "dailyGoal": 10,
      "autoAdvance": true,
      "showHints": true,
      "showExplanations": true
    },
    "accessibility": {
      "fontSize": "medium",
      "highContrast": false,
      "reduceMotion": false
    },
    "language": {
      "interface": "en",
      "practice": "es"
    }
  },
  "last_updated": "2025-11-27T12:00:00",
  "version": 1
}
```

---

### 2. Update All Settings

**PUT** `/api/settings`

Replace all user settings with new values.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "notifications": {
    "email": false,
    "push": true,
    "streakReminders": false
  },
  "practice": {
    "dailyGoal": 20,
    "autoAdvance": false,
    "showHints": true,
    "showExplanations": false
  },
  "accessibility": {
    "fontSize": "large",
    "highContrast": true,
    "reduceMotion": true
  },
  "language": {
    "interface": "es",
    "practice": "fr"
  }
}
```

**Response:** `200 OK`
```json
{
  "user_id": "1",
  "settings": { /* updated settings */ },
  "last_updated": "2025-11-27T12:05:00",
  "version": 2
}
```

**Validation:**
- `dailyGoal`: Must be between 1 and 100
- `fontSize`: Must be "small", "medium", or "large"
- `interface`/`practice`: Must be valid language codes (min 2 characters)

---

### 3. Update Notification Settings

**PATCH** `/api/settings/notifications`

Update only notification preferences. Other settings remain unchanged.

**Request Body:**
```json
{
  "email": false,
  "push": true,
  "streakReminders": true
}
```

**Response:** `200 OK` (full settings object with updated notifications)

---

### 4. Update Practice Settings

**PATCH** `/api/settings/practice`

Update only practice preferences.

**Request Body:**
```json
{
  "dailyGoal": 25,
  "autoAdvance": true,
  "showHints": false,
  "showExplanations": true
}
```

**Response:** `200 OK` (full settings object with updated practice settings)

**Validation:**
- `dailyGoal`: Must be between 1 and 100

---

### 5. Update Accessibility Settings

**PATCH** `/api/settings/accessibility`

Update only accessibility preferences.

**Request Body:**
```json
{
  "fontSize": "large",
  "highContrast": true,
  "reduceMotion": false
}
```

**Response:** `200 OK` (full settings object with updated accessibility settings)

**Validation:**
- `fontSize`: Must be "small", "medium", or "large"

---

### 6. Update Language Settings

**PATCH** `/api/settings/language`

Update only language preferences.

**Request Body:**
```json
{
  "interface": "fr",
  "practice": "de"
}
```

**Response:** `200 OK` (full settings object with updated language settings)

**Validation:**
- Both codes must be at least 2 characters long

---

### 7. Reset Settings to Defaults

**DELETE** `/api/settings`

Reset all settings to default values.

**Response:** `204 No Content`

---

### 8. Export Settings

**GET** `/api/settings/export`

Export all settings as JSON for backup or migration.

**Response:** `200 OK`
```json
{
  "export_date": "2025-11-27T12:10:00",
  "user_id": "1",
  "settings": {
    "notifications": { /* ... */ },
    "practice": { /* ... */ },
    "accessibility": { /* ... */ },
    "language": { /* ... */ }
  },
  "metadata": {
    "last_updated": "2025-11-27T12:05:00",
    "version": 2
  }
}
```

---

### 9. Import Settings

**POST** `/api/settings/import`

Import settings from exported JSON.

**Request Body:**
```json
{
  "notifications": { /* ... */ },
  "practice": { /* ... */ },
  "accessibility": { /* ... */ },
  "language": { /* ... */ }
}
```

**Response:** `200 OK` (full settings object)

---

## Error Responses

### 401 Unauthorized / 403 Forbidden
```json
{
  "detail": "Not authenticated"
}
```

### 400 Bad Request
```json
{
  "detail": "Daily goal must be between 1 and 100"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "practice", "dailyGoal"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

---

## Usage Examples

### JavaScript/TypeScript (Frontend)

```typescript
// Get settings
const response = await fetch('/api/settings', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
const data = await response.json();

// Update practice settings only
await fetch('/api/settings/practice', {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    dailyGoal: 25,
    autoAdvance: true,
    showHints: false,
    showExplanations: true
  })
});

// Export for backup
const exportData = await fetch('/api/settings/export', {
  headers: { 'Authorization': `Bearer ${accessToken}` }
}).then(r => r.json());

localStorage.setItem('settings-backup', JSON.stringify(exportData));
```

### Python

```python
import requests

# Get settings
response = requests.get(
    'http://localhost:8000/api/settings',
    headers={'Authorization': f'Bearer {access_token}'}
)
settings = response.json()

# Update all settings
new_settings = {
    "notifications": {"email": False, "push": True, "streakReminders": True},
    "practice": {"dailyGoal": 30, "autoAdvance": True, "showHints": True, "showExplanations": True},
    "accessibility": {"fontSize": "large", "highContrast": False, "reduceMotion": True},
    "language": {"interface": "en", "practice": "es"}
}

response = requests.put(
    'http://localhost:8000/api/settings',
    headers={'Authorization': f'Bearer {access_token}'},
    json=new_settings
)
```

### cURL

```bash
# Get settings
curl -X GET http://localhost:8000/api/settings \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update notifications only
curl -X PATCH http://localhost:8000/api/settings/notifications \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": true,
    "push": false,
    "streakReminders": true
  }'

# Reset to defaults
curl -X DELETE http://localhost:8000/api/settings \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Data Model

### UserSettings

```typescript
interface NotificationSettings {
  email: boolean;
  push: boolean;
  streakReminders: boolean;
}

interface PracticeSettings {
  dailyGoal: number;        // 1-100
  autoAdvance: boolean;
  showHints: boolean;
  showExplanations: boolean;
}

interface AccessibilitySettings {
  fontSize: 'small' | 'medium' | 'large';
  highContrast: boolean;
  reduceMotion: boolean;
}

interface LanguageSettings {
  interface: string;        // ISO language code
  practice: string;         // ISO language code
}

interface UserSettings {
  notifications: NotificationSettings;
  practice: PracticeSettings;
  accessibility: AccessibilitySettings;
  language: LanguageSettings;
}
```

---

## Default Values

| Setting | Default Value |
|---------|--------------|
| `notifications.email` | `true` |
| `notifications.push` | `false` |
| `notifications.streakReminders` | `true` |
| `practice.dailyGoal` | `10` |
| `practice.autoAdvance` | `true` |
| `practice.showHints` | `true` |
| `practice.showExplanations` | `true` |
| `accessibility.fontSize` | `"medium"` |
| `accessibility.highContrast` | `false` |
| `accessibility.reduceMotion` | `false` |
| `language.interface` | `"en"` |
| `language.practice` | `"es"` |

---

## Storage

Settings are stored in `user_data/settings/settings_{user_id}.json` as JSON files.

In production, this should be migrated to:
- PostgreSQL database
- Redis for caching
- MongoDB for document storage

---

## Version Management

The `version` field increments with each update, allowing for:
- Optimistic concurrency control
- Conflict detection in multi-device scenarios
- Audit trail of changes

---

## Best Practices

1. **Use PATCH for Partial Updates**: When changing only one section, use the specific PATCH endpoint to avoid overwriting other settings.

2. **Export Before Major Changes**: Use the export endpoint to backup settings before making significant changes.

3. **Handle Validation Errors**: Always validate user input on the frontend before sending to prevent 422 errors.

4. **Cache Settings**: Cache settings in localStorage/sessionStorage to reduce API calls.

5. **Sync Across Devices**: Use the version field to detect conflicts when syncing settings across multiple devices.

---

## Related Endpoints

- Authentication: `/api/auth/login`, `/api/auth/register`
- User Profile: `/api/auth/me`
- Progress: `/api/progress`

---

## Interactive Documentation

Visit `/api/docs` when the server is running to access the interactive Swagger UI where you can test all endpoints.
