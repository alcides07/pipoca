from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from utils.errors import errors
from models.user import User
from orm.common.index import delete_object, get_by_key_value, get_by_key_value_exists, get_by_id, get_all, update_object
from dependencies.authenticated_user import get_authenticated_user
from schemas.user import UserCreate, UserRead
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from passlib.context import CryptContext


USER_ID_DESCRIPTION = "identificador do usuário"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/",
            response_model=ResponsePaginationSchema[UserRead],
            summary="Lista usuários",
            dependencies=[Depends(get_authenticated_user)],
            )
async def read(
        db: Session = Depends(get_db),
        pagination: PaginationSchema = Depends(),
        token: str = Depends(oauth2_scheme)
):
    users, metadata = await get_all(
        db=db,
        model=User,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=users,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[UserRead],
            summary="Lista um usuário",
            dependencies=[Depends(get_authenticated_user)],
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=USER_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    users = await get_by_id(
        db=db,
        model=User,
        id=id,
        token=token,
        model_has_user_key=User
    )

    return ResponseUnitSchema(
        data=users
    )


@router.post("/",
             response_model=ResponseUnitSchema[UserRead],
             status_code=201,
             summary="Cadastra um usuário",
             responses={
                 400: errors[400],
                 422: errors[422],

             }
             )
def create(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    if (user.password != user.passwordConfirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. As senhas fornecidas não coincidem!")

    elif (get_by_key_value_exists(db, User, "username", user.username)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O nome de usuário fornecido está em uso!")

    elif (get_by_key_value_exists(db, User, "email", user.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O e-mail fornecido está em uso!")

    else:
        user.password = pwd_context.hash(user.password)
        data = create_user(db=db, user=user)

        return ResponseUnitSchema(data=data)


@router.put("/{id}/",
            response_model=ResponseUnitSchema[UserRead],
            summary="Atualiza um usuário por completo",
            responses={
                404: errors[404]
            },
            dependencies=[Depends(get_authenticated_user)],
            )
async def total_update(
        id: int = Path(description=USER_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        user: UserCreate = Body(),
        token: str = Depends(oauth2_scheme)
):
    await get_by_id(
        db=db,
        model=User,
        id=id,
        token=token,
        model_has_user_key=User
    )
    user_username = get_by_key_value(db, User, "username", user.username)
    user_email = get_by_key_value(db, User, "email", user.email)

    if (user.password != user.passwordConfirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. As senhas fornecidas não coincidem!")

    elif (user_username != None and user_username.id != id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O nome de usuário fornecido está em uso!")

    elif (user_email != None and user_email.id != id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O e-mail fornecido está em uso!")

    response = await update_object(db, User, id, user, token, User)
    return ResponseUnitSchema(
        data=response
    )


@router.delete("/{id}/",
               response_model=ResponseUnitSchema[UserRead],
               summary="Deleta um usuário",
               responses={
                   404: errors[404]
               },
               dependencies=[Depends(get_authenticated_user)],
               )
async def delete(
        id: int = Path(description=USER_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):

    user = await delete_object(
        db=db,
        model=User,
        id=id,
        token=token,
        model_has_user_key=User
    )
    return ResponseUnitSchema(
        data=user
    )
