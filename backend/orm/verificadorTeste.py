from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from models.verificador import Verificador
from models.verificadorTeste import VerificadorTeste
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from schemas.verificadorTeste import VereditoVerificadorTesteEnum, VerificadorTesteCreateSingle, VerificadorTesteUpdatePartial, VerificadorTesteUpdateTotal


async def create_verificador_teste(
    db: Session,
    verificador_teste: VerificadorTesteCreateSingle,
    token: str
):
    db_verificador = db.query(Verificador).filter(
        Verificador.id == verificador_teste.verificador_id
    ).first()

    if (not db_verificador):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O verificador não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    if (is_user(user) and db_verificador.problema.usuario_id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    for teste in db_verificador.testes:
        if (verificador_teste.numero == teste.numero):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Um teste com o mesmo número já foi registrado para este verificador!"
            )

    try:
        verificador_teste.veredito = verificador_teste.veredito.value  # type: ignore

        db_verificador_teste = VerificadorTeste(
            **verificador_teste.model_dump(exclude=set(["verificador"])))
        db_verificador.testes.append(db_verificador_teste)

        db.add(db_verificador_teste)
        db.commit()
        db.refresh(db_verificador_teste)
        db.refresh(db_verificador)

        return db_verificador_teste

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação do teste do verificador!"
        )


async def update_verificador_teste(
    db: Session,
    id: int,
    verificador_teste: VerificadorTesteUpdateTotal | VerificadorTesteUpdatePartial,
    token: str
):
    db_verificador_teste = db.query(VerificadorTeste).filter(
        VerificadorTeste.id == id).first()

    if (not db_verificador_teste):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O teste do verificador não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and db_verificador_teste.verificador.problema.usuario_id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for teste in db_verificador_teste.verificador.testes:
            if (verificador_teste.numero == teste.numero and bool(id != teste.id)):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Um teste com o mesmo número já foi registrado para este verificador!"
                )

        for key, value in verificador_teste:
            if (value is not None and hasattr(db_verificador_teste, key)):
                setattr(db_verificador_teste, key, value.value if isinstance(
                    value, VereditoVerificadorTesteEnum) else value)

        db.commit()
        db.refresh(db_verificador_teste)

        return db_verificador_teste

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na atualização do teste do verificador!"
        )


async def delete_verificador_teste(
    db: Session,
    id: int,
    token: str
):
    db_verificador_teste = db.query(VerificadorTeste).filter(
        VerificadorTeste.id == id).first()

    if (not db_verificador_teste):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O teste do verificador não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    try:
        if (is_user(user) and user.id != db_verificador_teste.verificador.problema.usuario_id):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        db.delete(db_verificador_teste)
        db.commit()
        return True

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na exclusão do teste do verificador!"
        )
