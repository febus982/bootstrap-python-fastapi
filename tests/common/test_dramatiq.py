import logging
from unittest.mock import MagicMock, patch

import orjson
import pytest
from dramatiq import get_broker, get_encoder
from dramatiq.brokers.stub import StubBroker
from dramatiq.encoder import DecodeError

from common import AppConfig
from common.config import DramatiqConfig
from common.dramatiq import ORJSONEncoder, init_dramatiq


@patch("common.dramatiq.orjson.dumps", return_value=b"serialized")
@patch("common.dramatiq.orjson.loads", return_value="deserialized")
def test_orjson_encoder(
    mocked_loads: MagicMock,
    mocked_dumps: MagicMock,
):
    encoder = ORJSONEncoder()

    serialized = encoder.encode({})
    assert serialized == b"serialized"
    mocked_dumps.assert_called_once_with({})
    deserialized = encoder.decode(serialized)
    assert deserialized == "deserialized"
    mocked_loads.assert_called_once_with(b"serialized")


@patch(
    "common.dramatiq.orjson.loads",
    side_effect=orjson.JSONDecodeError("msg", "doc", 123),
)
def test_orjson_encoder_fails(
    mocked_loads: MagicMock,
):
    encoder = ORJSONEncoder()

    with pytest.raises(DecodeError):
        encoder.decode(b"serialized")


def test_init_dramatiq_with_test_env():
    """Test if the StubBroker is set in the 'test' environment."""
    config = AppConfig(ENVIRONMENT="test", DRAMATIQ=DramatiqConfig())  # Mock config
    init_dramatiq(config)
    assert isinstance(get_broker(), StubBroker)
    assert isinstance(get_encoder(), ORJSONEncoder)


def test_init_dramatiq_with_redis():
    """Test if the RedisBroker is set with a valid Redis URL."""
    redis_url = "redis://localhost:6379/0"
    config = AppConfig(ENVIRONMENT="production", DRAMATIQ=DramatiqConfig(REDIS_URL=redis_url))  # Mock config
    with patch("common.dramatiq.RedisBroker") as mock_redis_broker:
        init_dramatiq(config)
        mock_redis_broker.assert_called_once_with(url=redis_url)
        assert get_broker() == mock_redis_broker.return_value
        assert isinstance(get_encoder(), ORJSONEncoder)


def test_init_dramatiq_without_redis_url(caplog):
    """Test if an exception is raised when in non-test environment without Redis URL."""
    config = AppConfig(ENVIRONMENT="production", DRAMATIQ=DramatiqConfig(REDIS_URL=None))  # Mock config
    with caplog.at_level(logging.CRITICAL):
        init_dramatiq(config)

    assert "Running a non-test/non-local environment without Redis URL set" in caplog.text
