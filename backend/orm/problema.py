import shutil
import tarfile
import io
import os
import tempfile
import docker
from typing import Optional
from docker.errors import DockerException
from compilers import commands
from sqlalchemy import Column
from constants import FILENAME_RUN, INPUT_TEST_FILENAME
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, status
from filters.arquivo import ArquivoFilter
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter, search_fields_problema
from filters.problemaTeste import ProblemaTesteFilter
from models.problemaResposta import ProblemaResposta
from models.problemaTeste import ProblemaTeste
from models.tag import Tag
from models.user import User
from models.validador import Validador
from models.validadorTeste import ValidadorTeste
from models.verificador import Verificador
from models.verificadorTeste import VerificadorTeste
from orm.common.index import filter_collection
from orm.problemaResposta import execute_teste_gerado, get_arquivo_gerador, get_arquivo_solucao
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.common.pagination import PaginationSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.arquivo import Arquivo
from models.declaracao import Declaracao
from models.problema import Problema
from schemas.declaracao import DeclaracaoCreate
from schemas.problema import ProblemaCreate, ProblemaCreateUpload, ProblemaIntegridade, ProblemaUpdatePartial, ProblemaUpdateTotal
from models.relationships.problema_tag import problema_tag_relationship
from schemas.problemaTeste import ProblemaTesteExecutado, TipoTesteProblemaEnum
from decouple import config


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
        verificador_teste.veredito = str(
            verificador_teste.veredito.value)

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
        validador_teste.veredito = str(
            validador_teste.veredito.value)

        db_validador_teste = ValidadorTeste(
            **validador_teste.model_dump())
        db.add(db_validador_teste)
        db_problema.validador.testes.append(db_validador_teste)


def create_arquivos(db, arquivo, db_problema):
    arquivo.secao = str(arquivo.secao.value)

    db_arquivo = Arquivo(
        **arquivo.model_dump())
    db.add(db_arquivo)
    db_problema.arquivos.append(db_arquivo)


def create_declaracoes(db, declaracao, db_problema):
    declaracao.idioma = str(declaracao.idioma.value)

    db_declaracao = Declaracao(
        **declaracao.model_dump(exclude=set(["imagens"])))
    db.add(db_declaracao)
    db_problema.declaracoes.append(db_declaracao)


def create_tags(db, tag, db_problema):
    db_tag = db.query(Tag).filter(Tag.nome == tag).first()
    if db_tag is None:
        db_tag = Tag(nome=tag)
        db.add(db_tag)
    db_problema.tags.append(db_tag)


def create_testes(db, teste, db_problema):
    teste.tipo = str(teste.tipo.value)

    db_teste = ProblemaTeste(**teste.model_dump())
    db.add(db_teste)
    db_problema.testes.append(db_teste)


def process_imagens_declaracoes(
    declaracoes: list[Declaracao],
    declaracoes_create: list[DeclaracaoCreate],
    db: Session
):
    try:
        for i, db_declaracao in enumerate(declaracoes):
            caminho_diretorio = f"static/problema-{db_declaracao.problema_id}/declaracao-{db_declaracao.id}"

            if not os.path.exists(caminho_diretorio):
                os.makedirs(caminho_diretorio)

            for j, _ in enumerate(declaracoes_create[i].imagens):
                caminho_imagem = os.path.join(
                    caminho_diretorio,
                    declaracoes_create[i].imagens[j].nome
                )

                with open(caminho_imagem, "wb") as buffer:
                    buffer.write(declaracoes_create[i].imagens[j].conteudo)

                db_declaracao.imagens = db_declaracao.imagens + \
                    [caminho_imagem]  # type: ignore

                db.commit()
                db.refresh(db_declaracao)

    except SQLAlchemyError:
        db.rollback()

        if os.path.exists(caminho_diretorio):
            shutil.rmtree(caminho_diretorio)

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro no armazenamento das imagens da declaração!"
        )


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

        process_imagens_declaracoes(
            declaracoes=db_problema.declaracoes,
            declaracoes_create=problema.declaracoes,
            db=db
        )

        return db_problema

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


