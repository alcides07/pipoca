from fastapi import APIRouter, Depends
from schemas.problema import Problema_Create, Problema_Read
from schemas.common.pagination import Pagination_Schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema, read_problemas
from schemas.common.response import Response_Schema_Pagination, Response_Schema_Unit
from fastapi import Depends


router = APIRouter(
    prefix="/problemas",
    tags=["problema"],
)


@router.get("/", response_model=Response_Schema_Pagination[Problema_Read], summary="Lista problemas")
def read(db: Session = Depends(get_db), common: Pagination_Schema = Depends()):
    problemas, metadata = read_problemas(db, common)

    return Response_Schema_Pagination(
        data=problemas,
        metadata=metadata
    )


@router.post("/", response_model=Response_Schema_Unit[Problema_Read], status_code=201, summary="Cadastra problema")
def create(
    problema: Problema_Create, db: Session = Depends(get_db)
):
    data = create_problema(db=db, problema=problema)

    return Response_Schema_Unit(data=data)
