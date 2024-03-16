from schemas.problemaTeste import TipoTesteProblemaEnum
from sqlalchemy import Boolean, CheckConstraint, Column, Enum, ForeignKey, Integer, String, UniqueConstraint
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
        Integer,
        CheckConstraint('numero >= 1'),
        CheckConstraint('numero <= 1000'),
        nullable=False,
    )

    tipo = Column(
        Enum(TipoTesteProblemaEnum),
        nullable=False,
    )

    entrada = Column(
        String(length=1000000),
        nullable=False,
    )

    exemplo = Column(
        Boolean(),
        nullable=False,
    )

    descricao = Column(
        String(length=250000)
    )

    problema_id = Column(
        Integer,
        ForeignKey(
            'problemas.id',
            name="problema_testes_problema_id_fkey"
        )
    )
    problema = relationship(
        "Problema",
        uselist=False,
        foreign_keys=[problema_id],
        post_update=True,
    )
