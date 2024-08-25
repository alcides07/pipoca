from schemas.problemaTeste import ProblemaTesteCreateSingle, ProblemaTesteUpdatePartial, ProblemaTesteUpdateTotal, TipoTesteProblemaEnum
from models.problemaTeste import ProblemaTeste
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema


async def create_problema_teste(
    db: Session,
    problema_teste: ProblemaTesteCreateSingle,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == problema_teste.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (db_problema.usuario_id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    for teste in db_problema.testes:
        if (problema_teste.numero == teste.numero):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Um teste com o mesmo número já foi registrado para este problema!"
            )

    try:
        problema_teste.tipo = str(problema_teste.tipo.value)  # type: ignore

        db_problema_teste = ProblemaTeste(
            **problema_teste.model_dump(exclude=set(["problema"])))

        # TEMPORÁRIO: EM BREVE DEVE-SE EXECUTAR O TESTE E ARMAZENAR A SAÍDA REAL
        db_problema_teste.saida = ""

        db_problema.testes.append(db_problema_teste)

        db.add(db_problema_teste)
        db.commit()
        db.refresh(db_problema_teste)

        return db_problema_teste

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação do teste!"
        )


async def update_problema_teste(
    db: Session,
    id: int,
    problema_teste: ProblemaTesteUpdateTotal | ProblemaTesteUpdatePartial,
    token: str
):
    db_problema_teste = db.query(ProblemaTeste).filter(
        ProblemaTeste.id == id).first()

    if (not db_problema_teste):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O teste não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (db_problema_teste.problema.usuario_id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for teste in db_problema_teste.problema.testes:
            if (problema_teste.numero == teste.numero and bool(id != teste.id)):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Um teste com o mesmo número já foi registrado para este problema!"
                )

        for key, value in problema_teste:
            if (value is not None and hasattr(db_problema_teste, key)):
                setattr(db_problema_teste, key, value.value if isinstance(
                    value, TipoTesteProblemaEnum) else value)

        db.commit()
        db.refresh(db_problema_teste)

        return db_problema_teste

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na atualização do teste!"
        )


async def get_problema_teste_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema_teste = db.query(ProblemaTeste).filter(
        ProblemaTeste.id == id).first()

    if (not db_problema_teste):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O teste não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    try:

        if (is_user(user) and db_problema_teste.problema.usuario_id != user.id):  # Não sou o dono
            # O problema é privado ou não é um teste de exemplo
            if (db_problema_teste.problema.privado == True or bool(db_problema_teste.exemplo) == False):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return db_problema_teste

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelo teste!"
        )
