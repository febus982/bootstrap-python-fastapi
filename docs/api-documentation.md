# API Documentation

API documentation is rendered by [FastAPI](https://fastapi.tiangolo.com/features/)
on `/docs` and `/redoc` paths using OpenAPI format.

## API versioning

Versioning an API at resource level provides a much more
flexible approach than versioning the whole API.

The example `books` domain provides 2 endpoints to demonstrate this approach

* `/api/books/v1` (POST)
* `/api/books/v2` (POST)

/// note | Media type versioning

An improvement could be moving to [media type versioning](https://opensource.zalando.com/restful-api-guidelines/#114)
///
