from sqlalchemy.orm import clear_mappers

from app import create_app


def test_without_config_test() -> None:
    """Test create_app without passing test config."""
    app = create_app()
    assert app.debug is False
    clear_mappers()


def test_with_config_test() -> None:
    app2 = create_app({"TESTING": True})
    assert app2.debug is True
    clear_mappers()

