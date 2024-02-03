.PHONY: docs docs-build adr

containers:
	# Use local UID to avoid files permission issues when mounting directories
	# We could do this at runtime, by specifying the user, but it's easier doing it
	# at build time, so no special commands will be necessary at runtime
	docker compose build --build-arg UID=`id -u` dev
	# To build shared container layers only once we build a single container before the other ones
	docker compose build --build-arg UID=`id -u`

dev:
	poetry run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory --reload

otel:
	OTEL_SERVICE_NAME=bootstrap-fastapi OTEL_TRACES_EXPORTER=none OTEL_METRICS_EXPORTER=none OTEL_LOGS_EXPORTER=none poetry run opentelemetry-instrument uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

run:
	poetry run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

test:
	poetry run pytest -n auto --cov

ci-test:
	poetry run pytest

ci-coverage:
	poetry run pytest --cov --cov-report lcov

typing:
	poetry run mypy

install-dependencies:
	poetry install --no-root --with http

dev-dependencies:
	poetry install --with http,dev

update-dependencies:
	poetry update --with http,dev

migrate:
	poetry run alembic upgrade heads

format:
	poetry run ruff format --check .

lint:
	poetry run ruff .

fix:
	poetry run ruff . --fix
	poetry run ruff format .

check: lint format typing test

docs:
	poetry run mkdocs serve

adr:
	adr-viewer --serve --adr-path docs/adr

docs-build:
	poetry run mkdocs build
