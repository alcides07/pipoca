from models.declaracao import Declaracao
from orm.declaracao import create_declaracao, get_declaracao_by_id, update_declaracao
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from models.problema import Problema
from orm.common.index import delete_object, get_all
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.declaracao import DeclaracaoCreateSingle, DeclaracaoReadFull, DeclaracaoReadSimple, DeclaracaoUpdatePartial, DeclaracaoUpdateTotal
from sqlalchemy.orm import Session
from utils.errors import errors

DECLARACAO_ID_DESCRIPTION = "Identificador da declaração de um problema"

router = APIRouter(
    prefix="/declaracoes",
    tags=["declarações"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/",
            response_model=ResponsePaginationSchema[DeclaracaoReadSimple],
            summary="Lista declarações de problemas",
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    declaracoes, metadata = await get_all(
        db=db,
        model=Declaracao,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=declaracoes,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[DeclaracaoReadFull],
            summary="Lista uma declaração de um problema",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=DECLARACAO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    declaracao = await get_declaracao_by_id(
        db=db,
        id=id,
        token=token
    )

    return ResponseUnitSchema(
        data=declaracao
    )


@router.post("/",
             response_model=ResponseUnitSchema[DeclaracaoReadFull],
             status_code=201,
             summary="Cadastra uma declaração para um problema",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             )
async def create(
    declaracao: DeclaracaoCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    declaracao = await create_declaracao(
        db=db,
        declaracao=declaracao,
        token=token
    )

    return ResponseUnitSchema(data=declaracao)


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[DeclaracaoReadFull],
              summary="Atualiza uma declaração de um problema parcialmente",
              responses={
                  404: errors[404]
              },
              )
async def partial_update(
        id: int = Path(description=DECLARACAO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: DeclaracaoUpdatePartial = Body(
            description="Declaração a ser atualizada parcialmente"),
        token: str = Depends(oauth2_scheme),
):
    declaracao = await update_declaracao(
        db=db,
        id=id,
        declaracao=data,
        token=token
    )
    return ResponseUnitSchema(
        data=declaracao
    )


@router.put("/{id}/",
            response_model=ResponseUnitSchema[DeclaracaoReadFull],
            summary="Atualiza uma declaração de um problema por completo",
            responses={
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=DECLARACAO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: DeclaracaoUpdateTotal = Body(
            description="Declaração a ser atualizada por completo"),
        token: str = Depends(oauth2_scheme),
):
    declaracao = await update_declaracao(
        db=db,
        id=id,
        declaracao=data,
        token=token
    )
    return ResponseUnitSchema(
        data=declaracao
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta uma declaração de um problema",
               responses={
                   404: errors[404]
               }
               )
async def delete(
        id: int = Path(description=DECLARACAO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    declaracao = await delete_object(
        db=db,
        model=Declaracao,
        id=id,
        token=token,
        model_has_user_key=Problema,
        return_true=True
    )

    if (declaracao):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
