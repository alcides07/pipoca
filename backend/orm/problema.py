from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, status
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter, search_fields_problema
from models.problemaResposta import ProblemaResposta
from models.problemaTeste import ProblemaTeste
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from models.verificador import Verificador
from models.verificadorTeste import VerificadorTeste
from orm.common.index import delete_object, filter_collection
from orm.tag import create_tag
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
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


def create_testes(db, teste, db_problema):
    db_teste = ProblemaTeste(**teste.model_dump())
    db.add(db_teste)
    db_problema.testes.append(db_teste)


async def create_problema(
    db: Session,
    problema: ProblemaCreate,
    token: str
):
    user = await get_authenticated_user(token, db)

    try:
        db_problema = Problema(
            **problema.model_dump(exclude=set(["tags", "declaracoes", "arquivos", "verificador", "validador", "usuario", "testes"])))
        db.add(db_problema)

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


async def update_problema(
    db: Session,
    id: int,
    problema: ProblemaUpdatePartial | ProblemaCreate,
    token: str,
):
    db_problema = db.query(Problema).filter(Problema.id == id).first()
    if not db_problema:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)
    if (is_user(user) and user.id != db_problema.usuario_id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        for key, value in problema:
            if (value != None):
                if (key == "declaracoes"):
                    declaracoes_ids = db.query(Declaracao.id).filter(
                        Declaracao.problema_id == db_problema.id).all()

                    for (declaracao_id,) in declaracoes_ids:
                        await delete_object(
                            db=db,
                            token=token,
                            model=Declaracao,
                            id=declaracao_id,
                            path_has_user_key="problema"
                        )

                    for declaracao in value:
                        create_declaracoes(db, declaracao, db_problema)

                elif (key == "arquivos"):
                    arquivos_ids = db.query(Arquivo.id).filter(
                        Arquivo.problema_id == db_problema.id).all()

                    for (arquivo_id,) in arquivos_ids:
                        await delete_object(
                            db=db,
                            token=token,
                            model=Arquivo,
                            id=arquivo_id,
                            path_has_user_key="problema"
                        )

                    for arquivo in value:
                        create_arquivos(db, arquivo, db_problema)

                elif (key == "testes"):
                    testes_ids = db.query(ProblemaTeste.id).filter(
                        ProblemaTeste.problema_id == db_problema.id).all()

                    for (teste_id, ) in testes_ids:
                        await delete_object(
                            db=db,
                            token=token,
                            model=ProblemaTeste,
                            id=teste_id,
                            path_has_user_key="problema"
                        )

                elif (key == "verificador"):
                    await delete_object(
                        db=db,
                        token=token,
                        model=Verificador,
                        id=db_problema.verificador_id,
                        path_has_user_key="problema"
                    )

                    create_verificador(db, problema, db_problema)
                    create_verificador_testes(db, problema, db_problema)

                elif (key == "validador"):
                    await delete_object(
                        token=token,
                        db=db,
                        model=Validador,
                        id=db_problema.validador_id,
                        path_has_user_key="problema"
                    )

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


async def get_testes_problema(
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
        query = db.query(ProblemaTeste).filter(
            ProblemaTeste.problema_id == id)

        db_problema_testes, metadata = filter_collection(
            model=ProblemaTeste,
            pagination=pagination,
            query=query
        )

        return db_problema_testes.all(), metadata

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
