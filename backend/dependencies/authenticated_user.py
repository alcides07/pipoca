from fastapi import Depends, HTTPException, status
from models.user import User
from orm.common.index import get_by_key_value
from schemas.auth import TokenData
from dependencies.database import get_db
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from decouple import config
from routers.auth import oauth2_scheme

ALGORITHM = str(config("ALGORITHM"))


async def get_authenticated_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Erro. Não foi possível validar as credenciais!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        SECRET_KEY = str(config("SECRET_KEY"))
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = str(payload.get("sub"))
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_by_key_value(db, User, "username", token_data.username)
    if user is None:
        raise credentials_exception
    return user
