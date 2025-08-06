from pydantic import BaseModel
from datetime import date


class BookModel(BaseModel):
    book_id: int
    title: str
    rating: float


class AuthorModel(BaseModel):
    author_id: int
    name: str
    birth_date: date


class JoinAuthorBooks(AuthorModel):
    books: list[BookModel]
