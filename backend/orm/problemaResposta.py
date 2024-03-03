import docker
import os
import tempfile
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, status
from models.problemaResposta import ProblemaResposta
from schemas.problemaResposta import ProblemaRespostaCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema
from docker.errors import DockerException
from languages_run import FILENAME_RUN, INPUT_FILENAME, commands


async def execute_user_code(
    resposta: str,
        linguagem: str,
        db_problema: Problema
):
    client = docker.from_env()
    image = commands[linguagem]["image"]
    command = commands[linguagem]["run"]

    with tempfile.TemporaryDirectory() as temp_dir:
        inp = "5\n8"

        with open(os.path.join(temp_dir, f"{FILENAME_RUN}{linguagem}"), "w") as file:
            file.write(resposta)

        with open(os.path.join(temp_dir, INPUT_FILENAME), "w") as file:
            file.write(inp)

        try:
            client.images.pull(image)
            volumes = {temp_dir: {'bind': '/user/submission/', 'mode': 'rw'}}

            container = client.containers.run(
                image,
                command,
                detach=True,
                volumes=volumes,
                working_dir='/user/submission/'
            )

            container.wait()

            stdout_logs = container.logs(stdout=True, stderr=False)
            stderr_logs = container.logs(stdout=False, stderr=True)

            stdout_logs_decode = stdout_logs.decode()
            stderr_logs_decode = stderr_logs.decode()

            container.stop()
            container.remove()

            if (stderr_logs_decode == ""):
                print("saida: ", stdout_logs_decode)
                print("executa testes aqui")

            return stdout_logs_decode, stderr_logs_decode

        except DockerException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


async def create_problema_resposta(
    db: Session,
    problema_resposta: ProblemaRespostaCreate,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == problema_resposta.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")

    user = await get_authenticated_user(token, db)
    if (bool(db_problema.privado) == True):
        if (is_user(user) and bool(user.id != db_problema.usuario_id)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Erro. O problema o qual se está tentando submeter uma resposta é privado!")

    try:
        stdout_logs, stderr_logs = await execute_user_code(
            resposta=problema_resposta.resposta,
            linguagem=problema_resposta.linguagem,
            db_problema=db_problema
        )

        veredito = "ok"

        if (stderr_logs != ""):
            print("erro: ", stderr_logs)
            veredito = stderr_logs

        db_problema_resposta = ProblemaResposta(
            **problema_resposta.model_dump(exclude=set(["problema", "usuario"])))

        db_problema.respostas.append(db_problema_resposta)

        db_problema_resposta.usuario = user
        db_problema_resposta.veredito = veredito

        # Código temporário
        db_problema_resposta.tempo = 250
        db_problema_resposta.memoria = 250

        if (is_admin(user)):
            db_problema_resposta.usuario = None

        db.add(db_problema_resposta)
        db.commit()
        db.refresh(db_problema_resposta)

        return db_problema_resposta

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_problema_resposta_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema_resposta = db.query(ProblemaResposta).filter(
        ProblemaResposta.id == id).first()

    if (not db_problema_resposta):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    try:

        if (
            is_user(user)
            and
            db_problema_resposta.usuario_id != user.id  # Não sou o autor da resposta
            and
            db_problema_resposta.problema.usuario_id != user.id  # Não sou o autor do problema
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return db_problema_resposta

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
