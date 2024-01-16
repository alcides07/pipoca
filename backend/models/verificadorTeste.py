from schemas.verificadorTeste import VereditoVerificadorTesteEnum
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Enum
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
        String(length=64),
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
