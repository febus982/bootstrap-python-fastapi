"""
`fixtures` is a dictionary following the format:

"BIND_NAME": "LIST_OF_FACTORIES"
"""

from factory import Factory

from domains.books._models import BookModel


class BookFactory(Factory):
    class Meta:
        model = BookModel


fixtures = {
    "default": [
        BookFactory(
            title="The Shining",
            author_name="Stephen King",
        ),
    ],
}
