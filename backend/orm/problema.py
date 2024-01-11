from models.validador import Validador
from models.verificador import Verificador
from sqlalchemy.orm import Session
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from models.problema import Problema
from models.tag import Tag
from schemas.problema import ProblemaCreate


def create_problema(db: Session, problema: ProblemaCreate):
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

    db_validador = Validador(**problema.validador.model_dump())
    db.add(db_validador)
    db_problema.validador = db_validador
    db_validador.problema = db_problema

    db.commit()
    db.refresh(db_problema)

    return db_problema
