from pydantic import BaseModel, Field, EmailStr


class User_Base(BaseModel):
    username: str = Field(
        max_length=32,
        description="Apelido do usuário"
    )

    email: EmailStr


class User_Create(User_Base):
    password: str = Field(
        max_length=32,
        description="Senha do usuário"
    )

    passwordConfirmation: str = Field(
        max_length=32,
        description="Confirmação da senha do usuário"
    )


class User_Read(User_Base):
    id: int

    class Config:
        from_attributes = True
