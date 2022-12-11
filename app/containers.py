from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import ThreadSafeSingleton, Dependency
from sqlalchemy_bind_manager import SQLAlchemyBindManager

from app import AppConfig
from app.domains.books import BookService
from app.storage.repositories.book_repository import BookRepositoryInterface


class Container(DeclarativeContainer):
    """
    Dependency injection container.

    Docs: https://python-dependency-injector.ets-labs.org/
    """

    # Enable injection on the whole app package
    wiring_config = WiringConfiguration(packages=["app"])

    """
    We could use the config provider but it would transform our nice typed
    configuration in a dictionary, therefore we return it as a raw object.
    """
    config = Dependency(instance_of=AppConfig)

    """
    Class mappings
    
    These are classes we want the container to manage the life cycle for
    (e.g. Singletons), we map them using their class name directly.
    """
    SQLAlchemyBindManager = ThreadSafeSingleton(
        SQLAlchemyBindManager,
        config=config.provided.SQLALCHEMY_CONFIG,
    )

    """
    Interface => Class mappings
    
    We use the interface class name as key so that we can trigger the injection
    using `class.__name__` and avoid using any hardcoded string or constant.
    
    e.g.
    Mapping
        MyInterface = providers.Factory("app.storage.repositories.ConcreteClass")

    Usage
        @inject
        def function(
            service: MyInterface = Provide[MyInterface.__name__],
        )
    """
    BookService: ThreadSafeSingleton[BookService] = ThreadSafeSingleton(
        "app.domains.books._local.LocalBookService"
    )
    BookRepositoryInterface: ThreadSafeSingleton[BookRepositoryInterface] = ThreadSafeSingleton(
        "app.storage.repositories.book_repository.BookRepository"
    )
