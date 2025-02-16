.PHONY: docs docs-build adr

containers:
	docker compose build --build-arg UID=`id -u`

dev-http:
	uv run ./src/http_app/dev_server.py

dev-socketio:
	uv run ./src/socketio_app/dev_server.py

run:
	uv run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

test:
	uv run pytest -n auto --cov

ci-test:
	uv run pytest -n 0

ci-coverage:
	uv run pytest -n 0 --cov --cov-report lcov

typing:
	uv run mypy

install-dependencies:
	uv sync --all-groups --no-dev --no-install-project --frozen

dev-dependencies:
	uv sync --all-groups --frozen

update-dependencies:
	uv lock --upgrade
	uv sync --all-groups --frozen

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
