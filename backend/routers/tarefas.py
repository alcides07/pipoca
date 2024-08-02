from dependencies.authenticated_user import get_authenticated_user
from fastapi import APIRouter, Depends, Query
from celery.result import AsyncResult
from schemas.tarefas import TarefaSchema

router = APIRouter(
    prefix="/tarefas",
    tags=["tarefas"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/",
            response_model=TarefaSchema,
            summary="Lista o estado de uma tarefa assíncrona"
            )
async def read(
    uuid: str = Query(description="Identificador da tarefa")
):
    task_result = AsyncResult(uuid)

    return TarefaSchema(
        uuid=uuid,
        status=task_result.status,
        resultado=task_result.result
    )
