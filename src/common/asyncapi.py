from typing import List, Literal, Optional, Type

import pydantic_asyncapi.v3 as pa
from pydantic import BaseModel

_info: pa.Info = pa.Info(
    title="AsyncAPI",
    version="1.0.0",
)


_servers = {}  # type: ignore
_channels = {}  # type: ignore
_operations = {}  # type: ignore
_components_schemas = {}  # type: ignore


def get_schema() -> pa.AsyncAPI:
    """
    Function `get_schema` provides the complete AsyncAPI schema for the application, complying with
    version 3.0.0 of the AsyncAPI specification. It includes detailed information about info metadata,
    components, servers, channels, and operations required to set up and describe the asynchronous
    communication layer.

    Returns:
        pa.AsyncAPI: A fully constructed AsyncAPI schema object based on predefined configurations.
    """
    return pa.AsyncAPI(
        asyncapi="3.0.0",
        info=_info,
        components=pa.Components(
            schemas=_components_schemas,
        ),
        servers=_servers,
        channels=_channels,
        operations=_operations,
    )


def init_asyncapi_info(
    title: str,
    version: str = "1.0.0",
) -> None:
    """
    Initializes the AsyncAPI information object with the specified title and version.

    This function creates and initializes an AsyncAPI Info object, which includes
    mandatory fields such as title and version. The title represents the name of the
    AsyncAPI document, and the version represents the version of the API.

    Parameters:
        title (str): The title of the AsyncAPI document.
        version (str): The version of the AsyncAPI document. Defaults to "1.0.0".

    Returns:
        None
    """
    # We can potentially add the other info supported by pa.Info
    global _info
    _info = pa.Info(
        title=title,
        version=version,
    )


def register_server(
    id: str,
    host: str,
    protocol: str,
    pathname: Optional[str] = None,
) -> None:
    """
    Registers a server with a unique identifier and its associated properties.
    This function accepts information about the server such as its host,
    protocol, and optionally its pathname, and stores it in the internal
    server registry identified by the unique ID. The parameters must be
    provided appropriately for proper registration. The server registry
    ensures that server configurations can be retrieved and managed based
    on the assigned identifier.

    Args:
        id: str
            A unique identifier for the server being registered. It is used
            as the key in the internal server registry.
        host: str
            The host address of the server. This may be an IP address or
            a domain name.
        protocol: str
            Communication protocol used by the server, such as "http" or "https".
        pathname: Optional[str]
            The optional pathname of the server. If provided, it will be
            associated with the registered server.

    Returns:
        None
            This function does not return a value. It modifies the internal
            server registry to include the provided server details.
    """
    # TODO: Implement other server parameters
    _servers[id] = pa.Server(
        host=host,
        protocol=protocol,
    )
    if pathname is not None:
        _servers[id].pathname = pathname


def _create_base_channel(address: str, channel_id: str) -> pa.Channel:
    """Create a basic channel with minimum required parameters."""
    return pa.Channel(
        address=address,
        servers=[],
        messages={},
    )


def _add_channel_metadata(channel: pa.Channel, description: Optional[str], title: Optional[str]) -> None:
    """Add optional metadata to the channel."""
    if description is not None:
        channel.description = description
    if title is not None:
        channel.title = title


def _add_server_reference(channel: pa.Channel, server_id: Optional[str]) -> None:
    """Add server reference to the channel if server exists."""
    if server_id is not None and server_id in _servers:
        channel.servers.append(pa.Reference(ref=f"#/servers/{server_id}"))  # type: ignore


def register_channel(
    address: str,
    id: Optional[str] = None,
    description: Optional[str] = None,
    title: Optional[str] = None,
    server_id: Optional[str] = None,
) -> None:
    """
    Registers a communication channel with the specified parameters.

    Args:
        address (str): The address of the channel.
        id (Optional[str]): Unique identifier for the channel. Defaults to None.
        description (Optional[str]): Description of the channel. Defaults to None.
        title (Optional[str]): Title to be associated with the channel. Defaults to None.
        server_id (Optional[str]): Server identifier to link this channel to. Defaults to None.

    Returns:
        None
    """
    channel_id = id or address
    channel = _create_base_channel(address, channel_id)
    _add_channel_metadata(channel, description, title)
    _add_server_reference(channel, server_id)
    _channels[channel_id] = channel


def _register_message_schema(message: Type[BaseModel], operation_type: Literal["receive", "send"]) -> None:
    """Register message schema in components schemas."""
    message_json_schema = message.model_json_schema(
        mode="validation" if operation_type == "receive" else "serialization",
        ref_template="#/components/schemas/{model}",
    )

    _components_schemas[message.__name__] = message_json_schema

    if message_json_schema.get("$defs"):
        _components_schemas.update(message_json_schema["$defs"])


def _create_channel_message(channel_id: str, message: Type[BaseModel]) -> pa.Reference:
    """Create channel message and return reference to it."""
    _channels[channel_id].messages[message.__name__] = pa.Message(  # type: ignore
        payload=pa.Reference(ref=f"#/components/schemas/{message.__name__}")
    )
    return pa.Reference(ref=f"#/channels/{channel_id}/messages/{message.__name__}")


def register_channel_operation(
    channel_id: str,
    operation_type: Literal["receive", "send"],
    messages: List[Type[BaseModel]],
    operation_name: Optional[str] = None,
) -> None:
    """
    Registerm a channel operation with associated messages.

    Args:
        channel_id: Channel identifier
        operation_type: Type of operation ("receive" or "send")
        messages: List of message models
        operation_name: Optional operation name

    Raises:
        ValueError: If channel_id doesn't exist
    """
    if not _channels.get(channel_id):
        raise ValueError(f"Channel {channel_id} does not exist.")

    operation_message_refs = []

    for message in messages:
        _register_message_schema(message, operation_type)
        message_ref = _create_channel_message(channel_id, message)
        operation_message_refs.append(message_ref)

    operation_id = operation_name or f"{channel_id}-{operation_type}"
    _operations[operation_id] = pa.Operation(
        action=operation_type,
        channel=pa.Reference(ref=f"#/channels/{channel_id}"),
        messages=operation_message_refs,
        traits=[],
    )

    # TODO: Define operation traits
    # if operation_name is not None:
    #     _operations[operation_name or f"{channel_id}-{operation_type}"].traits.append(
    #         pa.OperationTrait(
    #             title=operation_name,
    #             summary=f"{operation_name} operation summary",
    #             description=f"{operation_name} operation description",
    #         )
    #     )
