from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class ValidadorTeste(Base):
    __tablename__ = "validador_testes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    codigo = Column(
        String(length=64),
        nullable=False,
    )

    entrada = Column(
        String(length=250000),
        nullable=False,
    )

    validador_id = Column(Integer, ForeignKey('validadores.id'))
    validador = relationship(
        "Validador",
        uselist=False,
        foreign_keys=[validador_id],
        post_update=True,
    )

    __table_args__ = (
        UniqueConstraint('validador_id'),
    )
