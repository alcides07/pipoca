from typing import Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.common.pagination import Metadata_Schema, Pagination_Schema
from fastapi import status


def get_by_key_value_exists(db: Session, model: Any, key: str, value):
    object = db.query(model).filter(getattr(model, key) == value).first()
    return True if object != None else False


def get_by_key_value(db: Session, model: Any, key: str, value):
    object = db.query(model).filter(getattr(model, key) == value).first()
    return object


def get_by_id(db: Session, model: Any, id: int):
    object = db.query(model).filter(model.id == id).first()
    if (object):
        return object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def get_all(db: Session, model: Any, common: Pagination_Schema):
    objects = db.query(model).offset(common.offset).limit(common.limit)
    total = db.query(model).count()
    metadata = Metadata_Schema(
        count=objects.count(), total=total, offset=common.offset, limit=common.limit)

    return objects.all(), metadata


def create_object(db: Session, model: Any, schema: Any):
    db_object = model(**schema.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


def delete_object(db: Session, model: Any, id: int):
    object = db.query(model).filter(model.id == id).first()
    if (object):
        db.delete(object)
        db.commit()
        return object
    raise HTTPException(status.HTTP_404_NOT_FOUND)
