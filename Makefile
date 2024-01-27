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

grpc:
	poetry run python3 -m grpc_app

test:
	poetry run pytest -n auto --cov

ci-test:
	poetry run pytest

ci-coverage:
	poetry run pytest --cov --cov-report lcov

typing:
	poetry run mypy

install-dependencies:
	poetry install --no-root --with http,grpc

dev-dependencies:
	poetry install --no-root --with http,grpc,dev

update-dependencies:
	poetry update --with http,grpc,dev

migrate:
	poetry run alembic upgrade heads

format:
	poetry run black --check .

format-fix:
	poetry run black .

lint:
	poetry run ruff .

lint-fix:
	poetry run ruff . --fix

bandit:
	poetry run bandit -c .bandit.yml -r .

# There are issues on how python imports are generated when using nested
# packages. The following setup appears to work, however it might need
# to be reviewed. https://github.com/protocolbuffers/protobuf/issues/1491
generate-proto:
	rm -rf ./grpc_app/generated/*.p*
	touch ./grpc_app/generated/__init__.py
	poetry run python -m grpc_tools.protoc \
	-I grpc_app.generated=./grpc_app/proto/ \
	--python_out=. \
	--mypy_out=. \
	grpc_app/proto/*.proto
	poetry run python -m grpc_tools.protoc \
	-I grpc_app/generated=./grpc_app/proto/ \
	--grpc_python_out=. \
	grpc_app/proto/*.proto
	git add ./grpc_app/generated

fix:  format-fix lint-fix
check: format lint typing bandit test

docs:
	poetry run mkdocs serve

adr:
	adr-viewer --serve --adr-path docs/adr

docs-build:
	poetry run mkdocs build
