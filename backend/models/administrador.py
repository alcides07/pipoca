from sqlalchemy import Column, Integer, String
from database import Base


class Administrador(Base):
    __tablename__ = "administradores"

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
