from fastapi import APIRouter, Depends, Query, Path
from fastapi.params import Body
from sqlalchemy.orm import Session

from app.application.use_cases.book_use_case import BookUseCase
from app.domain.book import Book
from app.domain.schemas import BookCreate, BookResponse
from app.infrastructure.database import get_db
from app.infrastructure.repositories.pg_repositories.pg_book_repository import PGBookRepository

book_router = APIRouter()


@book_router.post(
    "/books/",
    response_model=BookResponse,
    summary="Add a new book",
    description="Add a new book to the library database.",
    responses={
        200: {
            "description": "Book successfully created.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "The Great Gatsby",
                        "author": "F. Scott Fitzgerald",
                        "year": 1925,
                        "isbn": "9780743273565",
                    }
                }
            },
        },
        400: {"description": "Validation error."},
    },
)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    """
        Add a new book to the library.

        - **title**: The title of the book.
        - **author**: The name of the author.
        - **year**: The year the book was published.
        - **isbn**: The ISBN of the book.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.add(book)


@book_router.get(
    "/book/",
    response_model=list[BookResponse],
    summary="List books by author or year",
    description="Retrieve a list of books filtered by the author's name or the year of publication.",
    tags=["Books"],
    responses={
        200: {
            "description": "A list of books that match the filter criteria.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "The Great Gatsby",
                            "author": "F. Scott Fitzgerald",
                            "year": 1925,
                            "isbn": "9780743273565"
                        },
                        {
                            "id": 2,
                            "title": "To Kill a Mockingbird",
                            "author": "Harper Lee",
                            "year": 1960,
                            "isbn": "9780061120084"
                        }
                    ]
                }
            },
        },
        404: {"description": "No books found matching the criteria."},
    },
)
def list_books(
        author: str = Query(
            None, description="The author's name to filter books by (case-insensitive)."
        ),
        year: int = Query(
            None, description="The publication year to filter books by."
        ),
        db: Session = Depends(get_db)
):
    """
        List books filtered by author or year.

        - **author**: (Optional) The name of the author.
        - **year**: (Optional) The year of publication.
        - If both parameters are omitted, all books are returned.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.get_by_author_or_year(author=author, year=year)


@book_router.get(
    "/books/search/",
    response_model=list[BookResponse],
    summary="Search books by any field",
    description="Search for books by matching the query against any field, including title, author, year, or ISBN.",
    tags=["Books"],
    responses={
        200: {
            "description": "A list of books matching the search query.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "The Great Gatsby",
                            "author": "F. Scott Fitzgerald",
                            "year": 1925,
                            "isbn": "9780743273565"
                        },
                        {
                            "id": 2,
                            "title": "To Kill a Mockingbird",
                            "author": "Harper Lee",
                            "year": 1960,
                            "isbn": "9780061120084"
                        }
                    ]
                }
            },
        },
        404: {"description": "No books found matching the query."},
    },
)
def search_books(
        query: str = Query(
            ...,
            description="The search query. Matches against title, author, year, or ISBN."
        ),
        db: Session = Depends(get_db)
):
    """
        Search for books in the library.

        This endpoint matches the provided query against all fields of the books, including:
        - **title**: The title of the book.
        - **author**: The name of the author.
        - **year**: The year the book was published.
        - **isbn**: The International Standard Book Number.

        - If no books match the query, a 404 error is returned.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.search(query=query)


@book_router.get(
    "/books/",
    response_model=list[BookResponse],
    summary="List all books",
    description="Retrieve a list of all books stored in the library's database.",
    tags=["Books"],
    responses={
        200: {
            "description": "A list of all books in the library.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "The Great Gatsby",
                            "author": "F. Scott Fitzgerald",
                            "year": 1925,
                            "isbn": "9780743273565"
                        },
                        {
                            "id": 2,
                            "title": "To Kill a Mockingbird",
                            "author": "Harper Lee",
                            "year": 1960,
                            "isbn": "9780061120084"
                        }
                    ]
                }
            },
        },
        404: {"description": "No books found."},
    },
)
def list_books(db: Session = Depends(get_db)):
    """
        List all books in the library.

        This endpoint returns a list of all books currently stored in the library's database.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.get_all()


@book_router.get(
    "/books/{book_id}/",
    response_model=BookResponse,
    summary="Get a book by ID",
    description="Retrieve the details of a specific book by its ID.",
    tags=["Books"],
    responses={
        200: {
            "description": "Details of the book with the given ID.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "The Great Gatsby",
                        "author": "F. Scott Fitzgerald",
                        "year": 1925,
                        "isbn": "9780743273565"
                    }
                }
            },
        },
        404: {"description": "Book not found."},
    },
)
def get_book_by_id(
        book_id: int = Path(..., description="The ID of the book to retrieve.", example=1),
        db: Session = Depends(get_db)
):
    """
        Get a book by its ID.

        - **book_id**: The unique identifier of the book to retrieve.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.get_by_id(book_id=book_id)


@book_router.put(
    "/books/{book_id}/",
    response_model=BookResponse,
    summary="Update a book",
    description="Update the details of an existing book by its ID.",
    tags=["Books"],
    responses={
        200: {
            "description": "Details of the updated book.",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "The Great Gatsby (Updated)",
                        "author": "F. Scott Fitzgerald",
                        "year": 1926,
                        "isbn": "9780743273565"
                    }
                }
            },
        },
        404: {"description": "Book not found."},
        400: {"description": "Invalid update data."},
    },
)
def update_book(
        book_id: int = Path(..., description="The ID of the book to update.", example=1),
        updates: dict = Body(
            ...,
            description="A dictionary containing the fields to update and their new values.",
            example={
                "title": "The Great Gatsby (Updated)",
                "author": "F. Scott Fitzgerald",
                "year": 1926,
                "isbn": "9780743273565"
            },
        ),
        db: Session = Depends(get_db)
):
    """
        Update a book's details.

        - **book_id**: The unique identifier of the book to update.
        - **updates**: A dictionary containing the fields to update. Only specified fields will be updated.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.update(book_id=book_id, updates=updates)


@book_router.delete(
    "/books/{book_id}/",
    summary="Delete a book",
    description="Delete a book from the library's database by its ID.",
    tags=["Books"],
    responses={
        200: {
            "description": "Confirmation that the book was successfully deleted.",
            "content": {
                "application/json": {
                    "example": {"message": "Book successfully deleted."}
                }
            },
        },
        404: {"description": "Book not found."},
    },
)
def delete_book(
        book_id: int = Path(..., description="The ID of the book to delete.", example=1),
        db: Session = Depends(get_db)
):
    """
        Delete a book from the library by its ID.

        - **book_id**: The unique identifier of the book to delete.
    """
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.delete(book_id=book_id)
