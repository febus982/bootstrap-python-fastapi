# Application structure

This application is structured following the principles of Clean Architecture.
Higher level layers can import directly lower level layers. An inversion of control
pattern has to be used for lower level layers to use higher level ones.

## Packager layers

Packages are ordered from the highest level to the lowest one.

------

* routes
* storage (database connection manager, repository implementation)

------

* domains (services, repository interfaces)

------

## Domain subpackages

Each subpackage in `domains` exposes only interface classes and the
relevant Data transfer objects. The concrete implementation for the
interfaces is in the nested modules. E.g.:

* `domains.books` contains the boundary interfaces
* `domains.books.local` contains the concrete implementation

In the example `domains.books.local` imports `domains.books`,
never the opposite, applying in this way the Interface
Segregation Principle.

The wiring between the boundary interfaces and concrete classes
is taken care by the IoC container. Code needing the service
need only declare the interface class from `domains.books` as
a parameter in a function and  DI container will take care of
passing the concrete class.
