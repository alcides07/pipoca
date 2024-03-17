import os
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status
from orm.common.index import get_by_key_value_exists
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdatePartial, UserUpdateTotal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    if (user.password != user.passwordConfirmation):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="As senhas fornecidas não coincidem!"
        )

    elif (get_by_key_value_exists(db, User, "username", user.username)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome de usuário fornecido está em uso!"
        )

    elif (get_by_key_value_exists(db, User, "email", user.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O e-mail fornecido está em uso!"
        )

    user.password = pwd_context.hash(user.password)

    db_user = User(
        **user.model_dump(exclude=set(["passwordConfirmation"])))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_user(
    db: Session,
    id: int,
    data: UserUpdateTotal | UserUpdatePartial,
    token: str
):
    user_db = db.query(User).filter(User.id == id).first()

    if (not user_db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(db=db, token=token)
    if (is_user(user) and user_db.id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        user_by_username = db.query(User).filter(
            User.username == data.username).first()

        if (user_by_username != None and bool(user_by_username.id != id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome de usuário fornecido está em uso!"
            )

        user_by_email = db.query(User).filter(
            User.email == data.email).first()

        if (user_by_email != None and bool(user_by_email.id != id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O e-mail fornecido está em uso!"
            )

        for key, value in data:
            if (value != None and hasattr(user_db, key)):
                setattr(user_db, key, value)

        db.commit()
        db.refresh(user_db)

        return user_db

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


async def create_imagem_user(
    imagem: UploadFile,
    token: str,
    db: Session,
    id=id
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(db=db, token=token)
    if (is_user(user) and db_user.id != user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    caminho_diretorio = f"static/users/profile/{user.id}"

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

    return caminho_imagem


async def get_imagem_user(
    db: Session,
    id=id
):
    db_user = db.query(User).filter(User.id == id).first()

    if (not db_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    caminho_imagem = str(db_user.caminho_imagem)

    if (caminho_imagem is None or not os.path.exists(caminho_imagem)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A imagem de perfil do usuário solicitado não foi encontrada!"
        )

    return caminho_imagem
