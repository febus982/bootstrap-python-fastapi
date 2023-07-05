from typing import List

import strawberry

from .resolvers import list_books
from .types import Book


@strawberry.type
class Query:
    books: List[Book] = strawberry.field(resolver=list_books)
