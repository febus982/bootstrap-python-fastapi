# Bootstrap FastAPI service
[![Python 3.8](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.8.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.8.yml)
[![Python 3.9](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.9.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.9.yml)
[![Python 3.10](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.10.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.10.yml)
[![Python 3.11](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.11.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.11.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/maintainability)](https://codeclimate.com/github/febus982/bootstrap-python-fastapi/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/test_coverage)](https://codeclimate.com/github/febus982/bootstrap-python-fastapi/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is an example implementation of a API service applying
concepts from [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
and [SOLID principles](https://en.wikipedia.org/wiki/SOLID).

* The book domain is isolated behind an interface class, enforcing the [Interface Segregation principle](https://en.wikipedia.org/wiki/Interface_segregation_principle) 
  and the [Inversion of Control principle](https://en.wikipedia.org/wiki/Inversion_of_control)
* The same principles are used for the BookRepository class

In this way our components are loosely coupled and the application logic
(the domains package) is completely independent of from the chosen framework
and the persistence layer.

## API Docs

This application uses [fastapi-versionizer](https://github.com/alexschimpf/fastapi-versionizer)
to provide easy API schema version management.

There are 3 different API documentation paths:

* `/api/v1/docs` and `/api/v1/redoc`: v1 OpenAPI schema
* `/api/v2/docs` and `/api/v2/redoc`: v2 OpenAPI schema
* `/docs` : non-versioned routes OpenAPI schema (e.g. health check endpoint)

## Class dependency schema

![](architecture.png)

## How to run

Build docker containers

```bash
make build
```

Run database migrations

```bash
make migrate
```

Run dev application with hot reload

```bash
make dev
```

Run test suite with coverage

```bash
make test
```
