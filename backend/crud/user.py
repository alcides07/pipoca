from sqlalchemy.orm import Session
from schemas.common.pagination import pagination_schema
from models.user import User
from schemas.user import User_Create


def read_users(db: Session, common: pagination_schema):
    return db.query(User).offset(common.skip).limit(common.limit).all()


def create_user(db: Session, user: User_Create):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
