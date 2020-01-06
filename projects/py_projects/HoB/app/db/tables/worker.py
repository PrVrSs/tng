from sqlalchemy import Column, String, Integer, Date
from app.db.db_connector import Base


class Worker(Base):

    __tablename__ = 'worker'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)

    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
