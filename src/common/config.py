from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field
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
    CORS_ORIGINS: list[str] = Field(default_factory=list)
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    AUTH: AuthConfig = AuthConfig()
    DRAMATIQ: DramatiqConfig = DramatiqConfig()
    DEBUG: bool = False
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"
    SQLALCHEMY_CONFIG: Dict[str, SQLAlchemyConfig] = dict(
        default=SQLAlchemyConfig(
            engine_url="mysql+asyncmy://corinna:gioieiiere@127.0.0.1/backend?charset=utf8mb4",
            async_engine=True,
        ),
    )
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = None
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT: Optional[str] = None
    OTEL_EXPORTER_OTLP_METRICS_ENDPOINT: Optional[str] = None
    OTEL_EXPORTER_OTLP_LOGS_ENDPOINT: Optional[str] = None
