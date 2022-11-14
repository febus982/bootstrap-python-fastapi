from pydantic import BaseSettings

from deps.sqlalchemy_manager import SQLAlchemyBindConfig, SQLAlchemyConfig


class AppConfig(BaseSettings):
    SQLALCHEMY_CONFIG: SQLAlchemyConfig = {
        "default": SQLAlchemyBindConfig(
            engine_url="sqlite:///./sqlite.db",
            engine_options=dict(
                connect_args={"check_same_thread": False},
                echo=True
            ),
            session_options=dict(expire_on_commit=False)
        ),
        # Add additional bindings here, e.g.:
        # "customer": SQLAlchemyBindConfig(engine_url="sqlite:///./customer.db"),
    }
