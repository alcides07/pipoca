from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.declaracao import Declaracao
from models.problema import Problema
from schemas.declaracao import DeclaracaoCreateSingle, DeclaracaoUpdatePartial, DeclaracaoUpdateTotal
from schemas.idioma import IdiomaEnum


async def get_declaracao_by_id(
    db: Session,
    id: int,
    token: str
):

    db_declaracao = db.query(Declaracao).filter(Declaracao.id == id).first()

    if (not db_declaracao):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    try:
        if (
            is_user(user)
            and
            db_declaracao.problema.privado == True
            and
            db_declaracao.problema.usuario_id != user.id
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return db_declaracao

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def create_declaracao(
    db: Session,
    token: str,
    declaracao: DeclaracaoCreateSingle
):
    db_problema = db.query(Problema).filter(
        Problema.id == declaracao.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problema não encontrado!"
        )

    user = await get_authenticated_user(token=token, db=db)
    if (is_user(user) and db_problema.usuario_id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        declaracao.idioma = declaracao.idioma.value  # type: ignore

        db_declaracao = Declaracao(
            **declaracao.model_dump(exclude=set(["problema"]))
        )

        db.add(db_declaracao)
        db_problema.declaracoes.append(db_declaracao)

        db.commit()
        db.refresh(db_declaracao)
        db.refresh(db_problema)

        return db_declaracao

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_declaracao(
    db: Session,
    id: int,
    declaracao: DeclaracaoUpdateTotal | DeclaracaoUpdatePartial,
    token: str
):
    db_declaracao = db.query(Declaracao).filter(Declaracao.id == id).first()

    if (not db_declaracao):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and user.id != db_declaracao.problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in declaracao:
            if (value is not None and hasattr(db_declaracao, key)):
                setattr(db_declaracao, key, value.value if isinstance(
                    value, IdiomaEnum) else value)

        db.commit()
        db.refresh(db_declaracao)

        return db_declaracao

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
