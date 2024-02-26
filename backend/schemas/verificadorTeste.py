from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

VERIFICADOR_TESTE_ID_DESCRIPTION = "Identificador do teste do verificador"
VERIFICADOR_ID_DESCRIPTION = "Identificador do verificador associado ao teste"


class VereditoVerificadorTesteEnum(Enum):
    OK = "ok"
    WA = "wrong-answer"
    PE = "presentation-error"
    CA = "crashed"


class VerificadorTesteBase(BaseModel):
    numero: int = Field(
        ge=1,
        le=1000,
        description="Código de numeração do teste"
    )

    veredito: VereditoVerificadorTesteEnum = Field(
        description="Status do veredíto esperado para o teste"
    )


class VerificadorTesteBaseFull(VerificadorTesteBase):
    entrada: str = Field(
        max_length=250000,
        description="Dados de entrada do teste do verificador"
    )


class VerificadorTesteReadFull(VerificadorTesteBaseFull):
    id: int = Field(
        description=VERIFICADOR_TESTE_ID_DESCRIPTION
    )

    verificador_id: int = Field(
        description=VERIFICADOR_ID_DESCRIPTION
    )


class VerificadorTesteReadSimple(VerificadorTesteBase):
    id: int = Field(
        description=VERIFICADOR_TESTE_ID_DESCRIPTION
    )

    verificador_id: int = Field(
        description=VERIFICADOR_ID_DESCRIPTION
    )

    class ConfigDict:
        from_attributes = True


class VerificadorTesteCreate(VerificadorTesteBaseFull):
    pass


class VerificadorTesteCreateSingle(VerificadorTesteBaseFull):
    verificador_id: int = Field(
        description=VERIFICADOR_ID_DESCRIPTION
    )


class VerificadorTesteUpdateTotal(VerificadorTesteBaseFull):
    pass


class VerificadorTesteUpdatePartial(VerificadorTesteBaseFull):
    numero: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description="Código de numeração do teste"
    )

    veredito: Optional[VereditoVerificadorTesteEnum] = Field(
        default=None,
        description="Status do veredíto esperado para o teste"
    )

    entrada: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Dados de entrada do teste do verificador"
    )
