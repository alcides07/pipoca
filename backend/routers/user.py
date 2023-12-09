from fastapi import APIRouter, Depends, HTTPException, Path, status
from schemas.common.exception import Exception_Schema
from openapi.http_response_openapi import http_response_openapi
from schemas.user import User_Create, User_Read
from schemas.common.pagination import Pagination_Schema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user, read_user_by_id, read_users, user_by_key_exists, delete_user
from schemas.common.response import Response_Schema
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/",
            response_model=Response_Schema[User_Read],
            summary="Lista usuários"
            )
def read(db: Session = Depends(get_db), common: Pagination_Schema = Depends()):
    users = jsonable_encoder(read_users(db, common))

    return Response_Schema(
        data=users
    )


@router.get("/{id}",
            response_model=Response_Schema[User_Read],
            summary="Lista um usuário",
            responses=http_response_openapi(
                status.HTTP_404_NOT_FOUND,
                Exception_Schema
            ))
def read_id(
        id: int = Path(description="identificador do usuário"),
        db: Session = Depends(get_db)):
    users = jsonable_encoder(read_user_by_id(db, id))

    return Response_Schema(
        data=users
    )


@router.post("/",
             response_model=Response_Schema[User_Read],
             status_code=201,
             summary="Cadastra um usuário",
             responses=http_response_openapi(
                 status.HTTP_400_BAD_REQUEST,
                 Exception_Schema,
             ))
def create(
    user: User_Create,
    db: Session = Depends(get_db),
):

    if (user.password != user.passwordConfirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. As senhas fornecidas não coincidem!")

    elif (user_by_key_exists(db, "username", user.username)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O nome de usuário fornecido está em uso!")

    elif (user_by_key_exists(db, "email", user.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O e-mail fornecido está em uso!")

    else:
        user.password = pwd_context.hash(user.password)
        data = jsonable_encoder(create_user(db=db, user=user))

        return Response_Schema(data=data)


@router.delete("/{id}",
               response_model=Response_Schema[User_Read],
               summary="Deleta um usuário",
               responses=http_response_openapi(
                   status.HTTP_404_NOT_FOUND,
                   Exception_Schema,
               )
               )
def delete(
        id: int = Path(description="identificador do usuário"),
        db: Session = Depends(get_db)
):

    user = jsonable_encoder(delete_user(db, id))
    return Response_Schema(
        data=user
    )
