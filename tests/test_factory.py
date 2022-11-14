import os
from uuid import uuid4

from sqlalchemy.orm import clear_mappers

from app import create_app, AppConfig
from deps.sqlalchemy_manager import SQLAlchemyBindConfig


def test_without_config_test() -> None:
    """Test create_app without passing test config."""
    app = create_app()
    assert app.debug is False
    clear_mappers()


def test_with_config_test() -> None:
    db_name = f"{uuid4()}.db"
    app2 = create_app(AppConfig(
        SQLALCHEMY_CONFIG={
            "default": SQLAlchemyBindConfig(
                engine_url=f"sqlite:///{db_name}",
                engine_options=dict(connect_args={"check_same_thread": False}),
            ),
        }
    ))
    assert app2.debug is True
    clear_mappers()
    os.unlink(db_name)

