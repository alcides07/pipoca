from enum import Enum
from dependencies.authorization_user import has_authorization_object_single, has_authorization_object_collection, is_admin, is_user
from schemas.common.direction_order_by import DirectionOrderByEnum
from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query
from schemas.common.pagination import MetadataSchema, PaginationSchema
from fastapi import status


def filter_collection(
    model: Any,
    filters: Any,
    pagination: PaginationSchema,
    query: Query[Any],
    search_fields: Any,
    field_order_by: Optional[Enum],
    direction: Optional[DirectionOrderByEnum],
):
    total = query.count()

    if (filters):
        for attr, value in filters.__dict__.items():
            if (hasattr(model, attr) and value != None):
                query = query.filter(getattr(model, attr) == value)

    if (pagination.q):
        search_query = or_(
            *[getattr(model, field).ilike(f"%{pagination.q}%") for field in search_fields if hasattr(model, field)])
        query = query.filter(search_query)

    if (field_order_by and hasattr(model, field_order_by.value)):
        if (direction == DirectionOrderByEnum.DESC):
            query = query.order_by(
                desc(getattr(model, field_order_by.value)))
        else:
            query = query.order_by(
                asc(getattr(model, field_order_by.value)))

    query = query.offset(pagination.offset).limit(pagination.limit)

    metadata = MetadataSchema(
        count=query.count(),
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
        search_fields=search_fields
    )

    return query, metadata


def get_by_key_value_exists(db: Session, model: Any, key: str, value):
    db_object = db.query(model).filter(getattr(model, key) == value).first()
    return True if db_object != None else False


def get_by_key_value(db: Session, model: Any, key: str, value):
    db_object = db.query(model).filter(getattr(model, key) == value).first()
    return db_object


def user_autenthicated(token: str, db: Session):
    from dependencies.authenticated_user import get_authenticated_user
    return get_authenticated_user(token, db)


async def get_by_id(
    db: Session,
    model: Any,
    id: int,
    token: str,
    model_has_user_key: Any,
):

    db_object = db.query(model).filter(model.id == id).first()

    if db_object:
        if (not await has_authorization_object_single(model, db, db_object, token, model_has_user_key)):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return db_object
    raise HTTPException(status.HTTP_404_NOT_FOUND)


async def get_all(
    db: Session,
    model: Any,
    pagination: PaginationSchema,
    token: str,
    field_order_by: Optional[Enum] = None,
    direction: Optional[DirectionOrderByEnum] = None,
    filters: Any = None,
    search_fields: list[str] = [],
    allow_any: bool = False,
    me_author: bool = False
):
    user = await user_autenthicated(token, db)

    if (allow_any == False and not is_admin(user)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    query = db.query(model)

    if (me_author == True and hasattr(model, "usuario_id")):
        if (is_user(user)):
            query = db.query(model).filter(model.usuario_id == user.id)

    db_objects, metadata = filter_collection(
        model,
        filters,
        pagination,
        query,
        search_fields,
        field_order_by,
        direction
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


async def delete_object(
    db: Session,
    model: Any,
    id: int,
    token: str = "",
    model_has_user_key: Any = None,
    return_true: bool = False
):
    db_object = db.query(model).filter(model.id == id).first()
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (token and not await has_authorization_object_single(model, db, db_object, token, model_has_user_key)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        db.delete(db_object)
        db.commit()
        if (return_true):
            return True
        return db_object
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_object(
    db: Session,
    model: Any,
    id: int,
    data: Any,
    token: str = "",
    model_has_user_key: Any = None,
):

    db_object = db.query(model).filter(model.id == id).first()
    if not db_object:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (token and not await has_authorization_object_single(model, db, db_object, token, model_has_user_key)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        with db.begin_nested():
            for key, value in data.model_dump().items():
                if hasattr(db_object, key):
                    setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)

        return db_object

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
