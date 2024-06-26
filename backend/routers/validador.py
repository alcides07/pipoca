from dependencies.is_admin import is_admin_dependencies
from orm.validador import create_validador, get_testes_validador, update_validador
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Body, Depends, Path, Response, status
from models.validador import Validador
from orm.common.index import delete_object, get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitRequiredSchema
from schemas.validador import VALIDADOR_ID_DESCRIPTION, ValidadorCreateSingle, ValidadorReadFull, ValidadorReadSimple, ValidadorUpdatePartial, ValidadorUpdateTotal
from sqlalchemy.orm import Session
from schemas.validadorTeste import ValidadorTesteReadFull
from utils.errors import errors

router = APIRouter(
    prefix="/validadores",
    tags=["validadores"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ValidadorReadSimple],
            summary="Lista validadores",
            dependencies=[Depends(is_admin_dependencies)]
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends()
):
    validadores, metadata = await get_all(
        db=db,
        model=Validador,
        pagination=pagination
    )

    return ResponsePaginationSchema(
        data=validadores,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitRequiredSchema[ValidadorReadFull],
            summary="Lista um validador",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=VALIDADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    validador = await get_by_id(
        db=db,
        model=Validador,
        id=id,
        token=token,
        path_has_user_key="problema"
    )

    return ResponseUnitRequiredSchema(
        data=validador
    )


@router.get("/{id}/testes/",
            response_model=ResponsePaginationSchema[ValidadorTesteReadFull],
            summary="Lista testes pertencentes a um validador",
            responses={
                404: errors[404]
            }
            )
async def read_validador_id_testes(
        id: int = Path(description=VALIDADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    testes_validador, metadata = await get_testes_validador(
        db=db,
        pagination=pagination,
        id=id,
        token=token
    )

    return ResponsePaginationSchema(
        data=testes_validador,
        metadata=metadata
    )


@router.post("/",
             response_model=ResponseUnitRequiredSchema[ValidadorReadFull],
             status_code=201,
             summary="Cadastra um validador",
             responses={
                 422: errors[422],
                 404: errors[404]
             },
             description="Ao cadastrar um validador em um problema que já possui um, **o antigo é deletado juntamente com seus testes** e o problema é vinculado ao novo validador."
             )
async def create(
    validador: ValidadorCreateSingle,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    validador = await create_validador(
        db=db,
        validador=validador,
        token=token
    )

    return ResponseUnitRequiredSchema(data=validador)


@router.patch("/{id}/",
              response_model=ResponseUnitRequiredSchema[ValidadorReadFull],
              summary="Atualiza um validador parcialmente",
              responses={
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=VALIDADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ValidadorUpdatePartial = Body(
            description="Validador a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme),
):
    validador = await update_validador(
        db=db,
        id=id,
        validador=data,
        token=token
    )
    return ResponseUnitRequiredSchema(
        data=validador
    )


@router.put("/{id}/",
            response_model=ResponseUnitRequiredSchema[ValidadorReadFull],
            summary="Atualiza um validador por completo",
            responses={
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=VALIDADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ValidadorUpdateTotal = Body(
            description="Validador a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme),
):
    validador = await update_validador(
        db=db,
        id=id,
        validador=data,
        token=token
    )
    return ResponseUnitRequiredSchema(
        data=validador
    )


@router.delete("/{id}/",
               status_code=204,
               summary="Deleta um validador",
               responses={
                   404: errors[404]
               }
               )
async def delete(
        id: int = Path(description=VALIDADOR_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):

    validador = await delete_object(
        db=db,
        model=Validador,
        id=id,
        token=token,
        path_has_user_key="problema"
    )

    if (validador):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
