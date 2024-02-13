from typing import Optional
from pydantic import BaseModel, Field
from schemas.idioma import IdiomaEnum


class DeclaracaoBase(BaseModel):

    titulo: str = Field(
        max_length=64,
        description="Título do problema"
    )

    contextualizacao: str = Field(
        max_length=10240,
        description="Contextualização do problema"
    )

    formatacao_entrada: str = Field(
        max_length=10240,
        description="Formatação da entrada do problema"
    )

    formatacao_saida: str = Field(
        max_length=10240,
        description="Formatação da saída do problema"
    )

    observacao: Optional[str] = Field(
        default=None,
        max_length=10240,
        description="Observações auxiliares acerca do problema"
    )

    tutorial: Optional[str] = Field(
        default=None,
        max_length=80240,
        description="Tutorial de resolução do problema"
    )

    idioma: IdiomaEnum = Field(
        description="Idioma em que o problema está escrito")


class DeclaracaoReadFull(DeclaracaoBase):
    id: int = Field(description="Identificador da declaração")
    problema_id: int = Field(
        description="Identificador do problema associado à declaração")


class DeclaracaoReadSimple(BaseModel):
    titulo: str = Field(
        max_length=64,
        description="Título do problema"
    )
    id: int = Field(description="Identificador da declaração")
    problema_id: int = Field(
        description="Identificador do problema associado à declaração")


class DeclaracaoCreate(DeclaracaoBase):
    pass
