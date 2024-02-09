from schemas.validadorTeste import VereditoValidadorTesteEnum
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base


class ValidadorTeste(Base):
    __tablename__ = "validador_testes"

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

    entrada = Column(
        String(length=250000),
        nullable=False,
    )

    veredito = Column(
        Enum(VereditoValidadorTesteEnum),
        nullable=False
    )

    validador_id = Column(Integer, ForeignKey('validadores.id'))
    validador = relationship(
        "Validador",
        uselist=False,
        foreign_keys=[validador_id],
        post_update=True,
    )
