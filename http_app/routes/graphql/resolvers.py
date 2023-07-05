from domains.books import Book, BookService


async def list_books():
    book_service = BookService()
    books = await book_service.list_books()
    return [Book(**x.dict()) for x in books]
