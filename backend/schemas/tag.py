from pydantic import BaseModel, Field


class TagBase(BaseModel):
    nome: str = Field(
        max_length=32,
        description="Palavra-chave utilizada como etiqueta"
    )


class Tag_Read(TagBase):
    id: int


class Tag_Create(TagBase):
    pass
