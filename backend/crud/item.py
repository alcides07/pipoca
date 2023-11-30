from sqlalchemy.orm import Session
from schemas.common.pagination import pagination_schema
from models.item import Item
from schemas.item import Item_Create


def read_items(db: Session, common: pagination_schema):
    return db.query(Item).offset(common.skip).limit(common.limit).all()


def create_item(db: Session, item: Item_Create):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
