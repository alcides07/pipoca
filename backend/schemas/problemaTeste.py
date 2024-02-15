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
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    id: int = Field(description=TESTE_ID_DESCRIPTION)


class ProblemaTesteReadSimple(ProblemaTesteBase):
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    id: int = Field(description=TESTE_ID_DESCRIPTION)


class ProblemaTesteCreate(ProblemaTesteBaseFull):
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    pass


class ProblemaTesteUpdateTotal(ProblemaTesteBaseFull):
    pass


class ProblemaTesteUpdatePartial(BaseModel):
    numero: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description="Código de numeração do teste"
    )

    tipo: Optional[TipoTesteProblemaEnum] = Field(
        default=None,
        description="Tipo do teste"
    )

    exemplo: Optional[bool] = Field(
        default=None,
        description="Define se o teste será ou não exibido na declaração do problema"
    )

    entrada: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Dados de entrada do teste"
    )

    descricao: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Descrição do teste"
    )
