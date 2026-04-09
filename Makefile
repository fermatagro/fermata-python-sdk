.PHONY: generate test lint fmt install

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
	python3 -m venv .venv
	$(VENV)/pip install -e ".[dev]"
