from dependencies.is_admin import is_admin_dependencies
from models.validadorTeste import ValidadorTeste
from orm.validadorTeste import create_validador_teste, delete_validador_teste, update_validador_teste
from schemas.validadorTeste import VALIDADOR_TESTE_ID_DESCRIPTION, ValidadorTesteCreateSingle, ValidadorTesteReadFull, ValidadorTesteReadSimple, ValidadorTesteUpdatePartial, ValidadorTesteUpdateTotal
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from orm.common.index import get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from sqlalchemy.orm import Session
from utils.errors import errors


router = APIRouter(
    prefix="/validadoresTestes",
    tags=["validadoresTestes"],
    dependencies=[Depends(get_authenticated_user)]
)


@router.get("/",
            response_model=ResponsePaginationSchema[ValidadorTesteReadSimple],
            summary="Lista testes de validadores",
            dependencies=[Depends(is_admin_dependencies)]
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends()
):
    validadores_testes, metadata = await get_all(
        db=db,
        model=ValidadorTeste,
        pagination=pagination
    )

    return ResponsePaginationSchema(
        data=validadores_testes,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ValidadorTesteReadFull],
            summary="Lista um teste de um validador",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=VALIDADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    validador_teste = await get_by_id(
        model=ValidadorTeste,
        path_has_user_key="validador.problema",
        db=db,
        id=id,
        token=token
    )

    return ResponseUnitSchema(
        data=validador_teste
    )


@router.post("/",
             response_model=ResponseUnitSchema[ValidadorTesteReadFull],
             status_code=201,
             summary="Cadastra um teste para um validador",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             )
async def create(
    validador_teste: ValidadorTesteCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    validador_teste = await create_validador_teste(
        db=db,
        validador_teste=validador_teste,
        token=token
    )

    return ResponseUnitSchema(data=validador_teste)


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[ValidadorTesteReadFull],
              summary="Atualiza um teste de um validador parcialmente",
              responses={
                  400: errors[400],
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=VALIDADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ValidadorTesteUpdatePartial = Body(
            description="Teste de validador a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme)
):
    validador_teste = await update_validador_teste(
        db=db,
        id=id,
        validador_teste=data,
        token=token
    )

    return ResponseUnitSchema(
        data=validador_teste
    )


@router.put("/{id}/",
            response_model=ResponseUnitSchema[ValidadorTesteReadFull],
            summary="Atualiza um teste de um validador por completo",
            responses={
                400: errors[400],
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=VALIDADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ValidadorTesteUpdateTotal = Body(
            description="Teste de validador a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme)
):
    validador_teste = await update_validador_teste(
        db=db,
        id=id,
        validador_teste=data,
        token=token
    )

    return ResponseUnitSchema(
        data=validador_teste
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta um teste de um validador",
               responses={
                   404: errors[404]
               }
               )
async def delete(
        id: int = Path(description=VALIDADOR_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    validador_teste = await delete_validador_teste(
        db=db,
        id=id,
        token=token
    )

    if (validador_teste):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
