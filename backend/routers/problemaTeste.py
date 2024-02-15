from orm.problemaTeste import create_problema_teste, get_problema_teste_by_id, update_problema_teste
from models.problema import Problema
from schemas.problemaTeste import ProblemaTesteCreateSingle, ProblemaTesteReadFull, ProblemaTesteReadSimple, ProblemaTesteUpdatePartial, ProblemaTesteUpdateTotal
from fastapi import APIRouter, Body, Depends, Path, Response, status
from models.problemaTeste import ProblemaTeste
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from orm.common.index import delete_object, get_all
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from sqlalchemy.orm import Session
from utils.errors import errors

PROBLEMA_TESTE_ID_DESCRIPTION = "Identificador do teste de um problema"

router = APIRouter(
    prefix="/problemaTestes",
    tags=["problemaTestes"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ProblemaTesteReadSimple],
            summary="Lista testes de problemas"
            )
async def read(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    token: str = Depends(oauth2_scheme),
):
    problemas_testes, metadata = await get_all(
        db=db,
        model=ProblemaTeste,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=problemas_testes,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ProblemaTesteReadFull],
            summary="Lista um teste de um problema",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=PROBLEMA_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    problema_teste = await get_problema_teste_by_id(
        db=db,
        id=id,
        token=token
    )
    return ResponseUnitSchema(
        data=problema_teste
    )


@router.post("/",
             response_model=ResponseUnitSchema[ProblemaTesteReadFull],
             status_code=201,
             summary="Cadastra um teste para um problema",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             )
async def create(
    problema_teste: ProblemaTesteCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    problema_teste = await create_problema_teste(
        db=db,
        problema_teste=problema_teste,
        token=token
    )

    return ResponseUnitSchema(data=problema_teste)


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[ProblemaTesteReadFull],
              summary="Atualiza um teste de um problema parcialmente",
              responses={
                  400: errors[400],
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=PROBLEMA_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ProblemaTesteUpdatePartial = Body(
            description="Teste de problema a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme)
):
    problema_teste = await update_problema_teste(
        db=db,
        id=id,
        problema_teste=data,
        token=token
    )
    return ResponseUnitSchema(
        data=problema_teste
    )


@router.put("/{id}/",
            response_model=ResponseUnitSchema[ProblemaTesteReadFull],
            summary="Atualiza um teste de um problema por completo",
            responses={
                400: errors[400],
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=PROBLEMA_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ProblemaTesteUpdateTotal = Body(
            description="Teste de problema a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme)
):
    problema_teste = await update_problema_teste(
        db=db,
        id=id,
        problema_teste=data,
        token=token
    )
    return ResponseUnitSchema(
        data=problema_teste
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta um teste de um problema",
               responses={
                   404: errors[404]
               }
               )
async def delete(
        id: int = Path(description=PROBLEMA_TESTE_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    problema_teste = await delete_object(
        db=db,
        model=ProblemaTeste,
        id=id,
        token=token,
        model_has_user_key=Problema,
        return_true=True
    )

    if (problema_teste):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
