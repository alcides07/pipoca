from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship
from .relationships.problema_tag import problema_tag_relationship


class Tag(Base):
    __tablename__ = "tags"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(length=32),
        index=True
    )

    problemas = relationship(
        "Problema",
        secondary=problema_tag_relationship,
        back_populates="tags",
    )
