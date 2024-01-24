from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Depends, Path
from models.validador import Validador
from orm.common.index import get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.validador import ValidadorReadFull, ValidadorReadSimple
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
def read(
        db: Session = Depends(get_db),
        common: PaginationSchema = Depends(),
):
    validadores, metadata = get_all(db, Validador, common)

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
def read_id(
        id: int = Path(description="Identificador do validador"),
        db: Session = Depends(get_db)
):
    validador = get_by_id(db, Validador, id)

    return ResponseUnitSchema(
        data=validador
    )
