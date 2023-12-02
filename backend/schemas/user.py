from pydantic import BaseModel, Field, EmailStr


class User_Base(BaseModel):
    username: str = Field(max_length=32)
    email: EmailStr()


class User_Create(User_Base):
    password: str = Field(max_length=32)
    passwordConfirmation: str = Field(max_length=32)

    def model_dump(self):
        data = super().model_dump()
        data.pop("passwordConfirmation")
        return data


class User_Read(User_Base):
    id: int

    class Config:
        from_attributes = True
