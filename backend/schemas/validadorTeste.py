from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

VALIDADOR_TESTE_ID_DESCRIPTION = "Identificador do teste do validador"
VALIDADOR_ID_DESCRIPTION = "Identificador do validador associado ao teste"


class VereditoValidadorTesteEnum(Enum):
    VALID = "valid"
    INVALID = "invalid"


class ValidadorTesteBase(BaseModel):
    numero: int = Field(
        ge=1,
        le=1000,
        description="Código de numeração do teste"
    )

    veredito: VereditoValidadorTesteEnum = Field(
        description="Status do veredíto esperado para o teste"
    )


class ValidadorTesteBaseFull(ValidadorTesteBase):
    entrada: str = Field(
        max_length=250000,
        description="Dados de entrada do teste do validador"
    )


class ValidadorTesteReadFull(ValidadorTesteBaseFull):
    id: int = Field(
        description=VALIDADOR_TESTE_ID_DESCRIPTION
    )

    validador_id: int = Field(
        description=VALIDADOR_ID_DESCRIPTION
    )


class ValidadorTesteReadSimple(ValidadorTesteBase):
    id: int = Field(
        description=VALIDADOR_TESTE_ID_DESCRIPTION
    )

    validador_id: int = Field(
        description=VALIDADOR_ID_DESCRIPTION
    )

    class ConfigDict:
        from_attributes = True


class ValidadorTesteCreate(ValidadorTesteBaseFull):
    validador_id: int = Field(
        description=VALIDADOR_ID_DESCRIPTION
    )


class ValidadorTesteUpdatePartial(BaseModel):
    numero: Optional[int] = Field(
        default=None,
        ge=1,
        le=1000,
        description="Código de numeração do teste"
    )

    veredito: Optional[VereditoValidadorTesteEnum] = Field(
        default=None,
        description="Status do veredíto esperado para o teste"
    )

    entrada: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Dados de entrada do teste do validador"
    )


class ValidadorTesteUpdateTotal(ValidadorTesteBaseFull):
    pass
