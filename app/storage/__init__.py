from app.config import AppConfig
from .SQLAlchemy import init_sqlalchemy


def init_storage(config: AppConfig):
    init_sqlalchemy(config.SQLALCHEMY_CONFIG)
