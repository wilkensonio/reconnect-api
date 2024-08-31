from api.schemas.BaseModel import CommonBaseModel


class ItemBase(CommonBaseModel):
    name: str
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
