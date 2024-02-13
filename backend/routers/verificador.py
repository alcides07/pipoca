from orm.verificador import create_verificador, delete_verificador, update_verificador
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from models.problema import Problema
from models.verificador import Verificador
from orm.common.index import get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.verificador import VERIFICADOR_ID_DESCRIPTION, VerificadorCreateSingle, VerificadorReadFull, VerificadorReadSimple, VerificadorUpdatePartial, VerificadorUpdateTotal
from sqlalchemy.orm import Session
from utils.errors import errors

router = APIRouter(
    prefix="/verificadores",
    tags=["verificador"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[VerificadorReadSimple],
            summary="Lista verificadores",
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    verificadores, metadata = await get_all(
        db=db,
        model=Verificador,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=verificadores,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[VerificadorReadFull],
            summary="Lista um verificador",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description="Identificador do verificador"),
        db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    verificador = await get_by_id(
        db=db,
        model=Verificador,
        id=id,
        token=token,
        model_has_user_key=Problema
    )

    return ResponseUnitSchema(
        data=verificador
    )


@router.post("/",
             response_model=ResponseUnitSchema[VerificadorReadFull],
             status_code=201,
             summary="Cadastra um verificador",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             description="Ao cadastrar um verificador em um problema que já possui um, **o antigo é deletado juntamente com seus testes** e o problema é vinculado ao novo verificador."
             )
async def create(
    verificador: VerificadorCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_authenticated_user(token=token, db=db)

    verificador = await create_verificador(
        db=db,
        verificador=verificador,
        user=user,
    )

    return ResponseUnitSchema(data=verificador)


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[VerificadorReadFull],
              summary="Atualiza um verificador parcialmente",
              responses={
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=VERIFICADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: VerificadorUpdatePartial = Body(
            description="Verificador a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme),
):
    user = await get_authenticated_user(token, db)

    verificador = await update_verificador(
        db=db,
        id=id,
        verificador=data,
        user=user
    )
    return ResponseUnitSchema(
        data=verificador
    )


@router.put("/{id}/",
            response_model=ResponseUnitSchema[VerificadorReadFull],
            summary="Atualiza um verificador por completo",
            responses={
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=VERIFICADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: VerificadorUpdateTotal = Body(
            description="Verificador a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme),
):
    user = await get_authenticated_user(token, db)

    verificador = await update_verificador(
        db=db,
        id=id,
        verificador=data,
        user=user
    )
    return ResponseUnitSchema(
        data=verificador
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta um verificador",
               responses={
                   404: errors[404]
               }
               )
async def delete(
        id: int = Path(description=VERIFICADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):

    user = await get_authenticated_user(db=db, token=token)

    verificador_deleted = await delete_verificador(
        db=db,
        id=id,
        user=user
    )

    if (verificador_deleted):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
