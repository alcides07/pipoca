import os
from datetime import timedelta
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status
from enviroments import ALGORITHM, API_BASE_URL, FRONT_BASE_URL, SECRET_KEY
from orm.common.index import get_by_key_value, get_by_key_value_exists
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdatePartial, UserUpdateTotal
from passlib.context import CryptContext
from decouple import config
from jose import ExpiredSignatureError, JWTError, jwt
from utils.create_token import create_token
from utils.send_email import send_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    if (user.password != user.passwordConfirmation):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "As senhas fornecidas não coincidem!"
        )

    elif (get_by_key_value_exists(db, User, "username", user.username)):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "O nome de usuário fornecido está em uso!"
        )

    elif (get_by_key_value_exists(db, User, "email", user.email)):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "O e-mail fornecido está em uso!"
        )

    try:
        user.password = pwd_context.hash(user.password)

        db_user = User(
            **user.model_dump(exclude=set(["passwordConfirmation"])))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação do usuário!"
        )


async def update_user(
    db: Session,
    id: int,
    data: UserUpdateTotal | UserUpdatePartial,
    token: str
):
    user_db = db.query(User).filter(User.id == id).first()

    if (not user_db):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    user = await get_authenticated_user(db=db, token=token)
    if (is_user(user) and user_db.id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        user_by_username = db.query(User).filter(
            User.username == data.username).first()

        if (user_by_username != None and bool(user_by_username.id != id)):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "O nome de usuário fornecido está em uso!"
            )

        user_by_email = db.query(User).filter(
            User.email == data.email).first()

        if (user_by_email != None and bool(user_by_email.id != id)):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "O e-mail fornecido está em uso!"
            )

        for key, value in data:
            if (value != None and hasattr(user_db, key)):
                setattr(user_db, key, value)

        db.commit()
        db.refresh(user_db)

        return user_db

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na atualização do usuário!"
        )


async def create_imagem_user(
    imagem: UploadFile,
    token: str,
    db: Session,
    id=id
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    user = await get_authenticated_user(db=db, token=token)
    if (is_user(user) and db_user.id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        caminho_diretorio = f"static/users-profile-{user.id}"

        if not os.path.exists(caminho_diretorio):
            os.makedirs(caminho_diretorio)

        if (imagem.content_type is not None):
            extensao_arquivo = imagem.content_type.split('/')[-1]

        caminho_imagem = os.path.join(
            caminho_diretorio, f"profile_image.{extensao_arquivo}")

        with open(caminho_imagem, "wb") as buffer:
            buffer.write(imagem.file.read())

        db_user.caminho_imagem = caminho_imagem  # type: ignore
        db.commit()
        db.refresh(db_user)

        endereco_imagem = API_BASE_URL + "/" + caminho_imagem

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro no armazenamento da imagem do usuário!"
        )

    return endereco_imagem


async def delete_imagem_user(
    token: str,
    db: Session,
    id=id
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    user = await get_authenticated_user(db=db, token=token)
    if (is_user(user) and db_user.id != user.id):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    caminho_imagem = str(db_user.caminho_imagem)

    if os.path.exists(caminho_imagem):
        try:
            os.remove(caminho_imagem)
            db_user.caminho_imagem = None  # type: ignore
            db.commit()
            db.refresh(db_user)
            return True

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro na exclusão da imagem do usuário!"
            )

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        "A imagem de perfil do usuário não foi encontrada!"
    )


async def get_imagem_user(
    db: Session,
    id=id
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário não foi encontrado!"
        )

    caminho_imagem = str(db_user.caminho_imagem)

    try:
        with open(caminho_imagem, "rb") as imagem_file:
            imagem_file.read()
            endereco_imagem = API_BASE_URL + "/" + caminho_imagem

    except IOError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "A imagem de perfil do usuário não foi encontrada!"
        )

    return endereco_imagem


async def activate_account(
    token: str,
    db: Session
):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Não foi possível validar a conta do usuário!",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")
        if email is None:
            raise credentials_exception

        db_user = get_by_key_value(db, User, "email", email)
        if db_user is None:
            raise credentials_exception

        db_user.ativa = True
        db.commit()
        db.refresh(db_user)

        return True

    except ExpiredSignatureError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "O link de ativação de conta expirou!"
        )

    except JWTError:
        raise credentials_exception


async def activate_acccount_simple(
    db: Session,
    db_user: User
):
    db_user.ativa = True  # type: ignore
    db.commit()
    db.refresh(db_user)


async def create_token_ativacao_conta_and_send_email(
    data_token: dict,
    destinatario: str,
):
    EXPIRE_MINUTES = 15
    access_token_expires = timedelta(minutes=EXPIRE_MINUTES)
    token = create_token(
        data=data_token,
        expires_delta=access_token_expires
    )

    url_ativacao = f"{FRONT_BASE_URL}?codigo={token}"

    send_email(
        remetente="plataformapipoca@gmail.com",
        destinatario=str(destinatario),
        assunto="Ativação de conta",
        corpo=f'''
        <p>O link de ativação ficará disponível por <b>{EXPIRE_MINUTES} minutos</b>.</p>
        <span>Para confirmar o seu endereço de e-mail, por favor clique <a href="{url_ativacao}">aqui</a>.</span>
        ''',
    )


async def verify_conta_user_resend_email(
    email: str,
    db: Session
):
    db_user = db.query(User).filter(User.email == email).first()

    if (not db_user):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "O usuário com o e-mail fornecido não foi encontrado!"
        )

    if (bool(db_user.ativa)):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "A conta do usuário já está ativa!"
        )
