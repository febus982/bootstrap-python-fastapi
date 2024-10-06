from typing import Annotated, Dict, Union

from pydantic import Field
from typing_extensions import TypeAlias

from .books.events import BookCreatedV1, BookUpdatedV1

event_registry: Dict[str, TypeAlias] = {
    "books": Annotated[Union[BookCreatedV1, BookUpdatedV1], Field(discriminator="type")]
}
