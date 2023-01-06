import os
from unittest.mock import patch, Mock
from uuid import uuid4

from sqlalchemy_bind_manager import SQLAlchemyBindManager, SQLAlchemyBindConfig

from storage.SQLAlchemy import TABLE_INIT_REGISTRY, init_tables


def test_init_tables_calls_only_supported_bind_initialisation(testapp):
    db1_path = f"./{uuid4()}.db"
    db2_path = f"./{uuid4()}.db"

    sa_manager = SQLAlchemyBindManager(
        config={
            "default": SQLAlchemyBindConfig(
                engine_url=f"sqlite:///{db1_path}",
                engine_options=dict(connect_args={"check_same_thread": False}),
                session_options=dict(expire_on_commit=False),
            ),
            "not_existing": SQLAlchemyBindConfig(
                engine_url=f"sqlite:///{db2_path}",
                engine_options=dict(connect_args={"check_same_thread": False}),
                session_options=dict(expire_on_commit=False),
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
    ), patch("storage.SQLAlchemy.default_tables.init_tables", return_value=None):
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
