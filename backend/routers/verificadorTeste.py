from models.verificadorTeste import VerificadorTeste
from orm.verificadorTeste import create_verificador_teste, delete_verificador_teste, update_verificador_teste
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from orm.common.index import get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from sqlalchemy.orm import Session
from schemas.verificadorTeste import VerificadorTesteCreateSingle, VerificadorTesteReadFull, VerificadorTesteReadSimple, VerificadorTesteUpdatePartial, VerificadorTesteUpdateTotal
from utils.errors import errors

VERIFICADOR_TESTE_ID_DESCRIPTION = "Identificador do teste do verificador"

router = APIRouter(
    prefix="/verificadorTestes",
    tags=["verificadorTestes"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/",
            response_model=ResponsePaginationSchema[VerificadorTesteReadSimple],
            summary="Lista testes de verificadores"
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    verificadores_testes, metadata = await get_all(
        db=db,
        model=VerificadorTeste,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=verificadores_testes,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[VerificadorTesteReadFull],
            summary="Lista um teste de um verificador",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=VERIFICADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    verificador_teste = await get_by_id(
        db=db,
        model=VerificadorTeste,
        id=id,
        token=token,
        path_has_user_key="verificador.problema"
    )

    return ResponseUnitSchema(
        data=verificador_teste
    )


@router.post("/",
             response_model=ResponseUnitSchema[VerificadorTesteReadFull],
             status_code=201,
             summary="Cadastra um teste para um verificador",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             )
async def create(
    verificador_teste: VerificadorTesteCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    verificador_teste = await create_verificador_teste(
        db=db,
        verificador_teste=verificador_teste,
        token=token
    )

    return ResponseUnitSchema(data=verificador_teste)


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[VerificadorTesteReadFull],
              summary="Atualiza um teste de um verificador parcialmente",
              responses={
                  400: errors[400],
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=VERIFICADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: VerificadorTesteUpdatePartial = Body(
            description="Teste de verificador a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme)
):
    verificador_teste = await update_verificador_teste(
        db=db,
        id=id,
        verificador_teste=data,
        token=token
    )

    return ResponseUnitSchema(
        data=verificador_teste
    )


@router.put("/{id}/",
            response_model=ResponseUnitSchema[VerificadorTesteReadFull],
            summary="Atualiza um teste de um verificador por completo",
            responses={
                400: errors[400],
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=VERIFICADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: VerificadorTesteUpdateTotal = Body(
            description="Teste de verificador a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme)
):
    verificador_teste = await update_verificador_teste(
        db=db,
        id=id,
        verificador_teste=data,
        token=token
    )

    return ResponseUnitSchema(
        data=verificador_teste
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta um teste de um verificador",
               responses={
                   404: errors[404]
               }
               )
async def delete(
        id: int = Path(description=VERIFICADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    verificador_teste = await delete_verificador_teste(
        db=db,
        id=id,
        token=token
    )

    if (verificador_teste):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
