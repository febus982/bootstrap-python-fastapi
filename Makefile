.PHONY: docs docs-build adr

containers:
	docker compose build --build-arg UID=`id -u`

dev-http:
	docker compose up dev-http

dev-socketio:
	docker compose up dev-socketio

migrate:
	docker compose run --rm migrate

autogenerate-migration:
	docker compose run --rm autogenerate-migration

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

docs-build:
	uv run mkdocs build
