import docker
import os
import tempfile
import requests
import shutil
from compilers import commands
from typing import List
from constants import FILENAME_RUN, INPUT_TEST_FILENAME, OUTPUT_JUDGE_FILENAME, OUTPUT_USER_FILENAME, URL_TEST_LIB
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, status
from models.arquivo import Arquivo
from models.problemaResposta import ProblemaResposta
from models.problemaTeste import ProblemaTeste
from schemas.arquivo import SecaoEnum
from schemas.problemaResposta import ProblemaRespostaCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema
from docker.errors import DockerException
from schemas.problemaTeste import TipoTesteProblemaEnum


def get_arquivo_solucao(
        db_problema: Problema
):
    for arquivo in db_problema.arquivos:
        if (arquivo.secao == SecaoEnum.SOLUCAO.value and arquivo.status == "main"):
            return arquivo

    raise HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "O arquivo de solução principal do problema não foi encontrado!"
    )


def get_arquivo_gerador(db_problema: Problema):
    for arquivo in db_problema.arquivos:
        if (arquivo.secao == SecaoEnum.GERADOR.value):
            return arquivo
    return None


async def execute_teste_gerado(
    teste: ProblemaTeste,
    arquivo_gerador: Arquivo
):
    linguagem_gerador: str = arquivo_gerador.linguagem  # type: ignore
    extensao_gerador: str = commands[linguagem_gerador]["extension"]

    client = docker.from_env()
    image = commands[linguagem_gerador]["image"]
    WORKING_DIR = "/problema/gerador/"

    teste_entrada = " ".join(teste.entrada.split()[1:])
    client.images.pull(image)
    volume = client.volumes.create()

    with tempfile.NamedTemporaryFile(delete=False) as temp_testlib:
        temp_filename_testlib = temp_testlib.name
        response = requests.get(URL_TEST_LIB, stream=True)
        response.raise_for_status()
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, temp_testlib)

    with tempfile.NamedTemporaryFile(delete=False) as temp_gerador:
        temp_gerador.write(arquivo_gerador.corpo.encode())
        temp_filename_gerador = temp_gerador.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_teste:
        temp_filename_teste = temp_teste.name
        temp_teste.write(teste_entrada.encode())

    volumes = {
        volume.name: {  # type: ignore
            'bind': WORKING_DIR,
            'mode': 'rw'
        },
        temp_filename_testlib: {
            'bind': '/temp_testlib',
            'mode': 'rw'
        },
        temp_filename_gerador: {
            'bind': '/temp_gerador',
            'mode': 'rw'
        },
        temp_filename_teste: {
            'bind': '/temp_teste',
            'mode': 'rw'
        }
    }
    script = f'''
        cp /temp_testlib {WORKING_DIR}/testlib.h
        cp /temp_gerador {WORKING_DIR}/{FILENAME_RUN}{extensao_gerador}
        cp /temp_teste {WORKING_DIR}/{INPUT_TEST_FILENAME}
        {commands[linguagem_gerador]["run_gerador"]}
        '''
    command = ['/bin/bash', '-c', script]

    try:
        container = client.containers.run(
            image,
            command,
            detach=True,
            volumes=volumes,
            working_dir=WORKING_DIR
        )

        container.wait()  # type: ignore

        stdout_logs = container.logs(  # type: ignore
            stdout=True, stderr=False)
        stderr_logs = container.logs(  # type: ignore
            stdout=False, stderr=True)

        stdout_logs_decode = stdout_logs.decode()
        stderr_logs_decode = stderr_logs.decode()

        container.stop()  # type: ignore
        container.remove()  # type: ignore
        volume.remove()  # type: ignore

        if (stderr_logs_decode != ""):
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "O arquivo gerador de testes do problema possui alguma falha!"
            )

    except DockerException:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na execução dos testes gerados!"
        )

    finally:
        os.remove(temp_filename_testlib)
        os.remove(temp_filename_teste)
        os.remove(temp_filename_gerador)

    return stdout_logs_decode


