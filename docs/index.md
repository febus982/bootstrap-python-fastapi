# Bootstrap python service
[![CI Pipeline](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/ci-pipeline.yml)
[![Python tests](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-tests.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/test_coverage)](https://codeclimate.com/github/febus982/bootstrap-python-fastapi/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/maintainability)](https://codeclimate.com/github/febus982/bootstrap-python-fastapi/maintainability)

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

This is an example implementation of a python application applying
concepts from [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
and [SOLID principles](https://en.wikipedia.org/wiki/SOLID).

* The repository classes are isolated behind interfaces, enforcing the [Interface Segregation principle](https://en.wikipedia.org/wiki/Interface_segregation_principle) 
  and the [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control) design pattern
* The application frameworks are decoupled from the domain logic
* The storage layer is decoupled from the domain logic

This template provides out of the box some commonly used functionalities:

* API Documentation using [FastAPI](https://fastapi.tiangolo.com/)
* Async tasks execution using [Celery](https://docs.celeryq.dev/en/stable/index.html)
* Repository pattern for databases using [SQLAlchemy](https://www.sqlalchemy.org/) and [SQLAlchemy bind manager](https://febus982.github.io/sqlalchemy-bind-manager/stable/)
* Database migrations using [Alembic](https://alembic.sqlalchemy.org/en/latest/) (configured supporting both sync and async SQLAlchemy engines)
* [TODO] Producer and consumer to emit and consume events using [CloudEvents](https://cloudevents.io/) format on [Confluent Kafka](https://docs.confluent.io/kafka-clients/python/current/overview.html)

## Documentation

The detailed documentation is available:

* Online on [GitHub pages](https://febus982.github.io/bootstrap-python-fastapi/)
* Offline by running `make docs` after installing dependencies with `make dev-dependencies`

## How to use

Create your GitHub repository using this template (The big green `Use this template` button).
Optionally tweak name and authors in the `pyproject.toml` file, however the metadata
are not used when building the application, nor are referenced anywhere in the code.

Locally:

* `make migrate`: Run database migrations
* `make install-dependencies`: Install runtime requirements
* `make dev-dependencies`: Install development requirements
* `make update-dependencies`: Updates requirements
* `make migrate`: Run database migrations
* `make dev`: Run HTTP application with hot reload
* `make test`: Run test suite

Using Docker:

* `make containers`: Build containers
* `docker compose run --rm dev make migrate`: Run database migrations
* `docker compose up dev`: Run HTTP application with hot reload
* `docker compose up celery-worker`: Run the celery worker
* `docker compose run --rm test`: Run test suite

## Other commands for development

* `make check`: Run tests, code style and lint checks
* `make fix`: Run tests, code style and lint checks with automatic fixes (where possible)
