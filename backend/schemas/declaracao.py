from typing import Optional
from pydantic import BaseModel, Field
from schemas.idioma import IdiomaEnum

PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado à declaração"
DECLARACAO_ID_DESCRIPTION = "Identificador da declaração"


class DeclaracaoBase(BaseModel):
    titulo: str = Field(
        max_length=64,
        description="Título do problema"
    )

    idioma: IdiomaEnum = Field(
        description="Idioma em que o problema está escrito"
    )


class DeclaracaoBaseFull(DeclaracaoBase):
    contextualizacao: str = Field(
        max_length=10240,
        description="Contextualização do problema"
    )

    formatacao_entrada: str = Field(
        max_length=10240,
        description="Formatação da entrada do problema"
    )

    formatacao_saida: str = Field(
        max_length=10240,
        description="Formatação da saída do problema"
    )

    observacao: Optional[str] = Field(
        default=None,
        max_length=10240,
        description="Observações auxiliares acerca do problema"
    )

    tutorial: Optional[str] = Field(
        default=None,
        max_length=80240,
        description="Tutorial de resolução do problema"
    )


class DeclaracaoReadFull(DeclaracaoBaseFull):
    id: int = Field(
        description=DECLARACAO_ID_DESCRIPTION
    )

    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION
    )


class DeclaracaoReadSimple(DeclaracaoBase):
    id: int = Field(
        description=DECLARACAO_ID_DESCRIPTION
    )

    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION
    )


class DeclaracaoImagem(BaseModel):
    nome: str = Field(
        description="Nome da imagem da declaração"
    )

    conteudo: bytes = Field(
        description="Conteúdo da imagem da declaração"
    )


class DeclaracaoCreate(DeclaracaoBaseFull):
    imagens: list[DeclaracaoImagem] = Field(
        description="Imagens da declaração de um problema"
    )


class DeclaracaoCreateSingle(DeclaracaoBaseFull):
    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION
    )


class DeclaracaoUpdateTotal(DeclaracaoBaseFull):
    pass


class DeclaracaoUpdatePartial(DeclaracaoBaseFull):
    titulo: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Título do problema"
    )

    idioma: Optional[IdiomaEnum] = Field(
        default=None,
        description="Idioma em que o problema está escrito"
    )

    contextualizacao: Optional[str] = Field(
        default=None,
        max_length=10240,
        description="Contextualização do problema"
    )

    formatacao_entrada: Optional[str] = Field(
        default=None,
        max_length=10240,
        description="Formatação da entrada do problema"
    )

    formatacao_saida: Optional[str] = Field(
        default=None,
        max_length=10240,
        description="Formatação da saída do problema"
    )

    observacao: Optional[str] = Field(
        default=None,
        max_length=10240,
        description="Observações auxiliares acerca do problema"
    )

    tutorial: Optional[str] = Field(
        default=None,
        max_length=80240,
        description="Tutorial de resolução do problema"
    )
