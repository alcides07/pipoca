from pydantic import BaseModel, Field


class User_Login(BaseModel):
    credential: str = Field(
        description="Apelido ou e-mail do usuário"
    )

    password: str = Field(
        max_length=32,
        description="Senha do usuário"
    )


class User_Login_Out(BaseModel):
    token: str = Field(
        description="Token do usuário")
