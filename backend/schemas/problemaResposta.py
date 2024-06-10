from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from schemas.common.compilers import CompilersEnum
from schemas.tarefas import TarefaIdSchema
from schemas.user import UserReadSimple

PROBLEMA_RESPOSTA_ID_DESCRIPTION = "Identificador da resposta do problema"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado à resposta"


class VereditoEnum(Enum):
    OK = "ok"
    WA = "wrong"
    FA = "fail"
    PE = "presentation"
    PC = "partially"


class ProblemaRespostaBase(BaseModel):
    resposta: str = Field(
        max_length=250000,
        description="Resposta fornecida para o problema"
    )

    linguagem: CompilersEnum = Field(
        description="Linguagem de programação em que a resposta está escrita"
    )

    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION
    )


class ProblemaRespostaBaseFull(ProblemaRespostaBase):
    respondido_em: datetime = Field(
        description="Data e horário em que a resposta foi submetida"
    )

    veredito: list[VereditoEnum] = Field(
        description="Veredítos da submissão da resposta."
    )

    saida_usuario: list[str] = Field(
        description="Resultados da execução do código do usuário"
    )

    saida_esperada: list[str] = Field(
        description="Resultados esperados para a resposta do problema"
    )

    erro: Optional[str] = Field(
        default=None,
        description="Erro gerado durante a execução do código do usuário"
    )


class ProblemaRespostaReadFull(ProblemaRespostaBaseFull):
    id: int = Field(
        description=PROBLEMA_RESPOSTA_ID_DESCRIPTION
    )

    usuario: UserReadSimple = Field(
        description="Usuário autor da resposta"
    )

    tempo: int = Field(
        ge=0,
        description="Tempo de execução do código de resposta"
    )

    memoria: int = Field(
        ge=0,
        description="Memória utilizada durante a execução do código de resposta"
    )


class ProblemaRespostaReadSimple(ProblemaRespostaBaseFull):
    id: int = Field(
        description=PROBLEMA_RESPOSTA_ID_DESCRIPTION
    )

    usuario_id: Optional[int] = Field(
        default=None,
        description="Identificador do autor da resposta"
    )


class ProblemaRespostaCreate(ProblemaRespostaBase):
    pass
