# Domains

The `domains` module contains all the application domain logic separated by domains
(this template provides a single domain: `books`).

Each domain should be self-contained and not invoke logic from other domains directly.
Same as we do for gateways, or 3rd party providers, other domains should be accessed
through the use of **interfaces**.

Using interfaces will:

* Make sure domains do not depend on each other
* Make easier to replace the concrete implementation with a HTTP adapter when the domain
  is extracted in a microservice

## Book domain structure

[TODO] Refactor needed to implement a better structure to the domain
