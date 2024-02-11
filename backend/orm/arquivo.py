from fastapi import HTTPException, status
from models.administrador import Administrador
from models.user import User
from schemas.arquivo import ArquivoCreateSingle
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.problema import Problema


async def create_arquivo(
    db: Session,
    arquivo: ArquivoCreateSingle,
    problema_id: int,
    user: User | Administrador
):
    problema = db.query(Problema).filter(Problema.id == problema_id).first()

    if (problema == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")
    try:
        if (isinstance(user, User) and problema.usuario_id != user.id):  # type: ignore
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
