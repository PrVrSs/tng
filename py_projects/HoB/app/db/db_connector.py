from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.db_backend import *


Base = declarative_base()


class DBConnector(object):

    def __init__(self):
        self._engine = create_engine("sqlite:///some.db")
        self._session: sessionmaker = sessionmaker(bind=self._engine)
        self._base = Base()

    def __del__(self):
        self.session().close()

    def session(self):
        return self._session()

    def create_item(self):
        pass

    def read_item(self, table):
        return select_all(self.session(), table)

    def update_item(self):
        pass

    def delete_item(self):
        pass
