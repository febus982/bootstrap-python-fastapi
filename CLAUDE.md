# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

**Package Management (uv):**
- `make dev-dependencies` - Install all dependencies including dev
- `make install-dependencies` - Install production dependencies only
- `make update-dependencies` - Update and sync dependencies

**Running Applications:**
- `make dev-http` - Run HTTP application with hot reload (Docker)
- `make dev-socketio` - Run Socket.io application with hot reload (Docker)
- `docker compose up dramatiq-worker` - Run Dramatiq worker

**Testing:**
- `make test` - Run full test suite with coverage (parallel execution)
- `uv run pytest tests/path/to/test_file.py` - Run a single test file
- `uv run pytest tests/path/to/test_file.py::test_function` - Run a specific test
- `uv run pytest -k "pattern"` - Run tests matching pattern

**Code Quality:**
- `make check` - Run all checks (lint, format, typing, test)
- `make fix` - Auto-fix linting and formatting issues
- `make typing` - Run mypy type checking
- `make lint` - Run ruff linter
- `make format` - Check code formatting

**Database:**
- `make migrate` - Run database migrations
- `make autogenerate-migration` - Generate new migration file

**Documentation:**
- `make docs` - Serve documentation locally

## Architecture Overview

This is a Clean Architecture Python application with multiple entry points (HTTP/FastAPI, WebSocket/Socket.io, async tasks/Dramatiq).

### Layer Structure (`src/`)

```
domains/       → Business logic (services, models, DTOs, events)
gateways/      → External system interfaces (event gateways)
http_app/      → FastAPI application and routes
socketio_app/  → Socket.io application and namespaces
dramatiq_worker/ → Async task worker
common/        → Shared infrastructure (config, DI, storage, telemetry)
migrations/    → Alembic database migrations
```

### Dependency Injection Pattern

Uses `dependency-injector` library. Interface mappings are defined in `src/common/di_container.py`:

```python
# Container maps interfaces to implementations
BookRepositoryInterface: Factory[BookRepositoryInterface] = Factory(
    SQLAlchemyAsyncRepository,
    bind=SQLAlchemyBindManager.provided.get_bind.call(),
    model_class=BookModel,
)
```

Services use `@inject` decorator with `Provide[]`:

```python
@inject
def __init__(
    self,
    book_repository: BookRepositoryInterface = Provide[BookRepositoryInterface.__name__],
)
```

### Application Bootstrap

All applications share common initialization via `application_init()` in `src/common/bootstrap.py`:
- Configures DI container
- Initializes logging (structlog)
- Sets up SQLAlchemy storage
- Configures Dramatiq
- Instruments OpenTelemetry

### Domain Structure (example: `domains/books/`)

- `_models.py` - SQLAlchemy models (imperative mapping)
- `_service.py` - Business logic services
- `_gateway_interfaces.py` - Repository/gateway protocols
- `_tasks.py` - Dramatiq async tasks
- `dto.py` - Pydantic DTOs for API layer
- `events.py` - CloudEvents definitions
- `interfaces.py` - Public domain interfaces

### Testing

Tests mirror source structure in `src/tests/`. Key patterns:
- Integration tests use `TestClient` with in-memory SQLite
- Unit tests mock dependencies via `AsyncMock`/`MagicMock`
- 100% coverage required (`fail_under = 100` in pyproject.toml)
- Storage tests in `tests/storage/` use isolated database fixtures

### Configuration

Environment-based configuration via Pydantic Settings in `src/common/config.py`. Nested configs use `__` delimiter (e.g., `DRAMATIQ__BROKER_URL`).
