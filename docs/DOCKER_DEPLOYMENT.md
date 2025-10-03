# Docker Deployment Guide

## Spanish Subjunctive Practice Application

This guide provides comprehensive instructions for deploying the Spanish Subjunctive Practice application using Docker and Docker Compose.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Production Deployment](#production-deployment)
5. [Development Setup](#development-setup)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Security](#security)
9. [Scaling](#scaling)

## Prerequisites

- Docker Engine 20.10+ 
- Docker Compose 2.0+
- Git
- 4GB+ available RAM
- 10GB+ available disk space

### Installation

#### Windows
```bash
# Install Docker Desktop from https://docker.com/products/docker-desktop
# Or use chocolatey
choco install docker-desktop
```

#### macOS
```bash
# Install Docker Desktop from https://docker.com/products/docker-desktop
# Or use homebrew
brew install --cask docker
```

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin
```

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd subjunctive_practice

# Copy environment configuration
cp .env.docker .env
```

### 2. Start Services
```bash
# Start all services
./scripts/deploy.sh

# Or manually
docker-compose up -d
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Configuration

### Environment Variables

Create or modify `.env` file:

```bash
# Application Settings
ENVIRONMENT=production
DEBUG=false
VERSION=1.0.0

# Database Configuration
POSTGRES_DB=subjunctive_practice
POSTGRES_USER=app_user
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://app_user:your_secure_password@postgres:5432/subjunctive_practice

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Security Keys (CHANGE THESE IN PRODUCTION!)
JWT_SECRET_KEY=your-super-secret-jwt-key
SESSION_SECRET_KEY=your-super-secret-session-key

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:80,https://yourdomain.com

# Optional: External Services
OPENAI_API_KEY=your_openai_api_key
SENTRY_DSN=your_sentry_dsn
```

### Service Configuration

#### Backend Service
- **Port**: 8000
- **Health Check**: `/health`
- **Documentation**: `/docs`
- **Technology**: FastAPI + Python 3.11

#### Frontend Service  
- **Port**: 3000 (development) / 80 (production)
- **Health Check**: `/health`
- **Technology**: React 18 + Vite

#### Database Service
- **Port**: 5432
- **Database**: PostgreSQL 15
- **Initialization**: Automatic schema creation

#### Cache Service
- **Port**: 6379
- **Technology**: Redis 7
- **Usage**: Session storage, caching

## Production Deployment

### 1. Production Environment

```bash
# Use production configuration
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d

# Or use the deployment script
ENVIRONMENT=production ./scripts/deploy.sh
```

### 2. SSL/HTTPS Setup

Update `nginx/nginx.conf` for HTTPS:

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Include your SSL configuration
}
```

### 3. Production Environment Variables

```bash
# Production overrides
ENVIRONMENT=production
DEBUG=false
WORKERS=4
MAX_REQUESTS=1000

# Strong passwords (generate unique ones!)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET_KEY=$(openssl rand -base64 64)
SESSION_SECRET_KEY=$(openssl rand -base64 64)
```

## Development Setup

### 1. Development Mode

```bash
# Start development environment
docker-compose run --rm dev

# Or specific services
docker-compose up backend frontend postgres redis
```

### 2. Live Reloading

Development containers support live reloading:
- Backend: FastAPI auto-reload on file changes
- Frontend: Vite HMR (Hot Module Replacement)

### 3. Debugging

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

## Service Management

### Start/Stop Services

```bash
# Start all services
./scripts/deploy.sh start

# Stop all services  
./scripts/deploy.sh stop

# Restart services
./scripts/deploy.sh restart

# View status
./scripts/deploy.sh status
```

### Individual Services

```bash
# Start specific service
docker-compose up -d backend

# Stop specific service
docker-compose stop frontend

# Restart specific service
docker-compose restart postgres
```

## Monitoring and Maintenance

### Health Checks

```bash
# Run comprehensive health checks
./scripts/health_check.sh

# Check specific service
./scripts/health_check.sh backend
./scripts/health_check.sh database

# Generate health report
./scripts/health_check.sh report
```

### Backup and Recovery

```bash
# Create backup
./scripts/backup.sh

# List backups
./scripts/backup.sh list

# Restore from backup
./scripts/backup.sh restore [backup_directory]

# Restore from latest backup
./scripts/backup.sh restore
```

### Log Management

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 frontend

# Export logs
docker-compose logs backend > backend.log
```

### Resource Monitoring

```bash
# View resource usage
docker stats

# View container information
docker-compose ps

# View system resource usage
./scripts/health_check.sh resources
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Scale with production config
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d --scale backend=2 --scale frontend=2
```

### Load Balancing

Nginx automatically load balances between scaled containers. Update upstream configuration for custom load balancing.

### Resource Limits

Production configuration includes resource limits:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

## Security

### 1. Change Default Passwords

```bash
# Generate secure passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET_KEY=$(openssl rand -base64 64)
SESSION_SECRET_KEY=$(openssl rand -base64 64)
```

### 2. Network Security

- Services communicate through isolated Docker network
- Only necessary ports exposed to host
- Nginx reverse proxy handles external requests

### 3. Container Security

- Non-root users in all containers
- Minimal base images (Alpine Linux)
- Security scanning with `docker scan`

### 4. Data Security

- Database data persisted in Docker volumes
- Automatic backups with retention
- SSL/TLS encryption for external communications

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check container logs
docker-compose logs [service_name]

# Check container status
docker-compose ps

# Rebuild problematic service
docker-compose build --no-cache [service_name]
```

#### Database Connection Issues

```bash
# Check database logs
docker-compose logs postgres

# Verify database is ready
docker-compose exec postgres pg_isready -U app_user

# Check database connections
docker-compose exec postgres psql -U app_user -d subjunctive_practice -c "SELECT 1;"
```

#### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Verify frontend build
docker-compose exec frontend ls -la /usr/share/nginx/html

# Check nginx configuration
docker-compose exec nginx nginx -t
```

#### Port Conflicts

```bash
# Check port usage
netstat -tulpn | grep :8000

# Use different ports
docker-compose up -d --scale backend=1 -p 8001:8000
```

### Performance Issues

#### Memory Usage

```bash
# Check memory usage
docker stats

# Increase memory limits
# Edit docker-compose.production.yml resource limits
```

#### Disk Space

```bash
# Clean unused Docker resources
docker system prune -a

# Remove old images
docker image prune -a

# Check volume usage
docker system df
```

### Rollback Deployment

```bash
# Quick rollback to previous version
./scripts/rollback.sh

# Rollback to specific backup
./scripts/rollback.sh /path/to/backup

# List available backups
./scripts/rollback.sh list-backups
```

## Commands Reference

### Deployment Commands

| Command | Description |
|---------|-------------|
| `./scripts/deploy.sh` | Deploy application |
| `./scripts/deploy.sh stop` | Stop all services |
| `./scripts/deploy.sh restart` | Restart services |
| `./scripts/deploy.sh status` | Show service status |
| `./scripts/deploy.sh logs` | Show all logs |

### Maintenance Commands

| Command | Description |
|---------|-------------|
| `./scripts/backup.sh` | Create backup |
| `./scripts/backup.sh restore` | Restore from backup |
| `./scripts/rollback.sh` | Rollback deployment |
| `./scripts/health_check.sh` | Run health checks |

### Docker Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start services |
| `docker-compose down` | Stop and remove services |
| `docker-compose build` | Build images |
| `docker-compose logs -f` | Follow logs |
| `docker-compose ps` | Show running services |

## Best Practices

### 1. Environment Management

- Use separate `.env` files for different environments
- Never commit secrets to version control
- Rotate secrets regularly

### 2. Resource Management

- Set appropriate resource limits
- Monitor resource usage regularly
- Scale services based on load

### 3. Data Management

- Regular automated backups
- Test restore procedures
- Monitor disk usage

### 4. Security

- Keep Docker and images updated
- Use security scanning tools
- Implement proper access controls

### 5. Monitoring

- Set up health checks
- Monitor application metrics
- Use centralized logging

## Support

For issues and questions:

1. Check logs: `docker-compose logs`
2. Run health checks: `./scripts/health_check.sh`
3. Review troubleshooting section
4. Create issue in repository

---

**Last Updated**: $(date +'%Y-%m-%d')  
**Version**: 1.0.0