from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_user
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from orm.common.index import get_by_key_value_exists
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdatePartial, UserUpdateTotal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    if (user.password != user.passwordConfirmation):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. As senhas fornecidas não coincidem!")

    elif (get_by_key_value_exists(db, User, "username", user.username)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O nome de usuário fornecido está em uso!")

    elif (get_by_key_value_exists(db, User, "email", user.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. O e-mail fornecido está em uso!")

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
    if (is_user(user) and user_db.id != user.id):  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        user_by_username = db.query(User).filter(
            User.username == data.username).first()

        if (user_by_username != None and user_by_username.id != id):  # type: ignore
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Erro. O nome de usuário fornecido está em uso!")

        user_by_email = db.query(User).filter(
            User.email == data.email).first()

        if (user_by_email != None and user_by_email.id != id):  # type: ignore
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Erro. O e-mail fornecido está em uso!")

        for key, value in data:
            if (value != None and hasattr(user_db, key)):
                setattr(user_db, key, value)

        db.commit()
        db.refresh(user_db)

        return user_db

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
