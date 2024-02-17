from orm.verificador import create_verificador, get_testes_verificador, update_verificador
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from models.problema import Problema
from models.verificador import Verificador
from orm.common.index import delete_object, get_all, get_by_id
from routers.verificadorTeste import VERIFICADOR_TESTE_ID_DESCRIPTION
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.verificador import VERIFICADOR_ID_DESCRIPTION, VerificadorCreateSingle, VerificadorReadFull, VerificadorReadSimple, VerificadorUpdatePartial, VerificadorUpdateTotal
from sqlalchemy.orm import Session
from schemas.verificadorTeste import VerificadorTesteReadFull
from utils.errors import errors

router = APIRouter(
    prefix="/verificadores",
    tags=["verificadores"],
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
        path_has_user_key="problema"
    )

    return ResponseUnitSchema(
        data=verificador
    )


@router.get("/{id}/testes/",
            response_model=ResponsePaginationSchema[VerificadorTesteReadFull],
            summary="Lista testes pertencentes a um verificador",
            responses={
                404: errors[404]
            }
            )
async def read_verificador_id_testes(
        id: int = Path(description=VERIFICADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    testes_verificador, metadata = await get_testes_verificador(
        db=db,
        pagination=pagination,
        id=id,
        token=token
    )

    return ResponsePaginationSchema(
        data=testes_verificador,
        metadata=metadata
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
    verificador = await create_verificador(
        db=db,
        verificador=verificador,
        token=token,
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
    verificador = await update_verificador(
        db=db,
        id=id,
        verificador=data,
        token=token
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
    verificador = await update_verificador(
        db=db,
        id=id,
        verificador=data,
        token=token
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

    verificador = await delete_object(
        db=db,
        model=Verificador,
        id=id,
        token=token,
        path_has_user_key="problema"
    )

    if (verificador):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
