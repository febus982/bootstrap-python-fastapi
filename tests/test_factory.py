from app import create_app


def test_config() -> None:
    """Test create_app without passing test config."""
    app = create_app()
    assert app.debug is False

    app2 = create_app({"TESTING": True})
    assert app2.debug is True
