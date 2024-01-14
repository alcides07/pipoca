from typing import Optional
from fastapi import Query
from enum import Enum
from pydantic import BaseModel, Field


class LimitSchema(int, Enum):
    CINCO = 5
    DEZ = 10
    QUINZE = 15
    VINTE = 20
    VINTE_CINCO = 25
    CINQUENTA = 50
    CEM = 100


class MetadataSchema(BaseModel):
    count: int = Field(
        description="Quantidade de registros retornados na consulta")
    limit: int = Field(description="Quantidade de registros desejados")
    offset: int = Field(description="Intervalo inicial da paginação")
    total: int = Field(
        description="Quantidade de registros existentes")


class PaginationSchema:
    def __init__(
        self,
        q: Optional[str] = Query(default=None,
                                 description="Palavras-chave para pesquisa"),
        limit: LimitSchema = Query(
            default=10, description="Quantidade de registros desejados"),
        offset: int = Query(
            default=0, description="Intervalo inicial da paginação"),

    ):
        self.q = q
        self.limit = limit
        self.offset = offset
