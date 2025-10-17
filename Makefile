# Makefile for FastAPI Backend
# Spanish Subjunctive Practice Application

.PHONY: help install dev test clean lint format docker-build docker-up docker-down migrate db-upgrade db-downgrade

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose
APP_NAME := subjunctive-backend

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)FastAPI Backend - Make Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ================================
# Installation & Setup
# ================================

install: ## Install production dependencies
	@echo "$(BLUE)Installing production dependencies...$(NC)"
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt

setup: ## Setup development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	cp .env.example .env
	@echo "$(GREEN)Environment file created. Please update .env with your configuration.$(NC)"

# ================================
# Development
# ================================

dev: ## Run development server with auto-reload
	@echo "$(BLUE)Starting development server...$(NC)"
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run: ## Run production server
	@echo "$(BLUE)Starting production server...$(NC)"
	gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

shell: ## Start Python interactive shell
	@echo "$(BLUE)Starting Python shell...$(NC)"
	$(PYTHON) -i -c "from main import app; print('FastAPI app available as: app')"

# ================================
# Testing
# ================================

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest

test-verbose: ## Run tests with verbose output
	@echo "$(BLUE)Running tests (verbose)...$(NC)"
	pytest -v -s

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	pytest-watch

# ================================
# Code Quality
# ================================

lint: ## Run all linters
	@echo "$(BLUE)Running linters...$(NC)"
	flake8 .
	pylint **/*.py
	mypy .

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	black .
	isort .

format-check: ## Check code formatting without changes
	@echo "$(BLUE)Checking code formatting...$(NC)"
	black --check .
	isort --check-only .

type-check: ## Run type checking
	@echo "$(BLUE)Running type checks...$(NC)"
	mypy .

# ================================
# Database
# ================================

migrate: ## Create a new database migration
	@echo "$(BLUE)Creating new migration...$(NC)"
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

db-upgrade: ## Upgrade database to latest version
	@echo "$(BLUE)Upgrading database...$(NC)"
	alembic upgrade head

db-downgrade: ## Downgrade database by one version
	@echo "$(YELLOW)Downgrading database...$(NC)"
	alembic downgrade -1

db-reset: ## Reset database (WARNING: Destroys all data)
	@echo "$(RED)WARNING: This will destroy all database data!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		alembic downgrade base && alembic upgrade head; \
	else \
		echo "$(YELLOW)Operation cancelled.$(NC)"; \
	fi

db-seed: ## Seed database with sample data
	@echo "$(BLUE)Seeding database...$(NC)"
	$(PYTHON) scripts/seed_db.py

# ================================
# Docker
# ================================

docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) up -d

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down

docker-logs: ## View Docker container logs
	@echo "$(BLUE)Viewing container logs...$(NC)"
	$(DOCKER_COMPOSE) logs -f

docker-restart: ## Restart Docker containers
	@echo "$(BLUE)Restarting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) restart

docker-clean: ## Remove Docker containers and volumes
	@echo "$(RED)Removing Docker containers and volumes...$(NC)"
	$(DOCKER_COMPOSE) down -v

docker-shell: ## Open shell in backend container
	@echo "$(BLUE)Opening shell in backend container...$(NC)"
	$(DOCKER_COMPOSE) exec backend /bin/bash

# ================================
# Cleanup
# ================================

clean: ## Clean up temporary files
	@echo "$(BLUE)Cleaning up temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage build/ dist/
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-logs: ## Clean log files
	@echo "$(BLUE)Cleaning log files...$(NC)"
	rm -rf logs/*.log

# ================================
# Deployment
# ================================

deploy-railway: ## Deploy to Railway
	@echo "$(BLUE)Deploying to Railway...$(NC)"
	railway up

deploy-render: ## Deploy to Render
	@echo "$(BLUE)Deploying to Render...$(NC)"
	@echo "$(YELLOW)Push to main branch to trigger Render deployment$(NC)"
	git push origin main

# ================================
# Utilities
# ================================

requirements: ## Update requirements.txt from current environment
	@echo "$(BLUE)Updating requirements.txt...$(NC)"
	$(PIP) freeze > requirements.txt

check-deps: ## Check for dependency updates
	@echo "$(BLUE)Checking for dependency updates...$(NC)"
	$(PIP) list --outdated

security-check: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	pip-audit

health: ## Check API health
	@echo "$(BLUE)Checking API health...$(NC)"
	curl -f http://localhost:8000/health || echo "$(RED)API is not responding$(NC)"

# ================================
# Documentation
# ================================

docs-serve: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation...$(NC)"
	mkdocs serve

docs-build: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	mkdocs build

# ================================
# Pre-commit
# ================================

pre-commit-install: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install

pre-commit-run: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files
