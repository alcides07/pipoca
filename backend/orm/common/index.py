from sqlalchemy.orm import joinedload
from typing import Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.common.pagination import MetadataSchema, PaginationSchema
from fastapi import status


def get_by_key_value_exists(db: Session, model: Any, key: str, value):
    db_object = db.query(model).filter(getattr(model, key) == value).first()
    return True if db_object != None else False


def get_by_key_value(db: Session, model: Any, key: str, value):
    db_object = db.query(model).filter(getattr(model, key) == value).first()
    return db_object


def get_by_id(db: Session, model: Any, id: int, relations: List[str] = []):
    query = db.query(model)
    for relation in relations:
        query = query.options(joinedload(getattr(model, relation)))
    db_object = query.filter(model.id == id).first()
    if db_object:
        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def get_all(db: Session, model: Any, common: PaginationSchema):
    db_objects = db.query(model).offset(common.offset).limit(common.limit)
    total = db.query(model).count()
    metadata = MetadataSchema(
        count=db_objects.count(), total=total, offset=common.offset, limit=common.limit)

    return db_objects.all(), metadata


def create_object(db: Session, model: Any, schema: Any):
    db_object = model(**schema.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


def delete_object(db: Session, model: Any, id: int):
    db_object = db.query(model).filter(model.id == id).first()
    if (db_object):
        db.delete(db_object)
        db.commit()
        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def update_total(db: Session, model: Any, id: int, data: Any):
    db_object = db.query(model).filter(model.id == id).first()
    if (db_object):
        for key, value in data.dict().items():
            if hasattr(db_object, key):
                setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)
