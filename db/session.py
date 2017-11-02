from contextlib import contextmanager

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.dao import Schema

engine = None


def boot_database(app: Flask):
    global engine

    if engine is not None:
        return

    engine = create_engine(app.config['database'], echo=app.debug)
    Schema.metadata.create_all(engine)


@contextmanager
def make_session():
    global engine
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
