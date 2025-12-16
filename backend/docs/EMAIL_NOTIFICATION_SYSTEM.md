# Email Notification System

## Overview

The email notification system provides automated, template-based email notifications to users for various events including streak reminders, achievement unlocks, weekly progress summaries, and account management.

## Features

- **Multiple Provider Support**: SendGrid and SMTP
- **Template-based Emails**: Jinja2 templates with HTML and plain text versions
- **Async Sending**: Non-blocking email delivery
- **Retry Logic**: Automatic retry on failure (up to 3 attempts)
- **Scheduled Notifications**: APScheduler for automated daily/weekly emails
- **Bulk Sending**: Rate-limited batch email support
- **User Preferences**: Respect user notification settings

## Architecture

### Components

1. **EmailService** (`backend/services/email_service.py`)
   - Core email sending logic
   - Provider abstraction (SendGrid/SMTP)
   - Template rendering
   - Retry mechanism

2. **NotificationScheduler** (`backend/services/notification_scheduler.py`)
   - Scheduled job management
   - Daily streak reminders
   - Weekly progress summaries
   - Achievement notifications

3. **Email Templates** (`backend/templates/emails/`)
   - HTML and text versions for all email types
   - Jinja2 template syntax
   - Responsive design

4. **Configuration** (`backend/core/config.py`)
   - Environment-based settings
   - Provider credentials
   - SMTP/SendGrid configuration

## Configuration

### Environment Variables

#### Email Provider Selection
```bash
# Choose provider: "smtp" or "sendgrid"
EMAIL_PROVIDER=smtp

# Sender information
EMAIL_FROM_ADDRESS=noreply@example.com
EMAIL_FROM_NAME="Spanish Subjunctive Practice"

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000
```

#### SMTP Configuration
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Note for Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password as `SMTP_PASSWORD`

#### SendGrid Configuration
```bash
SENDGRID_API_KEY=SG.your-api-key-here
```

## Usage

### Basic Email Sending

```python
from services.email_service import get_email_service

# Get service instance
email_service = get_email_service()

# Send streak reminder
await email_service.send_streak_reminder(
    user_email="user@example.com",
    user_name="John Doe",
    current_streak=7
)

# Send achievement notification
await email_service.send_achievement_notification(
    user_email="user@example.com",
    user_name="John Doe",
    achievement={
        "name": "First Steps",
        "description": "Complete your first exercise",
        "icon_url": "https://example.com/icon.png",
        "points": 10
    }
)

# Send weekly summary
await email_service.send_weekly_progress_summary(
    user_email="user@example.com",
    user_name="John Doe",
    stats={
        "week_start": "Dec 9",
        "week_end": "Dec 15, 2025",
        "total_exercises": 50,
        "accuracy": 85.5,
        "study_time_minutes": 120,
        "current_streak": 7,
        "verbs_mastered": 15,
        "achievements_earned": 3
    }
)
```

### Scheduled Notifications

```python
from services.notification_scheduler import start_scheduler, stop_scheduler

# Start scheduler (typically in main.py)
start_scheduler()

# Stop scheduler (on shutdown)
stop_scheduler()
```

### Manual Scheduling

```python
from services.notification_scheduler import get_scheduler

scheduler = get_scheduler()

# Send achievement notification immediately
await scheduler.send_achievement_notification(
    user_id=1,
    achievement_id=5
)

# Send welcome email to new user
await scheduler.send_welcome_email(user_id=1)
```

## Scheduled Jobs

### 1. Streak Reminders
- **Frequency**: Every hour
- **Checks**: Users with reminder time matching current hour
- **Conditions**:
  - User has `reminder_enabled=True`
  - User has `email_notifications=True`
  - User hasn't practiced today
  - Current hour matches user's `reminder_time`

### 2. Weekly Summaries
- **Frequency**: Sundays at 8 PM
- **Recipients**: All active users with email notifications enabled
- **Content**:
  - Total exercises completed
  - Accuracy percentage
  - Study time
  - Current streak
  - Verbs mastered
  - Achievements earned

### 3. Daily Cleanup
- **Frequency**: Daily at 3 AM
- **Purpose**: Clean up old notification records (future)

## Email Templates

### Available Templates

1. **streak_reminder** - Don't break your streak!
2. **achievement_unlocked** - Achievement earned
3. **weekly_summary** - Weekly progress report
4. **welcome** - New user welcome email
5. **password_reset** - Password reset instructions

### Template Structure

Each template has two versions:
- `{name}.html` - HTML version with styling
- `{name}.txt` - Plain text version

### Template Variables

