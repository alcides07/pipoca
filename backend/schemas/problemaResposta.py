from datetime import datetime
from pydantic import BaseModel, Field

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


class ProblemaRespostaReadFull(ProblemaRespostaBase):
    id: int = Field(
        description=PROBLEMA_RESPOSTA_ID_DESCRIPTION
    )

    respondido_em: datetime = Field(
        description="Data e horário em que a resposta foi submetida"
    )


class ProblemaRespostaCreate(ProblemaRespostaBase):
    pass
