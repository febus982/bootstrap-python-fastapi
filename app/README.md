# Application structure

This application is structured following the principles of Clean Architecture.
Higher level layers can import directly lower level layers. An inversion of control
pattern has to be used for lower level layers to use higher level ones.

## Modules layers

Layers are ordered from the highest level to the lowest one.

------

* routes
* storage (database, repositories(repo_interface))

------

* services (service_class, repo_interface)

------

* models

------

* deps (3rd party dependencies like SQLAlchemy manager)

------