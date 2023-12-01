from fastapi import APIRouter, Depends
from schemas.item import Item_Create
from schemas.common.pagination import pagination_schema
from dependencies.router_parameters import pagination_router
from dependencies.database import get_db
from sqlalchemy.orm import Session
from crud.item import create_item, read_items
from schemas.common.return_body import return_schema
from fastapi import status
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@router.get("/", response_model=return_schema)
def items(db: Session = Depends(get_db), common: pagination_schema = Depends(pagination_router)):
    items = jsonable_encoder(read_items(db, common))

    return {
        "type": "success",
        "message": "teste",
        "status": status.HTTP_200_OK,
        "data": items
    }


@router.post("/", response_model=Item_Create)
def item(
    item: Item_Create, db: Session = Depends(get_db)
):
    return create_item(db=db, item=item)
