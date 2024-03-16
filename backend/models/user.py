from models.problema import Problema
from models.problemaResposta import ProblemaResposta
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


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

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    problemas = relationship(
        Problema,
        back_populates="usuario"
    )

    problemas_respostas = relationship(
        ProblemaResposta,
        back_populates="usuario"
    )
