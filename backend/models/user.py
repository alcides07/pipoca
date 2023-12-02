from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=32), index=True, unique=True)
    email = Column(String(), index=True, unique=True)
    password = Column(String(length=64), index=True)
