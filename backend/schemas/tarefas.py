from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class TarefaStatus(Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    RETRY = "RETRY"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"


class TarefaIdSchema(BaseModel):
    task_uuid: str = Field(
        description="Identificador da tarefa"
    )


class TarefaSchema(BaseModel):
    uuid: str = Field(
        description="Identificador da tarefa"
    )

    status: TarefaStatus = Field(
        description="Status da tarefa"
    )

    resultado: Any = Field(
        description="Resultado da tarefa"
    )