async def execute_checker(
    db_problema: Problema,
    output_codigo_solucao: list[str],
    output_codigo_user: list[str],
    output_testes_gerados: List[str]
):
    codigo_verificador = db_problema.verificador.corpo
    linguagem_verificador: str = db_problema.verificador.linguagem
    extensao_verificador: str = commands[linguagem_verificador]["extension"]
    veredito: list[str] = []

    client = docker.from_env()
    image = commands[linguagem_verificador]["image"]
    WORKING_DIR = "/checker/testes/"

    client.images.pull(image)
    volume = client.volumes.create()

    with tempfile.NamedTemporaryFile(delete=False) as temp_testlib:
        temp_filename_testlib = temp_testlib.name
        response = requests.get(URL_TEST_LIB, stream=True)
        response.raise_for_status()
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, temp_testlib)

    with tempfile.NamedTemporaryFile(delete=False) as temp_verificador:
        temp_verificador.write(codigo_verificador.encode())
        temp_filename_verificador = temp_verificador.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_teste:
        temp_filename_teste = temp_teste.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_saida_user:
        temp_filename_saida_user = temp_saida_user.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_saida_solucao:
        temp_filename_saida_solucao = temp_saida_solucao.name

    volumes = {
        volume.name: {  # type: ignore
            'bind': WORKING_DIR,
            'mode': 'rw'
        },
        temp_filename_testlib: {
            'bind': '/temp_testlib',
            'mode': 'rw'
        },
        temp_filename_verificador: {
            'bind': '/temp_verificador',
            'mode': 'rw'
        },
        temp_filename_teste: {
            'bind': '/temp_teste',
            'mode': 'rw'
        },
        temp_filename_saida_user: {
            'bind': '/temp_saida_user',
            'mode': 'rw'
        },
        temp_filename_saida_solucao: {
            'bind': '/temp_saida_solucao',
            'mode': 'rw'
        }
    }
    script = f'''
    cp /temp_testlib {WORKING_DIR}/testlib.h
    cp /temp_verificador {WORKING_DIR}/{FILENAME_RUN}{extensao_verificador}
    cp /temp_teste {WORKING_DIR}/{INPUT_TEST_FILENAME}
    cp /temp_saida_user {WORKING_DIR}/{OUTPUT_USER_FILENAME}
    cp /temp_saida_solucao {WORKING_DIR}/{OUTPUT_JUDGE_FILENAME}
    {commands[linguagem_verificador]["run_checker"]}
    '''
    command = ['/bin/bash', '-c', script]

    try:
        for i, teste in enumerate(db_problema.testes):
            teste_entrada = teste.entrada

            if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                teste_entrada = output_testes_gerados[i]

            with open(temp_filename_teste, 'w') as temp_teste:
                temp_teste.write(teste_entrada)

            with open(temp_filename_saida_user, 'w') as temp_saida_user:
                temp_saida_user.write(output_codigo_user[i])

            with open(temp_filename_saida_solucao, 'w') as temp_saida_solucao:
                temp_saida_solucao.write(output_codigo_solucao[i])

            try:
                container = client.containers.run(
                    image=image,
                    command=command,
                    detach=True,
                    volumes=volumes,
                    working_dir=WORKING_DIR
                )

                container.wait()  # type: ignore

                stderr_logs = container.logs(  # type: ignore
                    stdout=False, stderr=True)

                stderr_logs_decode = stderr_logs.decode()

                if (stderr_logs_decode != ""):
                    veredito_mensagem = stderr_logs_decode.split()
                    veredito.append(veredito_mensagem[0].lower())

            except DockerException:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "Ocorreu um erro no processo de comparação dos resultados!"
                )

            finally:
                container.stop()  # type: ignore
                container.remove()  # type: ignore

    finally:
        os.remove(temp_filename_testlib)
        os.remove(temp_filename_teste)
        os.remove(temp_filename_verificador)
        os.remove(temp_filename_saida_user)
        os.remove(temp_filename_saida_solucao)
        volume.remove()  # type: ignore

    return veredito


