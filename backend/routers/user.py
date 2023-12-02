from fastapi import APIRouter, Depends
from schemas.user import User_Create, User_Read
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


@router.get("/", response_model=response_schema[User_Read])
def users(db: Session = Depends(get_db), common: pagination_schema = Depends(pagination_router)):
    users = jsonable_encoder(read_users(db, common))
    for user in users:
        user.pop("password", None)

    return response_schema(
        status=status.HTTP_200_OK,
        data=users
    )


@router.post("/", response_model=response_schema)
def user(
    user: User_Create, db: Session = Depends(get_db)
):

    if (user.password != user.passwordConfirmation):
        return response_schema(message="Erro. As senhas fornecidas não coincidem!",
                               status=status.HTTP_400_BAD_REQUEST)

    elif (read_user_by_key_exists(db, "username", user.username)):
        return response_schema(message="Erro. O nome de usuário fornecido está em uso!",
                               status=status.HTTP_400_BAD_REQUEST)

    elif (read_user_by_key_exists(db, "email", user.email)):
        return response_schema(message="Erro. O e-mail fornecido está em uso!",
                               status=status.HTTP_400_BAD_REQUEST)

    else:
        user.password = pwd_context.hash(user.password)
        data = jsonable_encoder(create_user(db=db, user=user))
        data.pop('password', None)

        return response_schema(message="Sucesso. O cadastro foi realizado!",
                               status=status.HTTP_201_CREATED, data=data)
