from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from enviroments import ENV
from filters.problemaResposta import OrderByFieldsProblemaRespostaEnum, search_fields_problema_resposta
from models.problemaResposta import ProblemaResposta
from models.user import User
from orm.common.index import filter_collection
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from schemas.problemaResposta import ProblemaRespostaCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema
from workers.correcaoProblema import correcao_problema
from models.problemaResposta import ProblemaResposta


async def create_problema_resposta(
    db: Session,
    problema_resposta: ProblemaRespostaCreate,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == problema_resposta.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (bool(db_problema.privado) == True):
        if (is_user(user) and bool(user.id != db_problema.usuario_id)):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "O problema o qual se está tentando submeter uma resposta é privado!"
            )

    if (problema_resposta.linguagem not in db_problema.linguagens):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "A linguagem de programação fornecida não é aceita nesse problema!"
        )

    try:
        problema_resposta_dict = problema_resposta.model_dump()
        task = correcao_problema.apply_async(
            args=[
                problema_resposta_dict,
                user.id,
                db_problema.id
            ]
        )

        if (ENV == "test"):
            return task.result

        return task.id

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação da resposta para o problema!"
        )


async def get_problema_resposta_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema_resposta = db.query(ProblemaResposta).filter(
        ProblemaResposta.id == id).first()

    if (not db_problema_resposta):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "A resposta não foi encontrada!"
        )

    user = await get_authenticated_user(token, db)

    try:

        if (
            is_user(user)
            and
            db_problema_resposta.usuario_id != user.id  # Não sou o autor da resposta
            and
            db_problema_resposta.problema.usuario_id != user.id  # Não sou o autor do problema
        ):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return db_problema_resposta

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pela resposta!"
        )


async def get_problemas_respostas_by_user(
        db: Session,
        pagination: PaginationSchema,
        token: str,
        field_order_by: OrderByFieldsProblemaRespostaEnum,
        direction: DirectionOrderByEnum,
        id: int
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(user.id != db_user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    query = db.query(ProblemaResposta)

    db_problemas_respostas, metadata = filter_collection(
        model=ProblemaResposta,
        pagination=pagination,
        query=query,
        direction=direction,
        field_order_by=field_order_by,
        search_fields=search_fields_problema_resposta
    )

    return db_problemas_respostas.all(), metadata


async def get_problema_id_respostas_by_user(
        db: Session,
        pagination: PaginationSchema,
        token: str,
        field_order_by: OrderByFieldsProblemaRespostaEnum,
        direction: DirectionOrderByEnum,
        id_problema: int,
        id_usuario: int
):
    db_user = db.query(User).filter(User.id == id_usuario).first()
    db_problema = db.query(Problema).filter(Problema.id == id_problema).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(user.id != db_user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    query = db.query(ProblemaResposta).filter(
        ProblemaResposta.problema_id == id_problema
    )

    db_problemas_respostas, metadata = filter_collection(
        model=ProblemaResposta,
        pagination=pagination,
        query=query,
        direction=direction,
        field_order_by=field_order_by,
        search_fields=search_fields_problema_resposta
    )

    return db_problemas_respostas.all(), metadata