async def execute_codigo_user(
    db_problema: Problema,
    problema_resposta: ProblemaRespostaCreate,
    output_testes_gerados: List[str]
):
    codigo_user = problema_resposta.resposta
    linguagem = problema_resposta.linguagem
    extension = commands[linguagem.value]["extension"]

    client = docker.from_env()
    image = commands[linguagem.value]["image"]
    WORKING_DIR = "/user/submission/"

    client.images.pull(image)
    volume = client.volumes.create()

    with tempfile.NamedTemporaryFile(delete=False) as temp_teste:
        temp_filename_teste = temp_teste.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_codigo_user:
        temp_codigo_user.write(codigo_user.encode())
        temp_filename_codigo_user = temp_codigo_user.name

    volumes = {
        volume.name: {  # type: ignore
            'bind': WORKING_DIR,
            'mode': 'rw'
        },
        temp_filename_codigo_user: {
            'bind': '/temp_codigo_user',
            'mode': 'rw'
        },
        temp_filename_teste: {
            'bind': '/temp_teste',
            'mode': 'rw'
        }
    }
    script = f'''
        cp /temp_codigo_user {WORKING_DIR}/{FILENAME_RUN}{extension}
        cp /temp_teste {WORKING_DIR}/{INPUT_TEST_FILENAME}
        {commands[linguagem.value]["run_test"]}
        '''
    command = ['/bin/bash', '-c', script]

    output_codigo_user: List[str] = []

    try:
        for i, teste in enumerate(db_problema.testes):
            teste_entrada = teste.entrada

            if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                teste_entrada = output_testes_gerados[i]

            with open(temp_filename_teste, 'w') as temp_teste:
                temp_teste.write(teste_entrada)

            try:
                container = client.containers.run(
                    image,
                    command,
                    detach=True,
                    volumes=volumes,
                    working_dir=WORKING_DIR
                )

                container.wait()  # type: ignore

                stdout_logs = container.logs(  # type: ignore
                    stdout=True, stderr=False)
                stderr_logs = container.logs(  # type: ignore
                    stdout=False, stderr=True)

                stdout_logs_decode = stdout_logs.decode()
                stderr_logs_decode = stderr_logs.decode()

                output_codigo_user.append(stdout_logs_decode)

                if (stderr_logs_decode != ""):
                    return f"Erro em tempo de execução no teste {i+1}"

            except DockerException:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "Ocorreu um erro no processamento do código do usuário!"
                )

            finally:
                container.stop()  # type: ignore
                container.remove()  # type: ignore

    finally:
        os.remove(temp_filename_teste)
        os.remove(temp_filename_codigo_user)
        volume.remove()  # type: ignore

    return output_codigo_user


async def execute_arquivo_solucao(
    db_problema: Problema,
    arquivo_solucao: Arquivo,
    arquivo_gerador: Arquivo | None
):
    codigo_solucao = str(arquivo_solucao.corpo)
    linguagem = str(arquivo_solucao.linguagem)
    extension = commands[linguagem]["extension"]

    client = docker.from_env()
    image = commands[linguagem]["image"]
    WORKING_DIR = "/arquivo/testes/"

    client.images.pull(image)
    volume = client.volumes.create()

    with tempfile.NamedTemporaryFile(delete=False) as temp_teste:
        temp_filename_teste = temp_teste.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_solucao:
        temp_solucao.write(codigo_solucao.encode())
        temp_filename_solucao = temp_solucao.name

    volumes = {
        volume.name: {  # type: ignore
            'bind': WORKING_DIR,
            'mode': 'rw'
        },
        temp_filename_solucao: {
            'bind': '/temp_solucao',
            'mode': 'rw'
        },
        temp_filename_teste: {
            'bind': '/temp_teste',
            'mode': 'rw'
        }
    }
    script = f'''
        cp /temp_solucao {WORKING_DIR}/{FILENAME_RUN}{extension}
        cp /temp_teste {WORKING_DIR}/{INPUT_TEST_FILENAME}
        {commands[linguagem]["run_test"]}
        '''
    command = ['/bin/bash', '-c', script]

    output_codigo_solucao: List[str] = []
    output_testes_gerados: List[str] = []

    try:
        for teste in db_problema.testes:
            teste_entrada = teste.entrada

            if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                if (arquivo_gerador is None):
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "O arquivo gerador de testes não foi encontrado!"
                    )

                teste_entrada = await execute_teste_gerado(
                    teste, arquivo_gerador)

            output_testes_gerados.append(teste_entrada)

            with open(temp_filename_teste, 'w') as temp_teste:
                temp_teste.write(teste_entrada)

            try:
                container = client.containers.run(
                    image=image,
                    command=command,
                    detach=True,
                    volumes=volumes,
                    working_dir=WORKING_DIR
                )

                container.wait()  # type: ignore

                stdout_logs = container.logs(  # type: ignore
                    stdout=True, stderr=False)
                stderr_logs = container.logs(  # type: ignore
                    stdout=False, stderr=True)

                stdout_logs_decode = stdout_logs.decode()
                stderr_logs_decode = stderr_logs.decode()
                output_codigo_solucao.append(stdout_logs_decode)

                if (stderr_logs_decode != ""):
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "O arquivo de solução oficial do problema possui alguma falha!"
                    )

            except DockerException:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "Ocorreu um erro no processamento do arquivo de solução oficial do problema!"
                )

            finally:
                container.stop()  # type: ignore
                container.remove()  # type: ignore

    finally:
        os.remove(temp_filename_teste)
        os.remove(temp_filename_solucao)
        volume.remove()  # type: ignore

    return output_codigo_solucao, output_testes_gerados


