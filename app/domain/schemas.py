from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    isbn: str


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
        orm_mode = True
