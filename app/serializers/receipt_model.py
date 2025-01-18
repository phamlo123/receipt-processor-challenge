from pydantic import BaseModel
from typing import Optional, List
from app.serializers.item_model import ItemModel


class ReceiptModel(BaseModel):
    retailer: str
    purchaseDate: str  
    purchaseTime: str  
    items: List[ItemModel]
    total: str