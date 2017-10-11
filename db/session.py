from contextlib import contextmanager

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.dao import Schema

connection = None


def boot_database(app: Flask):
    global connection

    if connection is not None:
        return

    connection = create_engine(app.config['database'], echo=app.debug or app.testing)
    Schema.metadata.create_all(connection)


@contextmanager
def make_session():
    global connection
    session = Session(bind=connection)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
