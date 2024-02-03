from typing import Union

import strawberry


@strawberry.type
class Book:
    book_id: Union[int, None] = None
    title: str
    author_name: str
