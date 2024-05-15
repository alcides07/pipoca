from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import EmailStr
from models.administrador import Administrador
from schemas.common.response import ResponseMessageSchema
from utils.create_token import create_token
from utils.errors import errors
from models.user import User
from orm.common.index import get_by_key_value
from schemas.auth import UserLoginOut
from dependencies.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from decouple import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="autenticacao")
ALGORITHM = str(config("ALGORITHM"))
TOKEN_EXPIRE_MINUTES = float(config("TOKEN_EXPIRE_MINUTES"))


def authenticate_user(db, credential: str, password: str):
    def authenticate_with_key(key: str):
        user_db = get_by_key_value(db, User, key, credential)
        if (user_db):
            if (not user_db.ativa):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "A conta do usuário não foi ativada!"
                )
            if (verify_password(password, user_db.password)):
                return user_db

        admin_db = get_by_key_value(db, Administrador, key, credential)
        if admin_db and verify_password(password, admin_db.password):
            return admin_db

        return False

    return authenticate_with_key("username") or authenticate_with_key("email")


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


router = APIRouter(
    prefix="/autenticacao",
    tags=["autenticação"],
)


@router.post("/",
             summary="Autentica um usuário",
             response_model=UserLoginOut,
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
            status.HTTP_401_UNAUTHORIZED,
            "Credenciais inválidas!",
            {"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    data = UserLoginOut(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        id=user.id
    )

    return data


@router.post("/ativacao/",
             summary="Ativa a conta de um usuário",
             response_model=ResponseMessageSchema,
             status_code=200,
             responses={
                 422: errors[422]
             },
             )
async def ativacao(
    codigo: str = Query(
        description="Código de ativação enviado para o e-mail do usuário"
    ),
    db: Session = Depends(get_db)
):
    from orm.user import activate_account

    data = await activate_account(
        token=codigo,
        db=db,
    )

    if (data):
        return ResponseMessageSchema(
            message="A conta do usuário foi ativada com sucesso!",
        )


@router.post("/ativacao/reenvio/",
             summary="Reenvia um e-mail de ativação da conta de um usuário",
             response_model=ResponseMessageSchema,
             status_code=200,
             responses={
                 422: errors[422],
                 400: errors[400],
                 404: errors[404]
             }
             )
async def ativacao_reenvio(
    email: EmailStr = Body(
        description="E-mail do usuário"
    ),
    db: Session = Depends(get_db)
):
    from orm.user import create_token_ativacao_conta_and_send_email, verify_conta_user_resend_email

    await verify_conta_user_resend_email(
        email=email,
        db=db
    )

    await create_token_ativacao_conta_and_send_email(
        data_token={
            "sub": email
        },
        destinatario=str(email)
    )

    return ResponseMessageSchema(
        message="Uma nova confirmação foi enviada para o e-mail fornecido!",
    )
