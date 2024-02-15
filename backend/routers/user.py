from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, Path, Response, status
from utils.errors import errors
from models.user import User
from orm.common.index import delete_object, get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.user import UserCreate, UserReadFull, UserUpdatePartial, UserUpdateTotal
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_user, update_user
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from passlib.context import CryptContext


USER_ID_DESCRIPTION = "identificador do usuário"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/",
            response_model=ResponsePaginationSchema[UserReadFull],
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
            response_model=ResponseUnitSchema[UserReadFull],
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
             response_model=ResponseUnitSchema[UserReadFull],
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
    data = create_user(db=db, user=user)

    return ResponseUnitSchema(data=data)


@router.put("/{id}/",
            response_model=ResponseUnitSchema[UserReadFull],
            summary="Atualiza um usuário por completo",
            responses={
                404: errors[404]
            },
            dependencies=[Depends(get_authenticated_user)],
            )
async def total_update(
        id: int = Path(description=USER_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: UserUpdateTotal = Body(
            description="Usuário a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme)
):
    response = await update_user(
        db=db,
        id=id,
        data=data,
        token=token
    )

    return ResponseUnitSchema(
        data=response
    )


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[UserReadFull],
              summary="Atualiza um usuário parcialmente",
              responses={
                  400: errors[400],
                  404: errors[404]
              },
              dependencies=[Depends(get_authenticated_user)],
              )
async def partial_update(
        id: int = Path(description=USER_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: UserUpdatePartial = Body(
            description="Usuário a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme)
):
    response = await update_user(
        db=db,
        id=id,
        data=data,
        token=token
    )

    return ResponseUnitSchema(
        data=response
    )


@router.delete("/{id}/",
               status_code=204,
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
    if (user):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
