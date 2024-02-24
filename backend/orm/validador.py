from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from orm.common.index import delete_object, filter_collection
from schemas.common.pagination import PaginationSchema
from schemas.validador import ValidadorCreateSingle, ValidadorUpdatePartial, ValidadorUpdateTotal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema


async def create_validador(
    db: Session,
    validador: ValidadorCreateSingle,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == validador.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")

    user = await get_authenticated_user(token=token, db=db)
    if (is_user(user) and db_problema.usuario_id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        db_validador = Validador(
            **validador.model_dump(exclude=set(["problema"])))

        if (db_problema.validador != None):
            await delete_object(
                db=db,
                token=token,
                model=Validador,
                id=db_problema.validador_id,
                path_has_user_key="Problema"
            )

        db.add(db_validador)
        db_validador.problema = db_problema
        db_problema.validador = db_validador

        db.commit()
        db.refresh(db_validador)
        db.refresh(db_problema)

        return db_validador

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_testes_validador(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str
):
    db_validador = db.query(Validador).filter(Validador.id == id).first()

    if (not db_validador):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    if (is_user(user) and db_validador.problema.usuario_id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(ValidadorTeste).filter(
            ValidadorTeste.validador_id == id)

        db_validador_testes, metadata = filter_collection(
            model=ValidadorTeste,
            pagination=pagination,
            query=query
        )

        return db_validador_testes.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_validador(
    db: Session,
    id: int,
    validador: ValidadorUpdateTotal | ValidadorUpdatePartial,
    token: str
):
    db_validador = db.query(Validador).filter(Validador.id == id).first()

    if (not db_validador):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and user.id != db_validador.problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:

        for key, value in validador:
            if (value != None and hasattr(db_validador, key)):
                setattr(db_validador, key, value)

        db.commit()
        db.refresh(db_validador)

        return db_validador

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
