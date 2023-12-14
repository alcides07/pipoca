from fastapi import Depends, HTTPException, status
from schemas.auth import Token_Data
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.user import read_user_by_key
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
        token_data = Token_Data(username=username)
    except JWTError:
        raise credentials_exception
    user = read_user_by_key(db, "username", token_data.username)
    if user is None:
        raise credentials_exception
    return user
