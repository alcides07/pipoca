from constants import DIRECTION_ORDER_BY_DESCRIPTION, FIELDS_ORDER_BY_DESCRIPTION
from enviroments import ENV
from fastapi import APIRouter, Depends, Path, Query
from dependencies.is_admin import is_admin_dependencies
from filters.problemaResposta import OrderByFieldsProblemaRespostaEnum, search_fields_problema_resposta
from models.problemaResposta import ProblemaResposta
from orm.problemaResposta import create_problema_resposta, get_problema_id_respostas_by_user, get_problemas_respostas_by_user, get_problema_resposta_by_id
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from orm.common.index import get_all
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitRequiredSchema
from schemas.problemaResposta import ProblemaRespostaCreate, ProblemaRespostaReadFull, ProblemaRespostaReadSimple
from sqlalchemy.orm import Session
from schemas.tarefas import TarefaIdSchema
from utils.errors import errors

PROBLEMA_RESPOSTA_ID_DESCRIPTION = "Identificador da resposta de um problema"

router = APIRouter(
    prefix="/problemasRespostas",
    tags=["problemasRespostas"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/",
            response_model=ResponsePaginationSchema[ProblemaRespostaReadSimple],
            summary="Lista respostas de problemas",
            dependencies=[Depends(is_admin_dependencies)]
            )
async def read(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    sort: OrderByFieldsProblemaRespostaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    )
):
    respostas_problema, metadata = await get_all(
        model=ProblemaResposta,
        db=db,
        pagination=pagination,
        search_fields=search_fields_problema_resposta,
        field_order_by=sort,
        direction=direction
    )

    return ResponsePaginationSchema(
        data=respostas_problema,
        metadata=metadata
    )


@router.get("/usuarios/{id}/",
            response_model=ResponsePaginationSchema[ProblemaRespostaReadFull],
            summary="Lista respostas fornecidas à problemas por um usuário",
            )
async def read_problemas_respostas_by_user(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    token: str = Depends(oauth2_scheme),
    sort: OrderByFieldsProblemaRespostaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    ),
    id: int = Path(description="Identificador do usuário")
):
    problemas_respostas, metadata = await get_problemas_respostas_by_user(
        db=db,
        pagination=pagination,
        token=token,
        field_order_by=sort,
        direction=direction,
        id=id
    )

    return ResponsePaginationSchema(
        data=problemas_respostas,
        metadata=metadata
    )


@router.get("/problemas/{idProblema}/usuarios/{idUsuario}/",
            response_model=ResponsePaginationSchema[ProblemaRespostaReadFull],
            summary="Lista respostas fornecidas por um usuário a um problema específico",
            )
async def read_problema_id_respostas_by_user(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    token: str = Depends(oauth2_scheme),
    sort: OrderByFieldsProblemaRespostaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    ),
    idProblema: int = Path(description="Identificador do problema"),
    idUsuario: int = Path(description="Identificador do usuário")
):
    problemas_respostas, metadata = await get_problema_id_respostas_by_user(
        db=db,
        pagination=pagination,
        token=token,
        field_order_by=sort,
        direction=direction,
        id_problema=idProblema,
        id_usuario=idUsuario
    )

    return ResponsePaginationSchema(
        data=problemas_respostas,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitRequiredSchema[ProblemaRespostaReadFull],
            summary="Lista uma resposta específica fornecida para um problema",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=PROBLEMA_RESPOSTA_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    problema_resposta = await get_problema_resposta_by_id(
        db=db,
        id=id,
        token=token,
    )
    return ResponseUnitRequiredSchema(
        data=problema_resposta
    )


@router.post("/",
             response_model=ResponseUnitRequiredSchema[
                 TarefaIdSchema |
                 ProblemaRespostaReadSimple
             ],
             status_code=201,
             summary="Cadastra uma resposta para um problema",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             )
async def create(
    problema_resposta: ProblemaRespostaCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    problema_resposta_or_uuid = await create_problema_resposta(
        db=db,
        problema_resposta=problema_resposta,
        token=token
    )

    if (ENV != "test"):
        return ResponseUnitRequiredSchema(
            data=TarefaIdSchema(task_uuid=problema_resposta_or_uuid)
        )

    return ResponseUnitRequiredSchema(
        data=problema_resposta_or_uuid
    )
