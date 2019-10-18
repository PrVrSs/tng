from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DB:

    __slots__ = (
    )

    engine = None
    session_factory = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DB, cls).__new__(cls)

        return cls._instance

    @classmethod
    def setup(cls, db_config):
        cls.engine = create_engine(db_config)
        cls.session_factory = sessionmaker(bind=cls.engine)

    def create_engine(self):
        pass

    def init_db(self):
        pass

    def close_db(self):
        pass
