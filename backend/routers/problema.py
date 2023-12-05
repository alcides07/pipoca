from fastapi import APIRouter, Depends
from schemas.problema import Problema_Create, Problema_Read, Problema_Base
from schemas.common.pagination import pagination_schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema
from schemas.common.response import response_schema
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, status


router = APIRouter(
    prefix="/problemas",
    tags=["problema"],
)


@router.post("/", response_model=response_schema[Problema_Create], status_code=201, summary="Cadastra problema")
def problema(
    problema: Problema_Create, db: Session = Depends(get_db)
):
    data = jsonable_encoder(create_problema(db=db, problema=problema))

    return response_schema(message="Sucesso. O problema foi cadastrado!",
                           status=status.HTTP_201_CREATED, data=data)
