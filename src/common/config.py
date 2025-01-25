from pathlib import Path
from typing import Dict, Literal, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy_bind_manager import SQLAlchemyConfig

TYPE_ENVIRONMENT = Literal["local", "test", "staging", "production"]


class DramatiqConfig(BaseModel):
    REDIS_URL: Optional[str] = None


class AuthConfig(BaseModel):
    JWT_ALGORITHM: str = "RS256"
    JWKS_URL: Optional[str] = None


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    APP_NAME: str = "bootstrap"
    AUTH: AuthConfig = AuthConfig()
    DRAMATIQ: DramatiqConfig = DramatiqConfig()
    DEBUG: bool = False
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"
    SQLALCHEMY_CONFIG: Dict[str, SQLAlchemyConfig] = dict(
        default=SQLAlchemyConfig(
            engine_url=f"sqlite+aiosqlite:///{Path(__file__).parent.parent.joinpath('sqlite.db')}",
            engine_options=dict(
                connect_args={
                    "check_same_thread": False,
                },
                echo=False,
                future=True,
            ),
            async_engine=True,
        ),
    )
