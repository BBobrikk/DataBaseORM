from datetime import date
from sqlalchemy import ForeignKey, CheckConstraint
from Connection import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from ObjectModels import BookModel, AuthorModel

intpk = Annotated[int, mapped_column(primary_key=True)]


class Authors(Base):
    __tablename__ = "Authors"

    author_id: Mapped[intpk]
    name: Mapped[str]
    birth_date: Mapped[date] = mapped_column(default=date.today())

    books: Mapped[list["Books"]] = relationship(back_populates="author")

    top_books: Mapped[list["Books"]] = relationship(
        back_populates="author",
        primaryjoin="and_(Books.author_id == Authors.author_id, Books.rating > 4)",
    )

    genres: Mapped[list["Genres"]] = relationship(
        back_populates="authors", secondary="AuthorsGenres"
    )

    def __repr__(self):
        return f"Id автора : {self.author_id}, Автор : {self.name}, Дата рождения : {self.birth_date}"


class Books(Base):
    __tablename__ = "Books"

    book_id: Mapped[intpk]

    title: Mapped[str]

    rating: Mapped[float] = mapped_column(default=0)

    author_id: Mapped[Authors] = mapped_column(
        ForeignKey("Authors.author_id", ondelete="CASCADE")
    )

    author: Mapped["Authors"] = relationship(back_populates="books")

    __table_args__ = (CheckConstraint("rating BETWEEN 0 and 5", "check_rating"),)

    def __repr__(self):
        return f"Id : {self.book_id}, Название : {self.title}, Рейтинг : {self.rating}"


class Genres(Base):
    __tablename__ = "Genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)

    genre_name: Mapped[str]

    authors: Mapped[list["Authors"]] = relationship(
        back_populates="genres", secondary="AuthorsGenres"
    )

    def __repr__(self):
        return f"Id : {self.genre_id}, Жанр : {self.genre_name}"


class AuthorsGenres(Base):

    __tablename__ = "AuthorsGenres"

    author_id: Mapped[int] = mapped_column(
        ForeignKey("Authors.author_id"), primary_key=True
    )

    genre_id: Mapped[int] = mapped_column(
        ForeignKey("Genres.genre_id"), primary_key=True
    )


# class Genres(Base):
#
#     __tablename__ = "Genres"
#
#     genre_id : Mapped[str] = mapped_column(primary_key = True)
#
#     genre_name : Mapped[str]
#
#     authors : Mapped[list["Authors"]] = relationship(back_populates= "genres", secondary = "AuthorsGenres")
#
#     def __repr__(self):
#         return f"Id :  {self.genre_id}, Жанр : {self.genre_name}"


# class AuthorsGenres(Base):
#
#     __tablename__ = "AuthorsGenres"
#
#     author_id : Mapped[int] = mapped_column(ForeignKey('Authors.author_id'), primary_key = True)
#
#     genres_id : Mapped[int] = mapped_column(ForeignKey('Genres.genre_id'), primary_key = True)
