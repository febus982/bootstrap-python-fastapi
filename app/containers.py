from dependency_injector import containers, providers

from app import AppConfig


class Container(containers.DeclarativeContainer):
    """
    Dependency injection container.

    Docs: https://python-dependency-injector.ets-labs.org/
    """

    # Modules allowed to do dependency injection
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.domains.books",
            "app.routes.books",
            "app.storage.SQLAlchemy",
            "app.storage.repositories.abstract",
        ],
    )

    """
    We could use the config provider but it would transform our nice typed
    configuration in a dictionary, therefore we return it as a raw object.
    """
    config = providers.Object(AppConfig())

    """
    Class mappings
    
    These are classes we want the container to manage the life cycle for
    (e.g. Singletons), we map them using their class name directly.
    """
    SQLAlchemyManager = providers.Singleton(
        "app.deps.sqlalchemy_manager.SQLAlchemyManager",
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
    BookService = providers.Singleton("app.storage.repositories.BookRepository")
    BookRepositoryInterface = providers.Singleton("app.storage.repositories.BookRepository")
