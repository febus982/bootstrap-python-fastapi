.PHONY: docs docs-build adr

containers:
	# Use local UID to avoid files permission issues when mounting directories
	# We could do this at runtime, by specifying the user, but it's easier doing it
	# at build time, so no special commands will be necessary at runtime
	docker compose build --build-arg UID=`id -u` dev
	# To build shared container layers only once we build a single container before the other ones
	docker compose build --build-arg UID=`id -u`

dev:
	uv run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory --reload

otel:
	OTEL_SERVICE_NAME=bootstrap-fastapi OTEL_TRACES_EXPORTER=none OTEL_METRICS_EXPORTER=none OTEL_LOGS_EXPORTER=none uv run opentelemetry-instrument uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

run:
	uv run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

test:
	uv run pytest -n auto --cov

ci-test:
	uv run pytest

ci-coverage:
	uv run pytest --cov --cov-report lcov

typing:
	uv run mypy

install-dependencies:
	uv sync --all-groups --no-dev --no-install-project

dev-dependencies:
	uv sync --all-groups

update-dependencies:
	uv lock --upgrade

migrate:
	uv run alembic upgrade heads

format:
	uv run ruff format --check .

lint:
	uv run ruff check .

fix:
	uv run ruff format .
	uv run ruff check . --fix
	uv run ruff format .

check: lint format typing test

docs:
	uv run mkdocs serve

adr:
	adr-viewer --serve --adr-path docs/adr

docs-build:
	uv run mkdocs build
