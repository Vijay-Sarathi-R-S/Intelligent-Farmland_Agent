## Docker & CI/CD Setup Guide - Intelligent Farmland Agent

### 📋 Contents

This setup includes:

- **GitHub Actions CI/CD Workflows** - Automated testing and deployment
- **Multi-stage Dockerfile** - Optimized production image
- **Docker Compose** - Local and production environments
- **Nginx Configuration** - Reverse proxy with security headers and rate limiting
- **Deployment Scripts** - Automation for building and deploying

---

## 🚀 Quick Start

### Local Development with Docker Compose

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Intelligent-Farmland_Agent

# 2. Copy environment template
cp .env.example .env

# 3. Add your API keys to .env
# GEMINI_API_KEY=your-key
# NASA_API_KEY=your-key

# 4. Start services
docker-compose up -d

# 5. Access application
# http://localhost:5000
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f redis
```

---

## 📦 Docker Images

### Image Tags Strategy

The CD workflow creates images with multiple tags:

- `main` - Latest main branch build
- `v1.2.3` - Semantic version (from git tags)
- `main-<sha>` - Commit SHA for traceability

### Building Locally

```bash
# Development build
docker build -t farmland-agent:dev .

# With specific Python version
docker build --build-arg PYTHON_VERSION=3.12 -t farmland-agent:3.12 .

# Using build script
./build-docker.sh
```

### Running Container

```bash
# Interactive mode
docker run -it -p 5000:5000 \
  -e GEMINI_API_KEY=your-key \
  -e NASA_API_KEY=your-key \
  farmland-agent:latest

# Detached mode
docker run -d -p 5000:5000 \
  --env-file .env \
  --name farmland-app \
  farmland-agent:latest
```

---

## 🐳 Docker Compose Environments

### Development (`docker-compose.yml`)

Services:
- **app** - Flask application
- **redis** - Cache (optional profiles)
- **postgres** - Database (optional profiles)

Start all services:
```bash
docker-compose up -d
```

Start with database:
```bash
docker-compose --profile with-db up -d
```

### Production (`docker-compose.prod.yml`)

Additional features:
- **Nginx** - Reverse proxy with SSL support
- **PostgreSQL** - Production database
- **Redis** - Cache with authentication
- **Logging** - JSON file logging with rotation
- **Health checks** - Service lifecycle management

Start production:
```bash
# Load production environment
export $(cat .env.prod | xargs)

# Use deployment script (recommended)
./deploy-prod.sh

# Or manual start
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔄 CI/CD GitHub Actions Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:** Push to main/develop, Pull Requests

**Jobs:**
- **Test** - Multi-version Python testing (3.10, 3.11, 3.12)
  - Install dependencies
  - Lint with flake8
  - Run pytest with coverage
  - Upload coverage to Codecov
  
- **Code Quality** - Security scanning
  - Bandit security audit
  - Safety dependency check

**Status Badge:**
```markdown
![CI](https://github.com/your-org/repo/workflows/CI%20-%20Test%20%26%20Lint/badge.svg)
```

### 2. CD Workflow (`.github/workflows/cd.yml`)

**Triggers:** Push to main, Version tags (v*)

**Jobs:**
- **Build and Push** - Multi-platform Docker builds
  - Sets up BuildX for multi-platform support
  - Logs into Docker Hub & GHCR
  - Builds and pushes with cache
  - Tags: branch, semantic version, commit SHA

- **Deploy** - Deployment trigger (on tags)
  - Calls deployment webhook
  - Creates GitHub Release

**Required Secrets:**
```
DOCKER_USERNAME      # Docker Hub username
DOCKER_PASSWORD      # Docker Hub access token
DEPLOYMENT_WEBHOOK_URL  # Optional: deployment endpoint
```

### Setting Up Secrets

GitHub → Settings → Secrets and Variables → Actions

```bash
# Generate Docker Hub access token
# https://hub.docker.com/settings/security

# Add secrets
gh secret set DOCKER_USERNAME
gh secret set DOCKER_PASSWORD
gh secret set DEPLOYMENT_WEBHOOK_URL  # Optional
```

---

## 📝 Configuration Files

### `.env.example`

Template with all required variables. Copy to `.env` and fill in values.

### `.dockerignore`

Excludes unnecessary files from Docker build context (like `.git`, `__pycache__`, etc.)

### `nginx.conf`

Nginx configuration featuring:
- Rate limiting (API: 50 req/min, General: 200 req/min)
- Gzip compression
- Security headers (CSP, X-Frame-Options, etc.)
- SSL/TLS support (commented, uncomment for HTTPS)
- Health check endpoint
- Reverse proxy to Flask app

### Deployment Scripts

#### `build-docker.sh`
Build and push Docker image with optional registry credentials.

```bash
./build-docker.sh
```

#### `setup-dev.sh`
Initialize development environment (creates .env, starts services).

```bash
./setup-dev.sh
```

#### `deploy-prod.sh`
Production deployment with health checks and verification.

```bash
./deploy-prod.sh
```

---

## 🔒 Security Best Practices

### Implemented

✅ Non-root user in container (UID 1000)
✅ Multi-stage build (reduces image size)
✅ Health checks enabled
✅ Security headers in Nginx
✅ Rate limiting
✅ Input validation ready
✅ .gitignore for sensitive files

### ToDo

- [ ] Enable HTTPS/SSL in production
- [ ] Set up secrets scanning in CI
- [ ] Implement dependency scanning
- [ ] Add container security scanning (Trivy)
- [ ] Enable SBOM generation
- [ ] Set up audit logging

### Production Checklist

```
[ ] Set strong DATABASE_URL and REDIS_PASSWORD
[ ] Update SECRET_KEY in production
[ ] Enable HTTPS in nginx.conf
[ ] Configure SSL certificates
[ ] Set up monitoring and alerting
[ ] Enable audit logging
[ ] Configure backup strategy for PostgreSQL
[ ] Set resource limits in Docker
[ ] Review security headers
[ ] Test disaster recovery
```

---

## 📊 Monitoring & Logging

### View Logs

```bash
# Tail all services
docker-compose logs -f

# Specific service with last 100 lines
docker-compose logs -f --tail=100 app

# Search logs
docker-compose logs app | grep "ERROR"
```

### Health Checks

```bash
# Check service health
docker-compose ps

# Manual health check
curl http://localhost:5000/
```
