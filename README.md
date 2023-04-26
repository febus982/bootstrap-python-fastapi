# Bootstrap python service
[![Python 3.9](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.9.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.9.yml)
[![Python 3.10](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.10.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.10.yml)
[![Python 3.11](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.11.yml/badge.svg?event=push)](https://github.com/febus982/bootstrap-python-fastapi/actions/workflows/python-3.11.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/maintainability)](https://codeclimate.com/github/febus982/bootstrap-python-fastapi/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/test_coverage)](https://codeclimate.com/github/febus982/bootstrap-python-fastapi/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

This is an example implementation of microservice applying
concepts from [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
and [SOLID principles](https://en.wikipedia.org/wiki/SOLID).

* The books domain is isolated behind an interface class, enforcing the [Interface Segregation principle](https://en.wikipedia.org/wiki/Interface_segregation_principle) 
  and the [Inversion of Control](https://en.wikipedia.org/wiki/Inversion_of_control) design pattern
* The same principles are used for the BookRepository class
* The application frameworks are decoupled from the domain logic
* The storage layer is decoupled from the domain logic

In this way our components are loosely coupled and the application logic
(the domains package) is completely independent of from the chosen framework
and the persistence layer.

## HTTP API Docs

This application uses [fastapi-versionizer](https://github.com/alexschimpf/fastapi-versionizer)
to provide easy API schema version management.

There are 3 different API documentation paths:

* `/api/v1/docs` and `/api/v1/redoc`: v1 OpenAPI schema
* `/api/v2/docs` and `/api/v2/redoc`: v2 OpenAPI schema
* `/docs` : non-versioned routes OpenAPI schema (e.g. health check endpoint)

## Package layers

This application is structured following the principles of Clean Architecture.
Higher level layers can import directly lower level layers. An inversion of control
pattern has to be used for lower level layers to use higher level ones.

Packages are ordered from the highest level to the lowest one.

------

* `http_app` (http presentation layer)
* `grpc_app` (grpc presentation layer)
* `storage` (database connection manager, repository implementation)

------

* `domains` (services, repository interfaces)

------

## Class dependency schema

![](architecture.png)

## How to run

Using Docker:

* `docker compose build`: Build containers
* `docker compose run --rm dev make migrate`: Run database migrations
* `docker compose up dev`: Run HTTP application with hot reload
* `docker compose up grpc`: Run GRPC application with hot reload
* `docker compose run --rm test`: Run test suite

Locally:

* `make migrate`: Run database migrations
* `make dev`: Run HTTP application with hot reload
* `make grpc`: Run GRPC application with hot reload
* `make test`: Run test suite
