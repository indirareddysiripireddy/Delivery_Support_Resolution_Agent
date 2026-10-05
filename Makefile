.PHONY: install test lint api infra-up infra-down

install:
	pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check backend ai tests

api:
	uvicorn backend.app.main:app --reload

infra-up:
	docker compose up -d

infra-down:
	docker compose down