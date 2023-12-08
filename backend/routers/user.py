from fastapi import APIRouter, Depends, Path
from utils.response_http_openapi import response_http_openapi
from schemas.user import User_Create, User_Read
from schemas.common.pagination import pagination_schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user, read_user_by_id, read_users, user_by_key_exists, delete_user
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


@router.get("/",
            response_model=response_schema[User_Read],
            summary="Lista usuários"
            )
def read(db: Session = Depends(get_db), common: pagination_schema = Depends()):
    users = jsonable_encoder(read_users(db, common))

    return response_schema(
        data=users
    )


@router.get("/{id}",
            response_model=response_schema[User_Read],
            summary="Lista um usuário",
            responses=response_http_openapi(
                status.HTTP_404_NOT_FOUND,
                response_schema
            ))
def read_id(
        id: int = Path(description="identificador do usuário"),
        db: Session = Depends(get_db)):
    users = jsonable_encoder(read_user_by_id(db, id))

    return response_schema(
        data=users
    )


@router.post("/",
             response_model=response_schema[User_Read],
             status_code=201,
             summary="Cadastra um usuário",
             responses=response_http_openapi(
                 status.HTTP_400_BAD_REQUEST,
                 response_schema,
                 description="Bad Request (erros em credenciais)"
             ))
def create(
    user: User_Create,
    response: Response,
    db: Session = Depends(get_db),
):

    if (user.password != user.passwordConfirmation):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response_schema(message="Erro. As senhas fornecidas não coincidem!")

    elif (user_by_key_exists(db, "username", user.username)):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response_schema(message="Erro. O nome de usuário fornecido está em uso!")

    elif (user_by_key_exists(db, "email", user.email)):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response_schema(message="Erro. O e-mail fornecido está em uso!")

    else:
        user.password = pwd_context.hash(user.password)
        data = jsonable_encoder(create_user(db=db, user=user))

        return response_schema(data=data)


@router.delete("/{id}",
               response_model=response_schema[User_Read],
               summary="Deleta um usuário",
               responses={404:
                          {"model": response_schema},
                          }
               )
def delete(
        id: int = Path(description="identificador do usuário"),
        db: Session = Depends(get_db)
):

    user = jsonable_encoder(delete_user(db, id))
    return response_schema(
        data=user
    )
