from sqlalchemy import Column, Integer, String
from database import Base


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
