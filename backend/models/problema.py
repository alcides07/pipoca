from datetime import datetime, timezone
from models.problemaResposta import ProblemaResposta
from models.problemaTeste import ProblemaTeste
from models.validador import Validador
from models.verificador import Verificador
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String, CheckConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from .relationships.problema_tag import problema_tag_relationship


class Problema(Base):
    __tablename__ = "problemas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(length=64),
        index=True,
        unique=True,
        nullable=False,
    )

    privado = Column(
        Boolean(),
        index=True,
        nullable=False,
    )

    nome_arquivo_entrada = Column(
        String(length=64),
        nullable=False,
    )

    nome_arquivo_saida = Column(
        String(length=64),
        nullable=False,
    )

    linguagens = Column(
        ARRAY(String()),
        nullable=False
    )

    tempo_limite = Column(
        Integer,
        CheckConstraint('tempo_limite >= 250'),
        CheckConstraint('tempo_limite <= 15000'),
        nullable=False,
    )

    memoria_limite = Column(
        Integer,
        CheckConstraint('memoria_limite >= 4'),
        CheckConstraint('memoria_limite <= 1024'),
        nullable=False,
    )

    criado_em = Column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    tags = relationship(
        "Tag",
        secondary=problema_tag_relationship,
        back_populates="problemas",
    )

    declaracoes = relationship(
        Declaracao,
        back_populates="problema",
    )

    arquivos = relationship(
        Arquivo,
        back_populates="problema"
    )

    testes = relationship(
        ProblemaTeste,
        back_populates="problema"
    )

    verificador_id = Column(
        Integer,
        ForeignKey(
            'verificadores.id',
            name="problemas_verificador_id_fkey",
            use_alter=True,
            ondelete='SET NULL'
        )
    )
    verificador = relationship(
        Verificador,
        uselist=False,
        foreign_keys=[verificador_id],
        passive_deletes=True
    )

    validador_id = Column(
        Integer,
        ForeignKey(
            'validadores.id',
            name="problemas_validador_id_fkey",
            use_alter=True,
            ondelete='SET NULL'
        )
    )
    validador = relationship(
        Validador,
        uselist=False,
        foreign_keys=[validador_id],
        passive_deletes=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            name="problemas_usuario_id_fkey",
            ondelete='SET NULL'
        )
    )
    usuario = relationship(
        "User",
        uselist=False,
        foreign_keys=[usuario_id],
        passive_deletes=True
    )

    respostas = relationship(
        ProblemaResposta,
        back_populates="problema"
    )

    __table_args__ = (
        UniqueConstraint('verificador_id'),
        UniqueConstraint('validador_id'),
    )
