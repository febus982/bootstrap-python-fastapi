from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from app.config import AppConfig
from app.containers import Container, providers
from app.routes import init_routes
from app.storage import init_storage


def create_app(
    test_config: AppConfig | None = None,
) -> FastAPI:
    app = FastAPI(debug=test_config is not None)

    # Initialise and wire DI container
    # TODO: Don't persist the container in the app object only to access it from pytest.
    app.di_container = Container(
        config=providers.Object(test_config or AppConfig()),
    )

    init_storage()

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics/", metrics)

    init_routes(app)

    return app
