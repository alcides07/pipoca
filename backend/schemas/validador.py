from pydantic import BaseModel, Field
from schemas.validadorTeste import ValidadorTesteCreate, ValidadorTesteReadFull, ValidadorTesteReadSimple

VALIDADOR_ID_DESCRIPTION = "Identificador do validador"
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
        description="Lista de testes do validador")


class ValidadorReadSimple(ValidadorBase):
    id: int = Field(description=VALIDADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: list[ValidadorTesteReadSimple] = Field(
        description="Lista de testes do validador")

    class ConfigDict:
        from_attributes = True


class ValidadorCreate(ValidadorWithBody):
    testes: list[ValidadorTesteCreate] = Field(
        description="Lista de testes do validador")
