# Environment Setup Guide

Complete guide for setting up environment variables and configuration for the Subjunctive Practice application.

## Quick Start

For automated setup, run the interactive setup script:

```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

For manual setup, follow the detailed instructions below.

## Environment Files

### Available Environment Templates

1. **`.env.example`** - Template with all possible configuration options
2. **`config/environments/.env.development`** - Development environment settings
3. **`config/environments/.env.staging`** - Staging environment settings  
4. **`config/environments/.env.production`** - Production environment settings

### Creating Your Environment File

Choose the appropriate template and copy it to `.env`:

```bash
# For development
cp config/environments/.env.development .env

# For staging
cp config/environments/.env.staging .env

# For production
cp config/environments/.env.production .env

# For custom setup
cp .env.example .env
```

## Required Configuration

### 1. Application Settings

```bash
APP_ENV=development                    # Environment: development, staging, production
APP_NAME=subjunctive-practice         # Application name
HOST=localhost                        # Host address
PORT=8000                             # Port number
DEBUG=true                            # Enable debug mode (false for production)
BASE_URL=http://localhost:8000        # Base URL for the application
CORS_ORIGINS=http://localhost:3000    # Comma-separated CORS origins
```

### 2. Database Configuration

#### PostgreSQL (Recommended)
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
DB_POOL_SIZE=10                       # Connection pool size
DB_MAX_OVERFLOW=20                    # Max overflow connections
DB_POOL_TIMEOUT=30                    # Pool timeout in seconds
DB_POOL_RECYCLE=3600                  # Pool recycle time in seconds
```

#### Example URLs:
- Local: `postgresql://postgres:password@localhost:5432/subjunctive_practice`
- Docker: `postgresql://postgres:password@db:5432/subjunctive_practice`
- Cloud: `postgresql://user:pass@cloud-host:5432/dbname`

### 3. Redis Configuration

```bash
REDIS_URL=redis://localhost:6379/0           # Redis cache database
REDIS_SESSION_URL=redis://localhost:6379/1   # Redis session database
CACHE_TTL=3600                               # Cache TTL in seconds
```

### 4. OpenAI API Configuration

```bash
OPENAI_API_KEY=sk-your-api-key-here    # Your OpenAI API key
OPENAI_MODEL=gpt-4                     # Model to use (gpt-4, gpt-3.5-turbo)
OPENAI_MAX_TOKENS=4000                 # Maximum tokens per request
OPENAI_TEMPERATURE=0.7                 # Temperature for responses
OPENAI_RATE_LIMIT=60                   # Requests per minute
```

**Getting an OpenAI API Key:**
1. Visit https://platform.openai.com/account/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)
4. Add billing information to your OpenAI account

### 5. Security Configuration

#### Generate Secure Secrets

Use the secrets manager to generate secure keys:

```bash
# Generate JWT secret
python3 config/secrets_manager.py generate-key JWT_SECRET_KEY

# Generate session secret
python3 config/secrets_manager.py generate-key SESSION_SECRET_KEY
```

Or use Python directly:
```python
import secrets
jwt_secret = secrets.token_urlsafe(64)
session_secret = secrets.token_urlsafe(32)
```

#### Security Settings
```bash
JWT_SECRET_KEY=your-64-character-jwt-secret-here
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24
JWT_REFRESH_TOKEN_EXPIRE_HOURS=168
SESSION_SECRET_KEY=your-32-character-session-secret-here
PASSWORD_SALT_ROUNDS=12
```

### 6. Rate Limiting

```bash
RATE_LIMIT_PER_MINUTE=100          # API requests per minute per IP
AUTH_RATE_LIMIT_PER_MINUTE=5       # Auth attempts per minute per IP
```

### 7. File Upload Configuration

```bash
MAX_UPLOAD_SIZE=10                    # Max upload size in MB
ALLOWED_FILE_TYPES=.txt,.pdf,.docx,.json  # Allowed file extensions
UPLOAD_DIR=uploads                    # Upload directory
```

### 8. Logging Configuration

```bash
LOG_LEVEL=INFO                        # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FILE=logs/app.log                 # Log file path
LOG_MAX_SIZE=10                       # Max log file size in MB
LOG_BACKUP_COUNT=5                    # Number of backup log files
```

## Optional Configuration

