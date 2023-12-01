from pydantic import BaseModel


class User_Base(BaseModel):
    username: str
    email: str


class User_Create(User_Base):
    password: str
    passwordConfirmation: str


class User_Read(User_Base):
    id: int

    class Config:
        from_attributes = True
