# Bootstrap FastAPI service

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