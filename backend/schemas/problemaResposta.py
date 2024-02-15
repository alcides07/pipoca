from datetime import datetime
from pydantic import BaseModel, Field
from schemas.user import UserReadSimple

PROBLEMA_RESPOSTA_ID_DESCRIPTION = "Identificador da resposta do problema"
PROBLEMA_ID_DESCRIPTION = "Identificador do problema associado à resposta"


class ProblemaRespostaBase(BaseModel):
    resposta: str = Field(
        max_length=250000,
        description="Resposta fornecida para o problema"
    )

    tempo: int = Field(
        ge=0,
        description="Tempo de execução do código de resposta"

    )

    memoria: int = Field(
        ge=0,
        description="Memória utilizada durante a execução do código de resposta"
    )

    linguagem: str = Field(
        description="Linguagem de programação em que a resposta está escrita"
    )

    problema_id: int = Field(
        description=PROBLEMA_ID_DESCRIPTION
    )


class ProblemaRespostaBaseFull(ProblemaRespostaBase):
    respondido_em: datetime = Field(
        description="Data e horário em que a resposta foi submetida"
    )


class ProblemaRespostaReadFull(ProblemaRespostaBaseFull):
    id: int = Field(
        description=PROBLEMA_RESPOSTA_ID_DESCRIPTION
    )

    usuario: UserReadSimple = Field(
        description="Usuário autor da resposta"
    )


class ProblemaRespostaReadSimple(ProblemaRespostaBaseFull):
    id: int = Field(
        description=PROBLEMA_RESPOSTA_ID_DESCRIPTION
    )

    usuario_id: int = Field(
        description="Identificador do autor da resposta"
    )


class ProblemaRespostaCreate(ProblemaRespostaBase):
    pass
