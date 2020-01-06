from sqlalchemy.exc import NoSuchTableError, NoSuchColumnError, OperationalError
from types import GeneratorType


def connect_to_db():
    pass


def insert_one(session, table_name):
    pass


def insert_many():
    pass


def select_one():
    pass


def select_all(session, table) -> GeneratorType:
    try:
        items = session.query(table).all()
        if items:
            return (i for i in items)
    except OperationalError as e:
        return ()


def update_one():
    pass


def delete_one():
    pass
