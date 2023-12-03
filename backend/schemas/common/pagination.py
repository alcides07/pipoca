from fastapi import Query


class pagination_schema:
    def __init__(
        self,
        q: str = Query(
            default=None, description="Palavras-chave para pesquisa"),
        skip: int = Query(
            default=None, description="Intervalo inicial da paginação"),
        limit: str = Query(
            default=None, description="Número de registros da paginação")

    ):
        self.q = q
        self.skip = skip
        self.limit = limit
