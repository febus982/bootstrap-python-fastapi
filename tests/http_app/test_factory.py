from unittest.mock import patch
from uuid import uuid4

from sqlalchemy_bind_manager import SQLAlchemyAsyncBindConfig

from config import AppConfig
from http_app import create_app


def test_without_config_test() -> None:
    """Test create_app without passing test config."""
    with patch("http_app.init_storage", return_value=None):
        app = create_app()
    assert app.debug is False


def test_with_config_test() -> None:
    db_name = f"{uuid4()}.db"
    # We don't need the storage to test the HTTP app
    with patch("http_app.init_storage", return_value=None):
        app = create_app(
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

    assert app.debug is True
