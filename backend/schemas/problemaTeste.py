from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

TESTE_ID_DESCRIPTION = "Identificador do teste"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado ao teste"


class TipoTesteProblemaEnum(Enum):
    MANUAL = "manual"
    GERADO = "gerado"


class ProblemaTesteBase(BaseModel):
    numero: int = Field(
        ge=1,
        le=1000,
        description="Código de numeração do teste"
    )

    tipo: TipoTesteProblemaEnum = Field(
        description="Tipo do teste"
    )

    exemplo: bool = Field(
        description="Define se o teste será ou não exibido na declaração do problema"
    )


class ProblemaTesteBaseFull(ProblemaTesteBase):
    entrada: str = Field(
        max_length=250000,
        description="Dados de entrada do teste"
    )

    descricao: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Descrição do teste"
    )


class ProblemaTesteReadFull(ProblemaTesteBaseFull):
    id: int = Field(description=TESTE_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class ProblemaTesteReadSimple(ProblemaTesteBase):
    id: int = Field(description=TESTE_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class ProblemaTesteCreate(ProblemaTesteBaseFull):
    pass
