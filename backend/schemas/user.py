from pydantic import BaseModel, Field, EmailStr
from schemas.problema import ProblemaReadSimple


class UserBase(BaseModel):
    username: str = Field(
        max_length=32,
        description="Apelido do usuário"
    )

    email: EmailStr = Field(description="E-mail do usuário")


class UserRead(UserBase):
    id: int
    problemas: list[ProblemaReadSimple] = Field(
        description="Lista de problemas do usuário")

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
