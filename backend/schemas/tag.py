from typing import Optional
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    nome: str = Field(
        max_length=32,
        description="Palavra-chave utilizada como etiqueta"
    )


class TagRead(TagBase):
    id: int


class TagCreate(TagBase):
    problema_id: Optional[int] = Field(
        default=None,
        description="Problema a ser associado com a tag"
    )
