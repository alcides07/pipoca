from pydantic import BaseModel, Field
from schemas.user import ID_USER_DESCRIPTION


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

    id: int = Field(
        description=ID_USER_DESCRIPTION
    )


class TokenData(BaseModel):
    username: str = Field(description="Apelido do usuário")
