from fastapi import APIRouter, Depends
from schemas.user import User_Read, User_Create
from schemas.common.pagination import pagination_schema
from dependencies.router_parameters import pagination_router
from dependencies.database import get_db
from sqlalchemy.orm import Session
from crud.user import create_user, read_users, read_user_by_key_exists
from schemas.common.response import response_schema
from fastapi import status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi import Depends, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/", response_model=list[User_Read])
def users(db: Session = Depends(get_db), common: pagination_schema = Depends(pagination_router)):
    users = read_users(db, common)
    return users


@router.post("/", response_model=response_schema)
def user(
    user: User_Create, db: Session = Depends(get_db)
):

    response = response_schema(message="", status=204)

    if (user.password != user.passwordConfirmation):
        response.message = "Erro. As senhas fornecidas não coincidem!"
        response.status = status.HTTP_400_BAD_REQUEST
        return response

    elif (read_user_by_key_exists(db, "username", user.username)):
        response.message = "Erro. O nome de usuário fornecido está em uso!"
        response.status = status.HTTP_400_BAD_REQUEST
        return response

    elif (read_user_by_key_exists(db, "email", user.email)):
        response.message = "Erro. O e-mail fornecido está em uso!"
        response.status = status.HTTP_400_BAD_REQUEST
        return response

    else:
        user.password = pwd_context.hash(user.password)
        response.message = "Sucesso. O cadastro foi realizado!"
        response.status = status.HTTP_201_CREATED
        response.data = jsonable_encoder(create_user(db=db, user=user))
        return response
