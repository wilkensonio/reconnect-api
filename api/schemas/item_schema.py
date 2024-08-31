from api.schemas.BaseModel import CommonBaseModel


from typing import ClassVar


class ItemBase(CommonBaseModel):
    name: str
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
