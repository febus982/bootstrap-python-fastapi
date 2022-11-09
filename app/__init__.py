from fastapi import FastAPI

from app.config import AppConfig
from app.containers import Container
from app.deps.sqlalchemy_manager import SQLAlchemyManager
from app.routes import init_routes
from app.storage import init_storage


def create_app(
        test_config: AppConfig | None = None,
        di_enabled: bool = True,
) -> FastAPI:
    if di_enabled:
        # Initialise and wire DI container
        Container()

    if test_config:
        app = FastAPI(debug=True)
    else:
        app = FastAPI(debug=False)

    init_storage()
    init_routes(app)

    return app
