from fastapi import Query
from enum import Enum
from pydantic import BaseModel


class Limit_Schema(int, Enum):
    cinco = 5
    dez = 10
    quinze = 15
    vinte = 20
    vinte_cinco = 25
    cinquenta = 50
    cem = 100


class Metadata_Schema(BaseModel):
    count: int
    limit: int
    offset: int


class Pagination_Schema:
    def __init__(
        self,
        q: str = Query(
            default=None, description="Palavras-chave para pesquisa"),
        limit: Limit_Schema = Query(
            default=10, description="Número de registros da paginação"),
        offset: int = Query(
            default=0, description="Intervalo inicial da paginação"),

    ):
        self.q = q
        self.limit = limit
        self.offset = offset
