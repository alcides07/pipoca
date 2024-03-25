from fastapi.responses import FileResponse
from constants import DIRECTION_ORDER_BY_DESCRIPTION, FIELDS_ORDER_BY_DESCRIPTION
from dependencies.authorization_user import is_admin
from dependencies.is_admin import is_admin_dependencies
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter, search_fields_problema
from filters.problemaResposta import OrderByFieldsProblemaRespostaEnum, search_fields_problema_resposta
from models.problema import Problema
from models.problemaResposta import ProblemaResposta
from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Response, UploadFile, status, File
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.problema import ProblemaReadSimple
from schemas.problemaResposta import ProblemaRespostaReadFull
from utils.errors import errors
from models.user import User
from orm.common.index import delete_object, get_by_id, get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.user import UserCreate, UserReadFull, UserUpdatePartial, UserUpdateTotal
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import create_imagem_user, create_user, delete_imagem_user, get_imagem_user, update_user
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
from passlib.context import CryptContext


USER_ID_DESCRIPTION = "identificador do usuário"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
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


@router.get("/eu/",
            response_model=ResponseUnitSchema[UserReadFull],
            summary="Lista dados do usuário autenticado",
            dependencies=[Depends(get_authenticated_user)],
            responses={
                501: {"501": 501}
            })
async def read_me(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    user_db = await get_authenticated_user(token, db)

    if (is_admin(user_db)):
        raise HTTPException(
            status.HTTP_501_NOT_IMPLEMENTED,
            "Funcionalidade não disponível para administradores!"
        )

    user = await get_by_id(
        id=user_db.id,
        path_has_user_key="user",
        db=db,
        model=User,
        token=token
    )

    return ResponseUnitSchema(
        data=user
    )


@router.get("/problemas/",
            response_model=ResponsePaginationSchema[ProblemaReadSimple],
            summary="Lista problemas pertencentes ao usuário autenticado",
            )
async def read_problemas_me(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    filters: ProblemaFilter = Depends(),
    token: str = Depends(oauth2_scheme),
    sort: OrderByFieldsProblemaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    )
):
    problemas, metadata = await get_all(
        db=db,
        model=Problema,
        pagination=pagination,
        token=token,
        field_order_by=sort,
        direction=direction,
        filters=filters,
        search_fields=search_fields_problema,
        me_author=True
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/problemasRespostas/",
            response_model=ResponsePaginationSchema[ProblemaRespostaReadFull],
            summary="Lista respostas fornecidas à problemas pelo usuário autenticado",
            )
async def read_problemas_respostas_me(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    token: str = Depends(oauth2_scheme),
    sort: OrderByFieldsProblemaRespostaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    )
):
    problemas, metadata = await get_all(
        db=db,
        model=ProblemaResposta,
        pagination=pagination,
        token=token,
        field_order_by=sort,
        direction=direction,
        search_fields=search_fields_problema_resposta,
        me_author=True
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/{id}/imagem/",
            response_class=FileResponse,
            summary="Retorna a imagem de perfil de um usuário",
            dependencies=[Depends(get_authenticated_user)],
            responses={
                404: {"404": 404}
            })
async def get_imagem(
    id: int = Path(description=USER_ID_DESCRIPTION),
    db: Session = Depends(get_db)
):
    data = await get_imagem_user(
        id=id,
        db=db
    )

    return FileResponse(data)


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
        path_has_user_key="user"
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
    user: UserCreate = Body(description="Dados do usuário"),
    db: Session = Depends(get_db),
):
    data = create_user(db=db, user=user)

    return ResponseUnitSchema(data=data)


@router.post("/{id}/imagem/",
             response_class=FileResponse,
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

    return FileResponse(path=data)


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
        path_has_user_key="user"
    )
    if (user):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
