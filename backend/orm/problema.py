from typing import Optional
from sqlalchemy import Column
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, UploadFile, status
from filters.arquivo import ArquivoFilter
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter, search_fields_problema
from filters.problemaTeste import ProblemaTesteFilter
from models.problemaResposta import ProblemaResposta
from models.problemaTeste import ProblemaTeste
from models.tag import Tag
from models.user import User
from orm.common.index import filter_collection
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from models.problema import Problema
from schemas.problema import ProblemaCreate, ProblemaCreateUpload, ProblemaIntegridade, ProblemaUpdatePartial, ProblemaUpdateTotal
from models.relationships.problema_tag import problema_tag_relationship
from schemas.problemaTeste import ProblemaTesteExecutado
from utils.create_file_timestamp import create_file_timestamp
from workers.importacao_problema import importacao_problema
from enviroments import ENV


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


async def create_problema_upload(
    db: Session,
    problema: ProblemaCreateUpload,
    pacote: UploadFile,
    token: str
):
    user = await get_authenticated_user(token, db)

    try:
        problema_dict = problema.model_dump()
        pacote_file_path = create_file_timestamp(pacote)

        task = importacao_problema.apply_async(
            args=[
                problema_dict,
                user.id,
                pacote_file_path
            ]
        )

        if (ENV == "test"):
            return task.result

        return task.id

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação do problema!"
        )


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

        return db_problema

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação do problema!"
        )


async def update_problema(
    db: Session,
    id: int,
    problema: ProblemaUpdatePartial | ProblemaUpdateTotal,
    token: str,
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()
    if not db_problema:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

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
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na atualização do problema!"
        )


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
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

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
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

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
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelas respostas do problema!"
        )


async def get_arquivos_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str,
    filters: ArquivoFilter
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(Arquivo).filter(
            Arquivo.problema_id == id)

        db_problema_arquivos, metadata = filter_collection(
            model=Arquivo,
            filters=filters,
            pagination=pagination,
            query=query
        )

        return db_problema_arquivos.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelos arquivos do problema!"
        )


async def get_testes_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    filters: ProblemaTesteFilter,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id)
    ):
        if (bool(db_problema.privado) == True or filters.exemplo == False):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

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
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelos testes do problema!"
        )


async def get_declaracoes_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(Declaracao).filter(
            Declaracao.problema_id == id)

        db_problema_declaracoes, metadata = filter_collection(
            model=Declaracao,
            pagination=pagination,
            query=query
        )

        return db_problema_declaracoes.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelas declarações do problema!"
        )


async def get_tags_problema(
    db: Session,
    id: int,
    pagination: PaginationSchema,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id)
        and
        bool(db_problema.privado) == True
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        query = db.query(Tag).join(problema_tag_relationship).filter(
            problema_tag_relationship.c.problema_id == db_problema.id)

        db_problema_tags, metadata = filter_collection(
            model=ProblemaTeste,
            pagination=pagination,
            query=query
        )

        return db_problema_tags.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelas tags do problema!"
        )


async def get_validador_problema(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return db_problema.validador


async def get_verificador_problema(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return db_problema.verificador


async def get_problema_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id)
        and
        bool(db_problema.privado == True)
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    testes_exemplo = [teste for teste in db_problema.testes if teste.exemplo]
    db_problema.testes = testes_exemplo

    return db_problema


async def get_meus_problemas(
        db: Session,
        pagination: PaginationSchema,
        token: str,
        field_order_by: OrderByFieldsProblemaEnum,
        direction: DirectionOrderByEnum,
        filters: ProblemaFilter,
        id: int
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(user.id != db_user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    query = db.query(Problema)

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


async def get_integridade_problema(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (is_user(user) and bool(db_problema.usuario_id != user.id)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    data = ProblemaIntegridade(
        declaracoes=len(db_problema.declaracoes) > 0,
        arquivos=len(db_problema.arquivos) > 0,
        testes=len(db_problema.testes) > 0,
        verificador=db_problema.verificador is not None,
        validador=db_problema.validador is not None
    )

    return data


async def get_testes_exemplo_de_problema_executados(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id and bool(db_problema.privado))
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        testes_exemplo = db.query(ProblemaTeste).filter(
            ProblemaTeste.problema_id == id,
            ProblemaTeste.exemplo == True
        ).all()

        testes_executados = [
            ProblemaTesteExecutado(
                entrada=str(teste.entrada),
                saida=str(teste.saida)
            ) for teste in testes_exemplo
        ]

        return testes_executados

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pelos testes de exemplo do problema!"
        )


async def get_linguagens_problema(
    db: Session,
    id: int,
    token: str
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)

    if (
        is_user(user)
        and
        bool(db_problema.usuario_id != user.id)
        and
        bool(db_problema.privado) == True
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    linguagens: list[str] = db_problema.linguagens

    return linguagens
