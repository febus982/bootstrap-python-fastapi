from domains.books import Book, BookService


async def list_books():
    book_service = BookService()
    books = await book_service.list_books()
    return [Book.model_validate(x, from_attributes=True) for x in books]
