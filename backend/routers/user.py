from fastapi import APIRouter, Depends
from schemas.user import User_Create, User_Read, User_Base
from schemas.common.pagination import pagination_schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user, read_users, read_user_by_key_exists
from schemas.common.response import response_schema
from fastapi import status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi import Depends, status, Response
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/", response_model=response_schema[User_Read], summary="Lista usuários")
def users(db: Session = Depends(get_db), common: pagination_schema = Depends()):
    users = jsonable_encoder(read_users(db, common))

    return response_schema(
        data=users
    )


@router.post("/",
             response_model=response_schema[User_Base],
             status_code=201,
             summary="Cadastra usuário",
             responses={400:
                        {"model": response_schema,
                         "description": "Bad Request (erros em credenciais)"
                         },
                        }
             )
def user(
    user: User_Create,
    db: Session = Depends(get_db),
    response: Response = Response
):

    if (user.password != user.passwordConfirmation):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response_schema(message="Erro. As senhas fornecidas não coincidem!")

    elif (read_user_by_key_exists(db, "username", user.username)):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response_schema(message="Erro. O nome de usuário fornecido está em uso!")

    elif (read_user_by_key_exists(db, "email", user.email)):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response_schema(message="Erro. O e-mail fornecido está em uso!")

    else:
        user.password = pwd_context.hash(user.password)
        data = jsonable_encoder(create_user(db=db, user=user))

        return response_schema(data=data)
