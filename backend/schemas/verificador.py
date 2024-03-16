from typing import Optional
from pydantic import BaseModel, Field
from schemas.verificadorTeste import VerificadorTesteCreate, VerificadorTesteReadFull, VerificadorTesteReadSimple
from schemas.common.compilers import CompilersEnum

VERIFICADOR_ID_DESCRIPTION = "Identificador do verificador"
VERIFICADOR_TESTS_DESCRITPTION = "Lista de testes do verificador"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado ao verificador"


class VerificadorBase(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do verificador"
    )

    linguagem: CompilersEnum = Field(
        description="Linguagem em que o verificador está escrito"
    )


class VerificadorBaseFull(VerificadorBase):
    corpo: str = Field(
        max_length=250000,
        description="Conteúdo do verificador"
    )


class VerificadorReadFull(VerificadorBaseFull):
    id: int = Field(description=VERIFICADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: Optional[list[VerificadorTesteReadFull]] = Field(
        default=None,
        description=VERIFICADOR_TESTS_DESCRITPTION
    )


class VerificadorReadSimple(VerificadorBase):
    id: int = Field(description=VERIFICADOR_ID_DESCRIPTION)
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)
    testes: Optional[list[VerificadorTesteReadSimple]] = Field(
        default=None,
        description=VERIFICADOR_TESTS_DESCRITPTION
    )

    class ConfigDict:
        from_attributes = True


class VerificadorCreate(VerificadorBaseFull):
    testes: list[VerificadorTesteCreate] = Field(
        description=VERIFICADOR_TESTS_DESCRITPTION)


class VerificadorCreateSingle(VerificadorBaseFull):
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION)


class VerificadorUpdateTotal(VerificadorBaseFull):
    pass


class VerificadorUpdatePartial(BaseModel):
    nome: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Nome do verificador"
    )

    # Talvez Enum em breve
    linguagem: Optional[str] = Field(
        default=None,
        description="Linguagem em que o verificador está escrito"
    )

    corpo: Optional[str] = Field(
        default=None,
        max_length=250000,
        description="Conteúdo do verificador"
    )
