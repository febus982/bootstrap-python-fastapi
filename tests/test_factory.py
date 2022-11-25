import os
from uuid import uuid4

from sqlalchemy.orm import clear_mappers
from sqlalchemy_bind_manager import SQLAlchemyBindConfig

from app import create_app, AppConfig


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
                "default": SQLAlchemyBindConfig(
                    engine_url=f"sqlite:///{db_name}",
                    engine_options=dict(connect_args={"check_same_thread": False}),
                ),
            }
        )
    )

    sa_manager = app2.di_container.SQLAlchemyBindManager()
    for k, v in sa_manager.get_binds().items():
        v.registry_mapper.metadata.create_all(v.engine)

    assert app2.debug is True
    os.unlink(db_name)
    clear_mappers()
