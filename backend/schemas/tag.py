from pydantic import BaseModel, Field


class Tag_Base(BaseModel):
    nome: str = Field(
        max_length=32,
        description="Palavra-chave utilizada como etiqueta"
    )


class Tag_Read(Tag_Base):
    id: int


class Tag_Create(Tag_Base):
    pass
