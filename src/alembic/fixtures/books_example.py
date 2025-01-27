"""
`fixtures` is a dictionary following the format:

"BIND_NAME": "LIST_OF_FACTORIES"
"""

from typing import Dict, List

from factory import Factory

from domains.books._models import BookModel


def fixtures() -> Dict[str, List]:
    class BookFactory(Factory):
        class Meta:
            model = BookModel

    return {
        "default": [
            BookFactory(
                title="The Shining",
                author_name="Stephen King",
            ),
        ],
    }
