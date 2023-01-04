from typing import Union

from dependency_injector.providers import Object
from fastapi import FastAPI
from fastapi_versionizer import versionize
from starlette_prometheus import PrometheusMiddleware, metrics

from app.config import AppConfig
from app.containers import Container
from app.routes import init_versioned_routes, init_unversioned_routes
from app.storage import init_storage


def create_app(
    test_config: Union[AppConfig, None] = None,
) -> FastAPI:
    app = FastAPI(debug=test_config is not None)

    # Initialise and wire DI container
    # TODO: Don't persist the container in the app object only to access it from pytest.
    app.di_container = Container(  # type: ignore
        config=Object(test_config or AppConfig()),
    )

    init_storage()

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics/", metrics)

    init_versioned_routes(app)

    versionize(
        app=app,
        prefix_format="/api/v{major}",
        docs_url="/docs",
        redoc_url="/redoc",
        enable_latest=True,
    )

    """
    Routes initalised after `versionize` are not versioned
    """
    init_unversioned_routes(app)

    return app
