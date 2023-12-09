from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.common.pagination import Pagination_Schema
from models.user import User
from schemas.user import User_Create


def read_users(db: Session, common: Pagination_Schema):
    return db.query(User).offset(common.skip).limit(common.limit).all()


def read_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    if (user):
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND)


def user_by_key_exists(db: Session, key: str, value):
    user = db.query(User).filter(getattr(User, key) == value).first()
    return True if user != None else False


def create_user(db: Session, user: User_Create):
    db_user = User(
        **user.model_dump(exclude="passwordConfirmation"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    if (user):
        db.delete(user)
        db.commit()
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND)