### Email Settings (SMTP)

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TLS=true
EMAIL_FROM=noreply@your-domain.com
EMAIL_SUBJECT_PREFIX=[Subjunctive Practice]
```

### Monitoring and Analytics

```bash
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
ANALYTICS_API_KEY=your-analytics-key
ENABLE_METRICS=true
METRICS_PORT=9090
```

## Environment-Specific Settings

### Development Environment

- Debug mode enabled
- Verbose logging
- Hot reload enabled
- Less strict security (for convenience)
- Mock external services option

### Staging Environment

- Production-like settings
- Debug logging enabled
- Test data reset capabilities
- Limited rate limiting

### Production Environment

- Debug mode disabled
- Strict security settings
- Performance optimizations
- Multiple workers
- SSL/TLS enabled
- Comprehensive monitoring

## Security Best Practices

### 1. Secret Management

- **Never commit `.env` files** to version control
- Use different secrets for each environment
- Rotate secrets regularly
- Use minimum required permissions

### 2. File Permissions

Set restrictive permissions on sensitive files:

```bash
chmod 600 .env
chmod 600 .secrets.json
chmod 600 .secrets_key
```

### 3. Environment Separation

- Use separate databases for each environment
- Use different API keys for dev/staging/production
- Isolate infrastructure between environments

### 4. Secrets Rotation

Regular rotation of sensitive values:

```bash
# Rotate encryption key
python3 config/secrets_manager.py rotate-key

# Update JWT secret
python3 config/secrets_manager.py set JWT_SECRET_KEY "new-secret-here"
```

## Validation and Testing

### Validate Configuration

Run the environment validator to check your configuration:

```bash
python3 backend/utils/env_validator.py
```

This will:
- Validate all required variables are set
- Check API key formats
- Test database connection
- Test Redis connection
- Test external service connectivity
- Verify file permissions
- Generate a validation report

### Test Services

#### Database Connection
```bash
# Using psql
psql "postgresql://username:password@host:port/database"

# Using pg_isready
pg_isready -h localhost -p 5432
```

#### Redis Connection
```bash
# Using redis-cli
redis-cli -h localhost -p 6379 ping
```

#### OpenAI API
```bash
# Using curl
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer your-api-key"
```

## Docker Configuration

When using Docker Compose, environment variables are automatically mapped from your `.env` file. Key Docker-specific settings:

```bash
# Docker database URL
DATABASE_URL=postgresql://postgres:password@db:5432/subjunctive_practice

# Docker Redis URL  
REDIS_URL=redis://redis:6379/0

# Host binding for Docker
HOST=0.0.0.0
```

## Troubleshooting

### Common Issues

1. **Database Connection Fails**
   - Check if PostgreSQL is running
   - Verify connection URL format
   - Check firewall settings
   - Verify user permissions

2. **Redis Connection Fails**
   - Check if Redis is running
   - Verify Redis URL format
   - Check Redis configuration
   - Verify network connectivity

3. **OpenAI API Errors**
   - Verify API key format (starts with `sk-`)
   - Check API key permissions
   - Verify billing is set up
   - Check rate limiting

4. **Permission Denied Errors**
   - Check file permissions on `.env`
   - Verify directory permissions
   - Check user/group ownership

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
DEBUG_SQL=true
```

### Health Checks

The application provides health check endpoints:

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed health check with dependencies
curl http://localhost:8000/health/detailed
```

## Advanced Configuration

### Using External Secret Managers

#### HashiCorp Vault

```bash
VAULT_URL=https://vault.example.com
VAULT_TOKEN=your-vault-token
VAULT_SECRET_PATH=secret/data/subjunctive-practice
```

#### AWS Secrets Manager

```bash
AWS_SECRET_NAME=subjunctive-practice-secrets
AWS_DEFAULT_REGION=us-east-1
```

### Custom Configuration Classes

For advanced use cases, you can create custom configuration classes in `backend/config/settings.py`:

```python
class CustomSettings(Settings):
    # Custom configuration overrides
    custom_feature_flag: bool = True
    
    class Config(Settings.Config):
        env_file = ".env.custom"
```

## Migration and Updates

### Updating Configuration

1. Backup current `.env` file
2. Review new configuration options in `.env.example`
3. Update your `.env` file with new variables
4. Run validation to ensure everything works
5. Update any custom configuration classes

### Environment Migration

When migrating between environments:

1. Export configuration from source environment
2. Update environment-specific values
3. Import to target environment
4. Validate configuration
5. Test all services

## Support and Resources

- **Configuration Templates**: `config/environments/`
- **Validation Scripts**: `backend/utils/env_validator.py`
- **Secrets Management**: `config/secrets_manager.py`
- **Setup Scripts**: `scripts/setup_env.sh`
- **Docker Configuration**: `docker-compose.yml`

For additional help, check the project documentation or create an issue in the repository.