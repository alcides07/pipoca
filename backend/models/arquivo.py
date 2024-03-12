from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from schemas.arquivo import SecaoEnum


class Arquivo(Base):
    __tablename__ = "arquivos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(length=64),
        index=True,
        nullable=False,
    )

    corpo = Column(
        String(length=250000),
        nullable=False,
    )

    linguagem = Column(
        String()
    )

    secao = Column(
        Enum(SecaoEnum),
        index=True
    )

    status = Column(
        String,
        index=True
    )

    problema_id = Column(
        Integer,
        ForeignKey(
            'problemas.id',
            name="arquivos_problema_id_fkey"
        )
    )
    problema = relationship(
        "Problema",
        back_populates="arquivos",
    )
