# Domain subpackages

Each subpackage in `domains` exposes only interface classes and the
relevant Data transfer objects. The domain logic implementation is
in the nested modules but should not be directly accessed. E.g.:

* `domains.books` contains the boundary interfaces
* other nested modules like `domains.books._dto` contains the concrete implementation

## Alternate approaches to Interface Segregation

The domain logic uses an IoC container to access the storage implementation,
however it is possible to achieve interface segregation without
using a Dependency Injection container.

These are some examples (note the local imports to avoid exposing the
imported classes).

Using a decorator to be applied to function:

```python
def inject_book_repository(f):
    """
    Decorator implementation for Dependency Injection
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        if "book_repository" not in kwds.keys():
            from gateways.storage import BookRepository
            kwds[
                "book_repository"] = BookRepository()  # Here we'll have to pass any required dependency for the repository
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
    from gateways.storage import BookRepository
    return BookRepository(sa_manager=sa_manager)
```
