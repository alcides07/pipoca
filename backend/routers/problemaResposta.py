from constants import DIRECTION_ORDER_BY_DESCRIPTION, FIELDS_ORDER_BY_DESCRIPTION
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from dependencies.is_admin import is_admin_dependencies
from filters.problemaResposta import OrderByFieldsProblemaRespostaEnum, search_fields_problema_resposta
from models.problemaResposta import ProblemaResposta
from orm.problemaResposta import create_problema_resposta, get_problema_resposta_by_id
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from orm.common.index import get_all
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.problemaResposta import ProblemaRespostaCreate, ProblemaRespostaReadFull, ProblemaRespostaReadSimple
from sqlalchemy.orm import Session
from utils.errors import errors

PROBLEMA_RESPOSTA_ID_DESCRIPTION = "Identificador da resposta de um problema"

router = APIRouter(
    prefix="/problemaRespostas",
    tags=["problemaRespostas"],
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


@router.get("/users/",
            response_model=ResponsePaginationSchema[ProblemaRespostaReadFull],
            summary="Lista respostas fornecidas à problemas pelo usuário autenticado",
            )
async def read_problemas_respostas_me(
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
    )
):
    problemas, metadata = await get_all(
        db=db,
        model=ProblemaResposta,
        pagination=pagination,
        token=token,
        field_order_by=sort,
        direction=direction,
        search_fields=search_fields_problema_resposta,
        me_author=True
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ProblemaRespostaReadFull],
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
    return ResponseUnitSchema(
        data=problema_resposta
    )


@router.post("/",
             response_model=ResponseUnitSchema[ProblemaRespostaReadSimple],
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
    problema_resposta = await create_problema_resposta(
        db=db,
        problema_resposta=problema_resposta,
        token=token
    )

    return ResponseUnitSchema(data=problema_resposta)


@router.patch("/{id}/", deprecated=True)
async def parcial_update(
):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/{id}/",  deprecated=True)
async def total_update(
):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{id}/",  deprecated=True)
async def delete(
):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)
