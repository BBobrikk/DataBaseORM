from sqlalchemy import select, update, func
from sqlalchemy.orm import joinedload, selectinload, contains_eager
import random

from Connection import (
    sync_sess_create,
    sync_engine,
    async_sess_create,
    async_engine,
    Base,
)
from ObjectModels import BookModel, AuthorModel
from TableModels import Books, Authors, Genres, AuthorsGenres
from datetime import date


def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    print("Таблицы созданы")


def insert_books():
    with sync_sess_create() as sess:
        sess.add_all(
            [
                Books(book_id=1, title="Fight Club", rating=4.3, author_id=1),
                Books(book_id=2, title="Game of Thrones", rating=3.3, author_id=2),
                Books(book_id=3, title="Little prince", rating=4.1, author_id=3),
            ]
        )
        sess.commit()


def select_books():
    with sync_sess_create() as sess:
        query = select(Books)
        res = sess.execute(query).all()
        print(res)


def insert_authors():
    with sync_sess_create() as sess:
        sess.add_all(
            [
                Authors(author_id=1, name="Sosik"),
                Authors(author_id=2, name="Babijon"),
                Authors(author_id=3, name="Farhat Babahov"),
            ]
        )
        sess.commit()


def select_authors():
    with sync_sess_create() as sess:
        query = select(Authors)
        res = sess.execute(query).all()
        print(res)


def insert_genres():
    with sync_sess_create() as sess:
        sess.add_all(
            [
                Genres(genre_id=1, genre_name="рассказ"),
                Genres(genre_id=2, genre_name="новелла"),
                Genres(genre_id=3, genre_name="повесть"),
                Genres(genre_id=4, genre_name="роман"),
                Genres(genre_id=5, genre_name="трагедия"),
                Genres(genre_id=6, genre_name="комедия"),
                Genres(genre_id=7, genre_name="мелодрама"),
            ]
        )
        sess.commit()


def authors_join_books():
    with sync_sess_create() as sess:
        query = select(Books.title, Authors.name).join(
            Authors, Authors.author_id == Books.author_id
        )
        res = sess.execute(query).all
        print(res)


def joinedload_books_authors():
    with sync_sess_create() as sess:
        query = (
            select(Authors)
            .join(Authors.books)
            .options(joinedload(Authors.books))
            .filter(Books.rating > 4)
        )
        # query = select(Authors).options(joinedload(Authors.top_books))
        res = sess.execute(query).scalars().unique().all()
        for i in res:
            print(i.books)


def get_ready_database():
    create_tables()
    insert_authors()
    insert_books()
    # insert_genres()
    insert_genres_to_auths()


def insert_genres_to_auths():
    lst = []
    genres = [
        Genres(genre_id=1, genre_name="рассказ"),
        Genres(genre_id=2, genre_name="новелла"),
        Genres(genre_id=3, genre_name="повесть"),
        Genres(genre_id=4, genre_name="роман"),
        Genres(genre_id=5, genre_name="трагедия"),
        Genres(genre_id=6, genre_name="комедия"),
        Genres(genre_id=7, genre_name="мелодрама"),
    ]

    with sync_sess_create() as sess:
        query = select(Authors).options(joinedload(Authors.genres))
        res = sess.execute(query).scalars().unique().all()
        for i in range(len(genres)):
            auth = random.choice(res)
            gen = random.choice(genres)
            if [auth, gen] not in lst:
                lst.append([auth, gen])
                auth.genres.append(gen)

        sess.commit()

