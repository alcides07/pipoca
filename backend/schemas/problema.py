from pydantic import BaseModel, Field
from schemas.tag import Tag_Read


class Problema_Base(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do problema"
    )

    nome_arquivo_entrada: str = Field(
        max_length=64,
        description="Nome do arquivo de entrada do problema"
    )

    nome_arquivo_saida: str = Field(
        max_length=64,
        description="Nome do arquivo de saída do problema"
    )

    tempo_limite: int = Field(
        ge=250,
        le=150000,
        description="Tempo limite do problema (em milissegundos)"
    )

    memoria_limite: int = Field(
        ge=4,
        le=1024,
        description="Memória limite do problema (em megabytes)"
    )


class Problema_Create(Problema_Base):
    tags: list[str]


class Problema_Read(Problema_Base):
    id: int
    tags: list[Tag_Read]

    class Config:
        from_attributes = True
