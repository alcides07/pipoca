from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from models.administrador import Administrador
from models.user import User
from schemas.arquivo import ArquivoCreateSingle, ArquivoUpdatePartial, ArquivoUpdateTotal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.problema import Problema


async def create_arquivo(
    db: Session,
    arquivo: ArquivoCreateSingle,
    user: User | Administrador
):
    problema = db.query(Problema).filter(
        Problema.id == arquivo.problema_id).first()

    if (problema == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")
    try:
        if (is_user(user) and problema.usuario_id != user.id):  # type: ignore
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db_arquivo = Arquivo(
            **arquivo.model_dump(exclude=set(["problema"])))
        db.add(db_arquivo)
        problema.arquivos.append(db_arquivo)

        db.commit()
        db.refresh(db_arquivo)

        return db_arquivo

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def update_arquivo(
    db: Session,
    id: int,
    arquivo: ArquivoUpdateTotal | ArquivoUpdatePartial,
    user: User | Administrador
):

    db_arquivo = db.query(Arquivo).filter(Arquivo.id == id).first()

    if (not db_arquivo):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (is_user(user) and user.id != db_arquivo.problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in arquivo:
            if (value != None and getattr(db_arquivo, key)):
                setattr(db_arquivo, key, value)

        db.commit()
        db.refresh(db_arquivo)

        return db_arquivo

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
