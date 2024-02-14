from fastapi import APIRouter, Depends, HTTPException, status
from orm.problemaResposta import create_problema_resposta
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from orm.common.index import delete_object, get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.problemaResposta import ProblemaRespostaCreate, ProblemaRespostaReadFull
from sqlalchemy.orm import Session
from utils.errors import errors

router = APIRouter(
    prefix="/problemaRespostas",
    tags=["problemaRespostas"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/", deprecated=True)
async def read(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/{id}/", deprecated=True)
async def read_id(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post("/",
             response_model=ResponseUnitSchema[ProblemaRespostaReadFull],
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
    user = await get_authenticated_user(token=token, db=db)

    problema_resposta = await create_problema_resposta(
        db=db,
        problema_resposta=problema_resposta,
        user=user
    )

    return ResponseUnitSchema(data=problema_resposta)


@router.patch("/{id}/", deprecated=True)
async def parcial_update(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/{id}/",  deprecated=True)
async def total_update(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{id}/",  deprecated=True)
async def delete(
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
