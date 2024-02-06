from fastapi import HTTPException, status
from models.user import User
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from models.verificador import Verificador
from models.verificadorTeste import VerificadorTeste
from orm.common.index import delete_object
from orm.tag import create_tag
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from models.problema import Problema
from schemas.problema import ProblemaCreate, ProblemaUpdatePartial


def create_verificador(db, problema, db_problema):
    db_verificador = Verificador(
        **problema.verificador.model_dump(exclude=set(["testes"])))
    db.add(db_verificador)
    db_problema.verificador = db_verificador
    db_verificador.problema = db_problema


def create_verificador_testes(db, problema, db_problema):
    for verificador_teste in problema.verificador.testes:
        db_verificador_teste = VerificadorTeste(
            **verificador_teste.model_dump())
        db.add(db_verificador_teste)
        db_problema.verificador.testes.append(
            db_verificador_teste)


def create_validador(db, problema, db_problema):
    db_validador = Validador(
        **problema.validador.model_dump(exclude=set(["testes"])))
    db.add(db_validador)
    db_problema.validador = db_validador
    db_validador.problema = db_problema


def create_validador_testes(db, problema, db_problema):
    for validador_teste in problema.validador.testes:
        db_validador_teste = ValidadorTeste(
            **validador_teste.model_dump())
        db.add(db_validador_teste)
        db_problema.validador.testes.append(db_validador_teste)


def create_arquivos(db, arquivo, db_problema):
    db_arquivo = Arquivo(
        **arquivo.model_dump())
    db.add(db_arquivo)
    db_problema.arquivos.append(db_arquivo)


def create_declaracoes(db, declaracao, db_problema):
    db_declaracao = Declaracao(
        **declaracao.model_dump())
    db.add(db_declaracao)
    db_problema.declaracoes.append(db_declaracao)


def create_tags(db, tag, db_problema):
    db_tag = create_tag(db, tag)
    db_problema.tags.append(db_tag)


def create_problema(db: Session, problema: ProblemaCreate, user: User):
    try:
        db_problema = Problema(
            **problema.model_dump(exclude=set(["tags", "declaracoes", "arquivos", "verificador", "validador", "usuario"])))
        db.add(db_problema)

        for declaracao in problema.declaracoes:
            create_declaracoes(db, declaracao, db_problema)

        for arquivo in problema.arquivos:
            create_arquivos(db, arquivo, db_problema)

        for tag in problema.tags:
            create_tags(db, tag, db_problema)

        create_verificador(db, problema, db_problema)
        create_verificador_testes(db, problema, db_problema)

        create_validador(db, problema, db_problema)
        create_validador_testes(db, problema, db_problema)

        db_problema.usuario = user

        db.commit()
        db.refresh(db_problema)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_problema


async def update_problema(db: Session,
                          id: int,
                          problema: ProblemaUpdatePartial | ProblemaCreate,
                          user: User,
                          ):
    db_problema = db.query(Problema).filter(Problema.id == id).first()
    if not db_problema:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (user.id != db_problema.usuario_id):  # type: ignore
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in problema:
            if (value != None):
                if (key == "declaracoes"):
                    declaracoes_ids = db.query(Declaracao.id).filter(
                        Declaracao.problema_id == db_problema.id).all()

                    for (declaracao_id,) in declaracoes_ids:
                        await delete_object(db, Declaracao, declaracao_id)

                    for declaracao in value:
                        create_declaracoes(db, declaracao, db_problema)

                elif (key == "arquivos"):
                    arquivos_ids = db.query(Arquivo.id).filter(
                        Arquivo.problema_id == db_problema.id).all()

                    for (arquivo_id,) in arquivos_ids:
                        await delete_object(db, Arquivo, arquivo_id)

                    for arquivo in value:
                        create_arquivos(db, arquivo, db_problema)

                elif (key == "verificador"):
                    await delete_object(db, Verificador,
                                        db_problema.verificador_id)  # type: ignore

                    create_verificador(db, problema, db_problema)
                    create_verificador_testes(db, problema, db_problema)

                elif (key == "validador"):
                    await delete_object(db, Validador,
                                        db_problema.validador_id)  # type: ignore

                    create_validador(db, problema, db_problema)
                    create_validador_testes(db, problema, db_problema)

                elif (key == "tags"):
                    db_problema.tags = []

                    for tag in value:
                        create_tags(db, tag, db_problema)

                else:
                    if getattr(db_problema, key):
                        setattr(db_problema, key, value)

        db_problema.usuario = user

        db.commit()
        db.refresh(db_problema)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_problema
