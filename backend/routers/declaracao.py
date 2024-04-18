from dependencies.is_admin import is_admin_dependencies
from models.declaracao import Declaracao
from orm.declaracao import create_declaracao, get_declaracao_by_id, get_imagens_declaracao, update_declaracao
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from orm.common.index import delete_object, get_all
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponseListSchema, ResponsePaginationSchema, ResponseUnitRequiredSchema, ResponseUnitSchema
from schemas.declaracao import DeclaracaoCreateSingle, DeclaracaoReadFull, DeclaracaoReadSimple, DeclaracaoUpdatePartial, DeclaracaoUpdateTotal
from sqlalchemy.orm import Session
from schemas.idioma import IdiomaEnum
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
            dependencies=[Depends(is_admin_dependencies)]
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends()
):
    declaracoes, metadata = await get_all(
        db=db,
        model=Declaracao,
        pagination=pagination,
    )

    return ResponsePaginationSchema(
        data=declaracoes,
        metadata=metadata
    )


@router.get("/idiomas/",
            response_model=ResponseListSchema[IdiomaEnum],
            summary="Lista idiomas em que as declarações podem ser escritas"
            )
async def read_idiomas():
    return ResponseListSchema(
        data=[idioma for idioma in IdiomaEnum]
    )


@router.get("/{id}/",
            response_model=ResponseUnitRequiredSchema[DeclaracaoReadFull],
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

    return ResponseUnitRequiredSchema(
        data=declaracao
    )


@router.get("/{id}/imagens/",
            response_model=ResponseListSchema[str],
            summary="Lista as imagens de uma declaração em base64",
            responses={
                404: errors[404]
            }
            )
async def read_imagens_declaracao(
        id: int = Path(description=DECLARACAO_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    imagens = await get_imagens_declaracao(
        db=db,
        id=id,
        token=token
    )

    return ResponseListSchema(
        data=imagens
    )


@router.post("/",
             response_model=ResponseUnitRequiredSchema[DeclaracaoReadFull],
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

    return ResponseUnitRequiredSchema(data=declaracao)


@router.patch("/{id}/",
              response_model=ResponseUnitRequiredSchema[DeclaracaoReadFull],
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
    return ResponseUnitRequiredSchema(
        data=declaracao
    )


@router.put("/{id}/",
            response_model=ResponseUnitRequiredSchema[DeclaracaoReadFull],
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
    return ResponseUnitRequiredSchema(
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
        path_has_user_key="problema"
    )

    if (declaracao):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
