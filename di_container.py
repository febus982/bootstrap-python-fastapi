from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import ThreadSafeSingleton, Dependency, Factory
from sqlalchemy_bind_manager import SQLAlchemyBindManager

from config import AppConfig
from domains.books._local.data_access_interfaces import BookRepositoryInterface
from storage.repositories.book_repository import BookRepository


class Container(DeclarativeContainer):
    """
    Dependency injection container.

    Docs: https://python-dependency-injector.ets-labs.org/
    """

    # Enable injection on the whole http_app package
    wiring_config = WiringConfiguration(packages=[
        "storage",
        "domains",
    ])

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
        MyInterface = providers.Factory("http_app.storage.repositories.ConcreteClass")

    Usage
        @inject
        def function(
            service: MyInterface = Provide[MyInterface.__name__],
        )
    """

    BookRepositoryInterface: Factory[
        BookRepositoryInterface
    ] = Factory(
        BookRepository,
        bind=SQLAlchemyBindManager.provided.get_bind.call(),
    )
