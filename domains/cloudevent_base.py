import abc
import datetime
import typing

import pydantic
from cloudevents.sdk.event import attribute


def type_field(default: typing.Union[str, None] = None) -> typing.Any:
    """
    Helper function to generate the CloudEvent `type` field,
    optionally with a default value.

    Args:
        default: The default value of the field

    Returns:
        The pydantic field object
    """
    field = pydantic.Field(
        title="Event Type",
        default=default,
        description=(
            "This attribute contains a value describing the type of event related to"
            " the originating occurrence. Often this attribute is used for routing,"
            " observability, policy enforcement, etc. The format of this is producer"
            " defined and might include information such as the version of the type"
        ),
        examples=[default or "com.github.pull_request.opened"],
    )
    return field


def source_field(default: typing.Union[str, None] = None) -> typing.Any:
    """
    Helper function to generate the CloudEvent `source` field,
    optionally with a default value.

    Args:
        default: The default value of the field

    Returns:
        The pydantic field object
    """
    field = pydantic.Field(
        title="Event Source",
        default=default,
        description=(
            "Identifies the context in which an event happened. Often this will include"
            " information such as the type of the event source, the organization"
            " publishing the event or the process that produced the event. The exact"
            " syntax and semantics behind the data encoded in the URI is defined by the"
            " event producer.\n"
            "\n"
            "Producers MUST ensure that source + id is unique for"
            " each distinct event.\n"
            "\n"
            "An application MAY assign a unique source to each"
            " distinct producer, which makes it easy to produce unique IDs since no"
            " other producer will have the same source. The application MAY use UUIDs,"
            " URNs, DNS authorities or an application-specific scheme to create unique"
            " source identifiers.\n"
            "\n"
            "A source MAY include more than one producer. In"
            " that case the producers MUST collaborate to ensure that source + id is"
            " unique for each distinct event."
        ),
        examples=[default or "https://github.com/cloudevents"],
    )
    return field


def dataschema_field(
    base_url, event_name: typing.Union[str, None] = None
) -> typing.Any:
    """
    Helper function to generate the CloudEvent `dataschema` field,
    pointing to the event schema url.

    Args:
        base_url: The base URL for event dataschema
        event_name: The event_name value of the field

    Returns:
        The pydantic field object
    """
    content = f"{base_url}/{event_name or 'some_event'}"
    schema = pydantic.Field(
        title="Event Data Schema",
        default=content,
        description=(
            "Identifies the schema that data adheres to. "
            "Incompatible changes to the schema SHOULD be reflected by a different URI"
        ),
        examples=[content],
    )
    return schema


def datacontenttype_field(default: typing.Union[str, None] = None) -> typing.Any:
    """
    Helper function to generate the CloudEvent `datacontenttype` field,
    optionally with a default value.

    :param default: The default value of the field
    :return:
    """
    field = pydantic.Field(
        title="Event Data Content Type",
        default=default,
        description=(
            "Content type of data value. This attribute enables data to carry any type"
            " of content, whereby format and encoding might differ from that of the"
            " chosen event format."
        ),
        examples=["text/xml"],
    )
    return field


def subject_field(default: typing.Union[str, None] = None) -> typing.Any:
    """
    Helper function to generate the CloudEvent `subject` field,
    optionally with a default value.

    Args:
        default: The default value of the field

    Returns:
        The pydantic field object
    """
    field = pydantic.Field(
        title="Event Subject",
        default=default,
        description=(
            "This describes the subject of the event in the context of the event"
            " producer (identified by source). In publish-subscribe scenarios, a"
            " subscriber will typically subscribe to events emitted by a source, but"
            " the source identifier alone might not be sufficient as a qualifier for"
            " any specific event if the source context has internal"
            " sub-structure.\n"
            "\n"
            "Identifying the subject of the event in context"
            " metadata (opposed to only in the data payload) is particularly helpful in"
            " generic subscription filtering scenarios where middleware is unable to"
            " interpret the data content. In the above example, the subscriber might"
            " only be interested in blobs with names ending with '.jpg' or '.jpeg' and"
            " the subject attribute allows for constructing a simple and efficient"
            " string-suffix filter for that subset of events."
        ),
        examples=["123"],
    )
    return field


class BaseEvent(pydantic.BaseModel, abc.ABC):
    """
    This is the implementation of a CloudEvent using pydantic. It is not
    using CloudEvents sdk base class on purpose, to avoid incompatibilities
    with pydantic V2 (the __iter__ method).

    This means that in order to use this event we'll manually create the
    relevant CloudEvent object (e.g. from `cloudevents.http`) and use it
    as we need.

    Could this be improved if created dynamically?
    Perhaps we can pick up dynamic information
    from the application config or inject data like the event type?.
    https://docs.pydantic.dev/latest/usage/models/#dynamic-model-creation
    """

    source: typing.Literal["this.service.url.here"] = source_field(
        "this.service.url.here"
    )
    type: str = type_field()
    dataschema: str = dataschema_field("this.service.url.here")
    datacontenttype: typing.Literal["application/json"] = datacontenttype_field(
        "application/json"
    )
    subject: typing.Optional[str] = subject_field()
    data: typing.Optional[pydantic.BaseModel] = None
    id: str = pydantic.Field(
        default_factory=attribute.default_id_selection_algorithm,
        title="Event ID",
        description=(
            "Identifies the event. Producers MUST ensure that source + id is unique for"
            " each distinct event. If a duplicate event is re-sent (e.g. due to a"
            " network error) it MAY have the same id. Consumers MAY assume that Events"
            " with identical source and id are duplicates. MUST be unique within the"
            " scope of the producer"
        ),
        examples=["A234-1234-1234"],
    )
    specversion: attribute.SpecVersion = pydantic.Field(
        default=attribute.DEFAULT_SPECVERSION,
        title="Specification Version",
        description=(
            "The version of the CloudEvents specification which the event uses. This"
            " enables the interpretation of the context.\n"
            "\n"
            "Currently, this attribute will only have the 'major'"
            " and 'minor' version numbers included in it. This allows for 'patch'"
            " changes to the specification to be made without changing this property's"
            " value in the serialization."
        ),
        examples=[attribute.DEFAULT_SPECVERSION],
    )
    time: typing.Optional[datetime.datetime] = pydantic.Field(
        default_factory=attribute.default_time_selection_algorithm,
        title="Occurrence Time",
        description=(
            " Timestamp of when the occurrence happened. If the time of the occurrence"
            " cannot be determined then this attribute MAY be set to some other time"
            " (such as the current time) by the CloudEvents producer, however all"
            " producers for the same source MUST be consistent in this respect. In"
            " other words, either they all use the actual time of the occurrence or"
            " they all use the same algorithm to determine the value used."
        ),
        examples=["2018-04-05T17:31:00Z"],
    )

    _ce_valid_attrs: tuple = (
        "source",
        "id",
        "type",
        "specversion",
        "time",
        "subject",
        "datacontenttype",
        "dataschema",
    )
