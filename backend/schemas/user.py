from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(
        max_length=32,
        description="Apelido do usuário"
    )

    email: EmailStr = Field(description="E-mail do usuário")


class UserRead(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True


class UserCreate(UserBase):
    password: str = Field(
        max_length=64,
        description="Senha do usuário"
    )

    passwordConfirmation: str = Field(
        max_length=64,
        description="Confirmação da senha do usuário"
    )


class UserUpdateTotal(UserBase):
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
