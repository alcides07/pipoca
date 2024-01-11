from pydantic import BaseModel, Field

VERIFICADOR_ID_DESCRIPTION = "Identificador do verificador"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado ao verificador"


class VerificadorBase(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do verificador"
    )

    # Talvez Enum em breve
    linguagem: str = Field(
        description="Linguagem em que o verificador está escrito"
    )


class VerificadorWithBody(VerificadorBase):
    corpo: str = Field(
        max_length=250000,
        description="Conteúdo do verificador"
    )


class VerificadorReadFull(VerificadorWithBody):
    id: int = Field(description=VERIFICADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class VerificadorReadSimple(VerificadorBase):
    id: int = Field(description=VERIFICADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)

    class ConfigDict:
        from_attributes = True


class VerificadorCreate(VerificadorWithBody):
    pass
