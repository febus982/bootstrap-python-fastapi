from asyncio import iscoroutinefunction
from functools import wraps
from typing import List, Dict, Literal, Type, Optional

from pydantic import BaseModel
import pydantic_asyncapi.v3 as pa


_asyncapi_registry: Dict[str, Dict[Literal["receive", "send"], List]] = {

}


# asyncapi_registry: Dict[str, Dict[Literal["receive", "send"], List]] = {
#     "chat_channel": {
#         "receive": [BookCreatedV1],
#         "send": [BookUpdatedV1],
#     }
# }


def add_channel_to_asyncapi_schema(
    receive: Optional[List[Type[BaseModel]]] = None,
    send: Optional[List[Type[BaseModel]]] = None,
    channel_name: Optional[str] = None,
):
    def decorator(func):
        _channel_name = channel_name or func.__name__
        if _asyncapi_registry.get(_channel_name) is not None:
            raise ValueError(f"The schema already contains a definition for function {_channel_name}. Please rename the function or provide a different channel name.")

        _asyncapi_registry[_channel_name] = {}
        if receive:
            _asyncapi_registry[_channel_name]["receive"] = receive
        if send:
            _asyncapi_registry[_channel_name]["send"] = send

        @wraps(func)
        def wrapper(*args, **kwargs):
            # You can optionally use decorator_args and decorator_kwargs here if needed
            return func(*args, **kwargs)

        @wraps(func)
        async def a_wrapper(*args, **kwargs):
            # You can optionally use decorator_args and decorator_kwargs here if needed
            return await func(*args, **kwargs)

        return a_wrapper if iscoroutinefunction(func) else wrapper

    return decorator


def get_asyncapi_schema():
    components_schemas = {}
    channels = {}
    operations = {}

    for channel, channel_operations in _asyncapi_registry.items():
        _channel_messages = {}
        for operation, messages in channel_operations.items():
            _operation_message_refs = []
            for message in messages:
                # TODO: Check for overlapping model schemas, if they are different log a warning!
                components_schemas[message.__name__] = message.model_json_schema(
                    mode="validation" if operation == "receive" else "serialization",
                    ref_template="#/components/schemas/{model}"
                )
                components_schemas.update(
                    message.model_json_schema(mode="serialization", ref_template="#/components/schemas/{model}")[
                        "$defs"])
                _channel_messages[message.__name__] = pa.Message(
                    payload=pa.Reference(ref=f"#/components/schemas/{message.__name__}")
                )
                # Cannot point to the /components path
                _operation_message_refs.append(
                    pa.Reference(ref=f"#/channels/{channel}/messages/{message.__name__}"))

            # TODO: Define operation names in decorator
            operations[f"{channel}-{operation}"] = pa.Operation(
                action=operation,
                channel=pa.Reference(ref=f"#/channels/{channel}"),
                messages=_operation_message_refs,
            )

        # TODO: Define channel metadata in decorator
        channels[channel] = pa.Channel(
            address=channel,
            description=f"Description for channel {channel}",
            title=f"Title for channel {channel}",
            servers=[pa.Reference(ref="#/servers/chat")],
            messages=_channel_messages,
        )

    # TODO: Implement function to initialize application and servers
    schema = pa.AsyncAPI(
        asyncapi="3.0.0",
        info=pa.Info(
            title="Bookstore API",
            version="1.0.0",
            description="A bookstore asyncapi specification",
        ),
        components=pa.Components(
            schemas=components_schemas,
        ),
        servers={
            "chat": pa.Server(
                host="localhost",
                protocol="ws",
            )
        },
        channels=channels,
        operations=operations,
    )

    return schema
