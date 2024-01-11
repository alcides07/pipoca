from models.verificador import Verificador
from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint, UniqueConstraint
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

    verificador_id = Column(Integer, ForeignKey('verificadores.id'))

    verificador = relationship(
        Verificador,
        uselist=False,
        foreign_keys=[verificador_id],
    )

    __table_args__ = (
        UniqueConstraint('verificador_id'),
    )
