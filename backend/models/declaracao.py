from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship
from schemas.idioma import IdiomaSchema


class Declaracao(Base):
    __tablename__ = "declaracoes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo = Column(
        String(length=64),
        index=True,
        nullable=False,
    )

    contextualizacao = Column(
        String(length=10240),
        nullable=False,
    )

    formatacao_entrada = Column(
        String(length=10240),
        nullable=False,
    )

    formatacao_saida = Column(
        String(length=10240),
        nullable=False,
    )

    observacao = Column(
        String(length=10240),
    )

    tutorial = Column(
        String(length=80240),
    )

    problema_id = Column(Integer, ForeignKey('problemas.id'))
    problema = relationship(
        "Problema",
        back_populates="declaracoes",
    )

    idioma = Column(Enum(IdiomaSchema))
