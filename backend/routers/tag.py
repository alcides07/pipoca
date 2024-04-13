from constants import DIRECTION_ORDER_BY_DESCRIPTION, FIELDS_ORDER_BY_DESCRIPTION
from dependencies.is_admin import is_admin_dependencies
from models.tag import Tag
from orm.tag import create_tag
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Query, Response, status
from orm.common.index import delete_object_simple, get_all, get_by_id_simple, update_object_simple
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitRequiredSchema
from sqlalchemy.orm import Session
from schemas.tag import TagBase, TagCreate, TagRead
from utils.errors import errors
from filters.tag import OrderByFieldsTagEnum, search_fields_tag

TAG_ID_DESCRIPTION = "Identificador da tag"


router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/",
            response_model=ResponsePaginationSchema[TagRead],
            summary="Lista tags"
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        sort: OrderByFieldsTagEnum = Query(
            default=None,
            description=FIELDS_ORDER_BY_DESCRIPTION
        ),
        direction: DirectionOrderByEnum = Query(
            default=None,
            description=DIRECTION_ORDER_BY_DESCRIPTION
        )
):
    tags, metadata = await get_all(
        db=db,
        model=Tag,
        pagination=pagination,
        search_fields=search_fields_tag,
        field_order_by=sort,
        direction=direction
    )

    return ResponsePaginationSchema(
        data=tags,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitRequiredSchema[TagRead],
            summary="Lista uma tag",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=TAG_ID_DESCRIPTION),
        db: Session = Depends(get_db)
):
    tag = await get_by_id_simple(
        db=db,
        id=id,
        model=Tag
    )
    return ResponseUnitRequiredSchema(
        data=tag
    )


@router.post("/",
             response_model=ResponseUnitRequiredSchema[TagRead],
             status_code=201,
             summary="Cadastra uma tag",
             responses={
                 422: errors[422]
             }
             )
async def create(
    tag: TagCreate = Body(description="Tag a ser criada"),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    data = await create_tag(
        db=db,
        tag=tag,
        token=token
    )
    return ResponseUnitRequiredSchema(data=data)


@router.patch("/{id}/",
              response_model=ResponseUnitRequiredSchema[TagRead],
              summary="Atualiza uma tag parcialmente",
              responses={
                  404: errors[404]
              },
              dependencies=[Depends(is_admin_dependencies)]
              )
async def partial_update(
        id: int = Path(description=TAG_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: TagBase = Body(
            description="Tag a ser atualizada parcialmente")
):
    tag = await update_object_simple(
        db=db,
        id=id,
        model=Tag,
        data=data
    )
    return ResponseUnitRequiredSchema(
        data=tag
    )


@router.put("/{id}/",
            response_model=ResponseUnitRequiredSchema[TagRead],
            summary="Atualiza uma tag por completo",
            responses={
                404: errors[404]
            },
            dependencies=[Depends(is_admin_dependencies)]
            )
async def total_update(
        id: int = Path(description=TAG_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: TagBase = Body(
            description="Tag a ser atualizada por completo")
):
    tag = await update_object_simple(
        db=db,
        id=id,
        model=Tag,
        data=data
    )
    return ResponseUnitRequiredSchema(
        data=tag
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta uma tag",
               responses={
                   404: errors[404]
               },
               dependencies=[Depends(is_admin_dependencies)]
               )
async def delete(
        id: int = Path(description=TAG_ID_DESCRIPTION),
        db: Session = Depends(get_db)
):
    tag = await delete_object_simple(
        db=db,
        model=Tag,
        id=id
    )

    if (tag):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
