from dependencies.authorization_user import has_authorization_user
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from typing import Any
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


def user_autenthicated(token: str, db: Session):
    from dependencies.authenticated_user import get_authenticated_user
    return get_authenticated_user(token, db)


async def get_by_id(db: Session,
                    model: Any,
                    id: int,
                    token: str = "",
                    model_has_user_key: Any = None,
                    ):

    db_object = db.query(model).filter(model.id == id).first()

    if db_object:
        if (token and not await has_authorization_user(model, db, db_object, token, model_has_user_key)):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def get_all(db: Session, model: Any, common: PaginationSchema, filters: Any = None, search_fields: list[str] = []):
    query = db.query(model)

    if filters:
        for attr, value in filters.__dict__.items():
            if value is not None:
                query = query.filter(getattr(model, attr) == value)

    if common.q and search_fields:
        search_query = or_(
            *[getattr(model, field).ilike(f"%{common.q}%") for field in search_fields if hasattr(model, field)])
        query = query.filter(search_query)

    db_objects = query.offset(common.offset).limit(common.limit)
    total = query.count()
    metadata = MetadataSchema(
        count=db_objects.count(),
        total=total,
        offset=common.offset,
        limit=common.limit,
        search_fields=search_fields
    )

    return db_objects.all(), metadata


def create_object(db: Session, model: Any, schema: Any):
    db_object = model(**schema.model_dump())
    try:
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_object


async def delete_object(db: Session,
                        model: Any,
                        id: int,
                        token: str = "",
                        model_has_user_key: Any = None,
                        ):
    db_object = db.query(model).filter(model.id == id).first()
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (token and not await has_authorization_user(model, db, db_object, token, model_has_user_key)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        db.delete(db_object)
        db.commit()
        return db_object
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_object(db: Session,
                        model: Any,
                        id: int,
                        data: Any,
                        token: str = "",
                        model_has_user_key: Any = None,
                        ):

    db_object = db.query(model).filter(model.id == id).first()
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (token and not await has_authorization_user(model, db, db_object, token, model_has_user_key)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        with db.begin_nested():
            for key, value in data.model_dump().items():
                if hasattr(db_object, key):
                    setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_object
