from models.problema import Problema
from orm.arquivo import create_arquivo, update_arquivo
from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, Path
from models.arquivo import Arquivo
from schemas.arquivo import ARQUIVO_ID_DESCRIPTION, ArquivoCreateSingle, ArquivoReadFull, ArquivoReadSimple, ArquivoUpdatePartial
from utils.errors import errors
from orm.common.index import delete_object, get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema


router = APIRouter(
    prefix="/arquivos",
    tags=["arquivo"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ArquivoReadSimple],
            summary="Lista arquivos",
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    arquivos, metadata = await get_all(
        db=db,
        model=Arquivo,
        pagination=pagination,
        token=token,
    )

    return ResponsePaginationSchema(
        data=arquivos,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ArquivoReadFull],
            summary="Lista um arquivo",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=ARQUIVO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    arquivo = await get_by_id(
        db=db,
        model=Arquivo,
        id=id,
        token=token,
        model_has_user_key=Problema
    )

    return ResponseUnitSchema(
        data=arquivo
    )


@router.post("/",
             response_model=ResponseUnitSchema[ArquivoReadFull],
             status_code=201,
             summary="Cadastra um arquivo",
             responses={
                 422: errors[422],
                 404: errors[404]
             }
             )
async def create(
    arquivo: ArquivoCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = await get_authenticated_user(token=token, db=db)

    arquivo = await create_arquivo(
        db=db,
        user=user,
        arquivo=arquivo,
    )

    return ResponseUnitSchema(data=arquivo)


@router.put("/{id}/",
            response_model=ResponseUnitSchema[ArquivoReadFull],
            summary="Atualiza um arquivo por completo",
            responses={
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=ARQUIVO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        arquivo: ArquivoCreateSingle = Body(
            description="Arquivo a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme),
):
    user = await get_authenticated_user(token, db)

    response = await update_arquivo(
        db=db,
        id=id,
        arquivo=arquivo,
        user=user
    )
    return ResponseUnitSchema(
        data=response
    )


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[ArquivoReadFull],
              summary="Atualiza um arquivo parcialmente",
              responses={
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=ARQUIVO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ArquivoUpdatePartial = Body(
            description="Arquivo a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme),
):
    user = await get_authenticated_user(token, db)

    response = await update_arquivo(
        db=db,
        id=id,
        arquivo=data,
        user=user
    )
    return ResponseUnitSchema(
        data=response
    )


@router.delete("/{id}/",
               response_model=ResponseUnitSchema[ArquivoReadFull],
               summary="Deleta um arquivo",
               responses={
                   404: errors[404]
               },
               dependencies=[Depends(get_authenticated_user)],
               )
async def delete(
        id: int = Path(description=ARQUIVO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):

    arquivo = await delete_object(
        db=db,
        model=Arquivo,
        id=id,
        token=token,
        model_has_user_key=Problema
    )
    return ResponseUnitSchema(
        data=arquivo
    )
