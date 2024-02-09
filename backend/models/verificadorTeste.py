from schemas.verificadorTeste import VereditoVerificadorTesteEnum
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base


class VerificadorTeste(Base):
    __tablename__ = "verificador_testes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    numero = Column(
        Integer,
        CheckConstraint('numero >= 1'),
        CheckConstraint('numero <= 1000'),
        nullable=False
    )

    entrada = Column(
        String(length=250000),
        nullable=False
    )

    veredito = Column(
        Enum(VereditoVerificadorTesteEnum),
        nullable=False
    )

    verificador_id = Column(Integer, ForeignKey('verificadores.id'))
    verificador = relationship(
        "Verificador",
        uselist=False,
        foreign_keys=[verificador_id],
        post_update=True,
    )
