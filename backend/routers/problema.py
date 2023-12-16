from fastapi import APIRouter, Depends
from utils.errors import errors
from models.problema import Problema
from orm.common.index import get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.problema import ProblemaCreate, Problema_Read
from schemas.common.pagination import Pagination_Schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from fastapi import Depends


router = APIRouter(
    prefix="/problemas",
    tags=["problema"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/", response_model=ResponsePaginationSchema[Problema_Read], summary="Lista problemas")
def read(db: Session = Depends(get_db), common: Pagination_Schema = Depends()):
    problemas, metadata = get_all(db, Problema, common)

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.post("/",
             response_model=ResponseUnitSchema[Problema_Read],
             status_code=201,
             summary="Cadastra problema",
             responses={
                 422: errors[422]
             }
             )
def create(
    problema: ProblemaCreate, db: Session = Depends(get_db)
):
    data = create_problema(db=db, problema=problema)

    return ResponseUnitSchema(data=data)
