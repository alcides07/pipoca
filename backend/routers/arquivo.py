from fastapi import APIRouter, Depends, Path
from models.arquivo import Arquivo
from schemas.arquivo import ArquivoRead
from utils.errors import errors
from orm.common.index import get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/arquivos",
    tags=["arquivo"],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ArquivoRead],
            summary="Lista arquivos",
            dependencies=[Depends(get_authenticated_user)],
            )
def read(
        db: Session = Depends(get_db),
        common: PaginationSchema = Depends(),
):
    arquivos, metadata = get_all(db, Arquivo, common)

    return ResponsePaginationSchema(
        data=arquivos,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ArquivoRead],
            summary="Lista um arquivo",
            dependencies=[Depends(get_authenticated_user)],
            responses={
                404: errors[404]
            }
            )
def read_id(
        id: int = Path(description="identificador do arquivo"),
        db: Session = Depends(get_db)
):
    arquivo = jsonable_encoder(get_by_id(db, Arquivo, id))

    return ResponseUnitSchema(
        data=arquivo
    )
