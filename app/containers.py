from dependency_injector import containers, providers
from sqlalchemy_bind_manager import SQLAlchemyBindManager

from app import AppConfig


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container.

    Docs: https://python-dependency-injector.ets-labs.org/
    """

    # Enable injection on the whole app package
    wiring_config = containers.WiringConfiguration(packages=["app"])

    """
    We could use the config provider but it would transform our nice typed
    configuration in a dictionary, therefore we return it as a raw object.
    """
    config = providers.Dependency(instance_of=AppConfig)

    """
    Class mappings
    
    These are classes we want the container to manage the life cycle for
    (e.g. Singletons), we map them using their class name directly.
    """
    SQLAlchemyBindManager = providers.ThreadSafeSingleton(
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
    BookService = providers.ThreadSafeSingleton(
        "app.domains.books._local.LocalBookService"
    )
    BookRepositoryInterface = providers.ThreadSafeSingleton(
        "app.storage.repositories.book_repository.BookRepository"
    )
