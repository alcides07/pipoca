from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from schemas.arquivo import ArquivoCreateSingle, ArquivoUpdatePartial, ArquivoUpdateTotal, SecaoEnum
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.problema import Problema


async def create_arquivo(
    db: Session,
    arquivo: ArquivoCreateSingle,
    token: str
):
    problema = db.query(Problema).filter(
        Problema.id == arquivo.problema_id).first()

    if (problema == None):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token=token, db=db)
    if (is_user(user) and problema.usuario_id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        arquivo.secao = arquivo.secao.value  # type: ignore

        db_arquivo = Arquivo(
            **arquivo.model_dump(exclude=set(["problema"])))
        db.add(db_arquivo)
        problema.arquivos.append(db_arquivo)

        db.commit()
        db.refresh(db_arquivo)

        return db_arquivo

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação do arquivo!"
        )


async def update_arquivo(
    db: Session,
    id: int,
    arquivo: ArquivoUpdateTotal | ArquivoUpdatePartial,
    token: str
):
    db_arquivo = db.query(Arquivo).filter(Arquivo.id == id).first()

    if (not db_arquivo):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O arquivo não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and user.id != db_arquivo.problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in arquivo:
            if (value is not None and hasattr(db_arquivo, key)):
                setattr(db_arquivo, key, value.value if isinstance(
                    value, SecaoEnum) else value)

        db.commit()
        db.refresh(db_arquivo)

        return db_arquivo

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na atualização do arquivo!"
        )
