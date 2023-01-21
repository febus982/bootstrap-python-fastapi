from unittest.mock import patch
from uuid import uuid4

from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyAsyncBindConfig

from config import AppConfig
from http_app import create_app


def test_without_config_test() -> None:
    """Test create_app without passing test config."""
    app = create_app()
    assert app.debug is False
    clear_mappers()


def test_with_config_test() -> None:
    db_name = f"{uuid4()}.db"
    app2 = create_app(
        test_config=AppConfig(
            SQLALCHEMY_CONFIG={
                "default": SQLAlchemyAsyncBindConfig(
                    engine_url=f"sqlite+aiosqlite:///{db_name}",
                    engine_options=dict(connect_args={"check_same_thread": False}),
                ),
            },
            ENVIRONMENT="test",
        )
    )

    # We don't need the storage to test the HTTP app
    with patch("storage.init_storage", return_value=None):
        assert app2.debug is True
