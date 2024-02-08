from pydantic import BaseModel, Field
from schemas.validadorTeste import ValidadorTesteCreate, ValidadorTesteReadFull, ValidadorTesteReadSimple

VALIDADOR_ID_DESCRIPTION = "Identificador do validador"
VALIDADOR_TESTS_DESCRITPTION = "Lista de testes do validador"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado ao validador"


class ValidadorBase(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do validador"
    )

    # Talvez Enum em breve
    linguagem: str = Field(
        description="Linguagem em que o validador está escrito"
    )


class ValidadorWithBody(ValidadorBase):
    corpo: str = Field(
        max_length=250000,
        description="Conteúdo do validador"
    )


class ValidadorReadFull(ValidadorWithBody):
    id: int = Field(description=VALIDADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: list[ValidadorTesteReadFull] = Field(
        description=VALIDADOR_TESTS_DESCRITPTION)


class ValidadorReadSimple(ValidadorBase):
    id: int = Field(description=VALIDADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: list[ValidadorTesteReadSimple] = Field(
        description=VALIDADOR_TESTS_DESCRITPTION)

    class ConfigDict:
        from_attributes = True


class ValidadorCreate(ValidadorWithBody):
    testes: list[ValidadorTesteCreate] = Field(
        description=VALIDADOR_TESTS_DESCRITPTION)
