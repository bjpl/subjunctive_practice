# Deployment Playbook

Complete step-by-step deployment guide for the Spanish Subjunctive Practice Application.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Migration](#database-migration)
4. [Deployment Procedures](#deployment-procedures)
5. [Rollback Procedures](#rollback-procedures)
6. [Disaster Recovery](#disaster-recovery)
7. [Post-Deployment Verification](#post-deployment-verification)

---

## Pre-Deployment Checklist

### Code Readiness

- [ ] All tests passing (backend and frontend)
- [ ] Code review completed and approved
- [ ] Version number updated in `package.json` and backend config
- [ ] CHANGELOG updated with release notes
- [ ] No critical security vulnerabilities
- [ ] Dependencies up to date and audited

### Environment Configuration

- [ ] Production environment variables configured
- [ ] Database connection strings verified
- [ ] API keys and secrets rotated
- [ ] CORS origins updated for production domains
- [ ] SSL certificates valid and not expiring soon

### Infrastructure

- [ ] Database backup completed
- [ ] Monitoring systems operational
- [ ] Log aggregation configured
- [ ] CDN configured (if applicable)
- [ ] DNS records verified

### Communication

- [ ] Stakeholders notified of deployment window
- [ ] Maintenance page ready (if needed)
- [ ] Rollback plan reviewed with team
- [ ] Support team briefed on new features

---

## Environment Setup

### Local Development Environment

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment template
cp .env.example .env

# Edit .env with development configuration
# Key settings:
# - ENVIRONMENT=development
# - DEBUG=true
# - DATABASE_URL=postgresql://localhost:5432/subjunctive_dev
# - REDIS_URL=redis://localhost:6379/0
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Staging Environment

#### Backend Staging

```bash
# Set staging environment variables
export ENVIRONMENT=staging
export DEBUG=false
export DATABASE_URL=$STAGING_DATABASE_URL
export REDIS_URL=$STAGING_REDIS_URL
export JWT_SECRET_KEY=$STAGING_JWT_SECRET
export CORS_ORIGINS=https://staging.subjunctivepractice.com

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start with gunicorn
gunicorn main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

#### Frontend Staging

```bash
# Set environment variables
export NEXT_PUBLIC_API_URL=https://api-staging.subjunctivepractice.com
export NODE_ENV=production

# Build application
npm run build

# Start production server
npm start
```

### Production Environment

#### Backend Production

```bash
# Set production environment variables
export ENVIRONMENT=production
export DEBUG=false
export DATABASE_URL=$PRODUCTION_DATABASE_URL
export REDIS_URL=$PRODUCTION_REDIS_URL
export JWT_SECRET_KEY=$PRODUCTION_JWT_SECRET
export SESSION_SECRET_KEY=$PRODUCTION_SESSION_SECRET
export OPENAI_API_KEY=$PRODUCTION_OPENAI_KEY
export CORS_ORIGINS=https://subjunctivepractice.com
export SENTRY_DSN=$PRODUCTION_SENTRY_DSN

# Install dependencies
pip install -r requirements.txt

# Run migrations (after backup)
alembic upgrade head

# Start with gunicorn (4 workers for production)
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

#### Frontend Production

```bash
# Set environment variables
export NEXT_PUBLIC_API_URL=https://api.subjunctivepractice.com
export NODE_ENV=production

# Build with optimizations
npm run build

# Start production server
npm start
```

---

## Database Migration

### Pre-Migration Steps

1. **Backup Database**

```bash
# PostgreSQL backup
pg_dump -h $DB_HOST -U $DB_USER -d subjunctive_practice \
  -F c -b -v -f backup_$(date +%Y%m%d_%H%M%S).dump

# Verify backup
pg_restore --list backup_YYYYMMDD_HHMMSS.dump
```

2. **Test Migrations on Staging**

```bash
# On staging environment
cd backend

# Check current migration status
alembic current

# Review pending migrations
alembic heads
alembic show head

# Test migration (dry run if possible)
alembic upgrade head --sql > migration_preview.sql
# Review migration_preview.sql
```

3. **Create Migration Rollback Plan**

```bash
# Document current version
alembic current > current_version.txt

# Prepare downgrade script
echo "alembic downgrade $(cat current_version.txt)" > rollback.sh
chmod +x rollback.sh
```

### Migration Execution

1. **Enable Maintenance Mode** (if required)

```bash
# Set maintenance flag in Redis
redis-cli SET maintenance_mode 1

# Or use environment variable
export MAINTENANCE_MODE=true
```

2. **Stop Application Services**

```bash
# Docker
docker-compose down backend

# Systemd
sudo systemctl stop subjunctive-backend

# Manual
kill -TERM $(cat backend.pid)
```

3. **Run Migrations**

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Run migrations
alembic upgrade head

# Verify migration completed
alembic current
```

4. **Restart Application**

```bash
# Docker
docker-compose up -d backend

# Systemd
sudo systemctl start subjunctive-backend

# Manual
gunicorn main:app --daemon --pid backend.pid
```

5. **Verify Application**

```bash
# Health check
curl https://api.subjunctivepractice.com/health

# Database connectivity
curl https://api.subjunctivepractice.com/health/db
```

6. **Disable Maintenance Mode**

```bash
redis-cli DEL maintenance_mode
```

### Post-Migration Verification

```bash
# Check database schema version
psql -h $DB_HOST -U $DB_USER -d subjunctive_practice \
  -c "SELECT version_num FROM alembic_version;"

# Verify critical tables
psql -h $DB_HOST -U $DB_USER -d subjunctive_practice \
  -c "\dt"

# Test critical queries
curl -X POST https://api.subjunctivepractice.com/api/v1/exercises \
  -H "Authorization: Bearer $TEST_TOKEN"
```

---

## Deployment Procedures

### Docker Deployment

#### Full Stack with Docker Compose

```bash
# Clone repository
git clone https://github.com/yourorg/subjunctive-practice.git
cd subjunctive-practice

# Create environment file
cp backend/.env.example backend/.env
# Edit backend/.env with production values

# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify services
docker-compose ps
```

#### Backend Only

```bash
cd backend

# Build production image
docker build -t subjunctive-backend:latest --target production .

# Run container
docker run -d \
  --name subjunctive-backend \
  -p 8000:8000 \
  --env-file .env.production \
  subjunctive-backend:latest

# Check logs
docker logs -f subjunctive-backend
```

#### Frontend Only

```bash
cd frontend

# Build production image
docker build -t subjunctive-frontend:latest .

# Run container
docker run -d \
  --name subjunctive-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.subjunctivepractice.com \
  subjunctive-frontend:latest
```

### Railway Deployment

#### Initial Setup

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to existing project
railway link [project-id]
```

#### Backend Deployment

```bash
cd backend

# Deploy
railway up

# Or use Git-based deployment
git push railway main

# View logs
railway logs

# Check status
railway status
```

#### Configure Services

```bash
# Add PostgreSQL
railway add postgresql

# Add Redis
railway add redis

# Set environment variables
railway variables set JWT_SECRET_KEY=[secret]
railway variables set SESSION_SECRET_KEY=[secret]
railway variables set OPENAI_API_KEY=[key]
railway variables set CORS_ORIGINS=https://your-frontend.railway.app
```

### Render Deployment

#### Backend Setup

1. **Connect Repository**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `backend` directory

2. **Configure Service**
   - Name: `subjunctive-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Database**
   - Click "New +" → "PostgreSQL"
   - Name: `subjunctive-postgres`
   - Link to web service

4. **Set Environment Variables**
   ```
   ENVIRONMENT=production
   DEBUG=false
   DATABASE_URL=[auto-populated]
   JWT_SECRET_KEY=[generate secure key]
   SESSION_SECRET_KEY=[generate secure key]
   OPENAI_API_KEY=[your key]
   CORS_ORIGINS=https://your-frontend.onrender.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment

#### Frontend Setup

1. **Create Web Service**
   - New Static Site or Web Service
   - Connect repository
   - Select `frontend` directory

2. **Configure Build**
   - Build Command: `npm run build`
   - Publish Directory: `.next`

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://subjunctive-backend.onrender.com/api/v1
   NODE_ENV=production
   ```

### Vercel Deployment (Frontend)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Production deployment
vercel --prod

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL production
```

### Manual VPS Deployment

#### Backend on Ubuntu Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv postgresql-client redis-tools nginx

# Create application user
sudo useradd -m -s /bin/bash appuser

# Clone repository
sudo -u appuser git clone https://github.com/yourorg/subjunctive-practice.git /home/appuser/app

# Setup backend
cd /home/appuser/app/backend
sudo -u appuser python3.11 -m venv venv
sudo -u appuser venv/bin/pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/subjunctive-backend.service
```

**systemd service file:**

```ini
[Unit]
Description=Subjunctive Practice Backend
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=appuser
Group=appuser
WorkingDirectory=/home/appuser/app/backend
Environment="PATH=/home/appuser/app/backend/venv/bin"
EnvironmentFile=/home/appuser/app/backend/.env.production
ExecStart=/home/appuser/app/backend/venv/bin/gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000 \
  --timeout 120 \
  --access-logfile /var/log/subjunctive/access.log \
  --error-logfile /var/log/subjunctive/error.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/subjunctive
sudo chown appuser:appuser /var/log/subjunctive

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable subjunctive-backend
sudo systemctl start subjunctive-backend

# Check status
sudo systemctl status subjunctive-backend
```

#### Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/subjunctive-practice
```

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.subjunctivepractice.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.subjunctivepractice.com;

    ssl_certificate /etc/letsencrypt/live/api.subjunctivepractice.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.subjunctivepractice.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Increase upload size
    client_max_body_size 10M;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /health {
        proxy_pass http://backend/health;
        access_log off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/subjunctive-practice /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## Rollback Procedures

### Immediate Rollback (Critical Issues)

#### Docker Deployment

```bash
# Stop current containers
docker-compose down

# Revert to previous image
docker tag subjunctive-backend:latest subjunctive-backend:backup
docker tag subjunctive-backend:v1.0.0 subjunctive-backend:latest

# Restart
docker-compose up -d

# Monitor
docker-compose logs -f
```

#### Railway/Render

```bash
# Railway - rollback to previous deployment
railway rollback

# Render - redeploy previous version from dashboard
# Or git revert and push
git revert HEAD
git push origin main
```

### Database Rollback

#### Rollback Migration

```bash
# Check current version
alembic current

# Downgrade one version
alembic downgrade -1

# Or downgrade to specific version
alembic downgrade <revision>

# Restart application
sudo systemctl restart subjunctive-backend
```

#### Restore from Backup

```bash
# Stop application
docker-compose down backend

# Restore database
pg_restore -h $DB_HOST -U $DB_USER -d subjunctive_practice \
  -c -v backup_YYYYMMDD_HHMMSS.dump

# Start application
docker-compose up -d backend
```

### Code Rollback

#### Git Revert

```bash
# Revert last commit
git revert HEAD

# Push revert
git push origin main

# Trigger redeployment
```

#### Git Reset (Use with caution)

```bash
# Create backup branch
git branch backup-before-reset

# Reset to previous version
git reset --hard HEAD~1

# Force push (only if safe)
git push --force origin main
```

### Frontend Rollback

```bash
# Vercel - rollback from dashboard or CLI
vercel rollback [deployment-url]

# Manual - redeploy previous version
git checkout v1.0.0
npm run build
vercel --prod
```

---

## Disaster Recovery

### Scenario 1: Complete Database Failure

#### Recovery Steps

1. **Assess Damage**

```bash
# Check database connectivity
pg_isready -h $DB_HOST -U $DB_USER

# Check replication status (if configured)
psql -h $DB_HOST -U $DB_USER -c "SELECT * FROM pg_stat_replication;"
```

2. **Failover to Replica** (if available)

```bash
# Promote replica to primary
pg_ctl promote -D /var/lib/postgresql/data

# Update application DATABASE_URL
export DATABASE_URL=postgresql://replica-host:5432/subjunctive_practice

# Restart application
sudo systemctl restart subjunctive-backend
```

3. **Restore from Backup**

```bash
# Create new database instance
createdb -h $NEW_DB_HOST -U $DB_USER subjunctive_practice

# Restore latest backup
pg_restore -h $NEW_DB_HOST -U $DB_USER -d subjunctive_practice \
  -v -c backup_latest.dump

# Update application configuration
export DATABASE_URL=postgresql://$NEW_DB_HOST:5432/subjunctive_practice

# Restart application
sudo systemctl restart subjunctive-backend
```

### Scenario 2: Complete Application Server Failure

#### Recovery Steps

1. **Spin Up New Server**

```bash
# Using infrastructure as code (Terraform example)
terraform apply -var="server_count=2"

# Or manually provision new server
# Follow VPS deployment guide above
```

2. **Deploy Application**

```bash
# Clone repository
git clone https://github.com/yourorg/subjunctive-practice.git

# Deploy using Docker
cd subjunctive-practice
docker-compose up -d

# Or deploy manually
# Follow manual deployment guide
```

3. **Update DNS**

```bash
# Point domain to new server IP
# Update A record: api.subjunctivepractice.com -> NEW_IP

# Verify DNS propagation
dig api.subjunctivepractice.com
```

### Scenario 3: Data Corruption

#### Recovery Steps

1. **Identify Affected Data**

```bash
# Check data integrity
psql -h $DB_HOST -U $DB_USER -d subjunctive_practice << EOF
SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL '1 hour';
SELECT COUNT(*) FROM exercises WHERE updated_at > NOW() - INTERVAL '1 hour';
EOF
```

2. **Restore Affected Tables**

```bash
# Extract specific table from backup
pg_restore -h $DB_HOST -U $DB_USER -d subjunctive_practice \
  -t users -t user_progress backup_latest.dump
```

3. **Verify Data Integrity**

```bash
# Run data validation scripts
python backend/scripts/validate_data.py

# Check application functionality
curl https://api.subjunctivepractice.com/api/v1/exercises
```

### Backup Strategy

#### Automated Backups

```bash
# Create backup script
cat > /usr/local/bin/backup-subjunctive.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/subjunctive"
DATE=$(date +%Y%m%d_%H%M%S)
DB_HOST="localhost"
DB_USER="app_user"
DB_NAME="subjunctive_practice"

# Create backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME \
  -F c -b -v -f $BACKUP_DIR/backup_$DATE.dump

# Compress
gzip $BACKUP_DIR/backup_$DATE.dump

# Upload to S3 (or other cloud storage)
aws s3 cp $BACKUP_DIR/backup_$DATE.dump.gz \
  s3://subjunctive-backups/database/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -type f -mtime +30 -delete

# Log
echo "$(date): Backup completed - backup_$DATE.dump.gz" >> /var/log/subjunctive/backup.log
EOF

chmod +x /usr/local/bin/backup-subjunctive.sh
```

#### Schedule Backups

```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /usr/local/bin/backup-subjunctive.sh

# Hourly backup during business hours (9 AM - 5 PM)
0 9-17 * * * /usr/local/bin/backup-subjunctive.sh
```

---

## Post-Deployment Verification

### Health Checks

```bash
# Backend health
curl https://api.subjunctivepractice.com/health

# Expected response:
# {"status": "healthy", "version": "1.0.0", "timestamp": "..."}

# Database health
curl https://api.subjunctivepractice.com/health/db

# Redis health
curl https://api.subjunctivepractice.com/health/redis
```

### Functional Testing

```bash
# User registration
curl -X POST https://api.subjunctivepractice.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# User login
curl -X POST https://api.subjunctivepractice.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Get exercises
curl https://api.subjunctivepractice.com/api/v1/exercises \
  -H "Authorization: Bearer $TOKEN"
```

### Performance Verification

```bash
# Response time check
time curl https://api.subjunctivepractice.com/api/v1/exercises

# Load test with Apache Bench
ab -n 1000 -c 10 https://api.subjunctivepractice.com/health

# Monitor server metrics
htop
iostat -x 1 10
```

### Monitoring Setup Verification

```bash
# Check logs are being collected
tail -f /var/log/subjunctive/access.log
tail -f /var/log/subjunctive/error.log

# Verify Sentry integration
# Trigger test error
curl https://api.subjunctivepractice.com/api/v1/test-error

# Check Sentry dashboard for error
```

### Frontend Verification

```bash
# Homepage accessible
curl -I https://subjunctivepractice.com

# API connectivity
# Visit https://subjunctivepractice.com in browser
# Open DevTools → Network tab
# Verify API calls successful
```

### SSL/TLS Verification

```bash
# Check SSL certificate
openssl s_client -connect api.subjunctivepractice.com:443 -servername api.subjunctivepractice.com

# Verify SSL grade
# Use: https://www.ssllabs.com/ssltest/
```

---

## Deployment Timeline

### Typical Deployment Schedule

**15 minutes before deployment:**
- Final backup verification
- Team standup
- Communication sent to users (if maintenance required)

**Deployment window (30-60 minutes):**
- T+0: Enable maintenance mode
- T+5: Database backup
- T+10: Deploy backend
- T+15: Run migrations
- T+20: Verify backend
- T+25: Deploy frontend
- T+30: Verify frontend
- T+35: Smoke tests
- T+40: Disable maintenance mode
- T+45: Monitor for issues

**Post-deployment (24 hours):**
- Continuous monitoring
- User feedback collection
- Performance metrics review

---

## Emergency Contacts

### Deployment Team

- **Deployment Lead:** [Name] - [Email] - [Phone]
- **Backend Lead:** [Name] - [Email] - [Phone]
- **Frontend Lead:** [Name] - [Email] - [Phone]
- **Database Admin:** [Name] - [Email] - [Phone]
- **DevOps Engineer:** [Name] - [Email] - [Phone]

### Escalation Path

1. **Level 1:** Deployment Team
2. **Level 2:** Engineering Manager
3. **Level 3:** CTO/VP Engineering

### External Services Support

- **Railway Support:** https://railway.app/help
- **Render Support:** https://render.com/docs/support
- **Vercel Support:** https://vercel.com/support
- **PostgreSQL Community:** https://www.postgresql.org/support/
