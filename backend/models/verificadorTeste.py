from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
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
        String(),
        nullable=False
    )

    verificador_id = Column(
        Integer,
        ForeignKey(
            'verificadores.id',
            name="verificador_testes_verificador_id_fkey",
            ondelete='CASCADE'
        )
    )
    verificador = relationship(
        "Verificador",
        uselist=False,
        foreign_keys=[verificador_id],
        post_update=True
    )
