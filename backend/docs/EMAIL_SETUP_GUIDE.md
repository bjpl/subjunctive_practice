# Email Notification System - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install email dependencies
pip install -r requirements.txt

# Or install individually
pip install aiosmtplib==3.0.1 jinja2==3.1.3 sendgrid==6.11.0 apscheduler==3.10.4
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure email settings:

```bash
cp .env.example .env
```

#### Option A: SMTP Configuration (Gmail Example)

```bash
EMAIL_PROVIDER=smtp
EMAIL_FROM_ADDRESS=your-app@gmail.com
EMAIL_FROM_NAME="Spanish Subjunctive Practice"

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-app@gmail.com
SMTP_PASSWORD=your-app-password

FRONTEND_URL=http://localhost:3000
```

**Gmail Setup:**
1. Enable 2-factor authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an "App Password" for "Mail"
4. Use the generated password as `SMTP_PASSWORD`

#### Option B: SendGrid Configuration

```bash
EMAIL_PROVIDER=sendgrid
EMAIL_FROM_ADDRESS=noreply@yourdomain.com
EMAIL_FROM_NAME="Spanish Subjunctive Practice"

SENDGRID_API_KEY=SG.your-api-key-here

FRONTEND_URL=http://localhost:3000
```

**SendGrid Setup:**
1. Sign up at https://sendgrid.com
2. Verify your sender identity (email or domain)
3. Create an API key with "Mail Send" permissions
4. Copy the API key to `SENDGRID_API_KEY`

### 3. Test Email Service

```bash
# Test email service
pytest tests/services/test_email_service.py -v

# Test scheduler
pytest tests/services/test_notification_scheduler.py -v

# Run all email-related tests
pytest tests/services/ -v
```

### 4. Start Scheduler in Application

Add to `main.py`:

```python
from services.notification_scheduler import start_scheduler, stop_scheduler

@app.on_event("startup")
async def startup_event():
    """Start services on application startup."""
    start_scheduler()
    logger.info("Notification scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown."""
    stop_scheduler()
    logger.info("Notification scheduler stopped")
```

## Usage Examples

### Send Welcome Email

```python
from services.notification_scheduler import get_scheduler

scheduler = get_scheduler()

# Send welcome email to new user
await scheduler.send_welcome_email(user_id=1)
```

### Send Achievement Notification

```python
# When user earns an achievement
await scheduler.send_achievement_notification(
    user_id=user_id,
    achievement_id=achievement_id
)
```

### Manual Email Sending

```python
from services.email_service import get_email_service

email_service = get_email_service()

# Send custom email
await email_service.send_email(
    recipient=EmailRecipient(
        email="user@example.com",
        name="John Doe"
    ),
    template=EmailTemplate(
        template_name="streak_reminder",
        subject="Don't break your streak!",
        context={
            "user_name": "John",
            "current_streak": 7,
            "app_name": "Spanish Practice",
            "year": 2025
        }
    )
)
```

## Testing Email Delivery

### Test SMTP Connection

```python
import asyncio
from services.email_service import get_email_service, EmailRecipient, EmailTemplate

async def test_email():
    service = get_email_service()

    result = await service.send_welcome_email(
        user_email="your-test-email@example.com",
        user_name="Test User"
    )

    print(f"Email sent: {result}")

asyncio.run(test_email())
```

### Check Email Logs

```bash
# View application logs
tail -f backend.log | grep -i "email"

# Check for email errors
grep -i "error.*email" backend.log
```

## Scheduled Jobs

### Default Schedule

1. **Streak Reminders**: Every hour (checks user reminder times)
2. **Weekly Summaries**: Sundays at 8 PM
3. **Cleanup**: Daily at 3 AM

### Customize Schedule

Edit `services/notification_scheduler.py`:

```python
# Change weekly summary time
self.scheduler.add_job(
    self._send_weekly_summaries,
    trigger=CronTrigger(day_of_week='sun', hour=18, minute=0),  # 6 PM instead of 8 PM
    id="weekly_summaries",
    name="Send weekly progress summaries",
    replace_existing=True
)
```

## User Notification Preferences

Users can manage their notification preferences via API:

```bash
# Update notification settings
curl -X PATCH http://localhost:8000/api/settings/notifications \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": true,
    "push": false,
    "streakReminders": true
  }'
```

## Troubleshooting

### SMTP Issues

**Problem**: Authentication failed
```
Solution:
1. Verify SMTP credentials are correct
2. For Gmail, use App Password (not regular password)
3. Enable "Less secure app access" if not using 2FA
```

**Problem**: Connection timeout
```
Solution:
1. Check firewall isn't blocking port 587
2. Verify SMTP_HOST is reachable
3. Try alternative ports (465 for SSL)
```

### SendGrid Issues

**Problem**: API key invalid
```
Solution:
1. Verify API key in SendGrid dashboard
2. Check API key has "Mail Send" permission
3. Regenerate API key if necessary
```

**Problem**: Sender verification failed
```
Solution:
1. Verify sender email/domain in SendGrid
2. Wait for verification email and confirm
3. Use verified sender address in EMAIL_FROM_ADDRESS
```

### Template Issues

**Problem**: Template not found
```
Solution:
1. Verify template files exist in backend/templates/emails/
2. Check file permissions
3. Ensure both .html and .txt versions exist
```

**Problem**: Template rendering error
```
Solution:
1. Check all required variables are in context
2. Verify Jinja2 syntax in template
3. Add default values for optional variables
```

## Production Checklist

- [ ] Use environment variables for all credentials
- [ ] Never commit API keys or passwords
- [ ] Use verified sender domain (not @gmail.com)
- [ ] Enable email tracking/analytics
- [ ] Set up SPF and DKIM records
- [ ] Monitor bounce rates
- [ ] Implement unsubscribe functionality
- [ ] Add email rate limiting
- [ ] Set up error alerting
- [ ] Test all email templates
- [ ] Configure proper retry logic
- [ ] Enable email logging

## Email Template Customization

### Modify Existing Template

1. Edit template file in `backend/templates/emails/`
2. Update both HTML and text versions
3. Test template rendering
4. Deploy changes

### Add New Template

1. Create `{name}.html` and `{name}.txt` in `backend/templates/emails/`
2. Add method in `EmailService` class
3. Define template context variables
4. Add tests
5. Document usage

## Monitoring

### Track Email Metrics

```python
from services.email_service import get_email_service

# Send bulk emails and get results
results = await email_service.send_bulk_emails(recipients, template)

print(f"Total: {results['total']}")
print(f"Sent: {results['sent']}")
print(f"Failed: {results['failed']}")
```

### Log Analysis

```bash
# Count emails sent today
grep "Email sent successfully" backend.log | \
  grep "$(date +%Y-%m-%d)" | wc -l

# Find failed emails
grep "Failed to send email" backend.log

# Track by email type
grep "streak_reminder" backend.log | wc -l
```

## Support

For issues or questions:
1. Check logs: `backend.log`
2. Review configuration: `.env`
3. Test connectivity: Run test suite
4. Check provider status (SendGrid/SMTP server)

## Resources

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Gmail SMTP Setup](https://support.google.com/mail/answer/7126229)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
