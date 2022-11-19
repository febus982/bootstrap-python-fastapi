from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from app.config import AppConfig
from app.containers import Container, providers
from app.routes import init_routes
from app.storage import init_storage


def create_app(
    test_config: AppConfig | None = None,
) -> FastAPI:
    # Initialise and wire DI container
    c = Container()
    if test_config:
        c.config.override(providers.Object(test_config))

    app = FastAPI(debug=test_config is not None)
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics/", metrics)

    init_storage()
    # TODO: Do this in a more elegant way
    if test_config:
        sa_manager = c.SQLAlchemyManager()
        for k, v in sa_manager.get_binds().items():
            v.registry_mapper.metadata.create_all(v.engine)

    init_routes(app)

    return app
