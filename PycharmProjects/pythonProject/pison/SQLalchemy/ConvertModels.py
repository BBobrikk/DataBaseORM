from sqlalchemy.orm import joinedload

from ObjectModels import AuthorModel, BookModel
from Connection import sync_sess_create
from sqlalchemy import select
from TableModels import Books, Authors
from pison.SQLalchemy.ObjectModels import JoinAuthorBooks


def convert_books():
    with sync_sess_create() as sess:
        query = select(Books)
        res_orm = sess.execute(query).scalars().all()
        res_dto = [
            BookModel.model_validate(row, from_attributes=True) for row in res_orm
        ]
        print(res_orm)
        print(res_dto)


def convert_authors():
    with sync_sess_create() as sess:
        query = select(Authors)
        res_orm = sess.execute(query).scalars().all()
        res_dto = [
            AuthorModel.model_validate(row, from_attributes=True) for row in res_orm
        ]
        print(res_orm)
        print(res_dto)


def joinedload_books_auths():
    with sync_sess_create() as sess:
        query = select(Authors).options(joinedload(Authors.books))
        res_orm = sess.execute(query).scalars().unique().all()
        res_dto = [
            JoinAuthorBooks.model_validate(row, from_attributes=True) for row in res_orm
        ]
        print(res_orm[0].books)
        print(res_dto[0].books)


def joinedload_auths_books():
    pass  # не забыть доделать + joinedload_auths_genres + joinedload_auths_books_genres


joinedload_books_auths()
