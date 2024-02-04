from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Factory, Singleton
from domains.books._gateway_interfaces import (
    BookEventGatewayInterface,
    BookRepositoryInterface,
)
from domains.books._models import BookModel
from gateways.event import NullEventGateway
from sqlalchemy_bind_manager import SQLAlchemyBindManager
from sqlalchemy_bind_manager.repository import SQLAlchemyAsyncRepository

from bootstrap.config import AppConfig


class Container(DeclarativeContainer):
    """
    Dependency injection container.

    Docs: https://python-dependency-injector.ets-labs.org/
    """

    wiring_config = WiringConfiguration(
        packages=[
            "bootstrap",
            "domains",
        ]
    )

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
    SQLAlchemyBindManager = Singleton(
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

    BookRepositoryInterface: Factory[BookRepositoryInterface] = Factory(
        SQLAlchemyAsyncRepository,
        bind=SQLAlchemyBindManager.provided.get_bind.call(),
        model_class=BookModel,
    )
    BookEventGatewayInterface: Factory[BookEventGatewayInterface] = Factory(
        NullEventGateway
    )
