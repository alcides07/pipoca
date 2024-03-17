from typing import Optional
from pydantic import BaseModel, Field
from schemas.common.compilers import CompilersEnum
from schemas.validadorTeste import ValidadorTesteCreate, ValidadorTesteReadFull, ValidadorTesteReadSimple

VALIDADOR_ID_DESCRIPTION = "Identificador do validador"
VALIDADOR_TESTS_DESCRITPTION = "Lista de testes do validador"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado ao validador"


class ValidadorBase(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do validador"
    )

    linguagem: CompilersEnum = Field(
        description="Linguagem em que o validador está escrito"
    )


class ValidadorBaseFull(ValidadorBase):
    corpo: str = Field(
        max_length=250000,
        description="Conteúdo do validador"
    )


class ValidadorReadFull(ValidadorBaseFull):
    id: int = Field(description=VALIDADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: Optional[list[ValidadorTesteReadFull]] = Field(
        default=None,
        description=VALIDADOR_TESTS_DESCRITPTION)


class ValidadorReadSimple(ValidadorBase):
    id: int = Field(description=VALIDADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: Optional[list[ValidadorTesteReadSimple]] = Field(
        default=None,
        description=VALIDADOR_TESTS_DESCRITPTION)

    class ConfigDict:
        from_attributes = True


class ValidadorCreate(ValidadorBaseFull):
    testes: list[ValidadorTesteCreate] = Field(
        description=VALIDADOR_TESTS_DESCRITPTION)


class ValidadorCreateSingle(ValidadorBaseFull):
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class ValidadorUpdateTotal(ValidadorBaseFull):
    pass


class ValidadorUpdatePartial(BaseModel):
    nome: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Nome do validador"
    )

    # Talvez Enum em breve
    linguagem: Optional[str] = Field(
        default=None,
        description="Linguagem em que o validador está escrito"
    )

    corpo: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Conteúdo do validador"
    )
