from fastapi import Query


class ProblemaTesteFilter:
    def __init__(
        self,
        exemplo: bool = Query(
            default=None,
            description="Teste que é exibido na declaração do problema"
        )
    ):
        self.exemplo = exemplo
