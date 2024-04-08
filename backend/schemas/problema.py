from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from schemas.arquivo import ArquivoCreate, ArquivoReadFull, ArquivoReadSimple
from schemas.problemaTeste import ProblemaTesteCreate, ProblemaTesteReadFull, ProblemaTesteReadSimple
from schemas.tag import TagRead
from schemas.declaracao import DeclaracaoCreate, DeclaracaoReadFull, DeclaracaoReadSimple
from schemas.user import UserReadSimple
from schemas.validador import ValidadorCreate, ValidadorReadFull, ValidadorReadSimple
from schemas.verificador import VerificadorCreate, VerificadorReadFull, VerificadorReadSimple

DECLARACAO_DESCRIPTION = "Declarações associadas ao problema"
VERIFICADOR_DESCRIPTION = "Arquivo verificador do problema"
VALIDADOR_DESCRIPTION = "Arquivo validador do problema"
ARQUIVOS_DESCRIPTION = "Arquivos associados ao problema"
TESTES_DESCRIPTION = "Testes associados ao problema"


class ProblemaBase(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do problema"
    )

    privado: bool = Field(
        description="Visibilidade de um problema"
    )

    nome_arquivo_entrada: str = Field(
        max_length=64,
        description="Nome do arquivo de entrada do problema"
    )

    nome_arquivo_saida: str = Field(
        max_length=64,
        description="Nome do arquivo de saída do problema"
    )

    tempo_limite: int = Field(
        ge=250,
        le=150000,
        description="Tempo limite do problema (em milissegundos)"
    )

    memoria_limite: int = Field(
        ge=4,
        le=1024,
        description="Memória limite do problema (em megabytes)"
    )


class ProblemaReadSimple(ProblemaBase):
    id: int = Field(
        description="Identificador do problema"
    )

    usuario: Optional[UserReadSimple] = Field(
        description="Criador do problema", default=None)

    tags: list[TagRead] = Field(
        description="Lista de palavras-chave"
    )

    declaracoes: list[DeclaracaoReadSimple] = Field(
        description=DECLARACAO_DESCRIPTION
    )

    criado_em: datetime = Field(
        description="Data e horário de criação do problema"
    )

    arquivos: list[ArquivoReadSimple] = Field(
        description=ARQUIVOS_DESCRIPTION
    )

    verificador: Optional[VerificadorReadSimple] = Field(
        default=None,
        description=VERIFICADOR_DESCRIPTION
    )

    validador: Optional[ValidadorReadSimple] = Field(
        default=None,
        description=VALIDADOR_DESCRIPTION
    )

    testes: list[ProblemaTesteReadSimple] = Field(
        description=TESTES_DESCRIPTION
    )

    class ConfigDict:
        from_attributes = True


class ProblemaReadFull(ProblemaBase):
    id: int = Field(
        description="Identificador do problema"
    )

    usuario: Optional[UserReadSimple] = Field(
        description="Criador do problema", default=None)

    tags: list[TagRead] = Field(
        description="Lista de palavras-chave"
    )

    criado_em: datetime = Field(
        description="Data e horário de criação do problema"
    )

    declaracoes: list[DeclaracaoReadFull] = Field(
        description=DECLARACAO_DESCRIPTION
    )

    testes: list[ProblemaTesteReadFull] = Field(
        description=TESTES_DESCRIPTION
    )

    class ConfigDict:
        from_attributes = True


class ProblemaCreate(ProblemaBase):
    pass


class ProblemaCreateUpload(ProblemaBase):
    tags: list[str] = Field(
        default=None,
        description="Palavras-chave utilizadas como etiquetas"
    )

    declaracoes: list[DeclaracaoCreate] = Field(
        description=DECLARACAO_DESCRIPTION
    )

    arquivos: list[ArquivoCreate] = Field(
        description=ARQUIVOS_DESCRIPTION
    )

    testes: list[ProblemaTesteCreate] = Field(
        description=TESTES_DESCRIPTION
    )

    verificador: VerificadorCreate = Field(
        description=VERIFICADOR_DESCRIPTION
    )

    validador: ValidadorCreate = Field(
        description=VALIDADOR_DESCRIPTION
    )


class ProblemaUpdateTotal(ProblemaBase):
    pass


class ProblemaUpdatePartial(BaseModel):
    nome: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Nome do problema"
    )

    nome_arquivo_entrada: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Nome do arquivo de entrada do problema"
    )

    nome_arquivo_saida: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Nome do arquivo de saída do problema"
    )

    tempo_limite: Optional[int] = Field(
        default=None,
        ge=250,
        le=150000,
        description="Tempo limite do problema (em milissegundos)"
    )

    memoria_limite: Optional[int] = Field(
        default=None,
        ge=4,
        le=1024,
        description="Memória limite do problema (em megabytes)"
    )


class ProblemaIntegridade(BaseModel):
    declaracoes: bool = Field(
        description=DECLARACAO_DESCRIPTION
    )

    arquivos: bool = Field(
        description=ARQUIVOS_DESCRIPTION
    )

    testes: bool = Field(
        description=TESTES_DESCRIPTION
    )

    verificador: bool = Field(
        description=VERIFICADOR_DESCRIPTION
    )

    validador: bool = Field(
        description=VALIDADOR_DESCRIPTION
    )
