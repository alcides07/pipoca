from dependencies.authenticated_user import get_authenticated_user
from dependencies.database import get_db
from fastapi import APIRouter, Depends, Path
from models.verificador import Verificador
from orm.common.index import get_all, get_by_id
from schemas.common.pagination import PaginationSchema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from schemas.verificador import VerificadorReadFull, VerificadorReadSimple
from sqlalchemy.orm import Session
from utils.errors import errors

router = APIRouter(
    prefix="/verificadores",
    tags=["verificador"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[VerificadorReadSimple],
            summary="Lista verificadores",
            )
def read(
        db: Session = Depends(get_db),
        common: PaginationSchema = Depends(),
):
    verificadores, metadata = get_all(db, Verificador, common)

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
def read_id(
        id: int = Path(description="Identificador do verificador"),
        db: Session = Depends(get_db)
):
    verificador = get_by_id(db, Verificador, id)

    return ResponseUnitSchema(
        data=verificador
    )
