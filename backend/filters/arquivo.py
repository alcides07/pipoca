from fastapi import Query
from schemas.arquivo import SecaoEnum


class ArquivoFilter:
    def __init__(
        self,
        secao: SecaoEnum = Query(
            default=None,
            description="Grupo o qual o arquivo faz parte"
        )
    ):
        self.secao = secao