async def execute_processo_resolucao(
    problema_resposta: ProblemaRespostaCreate,
    db_problema: Problema
):
    arquivo_solucao = get_arquivo_solucao(db_problema)
    arquivo_gerador = get_arquivo_gerador(db_problema)

    output_codigo_solucao, output_testes_gerados = await execute_arquivo_solucao(
        db_problema,
        arquivo_solucao,
        arquivo_gerador
    )

    output_codigo_user = await execute_codigo_user(
        db_problema,
        problema_resposta,
        output_testes_gerados
    )

    if (isinstance(output_codigo_user, str)):
        return [], [], [], output_codigo_user

    veredito = await execute_checker(
        db_problema,
        output_codigo_solucao,
        output_codigo_user,
        output_testes_gerados
    )
    return veredito, output_codigo_user, output_codigo_solucao, None


async def create_problema_resposta(
    db: Session,
    problema_resposta: ProblemaRespostaCreate,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == problema_resposta.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O problema não foi encontrado!"
        )

    user = await get_authenticated_user(token, db)
    if (bool(db_problema.privado) == True):
        if (is_user(user) and bool(user.id != db_problema.usuario_id)):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "O problema o qual se está tentando submeter uma resposta é privado!"
            )

    try:
        veredito, output_user, output_judge, erro = await execute_processo_resolucao(
            problema_resposta=problema_resposta,
            db_problema=db_problema
        )

        db_problema_resposta = ProblemaResposta(
            **problema_resposta.model_dump(exclude=set(["problema", "usuario"])))

        db_problema.respostas.append(db_problema_resposta)
        db_problema_resposta.usuario = user

        db_problema_resposta.veredito = veredito  # type: ignore
        db_problema_resposta.erro = erro  # type: ignore
        db_problema_resposta.saida_usuario = output_user  # type: ignore
        db_problema_resposta.saida_esperada = output_judge  # type: ignore

        # Bloco temporário
        db_problema_resposta.tempo = 250
        db_problema_resposta.memoria = 250
        #

        if (is_admin(user)):
            db_problema_resposta.usuario = None

        db.add(db_problema_resposta)
        db.commit()
        db.refresh(db_problema_resposta)

        return db_problema_resposta

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação da resposta para o problema!"
        )


async def get_problema_resposta_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema_resposta = db.query(ProblemaResposta).filter(
        ProblemaResposta.id == id).first()

    if (not db_problema_resposta):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "A resposta não foi encontrada!"
        )

    user = await get_authenticated_user(token, db)

    try:

        if (
            is_user(user)
            and
            db_problema_resposta.usuario_id != user.id  # Não sou o autor da resposta
            and
            db_problema_resposta.problema.usuario_id != user.id  # Não sou o autor do problema
        ):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return db_problema_resposta

    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na busca pela resposta!"
        )
