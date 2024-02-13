from orm.validador import create_validador
from routers.auth import oauth2_scheme
from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Depends, Path
from models.problema import Problema
from models.validador import Validador
from orm.common.index import get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.validador import ValidadorCreateSingle, ValidadorReadFull, ValidadorReadSimple
from sqlalchemy.orm import Session
from utils.errors import errors

router = APIRouter(
    prefix="/validadores",
    tags=["validador"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ValidadorReadSimple],
            summary="Lista validadores",
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    validadores, metadata = await get_all(
        db=db,
        model=Validador,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=validadores,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ValidadorReadFull],
            summary="Lista um validador",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description="Identificador do validador"),
        db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    validador = await get_by_id(
        db=db,
        model=Validador,
        id=id,
        token=token,
        model_has_user_key=Problema
    )

    return ResponseUnitSchema(
        data=validador
    )


@router.post("/",
             response_model=ResponseUnitSchema[ValidadorReadFull],
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
    user = await get_authenticated_user(token=token, db=db)

    validador = await create_validador(
        db=db,
        validador=validador,
        user=user
    )

    return ResponseUnitSchema(data=validador)
