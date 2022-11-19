from functools import wraps

from dependency_injector.wiring import inject, Provide

from app.domains.books.local.data_access_interfaces import BookRepositoryInterface
from deps.sqlalchemy_manager import SQLAlchemyManager


def inject_book_repository(f):
    """
    Decorator implementation for DI injection
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        if "book_repository" not in kwds.keys():
            kwds["book_repository"] = book_repository_factory()
        elif not isinstance(kwds["book_repository"], BookRepositoryInterface):
            import warnings

            warnings.warn(
                f"The specified object ({type(kwds['book_repository'])})"
                f" is not an instance of BookRepositoryInterface"
            )
        return f(*args, **kwds)

    return wrapper


@inject
def book_repository_factory(
    sa_manager: SQLAlchemyManager = Provide[SQLAlchemyManager.__name__],
) -> BookRepositoryInterface:
    """Factory for Book Repository instantiation.

    Args:
        sa_manager: a SQLAlchemyManager instance

    Returns:
        The book repository.
    """
    from app.storage.repositories.book_repository import BookRepository

    return BookRepository(sa_manager=sa_manager)
