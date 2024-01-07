from pydantic import BaseModel, Field
from schemas.arquivo import ArquivoCreate, ArquivoRead
from schemas.tag import TagRead
from schemas.declaracao import DeclaracaoCreate, DeclaracaoRead


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

    declaracoes: list[DeclaracaoRead] = Field(
        description="Declarações associadas ao problema")

    arquivos: list[ArquivoRead] = Field(
        description="Arquivos associados ao problema")

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
