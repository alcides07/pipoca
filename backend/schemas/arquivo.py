from pydantic import BaseModel, Field
from enum import Enum

ARQUIVO_ID_DESCRIPTION = "identificador do arquivo"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado ao arquivo"


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
    id: int = Field(description=ARQUIVO_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class ArquivoReadSimple(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do arquivo do problema"
    )
    id: int = Field(description=ARQUIVO_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class ArquivoCreate(ArquivoBase):
    pass


class ArquivoCreateSingle(ArquivoBase):
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
