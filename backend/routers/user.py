from fastapi.responses import FileResponse
from dependencies.is_admin import is_admin_dependencies
from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response, UploadFile, status, File
from utils.errors import errors
from models.user import User
from orm.common.index import delete_object, get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.user import UserCreate, UserReadFull, UserUpdatePartial, UserUpdateTotal
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_imagem_user, create_token_ativacao_conta_and_send_email, create_user, delete_imagem_user, get_imagem_user, update_user
from schemas.common.response import ResponseDataWithMessageSchema, ResponsePaginationSchema, ResponseUnitRequiredSchema
from passlib.context import CryptContext

USER_ID_DESCRIPTION = "identificador do usuário."

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/usuarios",
    tags=["usuários"],
)


@router.get("/",
            response_model=ResponsePaginationSchema[UserReadFull],
            summary="Lista usuários",
            dependencies=[Depends(is_admin_dependencies)]
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


@router.get("/{id}/imagem/",
            response_model=ResponseUnitRequiredSchema[str],
            summary="Retorna o endereço para a imagem de perfil de um usuário",
            dependencies=[Depends(get_authenticated_user)],
            responses={
                404: {"404": 404}
            })
async def get_imagem(
    id: int = Path(description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db)
):
    imagem = await get_imagem_user(
        id=id,
        db=db
    )

    return ResponseUnitRequiredSchema(
        data=imagem
    )


@router.get("/{id}/",
            response_model=ResponseUnitRequiredSchema[UserReadFull],
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
        path_has_user_key="user"
    )

    return ResponseUnitRequiredSchema(
        data=users
    )


@router.post("/",
             response_model=ResponseDataWithMessageSchema[UserReadFull],
             status_code=201,
             summary="Cadastra um usuário",
             responses={
                 400: errors[400],
                 422: errors[422],
             }
             )
async def create(
    user: UserCreate = Body(description="Dados do usuário"),
    db: Session = Depends(get_db),
):
    data = create_user(db=db, user=user)
    await create_token_ativacao_conta_and_send_email(
        data_token={
            "sub": data.email
        },
        destinatario=str(data.email)
    )

    return ResponseDataWithMessageSchema(
        data=data,
        message="Uma confirmação foi enviada para o e-mail fornecido!",
    )


@router.post("/{id}/imagem/",
             response_model=ResponseUnitRequiredSchema[str],
             status_code=200,
             summary="Cadastra uma imagem de perfil para um usuário",
             dependencies=[Depends(get_authenticated_user)],
             responses={
                 400: errors[400],
                 422: errors[422],
             }
             )
async def upload_imagem(
    id: int = Path(description=USER_ID_DESCRIPTION),
    imagem: UploadFile = File(
        description="Imagem **.jpeg** ou **.png** de perfil do usuário."
    ),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if (imagem.content_type not in ["image/jpeg", "image/png"]):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Formato de imagem inválido!"
        )

    data = await create_imagem_user(
        imagem=imagem,
        token=token,
        db=db,
        id=id
    )

    return ResponseUnitRequiredSchema(
        data=data
    )


@router.delete("/{id}/imagem/",
               status_code=204,
               summary="Deleta a imagem de perfil de um usuário",
               responses={
                   404: errors[404]
               }
               )
async def delete_image(
        id: int = Path(description=USER_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    imagem = await delete_imagem_user(
        db=db,
        token=token,
        id=id
    )

    if (imagem):
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}/",
            response_model=ResponseUnitRequiredSchema[UserReadFull],
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

    return ResponseUnitRequiredSchema(
        data=response
    )


@router.patch("/{id}/",
              response_model=ResponseUnitRequiredSchema[UserReadFull],
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

    return ResponseUnitRequiredSchema(
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
        path_has_user_key="user"
    )
    if (user):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