async def execute_arquivo_solucao_com_testes_exemplo(
    arquivo_solucao: Arquivo,
    testes: list[str]
):
    codigo_solucao = str(arquivo_solucao.corpo)
    linguagem = str(arquivo_solucao.linguagem)
    extension = commands[linguagem]["extension"]

    client = docker.from_env()
    image = commands[linguagem]["image"]
    command = commands[linguagem]["run_test"]
    WORKING_DIR = "/arquivo/testes/"

    client.images.pull(image)
    volume = client.volumes.create()

    volumes = {
        volume.name: {  # type: ignore
            'bind': WORKING_DIR,
            'mode': 'rw'
        }
    }

    testes_executados: list[ProblemaTesteExecutado] = []

    try:
        for teste in testes:
            try:
                container = client.containers.create(
                    image=image,
                    command=command,
                    detach=True,
                    volumes=volumes,
                    working_dir=WORKING_DIR
                )

                with tempfile.NamedTemporaryFile(delete=False) as temp_codigo_solucao:
                    temp_codigo_solucao.write(codigo_solucao.encode())
                    TEMP_CODIGO_SOLUCAO = temp_codigo_solucao.name

                with tempfile.NamedTemporaryFile(delete=False) as temp_teste_problema:
                    temp_teste_problema.write(teste.encode())
                    TEMP_TESTE_PROBLEMA = temp_teste_problema.name

                tarstream = io.BytesIO()
                tar = tarfile.TarFile(fileobj=tarstream, mode='w')

                tar.add(
                    name=TEMP_CODIGO_SOLUCAO,
                    arcname=f'{WORKING_DIR}/{FILENAME_RUN}{extension}'
                )
                tar.add(
                    name=TEMP_TESTE_PROBLEMA,
                    arcname=f'{WORKING_DIR}/{INPUT_TEST_FILENAME}'
                )

                tar.close()

                container.put_archive(  # type: ignore
                    '/',
                    tarstream.getvalue()
                )

                container.start()  # type: ignore
                container.wait()  # type: ignore

                stdout_logs = container.logs(  # type: ignore
                    stdout=True, stderr=False
                ).decode()

                stderr_logs = container.logs(  # type: ignore
                    stdout=False, stderr=True
                ).decode()

                if (stderr_logs != ""):
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "O arquivo de solução oficial do problema possui alguma falha!"
                    )

                teste_executado = ProblemaTesteExecutado(
                    entrada=teste,
                    saida=stdout_logs
                )

                testes_executados.append(teste_executado)

            finally:
                container.stop()  # type: ignore
                container.remove()  # type: ignore
                os.remove(TEMP_CODIGO_SOLUCAO)
                os.remove(TEMP_TESTE_PROBLEMA)

    except DockerException:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro no processamento do arquivo de solução oficial do problema!"
        )

    finally:
        volume.remove()  # type: ignore

    return testes_executados


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
        arquivo_solucao = get_arquivo_solucao(db_problema)

        testes_exemplo = db.query(ProblemaTeste).filter(
            ProblemaTeste.problema_id == id).filter(ProblemaTeste.exemplo == True).all()

        arquivo_gerador: Arquivo | None = get_arquivo_gerador(db_problema)
        entradas_testes: list[str] = []

        for teste in testes_exemplo:
            teste_entrada = str(teste.entrada)

            if (bool(teste.tipo == TipoTesteProblemaEnum.GERADO.value)):
                if (arquivo_gerador is None):
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "O arquivo gerador de testes não foi encontrado!"
                    )

                teste_entrada = await execute_teste_gerado(
                    teste, arquivo_gerador
                )

            entradas_testes.append(teste_entrada)

        testes_executados = await execute_arquivo_solucao_com_testes_exemplo(
            testes=entradas_testes,
            arquivo_solucao=arquivo_solucao
        )

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
