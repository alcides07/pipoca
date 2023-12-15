from fastapi import APIRouter, Depends, HTTPException, status
from utils.errors import errors
from models.user import User
from orm.common.index import get_by_key_value
from schemas.auth import User_Login_Out
from dependencies.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
from decouple import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
ALGORITHM = str(config("ALGORITHM"))
TOKEN_EXPIRE_MINUTES = float(config("TOKEN_EXPIRE_MINUTES"))


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    SECRET_KEY = str(config("SECRET_KEY"))
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db, credential: str, password: str):
    def authenticate_with_key(key: str):
        user_db = get_by_key_value(db, User, key, credential)
        if user_db and verify_password(password, user_db.password):
            return user_db
        return False

    return authenticate_with_key("username") or authenticate_with_key("email")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/",
             summary="Autentica um usuário",
             response_model=User_Login_Out,
             responses={
                 422: errors[422]
             }
             )
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro. Credenciais inválidas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    data = User_Login_Out(access_token=access_token, token_type="bearer")
    return data
