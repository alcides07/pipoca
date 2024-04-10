from pydantic import BaseModel, Field


class UserLogin(BaseModel):
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

    username: str = Field(description="Apelido do usuário")


class TokenData(BaseModel):
    username: str = Field(description="Apelido do usuário")
