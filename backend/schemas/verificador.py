from pydantic import BaseModel, Field
from schemas.verificadorTeste import VerificadorTesteCreate, VerificadorTesteReadFull, VerificadorTesteReadSimple

VERIFICADOR_ID_DESCRIPTION = "Identificador do verificador"
VERIFICADOR_TESTS_DESCRITPTION = "Lista de testes do verificador"
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
    testes: list[VerificadorTesteReadFull] = Field(
        description=VERIFICADOR_TESTS_DESCRITPTION)


class VerificadorReadSimple(VerificadorBase):
    id: int = Field(description=VERIFICADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: list[VerificadorTesteReadSimple] = Field(
        description=VERIFICADOR_TESTS_DESCRITPTION)

    class ConfigDict:
        from_attributes = True


class VerificadorCreate(VerificadorWithBody):
    testes: list[VerificadorTesteCreate] = Field(
        description=VERIFICADOR_TESTS_DESCRITPTION)
