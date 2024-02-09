from schemas.problemaTeste import TipoTesteProblemaEnum
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class ProblemaTeste(Base):
    __tablename__ = "problema_testes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    numero = Column(
        String(length=64),
        nullable=False,
    )

    tipo = Column(
        Enum(TipoTesteProblemaEnum),
        nullable=False,
    )

    entrada = Column(
        String(length=250000),
        nullable=False,
    )

    exemplo = Column(
        Boolean(),
        nullable=False,
    )

    descricao = Column(
        String(length=250000)
    )

    problema_id = Column(Integer, ForeignKey('problemas.id'))
    problema = relationship(
        "Problema",
        uselist=False,
        foreign_keys=[problema_id],
        post_update=True,
    )
