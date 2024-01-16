from models.tag import Tag
from fastapi import HTTPException, status
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from models.verificador import Verificador
from orm.common.index import delete_object
from orm.tag import create_tag
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from models.problema import Problema
from models.tag import Tag
from schemas.problema import ProblemaCreate, ProblemaUpdatePartial


def create_problema(db: Session, problema: ProblemaCreate):
    try:
        db_problema = Problema(
            **problema.model_dump(exclude=set(["tags", "declaracoes", "arquivos", "verificador", "validador"])))
        db.add(db_problema)

        for declaracao in problema.declaracoes:
            db_declaracao = Declaracao(
                **declaracao.model_dump())
            db.add(db_declaracao)
            db_problema.declaracoes.append(db_declaracao)

        for arquivo in problema.arquivos:
            db_arquivo = Arquivo(
                **arquivo.model_dump())
            db.add(db_arquivo)
            db_problema.arquivos.append(db_arquivo)

        for tag in problema.tags:
            db_tag = db.query(Tag).filter(Tag.nome == tag).first()
            if db_tag is None:
                db_tag = Tag(nome=tag)
                db.add(db_tag)
            db_problema.tags.append(db_tag)

        db_verificador = Verificador(**problema.verificador.model_dump())
        db.add(db_verificador)
        db_problema.verificador = db_verificador
        db_verificador.problema = db_problema

        db_validador = Validador(
            **problema.validador.model_dump(exclude=set(["testes"])))
        db.add(db_validador)
        db_problema.validador = db_validador
        db_validador.problema = db_problema

        for validador_teste in problema.validador.testes:
            db_validador_teste = ValidadorTeste(
                **validador_teste.model_dump())
            db.add(db_validador_teste)
            db_problema.validador.testes.append(db_validador_teste)

        db.commit()
        db.refresh(db_problema)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_problema


def update_problema(db: Session, id: int, problema: ProblemaUpdatePartial | ProblemaCreate):
    db_problema = db.query(Problema).filter(Problema.id == id).first()
    if not db_problema:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    try:
        for key, value in problema:
            if (value != None):
                if (key == "declaracoes"):
                    declaracoes_ids = db.query(Declaracao.id).filter(
                        Declaracao.problema_id == db_problema.id).all()

                    for (declaracao_id,) in declaracoes_ids:
                        delete_object(db, Declaracao, declaracao_id)

                    for declaracao in value:
                        db_declaracao = Declaracao(
                            **declaracao.model_dump())
                        db.add(db_declaracao)
                        db_problema.declaracoes.append(db_declaracao)

                elif (key == "arquivos"):
                    arquivos_ids = db.query(Arquivo.id).filter(
                        Arquivo.problema_id == db_problema.id).all()

                    for (arquivo_id,) in arquivos_ids:
                        delete_object(db, Arquivo, arquivo_id)

                    for arquivo in value:
                        db_arquivo = Arquivo(
                            **arquivo.model_dump())
                        db.add(db_arquivo)
                        db_problema.arquivos.append(db_arquivo)

                elif (key == "verificador"):
                    delete_object(db, Verificador,
                                  db_problema.verificador_id)  # type: ignore

                    db_verificador = Verificador(**value.model_dump())
                    db.add(db_verificador)
                    db_problema.verificador = db_verificador
                    db_verificador.problema = db_problema

                elif (key == "validador"):
                    delete_object(db, Validador,
                                  db_problema.validador_id)  # type: ignore

                    db_validador = Validador(
                        **value.model_dump(exclude=set(["testes"])))
                    db.add(db_validador)
                    db_problema.validador = db_validador
                    db_validador.problema = db_problema

                    for validador_teste in db_problema.validador.testes:
                        db_validador_teste = ValidadorTeste(
                            **validador_teste.model_dump())
                        db.add(db_validador_teste)
                        db_problema.validador.testes.append(db_validador_teste)

                elif (key == "tags"):
                    db_problema.tags = []

                    for tag in value:
                        db_tag = create_tag(db, tag)
                        db_problema.tags.append(db_tag)

                else:
                    if getattr(db_problema, key):
                        setattr(db_problema, key, value)

        db.commit()
        db.refresh(db_problema)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_problema
