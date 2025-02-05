import os
from unittest.mock import Mock, patch
from uuid import uuid4

from sqlalchemy_bind_manager import SQLAlchemyBindManager, SQLAlchemyConfig

from common.storage import init_storage
from common.storage.SQLAlchemy import TABLE_INIT_REGISTRY, init_tables


def test_init_tables_calls_only_supported_bind_initialisation():
    db1_path = f"./{uuid4()}.db"
    db2_path = f"./{uuid4()}.db"

    sa_manager = SQLAlchemyBindManager(
        config={
            "default": SQLAlchemyConfig(
                engine_url=f"sqlite+aiosqlite:///{db1_path}",
                engine_options=dict(connect_args={"check_same_thread": False}),
                session_options=dict(expire_on_commit=False),
                async_engine=True,
            ),
            "not_existing": SQLAlchemyConfig(
                engine_url=f"sqlite+aiosqlite:///{db2_path}",
                engine_options=dict(connect_args={"check_same_thread": False}),
                session_options=dict(expire_on_commit=False),
                async_engine=True,
            ),
        }
    )

    mock_db1_table_init = Mock(return_value=None)
    mock_db2_table_init = Mock(return_value=None)

    with patch.dict(
        TABLE_INIT_REGISTRY,
        {
            "default": mock_db1_table_init,
            "other": mock_db2_table_init,
        },
    ):
        init_tables(sqlalchemy_manager=sa_manager)

    mock_db1_table_init.assert_called_once()
    mock_db2_table_init.assert_not_called()

    try:
        os.unlink(db1_path)
    except FileNotFoundError:
        pass

    try:
        os.unlink(db2_path)
    except FileNotFoundError:
        pass


def test_init_storage_calls_sqlalchemy_init_tables():
    with patch("common.storage.SQLAlchemy.init_tables", return_value=None) as mocked_init_tables:
        init_storage()

    mocked_init_tables.assert_called_once()
