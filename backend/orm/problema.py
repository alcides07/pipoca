from typing import Optional
from sqlalchemy import Column
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, status
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter, search_fields_problema
from filters.problemaTeste import ProblemaTesteFilter
from models.problemaResposta import ProblemaResposta
from models.problemaTeste import ProblemaTeste
from models.tag import Tag
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from models.verificador import Verificador
from models.verificadorTeste import VerificadorTeste
from orm.common.index import filter_collection
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from models.problema import Problema
from schemas.problema import ProblemaCreate, ProblemaCreateUpload, ProblemaUpdatePartial, ProblemaUpdateTotal


def get_unique_nome_problema(
    db: Session,
    nome_problema: str,
    problema_id: Optional[Column[int]] = None
):
    db_problema = db.query(Problema).filter(
        Problema.nome == nome_problema).first()

    if (db_problema and bool(db_problema.id != problema_id)):
        i = 1
        while (True):
            new_name = db_problema.nome + f"-copy-{i}"

            db_new_problema = db.query(Problema).filter(
                Problema.nome == new_name).first()

            if (not db_new_problema):
                return new_name

            i += 1

    return None


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
    db_tag = db.query(Tag).filter(Tag.nome == tag).first()
    if db_tag is None:
        db_tag = Tag(nome=tag)
        db.add(db_tag)
    db_problema.tags.append(db_tag)


def create_testes(db, teste, db_problema):
    db_teste = ProblemaTeste(**teste.model_dump())
    db.add(db_teste)
    db_problema.testes.append(db_teste)


async def create_problema_upload(
    db: Session,
    problema: ProblemaCreateUpload,
    token: str
):
    user = await get_authenticated_user(token, db)

    try:
        db_problema = Problema(
            **problema.model_dump(exclude=set(["tags", "declaracoes", "arquivos", "verificador", "validador", "usuario", "testes"])))
        db.add(db_problema)

        new_name_problema = get_unique_nome_problema(
            db=db, nome_problema=problema.nome)
        if (bool(new_name_problema)):
            db_problema.nome = new_name_problema

        for declaracao in problema.declaracoes:
            create_declaracoes(db, declaracao, db_problema)

        for arquivo in problema.arquivos:
            create_arquivos(db, arquivo, db_problema)

        for tag in problema.tags:
            create_tags(db, tag, db_problema)

        for teste in problema.testes:
            create_testes(db, teste, db_problema)

        create_verificador(db, problema, db_problema)
        create_verificador_testes(db, problema, db_problema)

        create_validador(db, problema, db_problema)
        create_validador_testes(db, problema, db_problema)

        db_problema.usuario = user

        if (is_admin(user)):
            db_problema.usuario = None

        db.commit()
        db.refresh(db_problema)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_problema


async def create_problema(
    db: Session,
    problema: ProblemaCreate,
    token: str
):
    user = await get_authenticated_user(token, db)

    try:
        db_problema = Problema(
            **problema.model_dump(exclude=set(["tags", "declaracoes", "arquivos", "verificador", "validador", "usuario", "testes"])))

        new_name_problema = get_unique_nome_problema(
            db=db, nome_problema=problema.nome)
        if (bool(new_name_problema)):
            db_problema.nome = new_name_problema

        db.add(db_problema)
        db_problema.usuario = user

        if (is_admin(user)):
            db_problema.usuario = None

        db.commit()
        db.refresh(db_problema)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_problema


async def update_problema(
    db: Session,
    id: int,
    problema: ProblemaUpdatePartial | ProblemaUpdateTotal,
    token: str,
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()
    if not db_problema:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and user.id != db_problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        if (problema.nome):
            new_name_problema = get_unique_nome_problema(
                db=db, nome_problema=problema.nome, problema_id=db_problema.id)
            if (bool(new_name_problema)):
                problema.nome = new_name_problema

        for key, value in problema:
            if (value != None and hasattr(db_problema, key)):
                setattr(db_problema, key, value)

        db_problema.usuario = user
        if (is_admin(user)):
            db_problema.usuario = None

        db.commit()
        db.refresh(db_problema)

        return db_problema

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_all_problemas(
    db: Session,
    pagination: PaginationSchema,
    token: str,
    filters: ProblemaFilter,
    field_order_by: OrderByFieldsProblemaEnum,
    direction: DirectionOrderByEnum,
):

    user = await get_authenticated_user(token, db)
    query = db.query(Problema)

    if (is_user(user)):
        if (filters.privado == True):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        filters.privado = False

    db_problemas, metadata = filter_collection(
        model=Problema,
        pagination=pagination,
        filters=filters,
        query=query,
        direction=direction,
        field_order_by=field_order_by,
        search_fields=search_fields_problema
    )

    return db_problemas.all(), metadata


async def get_respostas_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(ProblemaResposta).filter(
            ProblemaResposta.problema_id == id)

        db_problema_respostas, metadata = filter_collection(
            model=ProblemaResposta,
            pagination=pagination,
            query=query
        )

        return db_problema_respostas.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_arquivos_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(Arquivo).filter(
            Arquivo.problema_id == id)

        db_problema_arquivos, metadata = filter_collection(
            model=Arquivo,
            pagination=pagination,
            query=query
        )

        return db_problema_arquivos.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_testes_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    filters: ProblemaTesteFilter,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id)
    ):
        if (bool(db_problema.privado) == True or filters.exemplo == False):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        filters.exemplo = True

    try:
        query = db.query(ProblemaTeste).filter(
            ProblemaTeste.problema_id == id)

        db_problema_testes, metadata = filter_collection(
            model=ProblemaTeste,
            pagination=pagination,
            filters=filters,
            query=query
        )

        return db_problema_testes.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_validador_problema(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return db_problema.validador


async def get_problema_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id)
        and
        bool(db_problema.privado == True)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return db_problema
