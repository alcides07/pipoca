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
    numero: str = Field(
        max_length=64,
        description="Código de numeração do teste"
    )

    veredito: VereditoVerificadorTesteEnum = Field(
        description="Status do veredíto esperado para o teste"
    )


class VerificadorTesteWithEntrada(VerificadorTesteBase):
    entrada: str = Field(
        max_length=250000,
        description="Dados de entrada do teste do verificador"
    )


class VerificadorTesteReadFull(VerificadorTesteWithEntrada):
    id: int = Field(description=VERIFICADOR_TESTE_ID_DESCRIPTION)
    verificador_id: int = Field(
        description=VERIFICADOR_ID_DESCRIPTION)


class VerificadorTesteReadSimple(VerificadorTesteBase):
    id: int = Field(description=VERIFICADOR_TESTE_ID_DESCRIPTION)
    verificador_id: int = Field(
        description=VERIFICADOR_ID_DESCRIPTION)

    class ConfigDict:
        from_attributes = True


class VerificadorTesteCreate(VerificadorTesteWithEntrada):
    pass
