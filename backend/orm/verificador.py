from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from models.verificador import Verificador
from models.verificadorTeste import VerificadorTeste
from orm.common.index import delete_object, filter_collection
from schemas.common.pagination import PaginationSchema
from schemas.verificador import VerificadorCreateSingle, VerificadorUpdatePartial, VerificadorUpdateTotal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema


async def create_verificador(
    db: Session,
    verificador: VerificadorCreateSingle,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == verificador.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")

    user = await get_authenticated_user(token=token, db=db)
    if (is_user(user) and db_problema.usuario_id != user.id):  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        db_verificador = Verificador(
            **verificador.model_dump(exclude=set(["problema"])))

        if (db_problema.verificador != None):
            await delete_object(
                db=db,
                model=Verificador,
                id=db_problema.verificador_id,  # type: ignore
                model_has_user_key=Problema
            )

        db.add(db_verificador)
        db_verificador.problema = db_problema
        db_problema.verificador = db_verificador

        db.commit()
        db.refresh(db_verificador)
        db.refresh(db_problema)

        return db_verificador

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_testes_verificador(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str
):
    db_verificador = db.query(Verificador).filter(Verificador.id == id).first()

    if (not db_verificador):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    if (is_user(user) and db_verificador.problema.usuario_id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(VerificadorTeste).filter(
            VerificadorTeste.verificador_id == id)

        db_verificador_testes, metadata = filter_collection(
            model=VerificadorTeste,
            pagination=pagination,
            query=query
        )

        return db_verificador_testes.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_verificador(
    db: Session,
    id: int,
    verificador: VerificadorUpdateTotal | VerificadorUpdatePartial,
    token: str
):
    db_verificador = db.query(Verificador).filter(Verificador.id == id).first()

    if (not db_verificador):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and user.id != db_verificador.problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in verificador:
            if (value != None and getattr(db_verificador, key)):
                setattr(db_verificador, key, value)

        db.commit()
        db.refresh(db_verificador)

        return db_verificador

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
