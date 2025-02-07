import pytest
from pydantic import BaseModel

from common.asyncapi import (
    get_schema,
    init_asyncapi_info,
    register_channel,
    register_channel_operation,
    register_server,
)


# Test fixtures
@pytest.fixture
def reset_asyncapi_state():
    """Reset all global state between tests"""
    from common.asyncapi import _channels, _components_schemas, _operations, _servers

    _servers.clear()
    _channels.clear()
    _operations.clear()
    _components_schemas.clear()
    yield
    _servers.clear()
    _channels.clear()
    _operations.clear()
    _components_schemas.clear()


# Test message models
class SomeTestMessage(BaseModel):
    content: str
    timestamp: int


class AnotherTestMessage(BaseModel):
    status: bool
    code: int
    nested: SomeTestMessage


# Test cases
def test_init_asyncapi_info():
    """Test initialization of AsyncAPI info"""
    title = "Test API"
    version = "2.0.0"

    init_asyncapi_info(title=title, version=version)
    schema = get_schema()

    assert schema.info.title == title
    assert schema.info.version == version


def test_register_server(reset_asyncapi_state):
    """Test server registration"""
    server_id = "test-server"
    host = "localhost"
    protocol = "ws"
    pathname = "/ws"

    register_server(id=server_id, host=host, protocol=protocol, pathname=pathname)

    schema = get_schema()
    assert server_id in schema.servers
    assert schema.servers[server_id].host == host
    assert schema.servers[server_id].protocol == protocol
    assert schema.servers[server_id].pathname == pathname


def test_register_channel(reset_asyncapi_state):
    """Test channel registration"""
    channel_id = "test-channel"
    address = "test/topic"
    description = "Test channel"
    title = "Test Channel"

    register_channel(address=address, id=channel_id, description=description, title=title)

    schema = get_schema()
    assert channel_id in schema.channels
    assert schema.channels[channel_id].address == address
    assert schema.channels[channel_id].description == description
    assert schema.channels[channel_id].title == title


def test_register_channel_with_server(reset_asyncapi_state):
    """Test channel registration with server reference"""
    server_id = "test-server"
    channel_id = "test-channel"

    register_server(id=server_id, host="localhost", protocol="ws")
    register_channel(address="test/topic", id=channel_id, server_id=server_id)

    schema = get_schema()
    assert len(schema.channels[channel_id].servers) == 1
    assert schema.channels[channel_id].servers[0].ref == f"#/servers/{server_id}"


def test_register_channel_operation(reset_asyncapi_state):
    """Test channel operation registration"""
    channel_id = "test-channel"
    operation_type = "receive"

    register_channel(address="test/topic", id=channel_id)
    register_channel_operation(
        channel_id=channel_id,
        operation_type=operation_type,
        messages=[SomeTestMessage],
        operation_name="test-operation",
    )

    schema = get_schema()
    assert "test-operation" in schema.operations
    assert schema.operations["test-operation"].action == operation_type
    assert schema.operations["test-operation"].channel.ref == f"#/channels/{channel_id}"
    assert SomeTestMessage.__name__ in schema.components.schemas


def test_register_channel_operation_invalid_channel(reset_asyncapi_state):
    """Test channel operation registration with invalid channel"""
    with pytest.raises(ValueError, match="Channel non-existent does not exist"):
        register_channel_operation(channel_id="non-existent", operation_type="receive", messages=[SomeTestMessage])


def test_multiple_messages_registration(reset_asyncapi_state):
    """Test registration of multiple messages for an operation"""
    channel_id = "test-channel"

    register_channel(address="test/topic", id=channel_id)
    register_channel_operation(
        channel_id=channel_id, operation_type="send", messages=[SomeTestMessage, AnotherTestMessage]
    )

    schema = get_schema()
    assert SomeTestMessage.__name__ in schema.components.schemas
    assert AnotherTestMessage.__name__ in schema.components.schemas
    assert SomeTestMessage.__name__ in schema.channels[channel_id].messages
    assert AnotherTestMessage.__name__ in schema.channels[channel_id].messages
