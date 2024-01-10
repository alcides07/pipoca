from pydantic import BaseModel, Field
from enum import Enum


class SecaoSchema(Enum):
    RECURSO = "recursos"
    FONTE = "arquivos fonte"
    ANEXO = "anexo"


class ArquivoBase(BaseModel):

    nome: str = Field(
        max_length=64,
        description="Nome do arquivo do problema"
    )

    corpo: str = Field(
        max_length=250000,
        description="Conteúdo do arquivo"
    )

    secao: SecaoSchema = Field(
        description="Grupo o qual o arquivo faz parte"
    )


class ArquivoRead(ArquivoBase):
    id: int = Field(description="Identificador do arquivo")
    problema_id: int = Field(
        description="Identificador do problema associado ao arquivo")


class ArquivoReadSimple(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do arquivo do problema"
    )
    id: int = Field(description="Identificador do arquivo")
    problema_id: int = Field(
        description="Identificador do problema associado ao arquivo")


class ArquivoCreate(ArquivoBase):
    pass


class ArquivoCreateSingle(ArquivoBase):
    problema_id: int = Field(
        description="Identificador do problema associado ao arquivo")
