# Bootstrap FastAPI service
<a href="https://codeclimate.com/github/febus982/bootstrap-python-fastapi/maintainability"><img src="https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/maintainability" /></a>
<a href="https://codeclimate.com/github/febus982/bootstrap-python-fastapi/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a2ab183e64778e21ae14/test_coverage" /></a>

This is an example implementation of a API service applying
concepts from [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
and [SOLID principles](https://en.wikipedia.org/wiki/SOLID).

* The book domain is isolated behind an interface class, enforcing the [Interface Segregation principle](https://en.wikipedia.org/wiki/Interface_segregation_principle) 
  and the [Inversion of Control principle](https://en.wikipedia.org/wiki/Inversion_of_control)
* The same principles are used for the BookRepository class

In this way our components are loosely coupled and the application logic
(the domains package) is completely independent of from the chosen framework
and the persistence layer.

## Class dependency schema

![](architecture.png)

## How to run

Build docker containers

```bash
make build
```

Run dev application with hot reload

```bash
make dev
```

Run test suite with coverage

```bash
make test
```
