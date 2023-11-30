from pydantic import BaseModel


class Item_Base(BaseModel):
    title: str
    description: str


class Item_Create(Item_Base):
    pass


class Item_Read(Item_Base):
    id: int

    class Config:
        from_attributes = True
