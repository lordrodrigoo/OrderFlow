# Force Bash shell for all commands
SHELL := /bin/bash

.PHONY: help init setup secret-key run test-unit test-integration test-functional test-all lint migrate migrate-down revision up up-database up-app down down-v down-app down-database logs logs-database shell shell-database ps restart restart-database migrate-docker prune prune-all remove-app remove-database quickstart

# ── Variables ─────────────────────────────────────────────────────────────────

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PYTEST := $(VENV)/bin/pytest
PYLINT := $(VENV)/bin/pylint
ALEMBIC := $(VENV)/bin/alembic

# Colors
RED    := \033[0;31m
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
CYAN   := \033[0;36m
BOLD   := \033[1m
NC     := \033[0m

.DEFAULT_GOAL := help

# ── Help ──────────────────────────────────────────────────────────────────────

help:
	@echo -e "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo -e "$(BLUE)  OrderFlow - Available Commands$(NC)"
	@echo -e "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo -e "$(GREEN)Setup:$(NC)"
	@echo "  make init                - Copy .env.example to .env"
	@echo "  make setup               - Create virtualenv and install dependencies"
	@echo "  make secret-key          - Generate a secure SECRET_KEY"
	@echo "  make quickstart          - Complete first-time setup"
	@echo ""
	@echo -e "$(GREEN)Development:$(NC)"
	@echo "  make run                 - Start the server in development mode"
	@echo ""
	@echo -e "$(GREEN)Tests:$(NC)"
	@echo "  make test-unit           - Run unit tests"
	@echo "  make test-integration    - Run integration tests"
	@echo "  make test-functional     - Run functional tests"
	@echo "  make test-all            - Run all tests with coverage report"
	@echo ""
	@echo -e "$(GREEN)Quality:$(NC)"
	@echo "  make lint                - Run pylint on the source code"
	@echo ""
	@echo -e "$(GREEN)Migrations:$(NC)"
	@echo "  make migrate             - Apply all pending migrations"
	@echo "  make migrate-down        - Revert the last migration"
	@echo "  make revision msg=''     - Create a new migration"
	@echo "  make migrate-docker      - Run migrations inside the app container"
	@echo ""
	@echo -e "$(GREEN)Docker - Full Stack:$(NC)"
	@echo "  make up                  - Start all containers"
	@echo "  make down                - Stop and remove all containers"
	@echo "  make down-v              - Stop and remove all containers and volumes"
	@echo "  make ps                  - Show status of all containers"
	@echo "  make prune               - Remove stopped containers and unused images"
	@echo "  make prune-all           - Remove all containers, volumes and images"
	@echo ""
	@echo -e "$(GREEN)Docker - Application:$(NC)"
	@echo "  make up-app              - Start only the app container"
	@echo "  make down-app            - Stop only the app container"
	@echo "  make restart             - Restart the app container"
	@echo "  make logs                - Show logs of the app container"
	@echo "  make shell               - Open a shell in the app container"
	@echo "  make remove-app          - Remove the app container and its image"
	@echo ""
	@echo -e "$(GREEN)Docker - Database:$(NC)"
	@echo "  make up-database         - Start only the database container"
	@echo "  make down-database       - Stop only the database container"
	@echo "  make restart-database    - Restart the database container"
	@echo "  make logs-database       - Show logs of the database container"
	@echo "  make shell-database      - Open a psql shell in the database container"
	@echo "  make remove-database     - Remove the database container and its volume"
	@echo ""
	@echo -e "$(BLUE)═══════════════════════════════════════════════════════$(NC)"

# ── Environment ───────────────────────────────────────────────────────────────

init:
	@echo -e "$(YELLOW)Initializing project...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo -e "$(GREEN)✓ .env created successfully!$(NC)"; \
	else \
		echo -e "$(YELLOW)⚠ .env already exists, skipping...$(NC)"; \
	fi

setup:
	@echo -e "$(YELLOW)Setting up project...$(NC)"
	@echo -e "$(BLUE)→ Creating virtualenv...$(NC)"
	@python3 -m venv $(VENV)
	@echo -e "$(BLUE)→ Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo -e "$(GREEN)✓ Setup complete! Run 'make run' to start the application.$(NC)"

secret-key:
	@echo -e "$(YELLOW)Generating SECRET_KEY...$(NC)"
	@echo -e "$(GREEN)✓ $(NC)$$(openssl rand -hex 32)"

quickstart: init setup
	@echo ""
	@echo -e "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo -e "$(GREEN)  ✓ Project setup complete!$(NC)"
	@echo -e "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo -e "$(BLUE)Next steps:$(NC)"
	@echo "  1. Review and update your .env file"
	@echo "  2. Run 'make migrate' to apply migrations"
	@echo "  3. Run 'make run' to start the application"
	@echo "  4. Access http://localhost:8000/docs"
	@echo ""

# ── Dev ───────────────────────────────────────────────────────────────────────

run:
	@echo -e "$(YELLOW)Starting server in development mode...$(NC)"
	@ENV=development $(UVICORN) src.main:app --host 0.0.0.0 --port 8000 --reload

# ── Tests ─────────────────────────────────────────────────────────────────────

test-unit:
	@echo -e "$(YELLOW)Running unit tests...$(NC)"
	@$(PYTEST) src/tests/unit_tests/ -v --tb=short
	@echo -e "$(GREEN)✓ Unit tests passed!$(NC)"

test-integration:
	@echo -e "$(YELLOW)Running integration tests...$(NC)"
	@$(PYTEST) src/tests/integration_tests/ -v --tb=short
	@echo -e "$(GREEN)✓ Integration tests passed!$(NC)"

test-functional:
	@echo -e "$(YELLOW)Running functional tests...$(NC)"
	@$(PYTEST) src/tests/functional_tests/ -v --tb=short
	@echo -e "$(GREEN)✓ Functional tests passed!$(NC)"

test-all:
	@echo -e "$(YELLOW)Running all tests with coverage...$(NC)"
	@$(PYTEST) --tb=short --cov=src --cov-report=term-missing --cov-report=html
	@echo -e "$(GREEN)✓ All tests passed!$(NC)"

# ── Quality ───────────────────────────────────────────────────────────────────

lint:
	@echo -e "$(YELLOW)Running pylint...$(NC)"
	@$(PYLINT) src/
	@echo -e "$(GREEN)✓ Linter checks passed!$(NC)"

# ── Migrations ────────────────────────────────────────────────────────────────

migrate:
	@echo -e "$(YELLOW)Applying all pending migrations...$(NC)"
	@$(ALEMBIC) upgrade head
	@echo -e "$(GREEN)✓ Migrations applied!$(NC)"

migrate-down:
	@echo -e "$(YELLOW)Reverting last migration...$(NC)"
	@$(ALEMBIC) downgrade -1
	@echo -e "$(GREEN)✓ Migration reverted!$(NC)"

revision:
	@echo -e "$(YELLOW)Creating new migration...$(NC)"
	@$(ALEMBIC) revision --autogenerate -m "$(msg)"
	@echo -e "$(GREEN)✓ Migration created!$(NC)"

migrate-docker:
	@echo -e "$(YELLOW)Running migrations inside app container...$(NC)"
	@docker compose exec app $(ALEMBIC) upgrade head
	@echo -e "$(GREEN)✓ Migrations applied!$(NC)"

# ── Docker: Full Stack ────────────────────────────────────────────────────────

up:
	@echo -e "$(YELLOW)Starting all containers...$(NC)"
	@docker compose up -d --build
	@echo -e "$(GREEN)✓ All containers started!$(NC)"
	@echo -e "$(BLUE)→ Application: http://localhost:8000$(NC)"
	@echo -e "$(BLUE)→ Docs: http://localhost:8000/docs$(NC)"

down:
	@echo -e "$(YELLOW)Stopping all containers...$(NC)"
	@docker compose down
	@echo -e "$(GREEN)✓ All containers stopped!$(NC)"

down-v:
	@echo -e "$(YELLOW)Stopping all containers and removing volumes...$(NC)"
	@docker compose down -v
	@echo -e "$(GREEN)✓ All containers and volumes removed!$(NC)"

ps:
	@echo -e "$(BLUE)Running containers:$(NC)"
	@docker compose ps

prune:
	@echo -e "$(YELLOW)Removing stopped containers and unused images...$(NC)"
	@docker system prune -f
	@echo -e "$(GREEN)✓ Cleanup complete!$(NC)"

prune-all:
	@echo -e "$(RED)⚠ This will remove ALL containers, volumes and images!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker system prune -af --volumes; \
		echo -e "$(GREEN)✓ Full cleanup complete!$(NC)"; \
	else \
		echo -e "$(YELLOW)Cancelled.$(NC)"; \
	fi

# ── Docker: Application ───────────────────────────────────────────────────────

up-app:
	@echo -e "$(YELLOW)Starting app container...$(NC)"
	@docker compose up -d app
	@echo -e "$(GREEN)✓ App container started!$(NC)"
	@echo -e "$(BLUE)→ Application: http://localhost:8000$(NC)"

down-app:
	@echo -e "$(YELLOW)Stopping app container...$(NC)"
	@docker compose stop app
	@echo -e "$(GREEN)✓ App container stopped!$(NC)"

restart:
	@echo -e "$(YELLOW)Restarting app container...$(NC)"
	@docker compose restart app
	@echo -e "$(GREEN)✓ App container restarted!$(NC)"

logs:
	@echo -e "$(BLUE)Showing app logs (Ctrl+C to exit)...$(NC)"
	@docker compose logs -f app

shell:
	@echo -e "$(BLUE)Opening shell in app container...$(NC)"
	@docker compose exec app sh

remove-app:
	@echo -e "$(YELLOW)Removing app container and image...$(NC)"
	@docker compose rm -f app
	@docker rmi $$(docker images -q orderflow_app) 2>/dev/null || true
	@echo -e "$(GREEN)✓ App container and image removed!$(NC)"

# ── Docker: Database ──────────────────────────────────────────────────────────

up-database:
	@echo -e "$(YELLOW)Starting database container...$(NC)"
	@docker compose up -d database
	@echo -e "$(GREEN)✓ Database container started!$(NC)"

down-database:
	@echo -e "$(YELLOW)Stopping database container...$(NC)"
	@docker compose stop database
	@echo -e "$(GREEN)✓ Database container stopped!$(NC)"

restart-database:
	@echo -e "$(YELLOW)Restarting database container...$(NC)"
	@docker compose restart database
	@echo -e "$(GREEN)✓ Database container restarted!$(NC)"

logs-database:
	@echo -e "$(BLUE)Showing database logs (Ctrl+C to exit)...$(NC)"
	@docker compose logs -f database

shell-database:
	@echo -e "$(BLUE)Opening psql shell in database container...$(NC)"
	@docker compose exec database psql -U $${DB_USER} -d $${DB_NAME}

remove-database:
	@echo -e "$(RED)⚠ This will delete ALL database data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose rm -f database; \
		docker volume rm $$(docker volume ls -q | grep postgres_data) 2>/dev/null || true; \
		echo -e "$(GREEN)✓ Database container and volume removed!$(NC)"; \
	else \
		echo -e "$(YELLOW)Cancelled.$(NC)"; \
	fi