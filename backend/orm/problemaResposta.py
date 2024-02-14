from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from models.problemaResposta import ProblemaResposta
from models.administrador import Administrador
from models.user import User
from schemas.problemaResposta import ProblemaRespostaCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema


async def create_problema_resposta(
    db: Session,
    problema_resposta: ProblemaRespostaCreate,
    user: User | Administrador
):
    db_problema = db.query(Problema).filter(
        Problema.id == problema_resposta.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")

    try:
        if (bool(db_problema.privado) == True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Erro. O problema o qual se está tentando submeter uma resposta é privado!")

        db_problema_resposta = ProblemaResposta(
            **problema_resposta.model_dump(exclude=set(["problema", "usuario"])))

        db_problema.respostas.append(db_problema_resposta)

        if (is_user(user)):
            db_problema_resposta.usuario = user

        db.add(db_problema_resposta)
        db.commit()
        db.refresh(db_problema_resposta)

        return db_problema_resposta

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
