from models.problema import Problema
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(length=32),
        unique=True,
        index=True,
        nullable=False,
    )

    email = Column(
        String(),
        unique=True,
        index=True,
        nullable=False,
    )

    password = Column(
        String(length=64),
        nullable=False,
    )

    problemas = relationship(
        Problema,
        back_populates="usuario"
    )
