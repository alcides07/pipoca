from pydantic import BaseModel, Field

VALIDADOR_TESTE_ID_DESCRIPTION = "Identificador do teste do validador"
VALIDADOR_ID_DESCRIPTION = "Identificador do validador associado ao teste"


class ValidadorTesteBase(BaseModel):
    numero: str = Field(
        max_length=64,
        description="Código de numeração do teste"
    )


class ValidadorTesteWithEntrada(ValidadorTesteBase):
    entrada: str = Field(
        max_length=250000,
        description="Dados de entrada do teste do validador"
    )


class ValidadorTesteReadFull(ValidadorTesteWithEntrada):
    id: int = Field(description=VALIDADOR_TESTE_ID_DESCRIPTION)
    validador_id: int = Field(
        description=VALIDADOR_ID_DESCRIPTION)


class ValidadorTesteReadSimple(ValidadorTesteBase):
    id: int = Field(description=VALIDADOR_TESTE_ID_DESCRIPTION)
    validador_id: int = Field(
        description=VALIDADOR_ID_DESCRIPTION)

    class ConfigDict:
        from_attributes = True


class ValidadorTesteCreate(ValidadorTesteWithEntrada):
    pass
