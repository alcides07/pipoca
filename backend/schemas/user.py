from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(
        max_length=32,
        description="Apelido do usuário"
    )

    email: EmailStr = Field(description="E-mail do usuário")


class UserCreate(UserBase):
    password: str = Field(
        max_length=32,
        description="Senha do usuário"
    )

    passwordConfirmation: str = Field(
        max_length=32,
        description="Confirmação da senha do usuário"
    )


class User_Read(UserBase):
    id: int

    class Config:
        from_attributes = True
