from pydantic import BaseModel, Field
from schemas.arquivo import ArquivoCreate, ArquivoReadSimple
from schemas.tag import TagRead
from schemas.declaracao import DeclaracaoCreate, DeclaracaoReadSimple
from schemas.validador import ValidadorCreate, ValidadorReadSimple
from schemas.verificador import VerificadorCreate, VerificadorReadSimple


class ProblemaBase(BaseModel):
    nome: str = Field(
        max_length=64,
        description="Nome do problema"
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


class ProblemaRead(ProblemaBase):
    id: int = Field(description="Identificador do problema")

    tags: list[TagRead] = Field(description="Lista de palavras-chave")

    declaracoes: list[DeclaracaoReadSimple] = Field(
        description="Declarações associadas ao problema")

    arquivos: list[ArquivoReadSimple] = Field(
        description="Arquivos associados ao problema")

    verificador: VerificadorReadSimple = Field(
        description="Arquivo verificador do problema"
    )

    validador: ValidadorReadSimple = Field(
        description="Arquivo validador do problema"
    )

    class ConfigDict:
        from_attributes = True


class ProblemaCreate(ProblemaBase):
    tags: list[str] = Field(default=None,
                            description="Palavras-chave utilizadas como etiquetas"
                            )

    declaracoes: list[DeclaracaoCreate] = Field(
        description="Declarações associadas ao problema")

    arquivos: list[ArquivoCreate] = Field(
        description="Arquivos associados ao problema")

    verificador: VerificadorCreate = Field(
        description="Arquivo verificador do problema"
    )

    validador: ValidadorCreate = Field(
        description="Arquivo validador do problema"
    )
