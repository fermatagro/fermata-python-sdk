.PHONY: generate test lint fmt install run

PYTHON := $(shell command -v python3)
VENV := .venv/bin

generate:
	bash scripts/generate.sh

test:
	$(VENV)/pytest

lint:
	$(VENV)/ruff check src/ tests/
	$(VENV)/mypy src/fermata/ --exclude src/fermata/_generated

fmt:
	$(VENV)/ruff format src/ tests/
	$(VENV)/ruff check --fix src/ tests/

install:
	$(PYTHON) -m venv .venv
	$(VENV)/pip install --upgrade pip
	$(VENV)/pip install -e ".[dev]"

run:
	env $$(cat .env | xargs) $(VENV)/python test.py
