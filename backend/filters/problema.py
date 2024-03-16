from enum import Enum
from fastapi import Query


search_fields_problema = ["nome"]


class OrderByFieldsProblemaEnum(Enum):
    NOME = "nome"
    CRIADO_EM = "criado_em"


class ProblemaFilter:
    def __init__(
        self,
        privado: bool = Query(
            default=None,
            description="Privacidade do problema (privado/público)"
        )
    ):
        self.privado = privado
