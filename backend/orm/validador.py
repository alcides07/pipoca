from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from models.administrador import Administrador
from models.user import User
from models.validador import Validador
from orm.common.index import delete_object
from schemas.validador import ValidadorCreateSingle, ValidadorUpdatePartial, ValidadorUpdateTotal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema


async def create_validador(
    db: Session,
    validador: ValidadorCreateSingle,
    user: User | Administrador
):
    db_problema = db.query(Problema).filter(
        Problema.id == validador.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")

    try:
        if (is_user(user) and db_problema.usuario_id != user.id):  # type: ignore
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db_validador = Validador(
            **validador.model_dump(exclude=set(["problema"])))

        if (db_problema.validador != None):
            await delete_object(
                db=db,
                model=Validador,
                id=db_problema.validador_id,  # type: ignore
                model_has_user_key=Problema
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


async def update_validador(
    db: Session,
    id: int,
    validador: ValidadorUpdateTotal | ValidadorUpdatePartial,
    user: User | Administrador
):
    db_validador = db.query(Validador).filter(Validador.id == id).first()

    if (not db_validador):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (is_user(user) and user.id != db_validador.problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in validador:
            if (value != None and getattr(db_validador, key)):
                setattr(db_validador, key, value)

        db.commit()
        db.refresh(db_validador)

        return db_validador

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
