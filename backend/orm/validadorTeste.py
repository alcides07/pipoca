from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from schemas.validadorTeste import ValidadorTesteCreateSingle, ValidadorTesteUpdatePartial, ValidadorTesteUpdateTotal


async def get_validador_teste_by_id(
    db: Session,
    id: int,
    token: str
):
    db_validador_teste = db.query(ValidadorTeste).filter(
        ValidadorTeste.id == id).first()

    if (not db_validador_teste):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    try:
        if (is_user(user) and user.id != db_validador_teste.validador.problema.usuario_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return db_validador_teste

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def create_validador_teste(
    db: Session,
    validador_teste: ValidadorTesteCreateSingle,
    token: str
):
    db_validador = db.query(Validador).filter(
        Validador.id == validador_teste.validador_id
    ).first()

    if (not db_validador):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Validador não encontrado!")

    user = await get_authenticated_user(token, db)

    if (db_validador.problema.usuario_id != user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED)

    for teste in db_validador.testes:
        if (validador_teste.numero == teste.numero):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Erro. Um teste com o mesmo número já foi registrado para este validador!")

    try:
        db_validador_teste = ValidadorTeste(
            **validador_teste.model_dump(exclude=set(["validador"])))
        db_validador.testes.append(db_validador_teste)

        db.add(db_validador_teste)
        db.commit()
        db.refresh(db_validador_teste)
        db.refresh(db_validador)

        return db_validador_teste

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_validador_teste(
    db: Session,
    id: int,
    validador_teste: ValidadorTesteUpdateTotal | ValidadorTesteUpdatePartial,
    token: str
):
    db_validador_teste = db.query(ValidadorTeste).filter(
        ValidadorTeste.id == id).first()

    if (not db_validador_teste):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (db_validador_teste.validador.problema.usuario_id != user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        for teste in db_validador_teste.validador.testes:
            if (validador_teste.numero == teste.numero and bool(id != teste.id)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Erro. Um teste com o mesmo número já foi registrado para este validador!")

        for key, value in validador_teste:
            if (value != None and getattr(db_validador_teste, key)):
                setattr(db_validador_teste, key, value)

        db.commit()
        db.refresh(db_validador_teste)

        return db_validador_teste

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def delete_validador_teste(
    db: Session,
    id: int,
    token: str
):
    db_validador_teste = db.query(ValidadorTeste).filter(
        ValidadorTeste.id == id).first()

    if (not db_validador_teste):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    try:
        if (is_user(user) and user.id != db_validador_teste.validador.problema.usuario_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db.delete(db_validador_teste)
        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
