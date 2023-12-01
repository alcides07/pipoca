from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=32), index=True)
    email = Column(String(), index=True)
    password = Column(String(32), index=True)
