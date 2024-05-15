from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

ID_USER_DESCRIPTION = "Identificador do usuário"


class UserBase(BaseModel):
    username: str = Field(
        max_length=32,
        description="Apelido do usuário"
    )


class UserBaseFull(UserBase):
    email: EmailStr = Field(description="E-mail do usuário")


class UserReadFull(UserBaseFull):
    id: int = Field(
        description=ID_USER_DESCRIPTION
    )

    criado_em: datetime = Field(
        description="Data e horário de criação do usuário"
    )

    ativa: bool = Field(
        description="Indica se a conta do usuário está ativa"
    )


class UserReadSimple(UserBase):
    id: int = Field(
        description=ID_USER_DESCRIPTION
    )

    class ConfigDict:
        from_attributes = True


class UserCreate(UserBaseFull):
    password: str = Field(
        max_length=64,
        description="Senha do usuário"
    )

    passwordConfirmation: str = Field(
        max_length=64,
        description="Confirmação da senha do usuário"
    )


class UserUpdateTotal(UserBaseFull):
    pass


class UserUpdatePartial(BaseModel):
    username: Optional[str] = Field(
        default=None,
        max_length=32,
        description="Apelido do usuário"
    )

    email: Optional[EmailStr] = Field(
        default=None,
        description="E-mail do usuário"
    )
