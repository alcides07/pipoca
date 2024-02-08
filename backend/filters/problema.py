from fastapi import Query


class ProblemaFilter:
    def __init__(
        self,
        privado: bool = Query(
            default=None,
            description="Privacidade do problema (privado/público)"
        ),
    ):
        self.privado = privado


search_fields_problema = ["nome"]
