from pydantic import BaseModel, Field


class User_Login(BaseModel):
    credential: str = Field(
        description="Username (apelido) ou e-mail do usuário"
    )

    password: str = Field(
        max_length=32,
        description="Senha do usuário"
    )


class UserLoginOut(BaseModel):
    access_token: str = Field(
        description="Token de acesso do usuário")

    token_type: str = Field(
        description="Tipo do token utilizado")


class Token_Data(BaseModel):
    username: str = Field(description="Apelido do usuário")
