from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase

from database.database import engine


class Base(DeclarativeBase): pass


class ImageModel(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)
