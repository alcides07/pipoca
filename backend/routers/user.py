from fastapi import APIRouter, Depends
from schemas.user import User_Read, User_Create
from schemas.common.pagination import pagination_schema
from dependencies.router_parameters import pagination_router
from dependencies.database import get_db
from sqlalchemy.orm import Session
from crud.user import create_user, read_users


router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/", response_model=list[User_Read])
def users(db: Session = Depends(get_db), common: pagination_schema = Depends(pagination_router)):
    users = read_users(db, common)
    return users


@router.post("/", response_model=User_Read)
def user(
    user: User_Create, db: Session = Depends(get_db)
):

    return create_user(db=db, user=user)
