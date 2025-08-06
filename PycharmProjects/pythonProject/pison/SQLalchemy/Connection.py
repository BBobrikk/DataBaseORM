from sqlalchemy import create_engine
from sqlalchemy.orm import create_session, sessionmaker, DeclarativeBase
from Configuration import settings

sync_engine = create_engine(url=settings.CREATE_SYNC_ENGINE())
async_engine = create_engine(url=settings.CREATE_ASYNC_ENGINE())

sync_session = sessionmaker(sync_engine)
async_session = sessionmaker(async_engine)


def sync_sess_create():
    with sync_session.begin() as sess:
        return sess


def async_sess_create():
    with async_session.begin() as sess:
        return sess


class Base(DeclarativeBase):
    pass
