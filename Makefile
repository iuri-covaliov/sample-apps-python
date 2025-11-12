# Makefile for Python projects using 'uv' for dependency management
# Adjust the parameters below to fit your project.

# ---------- Environment ----------
# include .env 				# uncomment if the file present

# ---------- Project parameters ----------
# Here you can set app-specific parameters, e.g.:
# APP_MODULE					:= app.main:api
# HOST                := 0.0.0.0
# PORT                := $(or $(APP_PORT),8000)

# Tools
UV                  := uv
RUN                 := $(UV) run          # <— use the project's venv

# ---------- Housekeeping ----------
.PHONY: help

SHELL := bash

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "• \033[36m%-18s\033[0m %s\n", $$1, $$2}'

env: ## Create .env from .env.example if missing
	@if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); echo "Created $(ENV_FILE)"; else echo "$(ENV_FILE) already exists"; fi

check: ## Quick sanity checks
	@command -v $(UV) >/dev/null || { echo "Missing 'uv'"; exit 1; }
	@command -v $(PYTEST) >/dev/null || { echo "Missing 'pytest'"; exit 1; }
	@echo "Tools OK."


# ---------- Dependencies ----------
deps: ## Install Python deps into local venv using uv
	@$(UV) sync

deps-lock: ## Export pinned requirements for Docker/CI
	$(UV) export --format requirements-txt --no-hashes > requirements.lock
	@echo "Wrote requirements.lock"


# ---------- Code quality ----------
fmt: ## Auto-format with ruff
	@$(RUN) ruff format

fmt-check: ## Check code style with ruff
	@$(RUN) ruff format --check

lint: ## Lint with ruff
	@$(RUN) ruff check

type: ## Static type-check of the whole project with mypy
	@$(RUN) mypy .

type-app: ## Static type-check of the app code with mypy
	@$(RUN) mypy app

test: ## Run unit tests
	@$(RUN) pytest -v

coverage: ## Tests + HTML coverage
	@$(RUN) coverage run -m pytest
	@$(RUN) coverage report -m
	@$(RUN) coverage html
	@echo "Open htmlcov/index.html"

.PHONY: ci
ci: ## Run the same steps CI does (lint, typecheck, tests with coverage)
	@$(RUN) ruff check .
	@$(RUN) ruff format --check .
	@$(RUN) mypy .
	@$(RUN) coverage run -m pytest
	@$(RUN) coverage report -m

# ---------- Run (local code) ----------
# Define run command for your app in the Makefile here
run: ## Run the app
	@$(RUN) app.main
# 	@$(RUN) <command to run the app>
