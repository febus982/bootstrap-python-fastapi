from faststream import context
from opentelemetry import trace
from structlog.typing import EventDict


def extract_from_record(_, __, event_dict: EventDict) -> EventDict:
    """
    Extract thread and process names and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName

    return event_dict


def faststream_context(_, __, event_dict: EventDict) -> EventDict:
    """
    Extract FastStream context information and adds them to the event dict.
    """
    c = context.get_local("log_context") or {}
    event_context = event_dict.get(
        "event_context",
        c.copy(),
    )

    # Handle undesired extra override from FastStream
    extra = event_dict.get("extra", {}).copy()
    if {"channel", "message_id"} == set(extra.keys()):
        event_context["channel"] = extra["channel"]
        event_context["message_id"] = extra["message_id"]
        del event_dict["extra"]

    if event_context:
        event_dict["event_context"] = event_context

    return event_dict


def drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    """
    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor drops the key from the event dict if it exists.
    """
    event_dict.pop("color_message", None)
    return event_dict


def add_logging_open_telemetry_spans(_, __, event_dict: EventDict) -> EventDict:
    span = trace.get_current_span()
    if not span.is_recording():
        event_dict["span"] = None
        return event_dict

    ctx = span.get_span_context()
    parent = getattr(span, "parent", None)

    event_dict["span"] = {
        "span_id": hex(ctx.span_id),
        "trace_id": hex(ctx.trace_id),
        "parent_span_id": None if not parent else hex(parent.span_id),
    }

    return event_dict
