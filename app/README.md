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
* `domains.books._local` contains the concrete implementation

In the example `domains.books._local` imports `domains.books`,
never the opposite, applying in this way the Interface
Segregation Principle.

The wiring between the boundary interfaces and concrete classes
is taken care by the DI container. Code needing the service
need only declare the interface class from `domains.books` as
a parameter in a function and the DI container will take care of
passing the concrete class.

## Alternate approaches to Interface Segregation

The application uses an IoC container, however it is possible to 
achieve interface segregation without using a Dependency Injection
container.

These are some examples (note the local imports to avoid exposing the
imported classes).

Using a decorator to be applied to function:

```python
def inject_book_repository(f):
    """
    Decorator implementation for DI injection
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        if "book_repository" not in kwds.keys():
            from app.storage.repositories.book_repository import BookRepository
            kwds["book_repository"] = BookRepository()  # Here we might have to pass the SQLAlchemy manager
        elif not isinstance(kwds["book_repository"], BookRepositoryInterface):
            import warnings
            warnings.warn(
                f"The specified object ({type(kwds['book_repository'])})"
                f" is not an instance of BookRepositoryInterface"
            )
        return f(*args, **kwds)

    return wrapper
```

Using a factory class:

```python
def book_repository_factory(sa_manager: SQLAlchemyBindManager) -> BookRepositoryInterface:
    """Factory for Book Repository instantiation.

    Args:
        sa_manager: a SQLAlchemyBindManager instance

    Returns:
        The book repository.
    """
    from app.storage.repositories.book_repository import BookRepository
    return BookRepository(sa_manager=sa_manager)
```
