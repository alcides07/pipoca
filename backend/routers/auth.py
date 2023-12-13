from fastapi import APIRouter, Depends, HTTPException, Path, status
from schemas.auth import User_Login, User_Login_Out
from schemas.common.exception import Exception_Schema
from openapi.http_response_openapi import http_response_openapi
from schemas.user import User_Create, User_Read
from schemas.common.pagination import Pagination_Schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user, read_user_by_id, read_user_by_key, read_users, user_by_key_exists, delete_user
from schemas.common.response import Response_Schema_Pagination, Response_Schema_Unit
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/",
             response_model=Response_Schema_Unit[User_Login_Out],
             summary="Autentica um usuário",
             responses=http_response_openapi(
                 status.HTTP_400_BAD_REQUEST,
                 Exception_Schema,
             ))
def login(
    user: User_Login,
    db: Session = Depends(get_db),
):
    user_db = read_user_by_key(db, "username", user.credential)
    if (user_db != None):
        if not verify_password(user.password, user_db.password):
            print("senha invalida 1!")
            return
        print("tudo certo via username!")

    else:
        user_db = read_user_by_key(db, "email", user.credential)
        if (user_db != None):
            if not verify_password(user.password, user_db.password):
                print("senha invalida 2!")
                return
            print("deu certo via email!")
