from fastapi import Depends, HTTPException, status
from enviroments import ALGORITHM, SECRET_KEY
from models.administrador import Administrador
from models.user import User
from orm.common.index import get_by_key_value
from schemas.auth import TokenData
from dependencies.database import get_db
from sqlalchemy.orm import Session
from jose import ExpiredSignatureError, JWTError, jwt
from routers.auth import oauth2_scheme


async def get_authenticated_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Não foi possível validar as credenciais!",
        {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str | None = (payload.get("sub"))
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except ExpiredSignatureError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "A sessão do usuário expirou!"
        )

    except JWTError:
        raise credentials_exception

    user = get_by_key_value(db, User, "username", token_data.username) or get_by_key_value(
        db, Administrador, "username", token_data.username)
    if user is None:
        raise credentials_exception
    return user
