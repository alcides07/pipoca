from fastapi import Query
from enum import Enum
from pydantic import BaseModel, Field


class LimitSchema(int, Enum):
    cinco = 5
    dez = 10
    quinze = 15
    vinte = 20
    vinte_cinco = 25
    cinquenta = 50
    cem = 100


class MetadataSchema(BaseModel):
    count: int = Field(
        description="Quantidade de registros retornados na consulta")
    limit: int = Field(description="Quantidade de registros desejados")
    offset: int = Field(description="Intervalo inicial da paginação")
    total: int = Field(
        description="Quantidade de registros existentes")


class Pagination_Schema:
    def __init__(
        self,
        q: str = Query(
            default=None, description="Palavras-chave para pesquisa"),
        limit: LimitSchema = Query(
            default=10, description="Quantidade de registros desejados"),
        offset: int = Query(
            default=0, description="Intervalo inicial da paginação"),

    ):
        self.q = q
        self.limit = limit
        self.offset = offset
