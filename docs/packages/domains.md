# Domains

The `domains` package contains all the application domain logic separated by domains
(this template provides a single domain: `books`).

Each domain should be self-contained and not invoke logic from other domains directly.
Same as we do for gateways, or 3rd party providers, other domains should be accessed
through the use of **interfaces**.

Using interfaces will:

* Make sure domains do not depend on each other
* Make easier to replace the concrete implementation with a HTTP adapter when the domain
  is extracted in a microservice

## Book domain structure

The `domains.book` package provides an example implementation for a domain. It contains
a list of public and protected modules.

Public package and modules are used by the application to invoke the
domain functionalities:

* The main `domains.book` package provides the entrypoint for our application:
  the `BookService` class. We export it here from the `domains.book._service`
  module to hide protected entities that should not be accessed directly.
* The `domains.book.interfaces` provides the `BookServiceInterface` protocol
  to be used for Inversion of Control (we don't currently use it in this
  application because Clean Architecture doesn't enforce Inversion of Control
  from the `http` application, and we don't have yet implemented other domains)
* The `domains.book.dto` provides the data transfer objects required to invoke
  the `BookService` class.
* The `domains.book.events` provides the event data structures that the domain
  is able to emit. They can be used by other domains to implement event handlers.

Protected package and modules are used by the implementation of the books domain
and can be used to bootstrap the application:

* The `domains.book._gateway_interfaces` contains the gateway protocols against
  which the domain logic is implemented. We use them to configure the dependency
  injection container.
* The `domains.book._models` contains the domain models. We use them also
  to bootstrap the SQLAlchemy imperative mapping in `bootstrap.storage.SQLAlchemy`
  package.
* The `domains.book._service` contains the `BookService` implementation.
* The `domains.book._tasks` contains the implementation of celery tasks
  for operations that can be queued without waiting for a result (e.g.
  send an email, invalidate cache).
