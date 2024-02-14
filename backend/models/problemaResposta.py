from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base


class ProblemaResposta(Base):
    __tablename__ = "problema_respostas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resposta = Column(
        String(length=250000),
        nullable=False
    )

    respondido_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    tempo = Column(
        Integer,
        CheckConstraint('tempo >= 0'),
        nullable=False
    )

    memoria = Column(
        Integer,
        CheckConstraint('memoria >= 0'),
        nullable=False
    )

    linguagem = Column(
        String(),
        nullable=False
    )

    problema_id = Column(
        Integer,
        ForeignKey(
            'problemas.id',
            name="problema_respostas_problema_id_fkey"
        )
    )
    problema = relationship(
        "Problema",
        back_populates="respostas",
        uselist=False,
        foreign_keys=[problema_id],
        post_update=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            name="problema_respostas_usuario_id_fkey"
        )
    )
    usuario = relationship(
        "User",
        uselist=False,
        foreign_keys=[usuario_id],
        post_update=True
    )
