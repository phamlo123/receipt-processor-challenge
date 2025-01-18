from pydantic import BaseModel

class ItemModel(BaseModel):
    shortDescription: str
    price: str