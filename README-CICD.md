# CI/CD Pipeline - Spanish Subjunctive Practice Application

> **Comprehensive CI/CD automation for testing, security scanning, and deployment**

## Quick Start

```bash
# 1. Verify setup
./scripts/verify-ci-setup.sh

# 2. Configure secrets
./scripts/setup-ci-secrets.sh

# 3. Test locally
cd backend && pytest
cd frontend && npm test

# 4. Push and create PR
git checkout -b feature/your-feature
git push origin feature/your-feature
```

## Overview

This project implements a production-ready CI/CD pipeline using GitHub Actions with:

- Automated Testing - Multi-version testing for Python and Node.js
- Security Scanning - CodeQL, Snyk, TruffleHog, Trivy, Bandit, Semgrep
- Code Quality - Linting, formatting, type checking
- E2E Testing - Playwright browser automation
- Continuous Deployment - Railway (backend) and Vercel (frontend)
- Release Automation - GitHub releases and Docker publishing
- Dependency Management - Dependabot weekly updates

## Complete Documentation

- **Setup Guide**: `C:\Users\brand\Development\Project_Workspace\active-development\language-learning\subjunctive_practice\docs\CI-CD-SETUP.md`
- **Quick Reference**: `C:\Users\brand\Development\Project_Workspace\active-development\language-learning\subjunctive_practice\docs\CI-CD-QUICK-REFERENCE.md`
- **Summary**: `C:\Users\brand\Development\Project_Workspace\active-development\language-learning\subjunctive_practice\docs\CI-CD-SUMMARY.md`
- **Architecture**: `C:\Users\brand\Development\Project_Workspace\active-development\language-learning\subjunctive_practice\docs\CI-CD-ARCHITECTURE.md`
- **File Listing**: `C:\Users\brand\Development\Project_Workspace\active-development\language-learning\subjunctive_practice\.github\CI-CD-FILES.txt`

---

**Last Updated**: 2025-10-02
**Total Files Created**: 21
