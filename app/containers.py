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
           "app.storage",
        ],
    )

    config = providers.Configuration(pydantic_settings=[AppConfig()])

    """
    Class mappings
    
    We use the class name as key so that we trigger the injection using class name.
    
    e.g.
    Mapping
        MyInterface = providers.Factory("app.storage.repositories.ConcreteClass")

    Usage
        @inject
        def function(
            service: MyInterface = Provide[MyInterface.__name__],
        )
    """
