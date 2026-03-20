.PHONY: help setup run test test-integration test-all lint up down down-v logs shell db-reset

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PYTEST := $(VENV)/bin/pytest
PYLINT := $(VENV)/bin/pylint

help: ## Shows this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Environment ──────────────────────────────────────────────────────────────────

setup: ## Creates virtualenv and installs dependencies
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ── Dev ───────────────────────────────────────────────────────────────────────

run: ## Starts the server in development mode (reload)
	ENV=development $(UVICORN) src.main:app --host 0.0.0.0 --port 8000 --reload

# ── Tests ──────────────────────────────────────────────────────────────────────

test-unit: ## Runs the unit tests
	$(PYTEST) src/tests/unit_tests/ -v --tb=short

test-integration: ## Runs the integration tests
	$(PYTEST) src/tests/integration_tests/ -v --tb=short

test-functional: ## Runs the functional tests
	$(PYTEST) src/tests/functional_tests/ -v --tb=short

test-all: ## Runs all tests with coverage report
	$(PYTEST) --tb=short --cov=src --cov-report=term-missing --cov-report=html

# ── Quality ─────────────────────────────────────────────────────────────────

lint: ## Runs pylint on the source code
	$(PYLINT) src/

# ── Docker ────────────────────────────────────────────────────────────────────

up: ## Starts the containers in the background
	docker compose up -d --build

down: ## Stops and removes the containers
	docker compose down

down-v: ## Stops and removes the containers and volumes
	docker compose down -v

logs: ## Shows the logs of the app container
	docker compose logs -f app

shell: ## Opens a shell in the app container
	docker compose exec app sh

# ── Database ─────────────────────────────────────────────────────────────────

db-reset: ## Truncates all tables and resets ID sequences (local dev only)
	PGPASSWORD=$(shell grep DB_PASSWORD .env | cut -d= -f2 | tr -d "'") \
	psql -h localhost -U $(shell grep DB_USERNAME .env | cut -d= -f2 | tr -d "'") -d delivery_db -c \
	"TRUNCATE TABLE reviews, order_items, orders, addresses, products, categories, accounts, users RESTART IDENTITY CASCADE;"
	@echo "Database reset — all tables truncated and sequences restarted."
