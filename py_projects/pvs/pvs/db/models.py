from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from .base import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    digest = Column(String, unique=True)


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    url = Column(String, primary_key=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    program = relationship(Program)


class Scheduled(Base):
    __tablename__ = "scheduled_programs"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    channel = relationship(Channel)
    program = relationship(Program)

    @property
    def duration(self):
        return self.end_time - self.start_time
