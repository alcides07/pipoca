from models.problema import Problema
from routers.auth import oauth2_scheme
from fastapi import APIRouter, Depends, Path
from models.arquivo import Arquivo
from schemas.arquivo import ArquivoReadFull, ArquivoReadSimple
from utils.errors import errors
from orm.common.index import get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema


router = APIRouter(
    prefix="/arquivos",
    tags=["arquivo"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ArquivoReadSimple],
            summary="Lista arquivos",
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
            response_model=ResponseUnitSchema[ArquivoReadFull],
            summary="Lista um arquivo",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description="Identificador do arquivo"),
        db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    arquivo = await get_by_id(db, Arquivo, id, token, Problema)

    return ResponseUnitSchema(
        data=arquivo
    )