#### Streak Reminder
```python
{
    "user_name": str,
    "current_streak": int,
    "app_name": str,
    "year": int
}
```

#### Achievement Unlocked
```python
{
    "user_name": str,
    "achievement_name": str,
    "achievement_description": str,
    "achievement_icon": str,
    "achievement_points": int,
    "app_name": str,
    "year": int
}
```

#### Weekly Summary
```python
{
    "user_name": str,
    "week_start": str,
    "week_end": str,
    "total_exercises": int,
    "accuracy": float,
    "study_time_minutes": int,
    "current_streak": int,
    "verbs_mastered": int,
    "achievements_earned": int,
    "app_name": str,
    "year": int
}
```

#### Welcome
```python
{
    "user_name": str,
    "app_name": str,
    "year": int
}
```

#### Password Reset
```python
{
    "user_name": str,
    "reset_url": str,
    "reset_token": str,
    "app_name": str,
    "year": int
}
```

## API Endpoints

### Update Notification Preferences

```http
PUT /api/settings/notifications
PUT /api/settings/users/me/notifications  # Alias

{
  "email": true,
  "push": false,
  "streakReminders": true
}
```

**Response:**
```json
{
  "user_id": "user123",
  "settings": {
    "notifications": {
      "email": true,
      "push": false,
      "streakReminders": true
    },
    "practice": { ... },
    "accessibility": { ... },
    "language": { ... }
  },
  "last_updated": "2025-12-16T10:00:00Z",
  "version": 2
}
```

## Error Handling

### Retry Logic

The email service implements exponential backoff:
1. Initial attempt
2. Retry after 2 seconds
3. Retry after 4 seconds
4. Retry after 6 seconds
5. Give up after 3 retries

### Error Logging

All email errors are logged with context:
```python
logger.error(f"Error sending email: {str(e)}", exc_info=True)
```

## Testing

### Run Email Service Tests
```bash
pytest backend/tests/services/test_email_service.py -v
```

### Run Scheduler Tests
```bash
pytest backend/tests/services/test_notification_scheduler.py -v
```

### Test Coverage Areas

1. **Email Service**
   - SMTP and SendGrid providers
   - Retry logic
   - Template rendering
   - Bulk sending
   - High-level notification methods

2. **Scheduler**
   - Job scheduling
   - Streak reminder logic
   - Weekly summary generation
   - Achievement notifications
   - User preference handling

## Security Considerations

### Credentials
- Never commit API keys or passwords to version control
- Use environment variables for all credentials
- Rotate API keys regularly

### Email Content
- Sanitize user-generated content in templates
- Validate email addresses before sending
- Rate limit bulk operations

### Privacy
- Respect user notification preferences
- Include unsubscribe links in all emails
- Don't include sensitive information in email subject lines

## Performance

### Rate Limiting

Bulk emails are sent in batches:
- Batch size: 10 emails
- Delay between batches: 1 second
- Prevents overwhelming email servers

### Async Operations

All email sending is asynchronous:
- Non-blocking operations
- Concurrent sending for bulk emails
- Doesn't delay API responses

## Troubleshooting

### SMTP Connection Issues

1. **Authentication Failed**
   - Verify SMTP credentials
   - Check if 2FA is enabled (use App Password)
   - Confirm SMTP server allows less secure apps

2. **Connection Timeout**
   - Check firewall settings
   - Verify SMTP_HOST and SMTP_PORT
   - Test network connectivity

### SendGrid Issues

1. **API Key Invalid**
   - Verify API key is active
   - Check API key permissions
   - Regenerate if necessary

2. **Rate Limit Exceeded**
   - Review SendGrid plan limits
   - Implement additional rate limiting
   - Consider upgrading plan

### Template Rendering Errors

1. **Template Not Found**
   - Verify template file exists
   - Check file permissions
   - Ensure correct template directory path

2. **Missing Template Variables**
   - Review template context
   - Add default values for optional variables
   - Check template syntax

## Future Enhancements

1. **Email Tracking**
   - Open rate tracking
   - Click-through tracking
   - Bounce handling

2. **Advanced Scheduling**
   - User timezone support
   - Custom reminder frequencies
   - Smart send time optimization

3. **Template Management**
   - Admin UI for template editing
   - A/B testing support
   - Localization/i18n

4. **Analytics**
   - Email delivery metrics
   - Engagement analytics
   - Conversion tracking

## Dependencies

```
aiosmtplib==3.0.1      # Async SMTP client
jinja2==3.1.3          # Template engine
sendgrid==6.11.0       # SendGrid API client
apscheduler==3.10.4    # Job scheduling
```

## License

Part of the Spanish Subjunctive Practice application.
