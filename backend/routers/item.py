from fastapi import APIRouter, Depends
from schemas.item import Item_Read, Item_Create
from schemas.common.pagination import pagination_schema
from dependencies.router_parameters import pagination_router
from dependencies.database import get_db
from sqlalchemy.orm import Session
from crud.item import create_item, read_items

router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@router.get("/", response_model=list[Item_Read])
def items(db: Session = Depends(get_db), common: pagination_schema = Depends(pagination_router)):
    items = read_items(db, common)
    return items


@router.post("/", response_model=Item_Create)
def item(
    item: Item_Create, db: Session = Depends(get_db)
):
    return create_item(db=db, item=item)
