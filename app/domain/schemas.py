from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    isbn: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "year": 1925,
                "isbn": "9780743273565",
            }
        }


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    year: Optional[int]
    isbn: Optional[str]


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "year": 1925,
                "isbn": "9780743273565",
            }
        }
